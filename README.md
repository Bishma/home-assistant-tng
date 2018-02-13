# Home Assistant: The Next Generation

After Home Assistant started adding in-app config editors that required a certain file layout I started from scratch with my configs.

## Structure
* All configs branch off configuration.yaml
* Files are broken up by functionality. Switches, sensors, scripts, etc.
* Generated files (.conf, .log, .json, etc) are not committed.
* All sensitive information is stored on secrets.yaml which is also not committed.
* Some customization still reference the hue bridge even though I don't use that any more.

## Platforms in use
* TP-Link
* Ecobee
* Harmony
* Tile
* Alexa (using Home Assistant Cloud)
* Ring
* Kodi
* Roku
* Dark Sky
* fast.com
* Synology