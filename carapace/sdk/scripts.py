from datetime import datetime
import os, subprocess

from twisted.conch.scripts import ckeygen
from twisted.internet import reactor
from twisted.python.filepath import FilePath
from twisted.web import client

from carapace.sdk import registry


class Script(object):
    """
    """
    def __init__(self):
        self.config = registry.getConfig()
        self.run()

    def run(self):
        raise NotImplementedError()


class KeyGen(Script):
    """
    """
    def run(self):
        path = self.config.ssh.keydir
        key = os.path.join(path, "id_rsa")
        if not os.path.exists(path):
            print "Creating SSH key dir '%s' ..." % path
            os.makedirs(path)
        else:
            print "SSH key dir '%s' already exists." % path
        if not os.path.exists(key):
            print "Creating SSH key at '%s' ..." % key
            print "  (This could take a while)"
            options = {"filename": key, "bits": 4096, "pass": None}
            ckeygen.generateRSAkey(options)
        else:
            print "SSH key '%s' already exists." % key


class ConnectToShell(Script):
    """
    """
    def run(self):
        print "Connecting to %s ..." % self.config.ssh.servicename
        subprocess.call(
            ["ssh",  "-p %s" % self.config.ssh.port,  self.config.ssh.ip])


class StopDaemon(Script):
    """
    """
    def run(self):
        print "Stopping %s ..." % self.config.ssh.servicename
        if not os.path.exists(self.config.ssh.pidfile):
            print "Could not find the server's PID file ..."
            print "Aborting."
        else:
            pid = open(self.config.ssh.pidfile).read()
            subprocess.call(["kill", pid])
            print "Stopped."


class GenerateConfig(Script):
    """
    """
    def backupConfig(self, src):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest = FilePath("%s.%s" % (src.path, timestamp))
        print "\tBacked up existing config to %s." % dest.path
        # if something goes wrong with the setContent call, don't remove the
        # source!
        try:
            dest.setContent(src.open().read())
            src.remove()
        except Exception, e:
            raise e

    def run(self):
        # get config file path
        configurator = self.config.configuratorFactory()
        filePath = FilePath(configurator.getConfigFile())
        # check to see if it exists, and if so, back it up
        if filePath.exists():
            self.backupConfig(filePath)
        # write the new config
        configurator.writeDefaults()
        print "\tWrote new config file to %s." % filePath.path


class ImportKeys(Script):
    """
    """
    lp_template = "https://launchpad.net/~%s/+sshkeys"

    def __init__(self, username, lp_username=None):
        self.username = username
        if not lp_username:
            lp_username = username
        self.lp_url = self.lp_template % lp_username
        super(ImportKeys, self).__init__()

    def finish(self):
        reactor.stop()

    def createDirs(self):
        userDir = FilePath(self.config.ssh.userdirtemplate % self.username)
        if not userDir.exists():
            userDir.makedirs()

    def getAuthKeys(self):
        authKeys = FilePath(self.config.ssh.userauthkeys % self.username)
        data = None
        if authKeys.exists():
            data = authKeys.open()
        return (authKeys, data.read())

    def saveKeys(self, result):
        self.createDirs()
        filePath, data = self.getAuthKeys()
        if data:
            filePath.setContent("%s\n%s" % (data, result))
        else:
            filePath.setContent(result)
        self.finish()

    def logError(self, failure):
        print failure
        self.finish()

    def run(self):
        deferred = client.getPage(self.lp_url)
        deferred.addCallback(self.saveKeys)
        deferred.addErrback(self.logError)
        reactor.run()
