# behansible

Execution of Ansible playbooks using Behave.
--------------------------------------------

My aim is to provide a test framework based in Behave where behavioral test cases over Ansible playbooks will be easy to implement and to be adapted to differente kind of scenarios.

I'm using the ansible playbooks used to install/configure Red Hat Gluster Clusters from:
https://github.com/gluster/gluster-ansible

Things to do:
- Implement a "servers factory" that will provide a set of clean Vm's/containers
- Create "Behaves" and different scenarios for test other Ansible playbooks
- Use of certificates to connect with repos
- Extend library of tests


Install the enviroment:
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
