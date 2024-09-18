# Setting up the Raspberry Pi Software Stack

The following instructions go over how to configure the Raspberry Pi to run the software provided in this repository.

This setup assume that Debian version Bookworm is installed, which includes recent updates requiring the use of virtual environments for Python. See the following reference: https://learn.adafruit.com/python-virtual-environment-usage-on-raspberry-pi?view=all

## Installing Python Dependencies

1. Install pip and git using command via SSH connection `sudo apt install python3-venv`
2. Create a new virtual environment named pipid: `python3 -m venv pipid`
3. Activate the virual environment using `source pipid/bin/activate`
4. Get all the dependencies:
`pip install luma.oled`
`pip install simple-pid`

## Install pigpio library

1. First clear any existing libraries (if there was an existing install) using `sudo rm master.zip` and `sudo rm -rf pigpio-master`
2. Download the latest pigpio library using `wget https://github.com/joan2937/pigpio/archive/master.zip`
3. Extract the installer `unzip master.zip` and navigate to the directory `cd pigpio-master`
4. Run the installer with the commands `make` and `sudo make install`
5. Install the pigpio specific packages `sudo apt-get install pigpio python3-pigpio`
6. After the installation is successful, the dameon needs to run in the background. It can be started at boot with `sudo systemctl enable pigpiod` and turned on with `sudo systemctl start pigpiod`. Note: To just get it running crudely without a service, use `sudo pigpiod`.
7. Install it in the virtual environment `pip install pigpio`

## Turn on I2C and SPI

1. Run `sudo raspi-config`, go to `Interface Options`, then `I2C` and set to enable. Similarly, do the same for `SPI` in the same menu.
2. Reboot the Pi
   - I2C is required to communicate with the display, SPI is used for the temperature sensor.
