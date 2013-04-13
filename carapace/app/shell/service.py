from twisted.cred import portal
from twisted.conch import manhole_ssh

from carapace.app import cred
from carapace.sdk import const
from carapace.util import ssh as util


def portalFactory(interpreterType, namespace):
    if interpreterType == const.PYTHON:
        from carapace.app.shell import pythonshell
        realm = pythonshell.PythonTerminalRealm(namespace)
    elif interpreterType == const.SHARED_PYTHON:
        from carapace.app.shell import pythonshell
        realm = pythonshell.SharedPythonTerminalRealm(namespace)
    elif interpreterType == const.ECHO:
        from carapace.app.shell import echoshell
        realm = echoshell.EchoTerminalRealm(namespace)
    return portal.Portal(realm)


def getShellFactory(interpreterType, **namespace):
    sshPortal = portalFactory(interpreterType, namespace)
    factory = manhole_ssh.ConchFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(cred.PublicKeyDatabase())
    return factory
