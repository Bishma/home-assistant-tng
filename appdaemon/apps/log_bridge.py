import appdaemon.plugins.hass.hassapi as hass

class LogBridge(hass.Hass):

    def initialize(self):
        self.listen_log(self.cb)
    
    def cb(self, name, ts, level, message):
        msg = "[AppDaemon] {}: {}".format(name, message)
        self.call_service("python_script/log", level = level, message = msg)