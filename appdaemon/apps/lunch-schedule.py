## Fetch the IDX Lunch Menu and put it into a sensor

import appdaemon.plugins.hass.hassapi as hass
import re, datetime, json, requests

class Lunch(hass.Hass):

    def initialize(self):
        time = datetime.time(0, 0, 0)
        self.run_daily(self.lunchState, time)
        self.lunchState(time)
        self.log("Lunch sensor initialized.")

    def lunchState(self, kwargs):
        # get the menu as a list
        lunchList = self.fetchMenu().get("data")

        # Turn it from a list of dictionaries into a single, useful, dictionary
        lunchDict = self.formatMenu(lunchList)

        # set the home assistant sensor
        self.setSensor(lunchDict)

    def fetchMenu(self):
        # @TODO handle get errors
        # @TODO handle unexpected data from api
        r = requests.get(self.get_state("sensor.appdaemon_lunch_api_endpoint"))
        lunchJson = r.json()
        return lunchJson
    
    def formatMenu(self, menuJson):
        menuDict = {}

        for dayInfo in menuJson:
            for lunchDateString, item in dayInfo.items():
                lunchDate = datetime.datetime.strptime(lunchDateString, "%m-%d-%y").date()
                menuDict[lunchDate.strftime("%Y%m%d")] = {
                    "item": item,
                    "dateObj": lunchDate
                }
        
        return menuDict

    def setSensor(self, lunchDict):
        today = datetime.date.today()
        sensorState = "none"
        nextThree = []

        nextCount = 0
        for dateString, lunchInfo in lunchDict.items():
            if lunchInfo["dateObj"] == today:
                sensorState = self.stripEmoji(lunchInfo["item"])
            
            if lunchInfo["dateObj"] >= today and nextCount < 3:
                nextThree.append(lunchInfo["dateObj"].strftime("%A, %m/%d") + ": "+self.stripEmoji(lunchInfo["item"]))
                nextCount+=1
        
        lastUpdated = datetime.datetime.now()
        lastUpdated = lastUpdated.strftime("%Y-%m-%d %H:%M:%S")

        self.set_state("sensor.janet_api_idx_lunch", state = sensorState, attributes = {
            "nextThree": nextThree,
            "lastUpdated": lastUpdated
        })
    
    def stripEmoji(self, itemString):
        emoji_pattern = re.compile("[\U00010000-\U0010ffff]+", flags=re.UNICODE)
        
        return emoji_pattern.sub(r'', itemString)