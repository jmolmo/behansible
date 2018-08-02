# behansible

Execution of Ansible playbooks using Behave.
--------------------------------------------

My aim is to provide a test framework based in Behave where behavioral test cases over Ansible playbooks will be easy to implement and to be adapted to different kind of scenarios.

I'm using:

The ansible playbooks used to install/configure Red Hat Gluster Clusters from:
https://github.com/gluster/gluster-ansible

Ansible runner to execute the playbooks:
https://github.com/ansible/ansible-runner

And Python Behave (https://behave.readthedocs.io/en/latest/) to "glue" all together and have nice tests like:

```
Feature: Set up firewall rules in a set of nodes (open ports, add services to zone)

  Scenario: Configure firewall in the cluster nodes
    Given we have "3" "virtual machines" with "rhel75" installed
    When we execute the playbook "infra.yml" with the following settings:
      | parameter                  | value                                                                           |
      | cmdline                    | --tags firewall                                                                 |
      | gluster_infra_fw_ports     | ['2049/tcp', '54321/tcp', '5900/tcp', '5900-6923/tcp', '5666/tcp', '16514/tcp'] |
      | gluster_infra_fw_state     | enabled                                                                         |
      | gluster_infra_fw_zone      | public                                                                          |
      | gluster_infra_fw_services  | ['glusterfs']                                                                   |
      | gluster_infra_fw_permanent | True                                                                            |
    Then we can check in all the servers that the ports and the service "glusterfs" are in the zone "public"

```



Things to do:
-------------

- Implement a "servers factory" that will provide a set of clean Vm's/containers
- Create "Behaves" and different scenarios for test other Ansible playbooks
- Use of certificates to connect with repos
- Extend library of tests


Install the environment:
------------------------
Note: Until "servers factory" implemented it will be needed to have a set of servers where to execute the playbooks

Use Virtualenv to deploy the project in your server:

```
# mkdir behansible_tests
# virtualenv behansible_tests
# cd behansible_tests
# git clone https://github.com/jmolmo/behansible.git
# source bin/activate
(behansible_tests)# pip install --upgrade setuptools
(behansible_tests)# pip install -r behansible/requirements.txt
```

Execution of tests (servers should be running and accesible from the test server)

```
(behansible_tests)# cd behansible/features
(behansible_tests)# behave gluster_firewall.feature
```code
