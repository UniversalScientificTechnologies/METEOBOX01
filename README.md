# METEOBOX01
Meteobox is a universal platform for logging data from various sensors, aiming primarily on sensors of meteorological variables. This platform was designed for purpose of comparing multiple sensors to each other or with other measuring systems. The device is not traying to be another meteorological station. 
This is primarily due to the features where multiple identical sensors can be connected to the device or  easy implementation of new sensors. 

The platform primarily requires a power source for working. Data transmission can be secured by internal LTE modem, ethernet connection or by wifi connection. Device supports remote monitoring.

## Abilities
The system records data from sensors connected via various interfaces. The data is immediately logged into the internal time-siries database. A CSV file is exported every hour, which serves as a backup and is automatically uploaded to a remote server. The system is equipped with a grafana dashboard for visualization of live data. 

![obrazek](https://user-images.githubusercontent.com/5196729/209866529-c32992f9-cd39-4d09-b133-cb17d4c95a39.png)


## Examples of use

### Comparison of particulate matter sensors

Our cooperating company [ThunderFly](www.thunderfly.cz) is developing a system TF-ATMON for measuring atmospheric quantities in 3D space (in atmosphere) using unmanned drones (UAVs). Specifically, they are using [TF-G2](https://github.com/ThunderFly-aerospace/TF-G2/) autogyro. This system was used with sensors of airborne particles from sensirion when measuring [New Year's fireworks 2021/2022](). The result was that the concentration of small particles more than doubled throught the height profile. After a discussion with experts from the Czech Hydrometeorological Institute arrise that it would be interesting to compare and vertify these micro-sensors with professional meteo-station, which have a defined solution for air intake, air drying and other stuff. Based on this, we prepared the METOBOX with their sensors for ThunderFly. Their setup includ the following sensors:

 * 2x SHT3x: Temperature and humidity, mounted in [TFHT01](https://github.com/ThunderFly-aerospace/TFHT01) board. 
 * 2x Sensirion SPS30, concentrotions of PM particles
 * 2x Sensirion SEN54, concentrations of PM particles, temperature, humidity, VOC

To connect a larger number of sensors with one address, we used an i2c address translator [TFI2CADT01](https://github.com/ThunderFly-aerospace/TFI2CADT01).
