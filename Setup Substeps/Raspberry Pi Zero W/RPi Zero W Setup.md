# Instruction on How to Set Up a Raspberry Pi Zero W (Headless)

## Setting up Raspberry Pi OS SD card

1. Go to the [Raspberry Pi OS](https://www.raspberrypi.org/software/operating-systems/) download site, and download the latest version of OS Lite. The Lite version is selected here since there won't be any desktop environment needed. Raspberry Pi OS was formally known as Raspbian.

   - Current version for refernce is Kernel 5.10
   - Extract the zip file to a good location

2. Install [balenaEtcher](https://www.balena.io/etcher/) on your PC. This will be used to write the Pi OS to the SD card.
3. Open balenaEtcher

   - Select `flash from file`, and select the img file of the Raspberry Pi OS
   - `Select target` to be the SD card for the Raspberry Pi.
   - Click `Flash`
   - balenaEtcher will now begin writing the image to the SD card. Windows may open prompts in the process as the ca    rd visibility comes and goes.

## Enabling SSH and Network Connection

1. After flash is complete, close balenaEtcher and open file explorer. In file explorer, open the partition called `boot`.

    - If you don't see the partition, remove and reinsert the SD1 card. If prompted to format from windows, DO NOT format!
2. Write an empty text file named `ssh` (no file extension) to the root of the directory of the card. When it sees the "ssh" on its first boot-up, Raspberry Pi OS will automatically enable SSH (Secure Socket Shell), which will allow you to remotely access the Pi command line from your PC.
3. Configure a network connection for your Raspberry Pi, by creating a file called `wpa_supplicant.conf`. You will need the following text in the file (Enter your actual SSID and password, within the quotes provided).

    ```bash
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US

    network={
        scan_ssid=1
        ssid="your_wifi_ssid"
        psk="your_wifi_password"
        key_mgmt=WPA-PSK
    }
    ```

4. Remove the SD card from your PC, and plug it into the Raspberry Pi. Power on the Raspberry Pi, and upon boot up it will log you into the wireless network you provided.

## Connecting to the Raspberry Pi

1. Now that the Pi should be on the network (after a few minutes), we need to connect via SSH. Download and install [Putty](https://www.putty.org/) if you don't already have it. Putty is the leading SSH client for Windows.
2. Determine the IP address of the Raspberry Pi by looking at your network connections on your router. Once you confirm it is connected, connect via ssh to the IP address of the Pi. This process may take up to 5 minutes.

   - If there is a connection issue after 5 minutes, reconnect and try again. Note the ssh file and wpa_supplicant are deleted by default in the process of boot when they are read in, and will need to get re-created.

3. Connecting via SSH in putty. Put in the IP address and port 22 connection. The first time it is connected, it will present to you a security warning that the host cannot be verified. Click Ok if you get a security warning alert. It's not a problem.
4. Enter pi as your username and raspberry as your password.

## Updating and basic configuration of the Pi

1. Update the password by entering command `passwd` and following the prompts 
2. Update the Pi by running `sudo apt update` and then `sudo apt full-upgrade`. After this it is a good idea to clean up packages with `sudo apt clean`
3. Update the hostname by editing the /etc/hostname file with the command `sudo nano /etc/hostname`
    - This file contains only one line - the name of your Raspberry Pi.  Change the name to whatever you like, but only use the letters 'a' to 'z' (upper or lower), digits '0' to '9', and the dash '-'.
    Save the file using Ctrl+x, then Y followed by Enter.
4. Update the hostname at a second file `sudo nano /etc/hosts`
    - Find the line starting with 127.0.0.1, and change the name following it to your new hostname.  Save the file using Ctrl+x, then Y followed by Enter.
5. Once you have rebooted your Raspberry Pi, all other computers on your network should see it with the new hostname.  On the Raspberry Pi itself, you can check your hostname by issuing the command `hostname` in a terminal

    - For this project, the hostname was updated to `gaggiapi` since this will be used in a Gaggia espresso maker.
