Feature: Set up gluster repositories in a set of nodes

  Scenario: Set the repositories in the nodes
      Given we have "3" "virtual machines" with "fedora28" installed
      When we execute the playbook "repo.yml" with the following parameters:
        | parameter                 | value                                                     |
        | gluster_repos_username    | user@redhat.com                                           |
        | gluster_repos_password    | xxxxxxxxxx                                                |
        | gluster_repos_disable_all | True                                                      |
        | gluster_repos_pools       | 8a85f98c617475400161756d571b1485                          |
        | gluster_repos_rhsmrepos   | ["rhel-7-server-rpms", "rhel-ha-for-rhel-7-server-rpms"]  |
      Then i can get information of the "glusterfs" package
