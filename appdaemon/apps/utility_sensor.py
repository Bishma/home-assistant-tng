## Utility Sensors

import appdaemon.plugins.hass.hassapi as hass
import datetime

#
# Dates
# Proof of concept to power intent speech
#
class Date(hass.Hass):

    def initialize(self):
        time = datetime.time(0, 0, 0)
        self.handle = self.run_minutely(self.dateState, time)
        self.log("Date sensor initialized.")

    def dateState(self, kwargs):
        now = datetime.datetime.now()
        self.set_state("sensor.janet_utility_date", state = now.strftime('%Y-%m-%d %H:%M'), attributes = {
            "r_dow": now.strftime('%A'),
            "r_month": now.strftime('%B'),
            "r_day": str(now.day) + self.suffix(now.day),
            "year": now.strftime('%Y')
        })

    def suffix(self, d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
