# Ultrasonic Capture

This module is responsible for initializing and managing multiple ultrasonic sensors connected to the Raspberry Pi’s GPIO interface.

**Author:** Josh Dean <br>
**Last Modified:** 21/10/2025

## Overview

The code implements the UltrasonicCapture class, which coordinates distance measurement across multiple ultrasonic sensors mounted on the vehicle’s corners. Each sensor provides distance data to nearby objects using sound wave reflections. The module ensures stable readings and returns results as DistanceReading objects.

## Strategy

The module performs the following key tasks:

- Initializes all ultrasonic sensors defined in the CarCorner enumeration.
- Triggers each sensor sequentially to avoid cross-talk between signals.
- Calculates distance based on the speed of sound and signal travel time.
- Validates and averages multiple readings to improve accuracy.
- Prepares a list of DistanceReading objects representing the environment around the vehicle.

## Core Functions

- `read_all` -> Collects distance readings from all active ultrasonic sensors and returns them as a list.
- `shutdown` -> Safely cleans up all GPIO resources when the program terminates.