##pyControl
pyControl is a control system for scientific instruments. It is designed to control the following instruments:

Newport ESP300 XYZ controller
Thorlabs MFF101 Flip Mirror
Lighthouse Photonics Sprout G12W Laser
Princeton Instruments Isoplane SCT320 Raman

Table of Contents
Introduction
Dependencies
Usage
Implementation
Contributing
License

Introduction
The pyControl repository contains working code for controlling a variety of scientific instruments. It includes Bayesian optimization code and LRPC implementations for rapid testing of different design patterns and parametric settings. This repository is designed to be easily readable and customizable for scientific applications.

Dependencies
The pyControl system requires the following dependencies:

Python 3.6 or higher
PyMeasure library
numpy
pandas
scipy
flipper
spectra
pressure
To install the dependencies, run the following command:

bash
Copy code
pip install pymeasure numpy pandas scipy flipper spectra pressure
Usage
To use the pyControl system, follow these steps:

Connect the hardware devices to your computer as specified in the documentation for each device.
Install the dependencies for the system (see Dependencies above).
Open the implementation for the device you want to use (in the LRPC_Implementations folder) and run the code.
Follow the instructions in the code to perform the desired scientific experiment.
Implementation
The line_codes file is a working model of the Bayesian Optimization code. The LRPC_Implementations folder is for rapid testing of different design patterns and parametric settings, which distinguishes it from the line_codes implementation. The LRPC Revisions are to be used for rapid testing of parametric boundaries and design shapes. It stands apart from the line_codes folder in that it is an object-oriented implementation of the code, which increases the readability.

Contributing
If you would like to contribute to the pyControl system, please follow these guidelines:

Fork the repository.
Create a new branch for your feature or bug fix.
Write tests for your changes.
Make your changes and ensure all tests pass.
Submit a pull request.
License
The pyControl system is released under the Apache License.

