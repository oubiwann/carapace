from ConfigParser import SafeConfigParser
import os

from zope.interface import moduleProvides

from carapace import meta
from carapace.sdk import interfaces


moduleProvides(interfaces.IConfig)


class Config(object):
    pass


# Main
main = Config()
main.config = Config()
main.config.datadir = os.path.expanduser("~/.%s" % meta.library_name)
main.config.localfile = "config.ini"
main.config.installedfile = os.path.join(
    main.config.datadir, main.config.localfile)

# Internal SSH Server
ssh = Config()
ssh.servicename = meta.description
ssh.ip = "127.0.0.1"
ssh.port = 2222
ssh.pidfile = "twistd.pid"
ssh.username = "root"
ssh.keydir = os.path.join(main.config.datadir, "ssh")
ssh.privkey = "id_rsa"
ssh.pubkey = "id_rsa.pub"
ssh.localdir = "~/.ssh"
ssh.userdirtemplate = os.path.join(main.config.datadir, "users", "{{USER}}")
ssh.userauthkeys = os.path.join(ssh.userdirtemplate, "authorized_keys")
ssh.usesystemkeys = False
ssh.banner = """:
: Welcome to
:_________
:\_   ___ \_____ ____________  ___________    ____  ____
:/    \  \/\__  \\\\_  __ \__  \ \____ \__  \ _/ ___\/ __ \\
:\     \____/ __ \|  | \// __ \|  |_> > __ \\\\  \__\  ___/
: \______  (____  /__|  (____  /   __(____  /\___  >___  >
:         \/     \/           \/|__|       \/     \/    \/
:
: You have logged into a Carapace Shell Server.
: {{HELP}}
:
: Enjoy!
:
"""


class Configurator(object):
    """
    """
    def __init__(self, main=None, ssh=None):
        self.main = main
        self.ssh = ssh

    def buildDefaults(self):
        config = SafeConfigParser()
        config.add_section("SSH")
        config.set("SSH", "servicename", self.ssh.servicename)
        config.set("SSH", "ip", str(self.ssh.ip))
        config.set("SSH", "port", str(self.ssh.port))
        config.set("SSH", "pidfile", self.ssh.pidfile)
        config.set("SSH", "username", self.ssh.username)
        config.set("SSH", "keydir", self.ssh.keydir)
        config.set("SSH", "privkey", self.ssh.privkey)
        config.set("SSH", "pubkey", self.ssh.pubkey)
        config.set("SSH", "localdir", self.ssh.localdir)
        config.set("SSH", "userdirtemplate", self.ssh.userdirtemplate)
        config.set("SSH", "userauthkeys", self.ssh.userauthkeys)
        config.set("SSH", "usesystemkeys", str(self.ssh.usesystemkeys))
        config.set("SSH", "banner", self.ssh.banner)
        return config

    def getConfigFile(self):
        if os.path.exists(self.main.config.localfile):
            return self.main.config.localfile
        if not os.path.exists(self.main.config.datadir):
            os.mkdir(os.path.expanduser(self.main.config.datadir))
        return self.main.config.installedfile

    def writeDefaults(self):
        config = self.buildDefaults()
        with open(self.getConfigFile(), "wb") as configFile:
            config.write(configFile)

    def getConfig(self):
        configFile = self.getConfigFile()
        if not os.path.exists(configFile):
            self.writeDefaults()
            return
        config = SafeConfigParser()
        config.read(configFile)
        return config

    def updateConfig(self):
        """
        If the configfile doesn't exist, this method will (indirectly) create
        it and exit.

        If it does exist, it will load the config values from the file (which
        may be different from those defined be default in this module), and
        update the in-memory config values with what it reads from the file.
        """
        config = self.getConfig()
        if not config:
            return
        self.ssh.servicename = config.get("SSH", "servicename")
        self.ssh.ip = config.get("SSH", "ip")
        self.ssh.port = int(config.get("SSH", "port"))
        self.ssh.pidfile = config.get("SSH", "pidfile")
        self.ssh.username = str(config.get("SSH", "username"))
        self.ssh.keydir = config.get("SSH", "keydir")
        self.ssh.privkey = config.get("SSH", "privkey")
        self.ssh.pubkey = config.get("SSH", "pubkey")
        self.ssh.localdir = config.get("SSH", "localdir")
        self.ssh.userdirtemplate = config.get("SSH", "userdirtemplate")
        self.ssh.userauthkeys = config.get("SSH", "userauthkeys")
        self.ssh.usesystemkeys = eval(config.get("SSH", "usesystemkeys"))
        self.ssh.banner = str(config.get("SSH", "banner"))
        return config


def configuratorFactory():
    return Configurator(main, ssh)


def updateConfig():
    configurator = configuratorFactory()
    configurator.updateConfig()
