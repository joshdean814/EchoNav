# EchoNav: Ultrasonic Obstacle Detection and Visual Feedback System

**Last Edited:** 21/10/2025

## Overview
The `EchoNav` project integrates low-cost ultrasonic sensors and a gyroscope with the RaspberryPi GPIO pin interface to create a real-time obstacle detection and navigation assistance system. 

`EchoNav` provides parking assistance via two feedback modalities: audio and visual. The system detects nearby objects and emits a corresponding alarm depending on the corresponding proximity. Depending on the steering wheel orientation, it also displays a vector indicating the current steering orientation of the RC vehicle, shown on the 8x8 LED grid of the RaspPi.

This project was developed for the course assignment for 1DT086 & 1DT032: Intro. to Studies in Embedded Systems.

## Team Members
| Name | Role | Responsibilities |
|------|------|------------------|
| Josh Dean | Leader | Task coordination, GitHub management, hardware setup, collision detection, testing |
| Yihang Feng | Time Keeper | Meeting scheduling, auditory alert feedback |
|  Prabandh Battu | Developer | Steering angle capturing, hardware setup |
| Anju Damodaran | Recorder | Visual feedback display |

## Timeline
**Week 1:** Project planning, literature review, equipment retrieval.
**Week 2:** Hardware setup & initial coding. \
**Week 3:** Distance detectors, gyroscope configured. \
**Week 4:** LED display, speaker output configured. \
**Week 5:** Building main process loop. \
**Week 6:** Integration of hardware\software. \
**Week 7:** Testing & optimization. \
**Week 8:** Final report & presentation preparation.

## Features
* Ultransonic distance detection
* Calibrated gyroscope orientation capture
* Dual-modal feedback mechanism

## Tech Stack

### Hardware
* 4 HC-SR04 ultrasonic distance sensors
* MPU6050 3-axis gyroscope
* Raspberry Pi 3-B, or similar
* Rasp Pi GPIO pin board extender

### Software
* SenseHat
* RPi.GPIO
* sounddevice
* mpu6050

## Setup Instructions

### Hardware Setup
1. Use the Rasp. Pi extender to expose the GPIO board.
2. Mount the ultrasonic detectors on the RC car, and the gyroscope on the remote control.
3. Wire the ultrasonic sensors to the following GPIO pin assignments:
> [!NOTE] 
> These are GPIO assignments, NOT physical pin assignments. VCC should come from a common 5V pin, and all grounds can be combined.

   | Car Corner | TRIG Pin | ECHO Pin |
   |---------|----------|----------|
   | Back Right | 17 | 27 |
   | Back Left | 16 | 26 |
   | Front Right | 5 | 6 |
   | Front Left | 20 | 21 |

> [!WARNING]
> You must reduce the 5V return voltage from the echo pin to 3.3V using a simple voltage divider circuit. We used a 1KΩ and 2KΩ to achieve this.

4. Wire the gyroscope to the following GPIO pin assignments:
> [!NOTE] 
> These are physical pin assignments. 

   | VCC Pin | GND Pin | SCL Pin | SDA Pin | ADO Pin |
   |---------|---------|---------|---------|---------|
   | 1 | ANY GND | 5 | 3 | ANY GND |

### Software Setup
1. Clone the repo:
```bash
git clone git@github.com:joshdean814/EchoNav.git
```

2. Install dependencies:
```bash
cd /path/to/EchoNav
python -m venv .EchoNav
source .EchoNav/bin/activate # or .EchoNav\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Start main execution loop:
```bash
python echo_nav.py
```