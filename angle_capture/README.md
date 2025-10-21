# Angle Capture

This module captures and interprets angle data using an MPU6050 gyroscope and 
provides real-time directional feedback through the Sense HAT display.

**Author:** Prabandh Battu
**Last Modified:** 21/10/2025

## Overview

The AngleCapture class continuously reads angular velocity data from the MPU6050 gyroscope via the I2C
protocol. It estimates the yaw (rotation) angle and determines whether the car is turning left, 
right, or remaining idle (facing straight up or down).

## Strategy

1. Initialization:

- Connects to the MPU6050 gyroscope.
- Performs bias calibration to remove sensor drift.
- Starts a background thread for continuous sampling.

2. Processing:

- Reads the z-axis angular velocity.
- Filters the data using a low-pass filter.
- Integrates over time to determine yaw angle.
- Determines the turning direction based on angle thresholds.

## Core Functions

- `start` -> begins background angle tracking and sets the display to idle.
- `_detect_loop` -> main sensor loop that updates turn direction in real time.
- `_direction_from_yaw` -> determines turn state based on yaw.
- `_calibrate` -> averages multiple readings to compute gyroscope bias.
- `stop` -> stops the loop and clears the LED display.