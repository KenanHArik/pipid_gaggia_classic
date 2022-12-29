# Setting up the Raspberry Pi Software Stack

The following instructions go over how to configure the Raspberry Pi to run the software provided in this repository.

## Installing Python Dependencies

1. Install pip and git using command `sudo apt-get install git python3-pip`
2. Get all the dependencies:

For reference, the following have been installed:

sudo apt-get install git python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y

The above dependencies are required for luma oled library.
sudo pip3 install luma.oled

PID control is based on the library below
pip3 install simple-pid

## Turn on I2C and SPI

1. Run `sudo raspi-config`, go to `Interface Options`, then `I2C` and set to enable. Similarly, do the same for `SPI` in the same menu.
2. Reboot the Pi
   - I2C is required to communicate with the display, SPI is used for the temperature sensor.

## Install pigpio library

1. First clear any existing libraries (if there was an existing install) using `sudo rm master.zip` and `sudo rm -rf pigpio-master`
2. Download the latest pigpio library using `wget https://github.com/joan2937/pigpio/archive/master.zip`
3. Extract the installer `unzip master.zip` and navigate to the directory `cd pigpio-master`
4. Run the installer with the commands `make` and `sudo make install`
5. Install the pigpio specific packages `sudo apt-get install pigpio python-pigpio python3-pigpio`
6. After the installation is successful, the dameon needs to run in the background. It can be started at boot with `sudo systemctl enable pigpiod` and turned on with `sudo systemctl start pigpiod`. Note: To just get it running crudely without a service, use `sudo pigpiod`.
