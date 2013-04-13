from carapace import config
from carapace.sdk import registry


config.updateConfig()
registry.registerConfig(config)
