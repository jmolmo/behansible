import os
import re
from behave import *
from lib.servers import *
import ansible_runner


import logging
logging.basicConfig(filename='behave_test.log',level=logging.INFO)


@given('we have "{num_servers}" "{kind_of_server}" with "{flavour}" installed')
def step_create_servers_cluster(context, num_servers, kind_of_server, flavour):
    # Create the servers
    context.servers = setup_cluster(num_servers, flavour)


@when('we execute the playbook "{playbook}" with the following parameters')
def step_execute_playbook(context, playbook):

    inventory = {'vdos': {'hosts': dict((srv.ip,'') for srv in context.servers)}}

    extra_vars = {}
    cmd_line = ''
    for row in context.table:
        if row['value'].startswith("["):
            extra_vars[row['parameter']] = eval(row['value'])
        else:
            if row['parameter'].startswith('cmdline'):
                cmd_line += row['value']
            else:
                extra_vars[row['parameter']] = row['value']

    # Save extra_vars for checkings
    context.extra_vars = extra_vars

    #no output
    settings = {'suppress_ansible_output': False}

    #get private data dir
    directory = os.getcwd() + '/ansible'

    #run playbook with inventory
    try:
        r = ansible_runner.run(private_data_dir = directory,
                               playbook = playbook,
                               inventory = inventory,
                               extravars = extra_vars,
                               cmdline = cmd_line,
                               verbosity = 0,
                               settings = settings)
    except Exception as ex:
        logging.info('Error %s' % ex)


@then('we can check in all the servers that the ports and the service "{service}" are in the zone "{zone}"')
def step_check_fw_status(context, service, zone):

    cmd = "firewall-cmd --info-zone=%s" % zone

    errors_fw = ""
    for server in context.servers:
        stdout = server.execute(cmd)

        # Check ports:
        ports_not_found = []
        for port in context.extra_vars['gluster_infra_fw_ports']:
            port_pattern = "ports:.*%s.*" % port
            match = re.search(port_pattern, stdout)
            if not match:
                errors_fw += "Port %s not found in %s firewall zone '%s'\n" % (port, server.ip, zone)

        # Check services
        service_pattern = "\s*services:.*%s.*" % service
        match = re.search(service_pattern, stdout)
        if not match:
            errors_fw += "Service '%s' not included in %s firewall zone '%s'\n" % (service, server.ip, zone)

    if errors_fw:
        print errors_fw
        assert False

@then('i can get information of the "{package}" package')
def step_check_package_info(context, package):

    # Package is reachable if we can get the yum info...
    # In the 'yum info package' command output
    # There must be a line like:
    # Name       : package
    pattern = "Name\s*:\s%s" % package

    result_errors= []
    for server in context.servers:
        stdout = server.execute("yum info %s" % package)
        match = re.search(pattern, stdout)
        if not match:
            result_errors.append(
                "Package %s not reachable from server:%s" % (package, server.ip))

    if result_errors:
        print result_errors
        assert False
