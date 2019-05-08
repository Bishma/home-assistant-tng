import appdaemon.plugins.hass.hassapi as hass
import datetime

class Alexa(hass.Hass):

    def initialize(self):
        pass

    def api_call(self, data):
        intent = self.get_alexa_intent(data)

        self.log("Alexa error encountered: {}".format(self.get_alexa_error(data)))

