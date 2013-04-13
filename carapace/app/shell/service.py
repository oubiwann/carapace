from twisted.cred import portal
from twisted.conch import manhole_ssh

from dreamssh.app import cred
from dreamssh.sdk import const
from dreamssh.util import ssh as util


def portalFactory(interpreterType, namespace):
    if interpreterType == const.PYTHON:
        from dreamssh.app.shell import pythonshell
        realm = pythonshell.PythonTerminalRealm(namespace)
    elif interpreterType == const.SHARED_PYTHON:
        from dreamssh.app.shell import pythonshell
        realm = pythonshell.SharedPythonTerminalRealm(namespace)
    elif interpreterType == const.ECHO:
        from dreamssh.app.shell import echoshell
        realm = echoshell.EchoTerminalRealm(namespace)
    return portal.Portal(realm)


def getShellFactory(interpreterType, **namespace):
    sshPortal = portalFactory(interpreterType, namespace)
    factory = manhole_ssh.ConchFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(cred.PublicKeyDatabase())
    return factory
