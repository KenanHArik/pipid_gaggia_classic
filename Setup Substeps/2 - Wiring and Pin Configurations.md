# Setting up Wiring and Pins Locations

The following guide goes over wiring of the hardware to the Raspberry Pi.

## Pinout Diagram

Notice there is a distinction between physical pins and BCM number.
![pinout](assets/2021-09-18-22-22-25.png)

## Display

The display is designed to occupy the top 6 pins of the header to operate over I2C communication. This is shown in the image below. No pin assignments are changed from this design. However, since the display is made remote of the Pi, pin 1 (3.3V) and pin 4 5V DC are not connected as they are not needed for the display.

![display](assets/2021-09-18-21-58-20.png)

## RTD Temperature Sensor

The RTD temperature sensor operates over SPI. The following pin assignments are used to interact with the MAX31865 RTD amplifier

- Pi 3.3V (physical pin 17) to sensor VIN
- Pi SPI_MOSI (physical pin 19, BCM 10) to sensor SD1
- Pi SPI_MISO (physical pin 21, BCM 9) to sensor SD0
- Pi SPI_SCLK (physical pin 23, BCM 11) to sensor CLK
- Pi SPI_CE0 (physical pin 24, BCM 8) to sensor CS
- Pi GND (physical pin 20) to sensor GND

## Button for Sleep / Wake

- Sleep / Wake Switch GPIO to GND (25) and sense physical pin 26, BCM 7

## Switch for Brew / Steam Toggle

- Brew / Steam Toggle switch GPIO to GND (39) and sense physical pin 40, BCM 21

## SSR

- Heater SSR Switch GPIO to GND (34) and PWM physical pin 33, BCM 13