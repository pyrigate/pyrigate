# pyrigate v0.1.0 💦🌱

[![Supported python versions](https://img.shields.io/badge/python-3.4%20%7C%203.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://shields.io/)

Water your plants with an automated irrigation system! This is an ongoing
project under development.

**DISCLAIMER**: I am not an electrical engineer or anything of the sort, use
the instructions and code at your own risk.

Progress pic:

![Progress pic](/coming_soon.png)

## Installation

Clone the repository and run the install script.

```bash
$ git clone https://github.com/MisanthropicBit/pyrigate
$ python setup.py install
```

## Current Setup

Below is a diagram of the current hardware setup and a full list of parts.

* [Relay](https://elextra.dk/details/H16117/5v-relaemodul-m-optokobler-til-arduino-2-kanals) (prevents current flyback that could fry the Raspberry Pi board)
* [5-12V self-priming water pump](https://www.ebay.com/itm/172845971977)
* [4mm silicone tube](https://www.ebay.com/itm/142324532992)
* [A universal power adpater](https://elextra.dk/details/H26063/universal-netadapter-3-12vdc-18w-15a-usb-6-stik)
* Water tank or some other container
* Jumper wires
* Moisture sensor (optional)
* Water level sensor (optional)

## TODO

- [ ] Test water pump operation
- [ ] Test email system
- [ ] Test water level sensor
- [ ] Test moisture sensor

## Similar Projects

There are many similar projects which were an inspiration for this project.

* [Chili irrigation system with webhooks](https://blog.serverdensity.com/automatically-watering-your-plants-with-sensors-a-pi-and-webhooks/)
* [TechRadar article](http://www.techradar.com/how-to/computing/how-to-automatically-water-your-plants-with-the-raspberry-pi-1315059)
* [PiPlanter](http://www.esologic.com/piplanter-a-plant-growth-automator/)
* [Aquaponics](https://github.com/matthewh415/PiPonics)
* [Solar-powered water bot](https://github.com/mistylackie/solar-water-bot)
* [pleasetakecareofmyplant](https://github.com/tylerjaywood/pleasetakecareofmyplant)
* [Plant Friends](http://dicksonchow.com/plant-friends/)
* [GreenPiThumb](https://mtlynch.io/greenpithumb/)
* [GardenPi](https://spin.atomicobject.com/2014/06/28/raspberry-pi-gardening/)
* [MyHydroPi](https://github.com/dombold/MyHydroPi)
