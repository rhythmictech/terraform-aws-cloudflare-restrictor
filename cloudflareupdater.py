import boto3
import json
import os
import urllib3
import logging

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', logging.DEBUG))

for handler in logger.handlers:
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s](%(name)s) %(message)s'))

for lib_logger in ['botocore', 'boto3', 'urllib3']:
    logging.getLogger(lib_logger).setLevel(
        os.environ.get('LIBRARY_LOG_LEVEL', logging.ERROR))

ec2 = boto3.client('ec2')

def get_cloudflare_ip_list():
    """ Call the CloudFlare API and return a list of IPs """
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://api.cloudflare.com/client/v4/ips')
    payload = json.loads(response.data.decode('utf-8'))
    logger.info("Retrieved current CloudFlare IPs: %s" % (payload))

    if 'result' in payload:
        return payload['result']

    raise Exception("Cloudflare response error")


def get_aws_security_groups(tag_key, tag_value):
    """ Return security groups based on `tag_key=tag_value """

    response = ec2.describe_security_groups(Filters=[
        {
            'Name': 'tag:{}'.format(tag_key),
            'Values': [
                tag_value,
            ]
        }])

    return response['SecurityGroups']


def check_ipv4_rule_exists(rules, address, port):
    """ Check if the rule currently exists """
    logger.debug("Looking for %s and port %i" % (address, port))
    for rule in rules:
        for ip_range in rule['IpRanges']:
            if ip_range['CidrIp'] == address and rule['FromPort'] == port:
                return True

    return False


def add_ipv4_rule(group, address, port):
    """ Add the IP address/port to the security group """
    ec2.authorize_security_group_ingress(
        GroupId=group['GroupId'],
        IpPermissions=[{
            'IpProtocol': "tcp",
            'FromPort': port,
            'ToPort': port,
            'IpRanges': [
                {
                    'CidrIp': address
                },
            ]
        }])

    logger.info("Added %s : %i to %s  " % (address, port, group['GroupId']))


def delete_ipv4_rule(group, address, port):
    """ Remove the IP address/port from the security group """

    ec2.revoke_security_group_ingress(
        GroupId=group['GroupId'],
        IpPermissions=[{
            'IpProtocol': "tcp",
            'FromPort': port,
            'ToPort': port,
            'IpRanges': [
                {
                    'CidrIp': address
                },
            ]
        }])

    logger.info("Removed %s : %i from %s  " % (address, port, group['GroupId']))


def check_ipv6_rule_exists(rules, address, port):
    """ Check if the rule currently exists """
    for rule in rules:
        for ip_range in rule['Ipv6Ranges']:
            if ip_range['CidrIpv6'] == address and rule['FromPort'] == port:
                return True
    return False


def add_ipv6_rule(group, address, port):
    """ Add the IP address/port to the security group """
    ec2.authorize_security_group_ingress(
        GroupId=group['GroupId'],
        IpPermissions=[{
            'IpProtocol': "tcp",
            'FromPort': port,
            'ToPort': port,
            'Ipv6Ranges': [
                {
                    'CidrIpv6': address
                },
            ]
        }])

    logger.info("Added %s : %i to %s  " % (address, port, group['GroupId']))


def delete_ipv6_rule(group, address, port):
    """ Remove the IP address/port from the security group """

    ec2.revoke_security_group_ingress(
        GroupId=group['GroupId'],
        IpPermissions=[{
            'IpProtocol': "tcp",
            'FromPort': port,
            'ToPort': port,
            'Ipv6Ranges': [
                {
                    'CidrIpv6': address
                },
            ]
        }])

    logger.info("Removed %s : %i from %s  " % (address, port, group['GroupId']))


def update_security_group_policies(ip_addresses):
    """ Update Information of Security Groups """
    logger.info("Checking policies of Security Groups")

    ports = list(map(int, os.environ['PORTS_LIST'].split(",")))
    if not ports:
        ports = [443]

    logger.debug("Will allow traffic on ports %s" % (ports))
    security_groups = get_aws_security_groups(
        os.environ['TAG_KEY'], os.environ['TAG_VALUE'])

    if len(security_groups) == 0:
        logger.warn("No security groups matched %s/%s" % (
            os.environ['TAG_KEY'], os.environ['TAG_VALUE']))
        return

    logger.debug("Will scan security groups: %s" % (security_groups))

    for security_group in security_groups:
        logger.info("Processing group %s" % (security_group['GroupId']))
        current_rules = security_group['IpPermissions']

        # IPv4
        logger.debug("Checking for rules to remove")
        # remove old addresses
        for port in ports:
            for rule in current_rules:
                # is it necessary/correct to check both From and To?
                if rule['FromPort'] == port and rule['ToPort'] == port:
                    for ip_range in rule['IpRanges']:
                        if ip_range['CidrIp'] not in ip_addresses['ipv4_cidrs']:
                            delete_ipv4_rule(
                                security_group, ip_range['CidrIp'], port)

        # add new addresses
        logger.debug("Checking for rules to add")
        for ipv4_cidr in ip_addresses['ipv4_cidrs']:
            logger.debug("Looking for %s" % (ipv4_cidr))
            for port in ports:
                if not check_ipv4_rule_exists(current_rules, ipv4_cidr, port):
                   add_ipv4_rule(security_group, ipv4_cidr, port)

        logger.debug("Checking for ipv6 rules to add")
        # IPv6 -- because of boto3 syntax, this has to be separate
        # remove old addresses
        logger.debug("Checking for ipv6 rules to remove")
        for port in ports:
            for rule in current_rules:
                for ip_range in rule['Ipv6Ranges']:
                    if ip_range['CidrIpv6'] not in ip_addresses['ipv6_cidrs']:
                        delete_ipv6_rule(
                            security_group, ip_range['CidrIpv6'], port)

        # add new addresses
        for ipv6_cidr in ip_addresses['ipv6_cidrs']:
            for port in ports:
                if not check_ipv6_rule_exists(current_rules, ipv6_cidr, port):
                    add_ipv6_rule(security_group, ipv6_cidr, port)


def lambda_handler(event, context):
    """ AWS Lambda main function """

    ip_addresses = get_cloudflare_ip_list()
    update_security_group_policies(ip_addresses)
