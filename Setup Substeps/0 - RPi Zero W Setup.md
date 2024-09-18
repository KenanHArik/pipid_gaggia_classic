# Instruction on How to Set Up a Raspberry Pi Zero W (Headless)

The following instructions go over first setup a Raspberry Pi for running the software of this repository.

## Setting up Raspberry Pi OS SD card

1. Download and Install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your PC. This will be used to write the Pi OS to the SD card.
   1. Choose OS as Raspberry Pi OS (other) -> Raspberry Pi OS Lite 32-bit
   2. Choose SD card in storage
   3. Enable OS customization
      1. Enable SSH with password authentication
      2. Set a username (recommended pi) and password
      3. Configure the wireless WLAN, including country
      4. Set locale settings for timezone
      5. Disable Telemetry
      6. Click Save
   4. Click Yes to Flash

> If you ever need to change wifi settings, ssh and edit the wpa supplicant:
> `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

## Connecting to the Raspberry Pi

1. Insert the SD card to the Pi Zero W (if not already) and allow time for it to boot.
2. After booting, the Pi should be on the network and we need to connect via SSH. Download and install [Putty](https://www.putty.org/) if you don't already have it. Putty is the leading SSH client for Windows.
3. Determine the IP address of the Raspberry Pi by looking at your network connections on your router. Once you confirm it is connected, connect via ssh to the IP address of the Pi. This process may take up to 5 minutes.

   - If there is a connection issue after 5 minutes, reconnect and try again. Note the ssh file and wpa_supplicant are deleted by default in the process of boot when they are read in, and will need to get re-created.

4. Connecting via SSH. This can be done inbuilt with Windows, or via PuTTY
   1. For Windows console, an example is `ssh pi@XXX.XXX.XXX.XXX` where format follows user@IP address.
   2. For PuTTY: Put in the IP address and port 22 connection. The first time it is connected
5. For the first connection, it will present to you a security warning that the host cannot be verified. Click Ok if you get a security warning alert. It's not a problem.
6. Enter pi as your username and raspberry as your password.

## Updating and basic configuration of the Pi

1. Update the Pi OS to the latest by running `sudo apt update` and then `sudo apt full-upgrade`. After this it is a good idea to clean up packages with `sudo apt clean`
