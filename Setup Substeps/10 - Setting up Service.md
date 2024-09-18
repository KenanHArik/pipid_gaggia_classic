# System Service Setup

The Raspberry Pi will be configured to run the python script always so that it comes up on boot, and goes on in the background.

To do this, there are a few ways, but the recommended way is to setup the python script as a service.

Instructions for this were inspired from this site: https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/

Run the command to create the service file
`sudo nano /etc/systemd/system/pi_espresso.service`

Copy the following contents - make sure the path matches where you have items stored. In the case below, it is in /home/pi/espresso/ directory

```bash
[Unit]
Description=Raspberry Pi Espresso Service
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/bin/bash -c "source /home/pi/pipid/bin/activate/ && /home/pi/espresso/pi_espresso.py"
Restart=always

[Install]
WantedBy=multi-user.target
```

Change the file permissions
`sudo chmod 644 /etc/systemd/system/pi_espresso.service`

Configure the system services, and set it to enabled.
`sudo systemctl daemon-reload`
`sudo systemctl enable pi_espresso.service`

For further reference on system services, refer to https://www.fosslinux.com/50724/how-to-start-stop-and-restart-services-on-debian.htm
