from twisted.application.service import ServiceMaker


CarapaceSSHService = ServiceMaker(
    "Carapace SSH Server",
    "carapace.app.service",
    ("A highly flexible pure-Python, Twisted-based SSH Server with custom "
     "account shells"),
    "carapace")
