from assistant.core.config import ConfigurationManager

config = ConfigurationManager()

print(config.get("assistant.name"))
print(config.get("assistant.version"))
print(config.get("database.path"))
print(config.get("voice.language"))