# Home Assistant: The Next Generation

After Home Assistant started adding in-app config editors that required a certain file layout I started from scratch with my configs.

## Structure
* All configs branch off configuration.yaml
* Files are broken up by functionality. Switches, sensors, scripts, etc.
* Generated files (.conf, .log, .json, etc) are not committed.
* All sensitive information is stored on secrets.yaml which is also not committed.

## Platforms in use
* TP-Link
* Ecobee
* Harmony
* Tile
* Alexa (using a custom skill / intents / scripts)
* Ring
* Broadlink
* Roku
* Dark Sky
* Speedtest.net
* Synology