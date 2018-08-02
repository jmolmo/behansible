# Server objects and functions that ease the work with servers ( vm's and containers )
import paramiko

class Server():
    """Server objects"""

    def __init__(self, name, ip, vm):
        """Init the server basic properties (by default Virtual Machines)

        @name: hostname of the server
        @ip: IP address of the admin interface
        @vm: If this server is a Virtual Machine or not
        """
        self.name = name
        self.ip = ip
        self.vm = vm
        self.ssh_client = None
        self.username = 'root'
        self.password = 'admin'

    def connect_ssh(self):

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.ssh_client.connect(self.ip,
                                username=self.username,
                                password=self.password)

    def execute(self, command):
        """Use ssh to execute a command

        @command: Command to execute
        returns a string with the output of the command
        """

        if not self.ssh_client:
            self.connect_ssh()

        result = ""
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            # Wait until command finishes
            stdout.channel.recv_exit_status()

            # gather the result
            for line in stdout.readlines():
                result += line

        except Exception as ex:
            print "Error executing ssh command: %s" % ex

        return result


def setup_cluster(num_servers, flavour, vms=True):
    """Create a set of servers num_servers based in the flavour selected

    @num_servers: The number os servers to be created
    @flavour: the operating system and version installed in these servers
    @vms: Boolean (True by default) to indicate if the server is
          a Virtual Machine or a container

    @returns: A list of Server objects
    """

    # TODO: Now I just return a fixed list of servers

    # fedora 28 servers
    fedora28 = [Server("rhst01", "192.168.122.225", vms),
                Server("rhst02", "192.168.122.108", vms),
                Server("rhst03", "192.168.122.86", vms)]

    #rhel 7.5 servers
    rhel75 = [Server("rhel75st01", "192.168.122.13", vms),
              Server("rhel75st02", "192.168.122.206", vms)]

    return rhel75
