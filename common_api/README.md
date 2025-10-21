# Distance & Angle Interfaces

These modules define the data interfaces and sensor abstractions used by the EchoNav system to connect hardware-level readings (from ultrasonic and gyroscope sensors) with feedback components.

**Author:** Josh Dean <br>
**Last Modified:** 21/10/2025

## Overview

The Distance and Angle interface serve as the standardized communication layer between the system’s sensor hardware and processing modules.

# Distance

The Distance module defines how ultrasonic distance sensors mounted on the four corners of the car are represented and accessed.

## Core Components:

- `CarCorner` -> identifies each sensor location (Front Left, Front Right, Back Left, Back Right) and stores its GPIO pin assignments for trigger/echo signals.
- `DistanceReading` -> stores a single distance measurement and its associated corner, allowing other modules to interpret proximity data uniformly.

## Used By:

- `UltrasonicCapture` -> for reading and validating sensor data.
- `SpeakerBeep` -> for determining how frequently to emit beeps based on the closest detected obstacle.

# Angle

The Angle module provides an abstraction layer for gyroscope or data. It tracks the car’s orientation and turning direction.

## Core Components:

- `TurnState` -> defines vehicle turn direction (Left Turn, Idle, Right Turn) for consistent communication with control systems.
- `AngleReading` -> represents orientation or angular velocity readings from the gyroscope sensor, typically including yaw or heading data.