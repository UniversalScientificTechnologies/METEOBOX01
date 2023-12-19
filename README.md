# METEOBOX01 - atmospheric sensors testing platform
Meteobox is a universal platform for logging data from various meteorological or atmospheric sensors, aiming primarily at sensors of atmospheric variables like temperature, humidity, aerosols, etc. This platform was designed to compare multiple sensor types to each other or with other measuring systems. The device is not trying to be another generic meteorological station.
This is primarily due to the features where multiple identical sensors can be connected to the device or easy implementation of new [DUT](https://en.wikipedia.org/wiki/Device_under_test) sensors.

<p align="center">
<img src="/doc/img/METEOBOX01.jpg" width="45%"/>
</p>

The platform primarily requires a power source for working. Data transmission can be provided by an internal LTE modem, ethernet connection, or by wifi connection. The device supports remote monitoring.

## Abilities
The system records data from sensors connected via various interfaces. The data is immediately logged into the internal time series database. A CSV file is exported every hour, which serves as a backup and is automatically uploaded to a remote server. The system is equipped with a [grafana](https://grafana.com/) dashboard for visualization of live data.

<p align="center">
<img src="/doc/img/grafana_dashboard1.png" width="45%"/> <img src="/doc/img/grafana_dashboard2.png" width="45%"/> 
</p>

## Examples of use

### Comparison of particulate matter sensors

Our cooperating company [ThunderFly](https://www.thunderfly.cz) is developing a system [TF-ATMON](https://www.thunderfly.cz/tf-atmon.html) for measuring atmospheric quantities in 3D space (in the atmosphere) using unmanned drones (UAVs). Specifically, they are using [TF-G2](https://github.com/ThunderFly-aerospace/TF-G2/) autogyro. This system was used with sensors of airborne particles from Sensirion when measuring [New Year's fireworks 2021/2022](https://www.thunderfly.cz/tf-atmon/ThunderFly_PressRelease_MereniZnecisteniAtmosferyZpusobeneNovorocnimiOhnostroji.pdf). The result was that the concentration of small particles more than doubled through the height of atmospheric profile column. After a discussion with experts from the [Czech Hydrometeorological Institute](https://www.chmi.cz/) arise a requirement to compare and verify these micro-sensors with professional meteo-station reference, which are mainly different in a defined pre-processing of air intake e.g. air drying and some other treatment before entering the sensor itself. Based on this, we prepared the METOBOX with multiple sensors for ThunderFly s.r.o. The setup includes the following sensors:

 * 2x SHT3x: Temperature and humidity, mounted in [TFHT01](https://github.com/ThunderFly-aerospace/TFHT01) board.
 * 2x [Sensirion SPS30](https://sensirion.com/products/catalog/SPS30/), concentrotions of PM particles
 * 2x [Sensirion SEN54](https://sensirion.com/products/catalog/SEN54/), concentrations of PM particles, temperature, humidity, and [VOC](https://en.wikipedia.org/wiki/Volatile_organic_compound)

To connect a larger number of sensors with one address, we used an i2c address translator [TFI2CADT01](https://github.com/ThunderFly-aerospace/TFI2CADT01).

## Technical details

The device uses MLAB components to connect to the sensors. Specifically, the [USBI2C01](https://github.com/mlab-modules/USBI2C01) module creates an I²C interface from USB. Then [pymlab framework](https://github.com/MLAB-project/pymlab/tree/dev/examples/mongolog) is used to read the sensor data and log it to mongo based database.
