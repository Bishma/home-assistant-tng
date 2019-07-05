import appdaemon.plugins.hass.hassapi as hass
import datetime
import pymysql
import re

class Alexa(hass.Hass):

    def initialize(self):
        self.register_endpoint(self.api_call, "alexa")
    
    def api_call(self, data):
        to_amazon = self.alexa_request_parser(data)
        return self.format_alexa_response(**to_amazon), 200

    def alexa_request_parser(self, data):
        """
        All alexa requests come thought this function to be parsed into constituent parts.

        Parameters:
            data (dict): The alexa request.
        """

        # The intent can be fetched from a helper function.
        self.intent_name = str(self.get_alexa_intent(data))
        # We can get all the slots from the request using this helper function.
        self.slots = self.get_alexa_slot_value(data)

        # Get the request meta data or None if not found
        self.dialog_state = data["request"]["dialogState"] if "request" in data and "dialogState" in data["request"] else "None"
        self.request_type = data["request"]["type"] if "request" in data and "type" in data["request"] else "None"
        self.alexa_error = data["request"]["error"]["message"] if "request" in data and "error" in data["request"] and "message" in data["request"]["error"] else "None"

        # If we got an error, log it
        if self.alexa_error != 'None':
            self.log(self.alexa_error, level = "ERROR")
        
        # Log the pieces that we just parsed out.
        self.log("dialog state: " + str(self.dialog_state), level = "INFO")
        
        # At the moment I'm only handling intent requests, but I still need a check
        if self.request_type == "IntentRequest":
            self.log("intent: " + self.intent_name, level = "INFO")
            result = self.alexa_intent_parser()
        else:
            self.log("request type: " + str(self.request_type), level = "INFO")

        if not isinstance(result, dict):
            self.log("Did not receive a dictionary from the parser. Stringified value:" + str(result), level = "ERROR")
            result = self.just_saying("An unknown error has occurred.")
        
        return result

    
    def alexa_intent_parser(self):
        """
        Send the given alexa intent to its corrent worker method.
        """

        # Validate that we have a method for the given intent
        intents = {
            "turn_on": "int_turn_on"
        }

        # Relate the intent value to its method name or fall back to the fallback
        validated_intent = intents.get(self.intent_name, "fallback")
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, validated_intent, lambda: "invalid intent data")
        # Call the method as we return it
        return method()

    def int_turn_on(self):
        heard_device_tokens = self.device_tokenizer(self.slots['device_on']['value'])

        device = self.device_by_name(heard_device_tokens)

        service = device["domain"] + "/turn_on"
        entity = device["domain"] + "." + device["name"]
        self.call_service(service, entity_id = entity)

        msg = self.just_saying("I'll turn on {}".format(device))
        return msg

    def fallback(self):
        self.log("We landed in fallback.")

        return self.just_saying("I'm a fallback kind of AI.")
    
    def device_by_name(self, device):
        # try to find in sql using all tokens
            # soundex?
        # else loop though valid domains in likely order
        # cache successes and their tokens
            # Don't cache a soundex match?
        return { "domain": "switch", "name": "the_sparkle" }

    def device_tokenizer(self, device):
        """
        When we search for devices the alexa SearchQuery will deliver exactly what it
        heard, and I want to be forgiving of speech. This will allow to query for and
        cache various search permutations.

        Parameters:
            device (str): the device as given through the alexa search query slot.
        """
        device = str(device).lower().replace(" ", "_")
        tokens = [ device ]
        if device.startswith("the"):
            tokens.append(device.replace("the_", ""),)
        else:
            tokens.append("the_" + device)
        
        return tokens

    def just_saying(self, speech):
        return { "speech": str(speech) }