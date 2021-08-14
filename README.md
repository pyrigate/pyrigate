<div>
    <img src="pyrigate-logo.png" align="left" width="22%" style="margin-right:40px" />
</div>

# pyrigate 💦🌱
#### v0.1.0

[![Supported python versions](https://img.shields.io/badge/python-3.4%20%7C%203.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://shields.io/)

<div style="margin-top:40px" />

Water your plants with an automated irrigation system! This is an ongoing
project under development. There is also a [companion mobile
app](https://www.github.com/pyrigate/mobile-app) under development.

**DISCLAIMER**: I am not an electrical engineer or anything of the sort, use
the instructions and code at your own risk.

## Installation

Clone the repository and run the install script.

```bash
$ git clone https://github.com/MisanthropicBit/pyrigate
$ python setup.py install
```

## Current Setup

Below is a list of hardware parts.

* Relay (prevents current flyback that could fry the Raspberry Pi board)
* 5-12V self-priming water pump
* 2 x 4mm silicone tube
* A universal power adpater
* Water tank or some other container
* Jumper wires

Future hardware:
* Moisture sensor (optional)
* Water level sensor (optional)

## TODO

- [x] Test water pump operation
- [ ] Test email system
- [ ] Test water level sensor
- [ ] Test moisture sensor

### Similar Projects

There are many similar projects which were an inspiration for this project.

* [Chili irrigation system with webhooks](https://blog.serverdensity.com/automatically-watering-your-plants-with-sensors-a-pi-and-webhooks/)
* [TechRadar article](http://www.techradar.com/how-to/computing/how-to-automatically-water-your-plants-with-the-raspberry-pi-1315059)
* [PiPlanter](http://www.esologic.com/piplanter-a-plant-growth-automator/)
* [PiPonics](https://github.com/matthewh415/PiPonics)
* [Solar-powered water bot](https://github.com/mistylackie/solar-water-bot)
* [pleasetakecareofmyplant](https://github.com/tylerjaywood/pleasetakecareofmyplant)
* [Plant Friends](http://dicksonchow.com/plant-friends/)
* [GreenPiThumb](https://mtlynch.io/greenpithumb/)
* [GardenPi](https://spin.atomicobject.com/2014/06/28/raspberry-pi-gardening/)
* [MyHydroPi](https://github.com/dombold/MyHydroPi)
