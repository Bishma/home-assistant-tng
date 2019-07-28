"""
This creates a service that can be used to pass log messages into the main home assistant logger.
Adapted from: https://community.home-assistant.io/t/adding-logs-from-appdaemon-to-the-main-home-assistant-log/105722 
"""
message = data.get('message')
if not message:
  logger.error('No message provided')

# Send to the appropriate log level
received_level = str(data.get('level')).lower()
if received_level == 'debug':
  logger.debug(message)
elif received_level == 'warning':
  logger.warning(message)
elif received_level == 'error':
  logger.error(message)
else:
  logger.info(message)