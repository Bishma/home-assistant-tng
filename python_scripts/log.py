component = data.get('component')
if not component:
  logger.error('No component provided')

message = data.get('message')
if not message:
  logger.error('No message provided')

complete_msg = "{}: {}".format(component, message)

logger.info(complete_msg)