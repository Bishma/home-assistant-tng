import appdaemon.plugins.hass.hassapi as hass
import datetime
import pymysql
import re

class Alexa(hass.Hass):

    def initialize(self):
        # the domains we will search for devices in.
        self.search_domains = [
            'light',
            'switch',
            'group',
            'input_boolean',
            'script',
            'timer'
        ]

        # Connection parameters for sql server.
        self.sql_params = {
            "host": '192.168.131.2',
            "user": 'yggdrasil_ad',
            "password": self.get_state("input_text.appdaemon_database_passwd"),
            "port": 3307,
            "db": "appdaemon"
        }

        self.register_endpoint(self.api_call, "alexa")

    def set_context(self, data):
        """
        Reformat context data from the alexa request.

        Parameters:
            data (dict): The context data from alexa.
        """
        context = {
            "application_id": data["context"]["System"]["application"]["applicationId"],
            "user_id": data["context"]["System"]["user"]["userId"],
            "device_id": data["context"]["System"]["device"]["deviceId"] if "deviceId" in data["context"]["System"]["device"] else None
        }

        return context
    
    def get_request(self, data):
        """
        Reformat the requestion information from the alexa request.

        Parameters:
            data (dict): The request data from alexa.
        """
        request = {
            "dialog_state": data["request"]["dialogState"] if "request" in data and "dialogState" in data["request"] else None,
            "type": data["request"]["type"] if "request" in data and "type" in data["request"] else None,
            "alexa_error": data["request"]["error"]["message"] if "request" in data and "error" in data["request"] and "message" in data["request"]["error"] else None
        }

        return request

    def api_call(self, data):
        """
        All alexa requests come thought this function to be parsed into constituent parts.

        Parameters:
            data (dict): The alexa request.
        """

        # The intent can be fetched from a helper function.
        self.intent_name = str(self.get_alexa_intent(data))
        # We can get all the slots from the request using this helper function.
        self.slots = self.get_alexa_slot_value(data)

        # Get context data we'll need for... we'll see
        self.context = self.set_context(data)
        self.log("Context information: {}".format(self.context), level = "DEBUG")

        # Get the request data
        self.request = self.get_request(data)
        self.log("Request information: {}".format(self.request), level = "DEBUG")

        # If we got an error, log it
        if self.request["alexa_error"] is not None:
            self.log(self.request["alexa_error"], level = "ERROR")
        
        # At the moment I'm only handling intent requests, but I still need a check
        if self.request["type"] == "IntentRequest":
            result = self.alexa_intent_parser()
        else:
            result = self.just_saying("I fell into an unknown request type.")

        if not isinstance(result, dict):
            self.log("Did not receive a dictionary from the parser. Stringified value:" + str(result), level = "ERROR")
            result = self.just_saying("An unknown error has occurred.")
        
        return result, 200

    def alexa_intent_parser(self):
        """
        Trigger the correct intent processor based on the intent name.
        """

        # Validate that we have a method for the given intent
        intents = {
            #"AMAZON.CancelIntent": self.amazon_cancel_intent_handler,
            #"AMAZON.HelpIntent": self.amazon_help_intent_handler,
            #"AMAZON.NoIntent": self.amazon_no_intent_handler,
            #"AMAZON.StopIntent": self.amazon_stop_intent_handler,
            #"AMAZON.YesIntent": self.amazon_yes_intent_handler,
            "turn_on": "int_turn_on_off",
            "turn_off": "int_turn_on_off",
            "turn_up_down_by": "int_up_down",
            "media_control": "int_media_control"
            # fan oscillate/turn on & oscillate
            # ecobee resume schedule (cancel hold) / set to specific temperature
        }

        # Check that the sent intent is mapped above.
        if self.intent_name in intents:
            method = getattr(self, intents[self.intent_name])
            return method()
        else:
            self.log("Unmapped intent request.", level = "ERROR")
            return self.just_saying("I'm sorry, I don't know how to do that.")

    ###
    # Intent Handlers.
    ###

    def int_up_down(self):
        """
        An intent for turning something up of down incrementally.
        TV volume, fan speed, thermostat, etc.
        """
        
        # The increment can be controlled by a number slot or a once/twice slot
        if "up_down_by_once_twice" in self.slots:
            increment = 2 if self.slots['up_down_by_once_twice']['value'] == "twice" else 1
        elif "value" in self.slots['up_down_by_increment']:
            increment = int(self.slots['up_down_by_increment']['value'])
        else:
            increment = 1
        
        device_id = self.slots['up_down_by_device']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
        up_down = self.slots['up_down_by_up_down']['value']
        service = ""
        service_data = {}

        # The TV can have it's volume increased or decreased incrementally.
        if device_id == "the_tv":
            service = "remote/send_command"
            service_data = {
                "entity_id": "remote.living_room",
                "device": 60888940,
                "command": "VolumeUp" if up_down == "up" else "VolumeDown",
                "num_repeats": increment
            }
            self.call_service(service, **service_data)
        # The fan only increments. It loops to the slowest speed when after maxing out.
        elif device_id == "the_fan":
            service = "remote/send_command"
            service_data = {
                "entity_id": "remote.living_room",
                "device": 55184762,
                "command": "FanSpeed",
                "num_repeats": increment
            }
            self.call_service(service, **service_data)
        # The bedroom AC's temperature can been incremented or decremented.
        elif device_id == "bedroom_ac":
            service = "broadlink/send"
            if up_down == "up":
                packet = "JgBQAAABJZMRExMSEBUSNxISEhMRFBISEzcRExE5ERMRORE4ETgSOBETETkROBE4EhMRFBAUERQROBEUEBQRFBA5EjgROBE4EgAFOwABIkwUAA0FAAAAAAAAAAA="
            else:
                packet = "JgBQAAABI5YRExITEBQSOBETEhMRFBETEjgRExE5ERMROBE5ETgSOBE4ERQROBE4EhMRFBETERQRExI4ERMSExA5EjgROBE4EgAFOwABIk0RAA0FAAAAAAAAAAA="
            service_data = {
                "host": "192.168.131.4",
                "packet": [ packet ] * increment
            }
            self.call_service(service, **service_data)
        # Climate is less straight forward. We can't increment directly.
        elif device_id == "the_thermostat":
            service = "climate/set_temperature"
            thermostate_entity_id =  "climate.cottage"

            # We need to get the current temp then add or remove the get to the new value.
            current_temp = self.get_state(thermostate_entity_id, attribute="temperature")

            if up_down == "up":
                target_temp = current_temp + increment
            else:
                target_temp = current_temp - increment

            service_data = {
                "entity_id": thermostate_entity_id,
                "temperature": target_temp
            }
            self.call_service(service, **service_data)
        else:
            service = None
            service_data = None
        # TODO: phase2: Add bedroom tv volume control
        # TODO: phase2: sanity check (especially thermostat) and throw errors if outside. Gracefully handle in alexa_intent_parser
        
        self.log("Device: {} - Up/Down: {} - Service: {} - Service Data: {}".format(device_id, up_down, service, service_data), level = "DEBUG")

        return self.just_saying("Up down! Whooooo!")

    def int_turn_on_off(self):
        """
        Find a device by name (Amazon.SearchQuery intent type) and then turn it on or off.
        Devices defined in the database as being in the "method" domain will send
            their data to the method special_on_off
        """

        # Use the intent name to decide if this is an on or an off.
        if self.intent_name == "turn_on":
            on_off = "on"
            slot_name = "on_device"
        else:
            on_off = "off"
            slot_name = "off_device"

        # Turn the sent value into a dictionary or search tokens.
        heard_device_tokens = self.device_tokenizer(self.slots[slot_name]['value'])

        # Find the device by name.
        device = self.device_by_name(heard_device_tokens)

        # If were don't need to fall back then we should have domain and entity data.
        if device["fallback"] == False:
            service = ""
            service_data = {}
            # HA devices can be turned on and off directly
            if device['domain'] != "method":
                service = "homeassistant/turn_{}".format(on_off)
                service_data = { "entity_id": device["entity_id"] }
            # Python methods can return explicit service and service data.
            else:
                method = getattr(self, device['entity_id'])
                service, service_data = method(device["name"], on_off)

            # Call the service that was found.
            self.log("Service: {} - Service Data: {}".format(service, service_data), level = "DEBUG")
            if service and service_data:
                self.call_service(service, **service_data)
                msg = "I'll turn {} {}".format(on_off, device["name"].replace("_", " "))
            else:
                self.log("Invalid service or service data values. Service: {} - Service Data: {}".format(service, service_data), level = "ERROR")
                msg = self.fallback(fb_from = "service and service data check")
        else:
            msg = self.fallback(fb_from = "device check")

        return self.just_saying(msg)

    def int_media_control(self):
        """
        Basic media control functionality. Play, Pause, Stop, etc
        """

        msg = "Hey weird future Daryl"

        return self.just_saying(msg)

    ###
    # Special control methods.
    ###

    def special_on_off(self, name, on_off):
        """
        There are some devices that don't have explicit on off comands.
        
        Parameters:
            name (string): The device name as it appears in the database.
            on_off (string): Either 'on' or 'off'
        """
        self.log("Special on/off values. Name: {} - On/Off: {}".format(name, on_off), level = "DEBUG")

        service = ""
        service_data = {}
        if name == "the_tv":
            service = "script.media_on_off"
            service_data = {
                "entity_id": "script.media_on_off",
                "on_off": on_off
            }
        elif name == "the_fan":
            service = "remote/send_command"
            service_data = {
                "entity_id": "remote.living_room",
                "device": 55184762,
                "command": "PowerToggle"          
            }
        elif name == "bedroom_ac":
            service = "broadlink/send"
            service_data = {
                "host": "192.168.131.4",
                "packet": [ "JgBYAAABI5YQFBEUEBUQORAVEBQQFRAUETkQFBE5EBQRORA5EDkRORA5ERQQFRAUEDkRFBAVEBQRFBA5ETkQOREUEDkRORA5EAAFPQABJUoQAAxLAAEhTBEADQU=" ]
            }
        else:
            service = None
            service_data = None
        # TODO: The bedroom TV
        # TODO: Thermostat
        #   Multistep: mode to auto then ask for temp or normal schedule
        
        return service, service_data
    
    def fallback(self, **kwargs):
        msg = "We landed in fallback."
        if "fb_from" in kwargs:
            msg += " From " + kwargs.get("fb_from")
        self.log(msg, level = "WARNING")

        return "I'm a fallback kind of AI."
    
    ###
    # Device searching and caching.
    ###
    
    def device_by_name(self, tokens):
        # try to find in sql using all tokens
        sql_hit = self.device_from_sql(tokens)

        self.log("data from sql: {}".format(sql_hit), level = "DEBUG")
        # else loop though valid domains in likely order
        # cache successes and their tokens
            # Don't cache a soundex match?
        if sql_hit:
            device_data = sql_hit
        else:
            api_hit = self.device_from_api(tokens)
            device_data = api_hit if api_hit else None
        
        self.log("device data: {}".format(device_data), level = "DEBUG")

        # We always want to return sane data, so we add a sanity key
        if isinstance(device_data, dict) and "domain" in device_data and "entity_id" in device_data:
            device_data["fallback"] = False
        # If our data is bad we'll improve it
        else:
            self.log("Invalid device data returned. Data: {}".format(device_data))
            device_data = { "fallback": True }

        return device_data

    def device_from_api(self, tokens):
        """
        Gets a list of strings and searches a defined set of domains for them.
        If a find is made it will also store the result in sql for later.

        Parameters:
            tokens (list): device name tokens from the tokenizer method.
        """
        if not isinstance(tokens, list) or len(tokens) == 0:
            self.log("No list of tokens given with which to query.", level = "WARNING")
            return False

        device_found = False
        for domain in self.search_domains:
            if device_found:
                break
            
            for token in tokens:
                api_check = self.entity_exists(domain + "." + token)
                self.log("Searching for {} in domain {} resulted in a {}".format(token, domain, api_check), level = "DEBUG")

                if api_check:
                    self.log("Found {} in domain {}".format(token, domain))
                    device_found = True
                    device = {
                        "domain": domain,
                        "name": token,
                        "entity_id": domain + "." + token,
                        "fallback": False
                    }

                    self.cache_device(device, tokens, token)

                    break
        else:
            device = False

        return device

    def cache_device(self, device, tokens, best_match):
        """
        Any matches that we needed to search the API for should get cached in sql.
        """
        if not isinstance(device, dict) or not isinstance(tokens, list):
            return False
        
        connection = pymysql.connect(**self.sql_params)

        # assemble insert values
        values = []
        for token in tokens:
            exact_match = 1 if token == best_match else 0
            values.append("('{}', '{}', '{}', '{}', NOW())".format(
                connection.escape_string(token), 
                connection.escape_string(device["domain"]),
                connection.escape_string(device["entity_id"]),
                exact_match
            ))


        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO `devices` (`name`, `domain`, `entity_id`, `exact_match`, `cached_on`)
                    VALUES {} ON DUPLICATE KEY
                    UPDATE `domain` = '{}', `entity_id` = '{}', `cached_on` = NOW()""".format(
                        ",".join(values),
                        device["domain"],
                        device["entity_id"])

                self.log("Insert Statement: " + ' '.join(sql.replace('\r', ' ').replace('\n', ' ').split()), level = "DEBUG")
                cursor.execute(sql)
            
            connection.commit()
        except pymysql.InternalError as e:
            self.log('Got error {}, errno is {}'.format(e.args[1], e.args[0]), level = "ERROR")
            return False
        else:
            return True
        finally:
            connection.close()

    def device_from_sql(self, tokens):
        """
        Gets a list of strings and searches the sql backend for them.

        Parameters:
            tokens (list): device name tokens from the tokenizer method.
        """

        if not isinstance(tokens, list) or len(tokens) == 0:
            self.log("No list of tokens given with which to query.", level = "WARNING")
            return False

        try:
            connection = pymysql.connect(**self.sql_params)

            if len(tokens) > 1:
                where = "' OR `name` = '".join(tokens)
            else:
                where = tokens[0]
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT `name`, `entity_id`, `domain`, `exact_match` FROM `devices` WHERE `name` = '" + where + "' ORDER BY `exact_match` DESC LIMIT 1"
                cursor.execute(sql)
                result = cursor.fetchall()
                if isinstance(result, list) and isinstance(result[0], dict):
                    result = result[0]
        except pymysql.InternalError as e:
            self.log('Got error {}, errno is {}'.format(e.args[1], e.args[0]), level = "ERROR")
        else:
            if not isinstance(result, dict):
                result = False
            return result
        finally:
            connection.close()

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
            if not device.startswith("a_"):
                tokens.append("a_" + device)
                tokens.append(device + "s")
            tokens.append("the_" + device)
        
        return tokens
    
    ###
    # Reply formatters
    ###

    def just_saying(self, speech):
        response = {
            "outputSpeech": {
                "type": "PlainText",
                "text": speech
            },
            "shouldEndSession": True
        }

        sessionAttributes = {} #self.getSessionAttributes(data)

        return {
            "version": "1.0",
            "response": response,
            "sessionAttributes": sessionAttributes
        }