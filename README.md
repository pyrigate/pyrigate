# pyrigate v0.1.0 💦🌱

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

* Relay (prevents current flyback that could fry the Raspberry Pi board)
* [5-12V self-priming water pump](https://www.ebay.com/itm/172845971977)
* [4mm silicone tube](https://www.ebay.com/itm/142324532992)
* Water tank
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
