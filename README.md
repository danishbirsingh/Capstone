# Animal Intrusion Detection and Repellent System using Raspberry Pi, Pi Camera, Python, TensorFlow Lite, and Twilio API


The **Animal Intrusion Detection and Repellent System** is a project that aims to prevent unwanted animal intrusions in a specific area by using a combination of hardware components, image processing techniques, machine learning, and remote messaging capabilities. The system utilizes a Raspberry Pi, Pi Camera module, Python programming, TensorFlow Lite for object detection, and the Twilio API for over-the-internet messaging.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Hardware Components](#hardware-components)
- [Installation](#installation)
- [Usage](#usage)
- [Object Detection](#object-detection)
- [Messaging](#messaging)
- [Contributions](#contributions)
- [License](#license)

## Introduction

Unwanted animal intrusions can cause damage to property, crops, and gardens. The Animal Intrusion Detection and Repellent System offers a solution to this problem by detecting the presence of animals using image analysis and then triggering a repellent mechanism to drive them away. The system can also notify the user remotely through messaging if an intrusion is detected.

## Features

- **Real-time Animal Detection**: Utilize TensorFlow Lite's pre-trained model to detect animals in real-time using the Pi Camera feed.
- **Repellent Activation**: Activate a repellent system, such as ultrasonic sound or flashing lights, to scare away detected animals.
- **Remote Notifications**: Receive SMS or email notifications using the Twilio API to stay informed about intrusion events even when not on-site.
- **Customization**: Easily adjust detection sensitivity, repellent methods, and notification preferences.
- **User-friendly Interface**: Monitor and control the system through a simple web interface accessible from any device.

## Hardware Components

- Raspberry Pi
- Pi Camera module
- Ultrasonic or Passive Infrared (PIR) motion sensor
- Repellent devices (ultrasonic speaker, LED lights, etc.)
- Internet connectivity (Wi-Fi/Ethernet)
- Power source (battery or mains power)

## Installation

1. Clone this repository to your Raspberry Pi.
2. Install the required Python packages by running: `pip install -r requirements.txt`.
3. Set up your Twilio account and obtain API credentials.
4. Configure the system settings in the `config.py` file.
5. Connect the Pi Camera module and other hardware components.

## Usage

1. Run the main script: `python main.py`.
2. The system will capture camera feed and perform real-time animal detection.
3. If an animal is detected, the repellent mechanism will be activated.
4. You will receive a notification via SMS or email if configured.

## Object Detection

We employ TensorFlow Lite's pre-trained model for object detection. The model is optimized for resource-constrained devices like Raspberry Pi, ensuring real-time performance.

## Messaging

The Twilio API integration enables the system to send SMS alerts or emails to the user when an intrusion is detected. Make sure to securely configure your API credentials and messaging preferences in the `config.py` file.

## Contributions

Contributions to this project are welcome! If you have suggestions, bug reports, or feature requests, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to customize and enhance this README to better suit your project's specifics and your personal style. Good luck with your Animal Intrusion Detection and Repellent System!
