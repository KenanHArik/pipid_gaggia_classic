# Instruction on How to Set Up a Raspberry Pi Zero W (Headless)

The following instructions go over first setup a Raspberry Pi for running the software of this repository.

## Setting up Raspberry Pi OS SD card

1. Download and Install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your PC. This will be used to write the Pi OS to the SD card.
   1. Choose OS as Raspberry Pi OS Lite 32-bit
   2. Choose SD card in storage
   3. Click on the Gear Icon
      1. Enable SSH with password authentication
      2. Set a username and password
      3. Configure the wireless LAN, including country
      4. Set locale settings for timezone
      5. Click Save
   4. Click Flash

## Connecting to the Raspberry Pi

1. Now that the Pi should be on the network (after a few minutes), we need to connect via SSH. Download and install [Putty](https://www.putty.org/) if you don't already have it. Putty is the leading SSH client for Windows.
2. Determine the IP address of the Raspberry Pi by looking at your network connections on your router. Once you confirm it is connected, connect via ssh to the IP address of the Pi. This process may take up to 5 minutes.

   - If there is a connection issue after 5 minutes, reconnect and try again. Note the ssh file and wpa_supplicant are deleted by default in the process of boot when they are read in, and will need to get re-created.

3. Connecting via SSH in putty. Put in the IP address and port 22 connection. The first time it is connected, it will present to you a security warning that the host cannot be verified. Click Ok if you get a security warning alert. It's not a problem.
4. Enter pi as your username and raspberry as your password.

## Updating and basic configuration of the Pi

1. Update the Pi by running `sudo apt update` and then `sudo apt full-upgrade`. After this it is a good idea to clean up packages with `sudo apt clean`
