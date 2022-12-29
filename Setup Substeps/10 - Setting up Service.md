# System Service Setup

The Raspberry Pi will be configured to run the python script always so that it comes up on boot, and goes on in the background.

To do this, there are a few ways, but the recommended way is to setup the python script as a service.

Instructions for this were inspried from this site: https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/

Run the command to create the service file
`sudo nano /etc/systemd/system/pi_espresso.service`

Copy the following contents - make sure the path matches where you have items stored. In the case below, it is in /home/espresso/ directory

```bash
[Unit]
Description=pi_espresso Service
After=multi-user.target

[Service]
WorkingDirectory=/home/espresso/
ExecStart=/usr/bin/python3 /home/espresso/pi_espresso.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Change the file permissions
`sudo chmod 644 /etc/systemd/system/pi_espresso.service`

Configure the system services, and set it to enabled.
`sudo systemctl daemon-reload`
`sudo systemctl enable pi_espresso.service`
