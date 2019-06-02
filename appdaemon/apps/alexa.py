import appdaemon.plugins.hass.hassapi as hass
import datetime

class Alexa(hass.Hass):

    def initialize(self):
        self.register_endpoint(self.api_call, "alexa")
        return

    def api_call(self, data):
        self.alexa_request_parser(data)
        #response = self.format_alexa_response(speech = "The intent {} got a device_on value of {}".format(intent, device))
        return self.format_alexa_response(speech = "dang donkey doug"), 200

    def alexa_request_parser(self, data):
        """All alexa requests come thought this function to be parsed into constituent parts.

        Parameters:
        data (dict): The alexa request.
        """

        # The intent can be fetched from a helper function.
        self.intent_name = self.get_alexa_intent(data)
        # We can get all the slots from the request using this helper function.
        self.slots = self.get_alexa_slot_value(data)

        # Get the request meta data or None if not found
        self.dialog_state = data["request"]["dialogState"] if "request" in data and "dialogState" in data["request"] else "None"
        self.request_type = data["request"]["type"] if "request" in data and "type" in data["request"] else "None"
        self.alexa_error = data["request"]["error"]["message"] if "request" in data and "error" in data["request"] and "message" in data["request"]["error"] else "None"
        
        # Log the pieces that we just parsed out.
        request_metadata = "dialog state: " + str(self.dialog_state) + "\nrequest type: " + str(self.request_type)
        request_errors = "alexa error: " + str(self.alexa_error)
        request_intent = "intent: " + str(self.intent_name)
        self.log("Alexa request received:\n" + request_metadata + "\n" + request_errors + "\n" + request_intent)
        #slottext = "slots: "
        #for slot,slotvalue in self.slots.items():
        #    slottext = slottext + slot + "= " + str(slotvalue) + ", "
        #self.alexalog(slottext)  
        #self.alexalog("error = " + str(self.alexa_error))