# Home Assistant

![Universal remote phone view](screenshots/mobile_media.png)

I have been work to automate my home as much as my 50 year old wiring allows. I aim to accomplish all my automations with a RaspPi, no other hubs apart from the usb z-wave stick. This has been a slow evolutionary config.

# Features

* Meant for default lovelace.
  * My legacy config is still in place but far less capable.
* Fully managed for all my sensors and devices. No auto discovery.
* Universal remote for my media center.
* Dynamic alexa intents. So far just for my media center.
  * "Alexa ask home assistant to turn the tv up by 5."
* Presence detection using Tile trackers.
  * Sensor template to indicate when the house is empty.
* On/Off control for Z-Waze through Home Assistant Cloud / Nebu Casa
  * Mainly to suppost the Home Assisant.
* Documentation tab in the app through markdown cards
* Custom Button Card from [kuuji/button-card](https://github.com/kuuji/button-card)
* Custom Attribute Card from [ciotlosm/custom-lovelace](https://github.com/ciotlosm/custom-lovelace)
* IFrame-able weather map from [windy.com](https://www.windy.com/)

## Screen Shots

* [Home Tab](screenshots/view_home.png)
* [Climate Tab](screenshots/view_climate.png)
* [Indoor Climate Tab](screenshots/view_ndoor-climate.png)
* [Camera Tab](screenshots/view_camera.png)
* [Network Tab](screenshots/view_network.png)
* [Media Center Tab](screenshots/view_media.gif)

# My Setup

## Hardware

* Raspberry Pi 3
* Aeotech Z-Wave Stick
* GE Outdoor Z-Wave Switch
* EcoBee 2 Thermostat
* Harmony Home Hub
* Broadlink Mini 3 IP Blaster
* Intel NUC D54250WYK1 Intel 4th Gen Core i5-4250U running Windows 10 (HTPC / Plex Server)
* Roku Stick
* Synology
* Amazon Echo
* Amazon Echo Dot
* TP Link LB120 Tunable A19
* TP Link LB230 Multi-Color BR30
* 2x TP Link HS100 Wifi Switch
* TP Link HS105 Mini Wifi Switch
* 3x Tile Trackers
* Ring Video Doorbell 2
* Netatmo Indoor and Outdoor climate sensors

## Software / API

* Home Assistant
* Home Assisant Cloud
* Hass.io
* Custom Alexa Skill
* Dask Sky and Yahoo Weather
* Speedtest.net
* Waze Travel Time
* Windy.com

# This Repo

* This is a living document. What you see here is what is running my house.

## Structure
* All configs branch off configuration.yaml
* Files are broken up by functionality. Switches, sensors, scripts, etc.
  * The yaml that controls the individual lovelace tabes are stored in ```lovelace_cards/```
* Generated files (.conf, .log, .json, etc) are generally not committed.
* All sensitive information is stored on secrets.yaml which is also not committed.

## Home Assistant "TNG?"

The Next Generation: In 2017 in app config editors started to become available. When it was clear that I'd have to rework how I have split up my cofigs to make them work I decided to just start over from scratch.

The old conig is [here](https://github.com/Bishma/homeassistant). Yes, if I ever start over again the new repo will be ds9.