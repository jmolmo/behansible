Feature: Set up firewall rules in a set of nodes (open ports, add services to zone)

  Scenario: Configure firewall in the cluster nodes
    Given we have "3" "virtual machines" with "fedora28" installed
    When we execute the playbook "infra.yml" with the following parameters:
      | parameter                  | value                                                                           |
      | cmdline                    | --tags firewall                                                                 |
      | gluster_infra_fw_ports     | ['2049/tcp', '54321/tcp', '5900/tcp', '5900-6923/tcp', '5666/tcp', '16514/tcp'] |
      | gluster_infra_fw_state     | enabled                                                                         |
      | gluster_infra_fw_zone      | public                                                                          |
      | gluster_infra_fw_services  | ['ssh']                                                                   |
      | gluster_infra_fw_permanent | True                                                                            |
    Then we can check in all the servers that the ports and the service "ssh" are in the zone "public"
