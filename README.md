# Home Assistant

I have been work to automate my home as much as my 50 year old wiring allows. I aim to accomplish all my automations with a RaspPi, no other hubs apart from the usb z-wave stick. This has been a slow evolutionary config.

## Home Assistant The Next Generation?

After Home Assistant started adding in-app config editors that required a certain file layout I started from scratch with my configs.

# Features

* Fully managed for all my sensors and devices. No auto discovery.
* Harmony controls through scripts.
  * I am working toward having a universal remote in Home Assisant.
* Dynamic alexa intents. So far just for my media center.
  * "Alexa ask home assistant to turn the tv up by 5"
* Presence detection using Tile trackers.
  * Sensor template to indicate when the house is empty.
* Custom Button Card from [kuuji/button-card](https://github.com/kuuji/button-card)
* Custom Attribute Card from [ciotlosm/custom-lovelace](https://github.com/ciotlosm/custom-lovelace)
* IFrame-able weather map from [windy.com](https://www.windy.com/) 

## Screen Shots

I will add these as soon as I finish migraging to lovelace.

# This Repo

* This is a living document. What you see here is what is running my house.

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
* Home Assistant Cloud
* Ring
* Broadlink
* Dark Sky
* Speedtest.net
* Synology
* Yahoo Weather
* Z-Wave