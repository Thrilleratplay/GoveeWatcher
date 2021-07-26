# Govee Watcher

This is deprecated.  

The work done here was continued as a [Home Assistant Component](https://github.com/Home-Is-Where-You-Hang-Your-Hack/sensor.goveetemp_bt_hci) and [ble_monitor](https://github.com/custom-components/ble_monitor)

#### Multiple Govee device Thermometer Hygrometer
* [Python debugger](./debugger) - Display values from GoveeAdvertisement parser
 found in [Home Assistant Component](https://github.com/Home-Is-Where-You-Hang-Your-Hack/sensor.goveetemp_bt_hci), works with multiple Govee devices.


#### Orinignal proof of concept Bluetooth broadcast decoder from Govee H5075 Thermometer Hygrometer Versions:
* [NodeJS](./odeJS)
* [Python 3](./python)


## How does it work
The Govee H5075 Thermometer Hygrometer broadcasts the current temperature and humidity through Bluetooth low energy (BLE) advertisement data.

### Packets

From the socket data provided by [python-bleason](https://github.com/TheCellule/python-bleson) debug logging and [advlib's decoding information](https://github.com/reelyactive/advlib)

#### Base
| Octets | Value if static | Description |
| :--- | :--- | :--- |
| 1-3 |  | Header?
| 4 - 9 |  `ZZ YY XX 38 c1 a4` | [MAC Address in reverse order.  Example a4:c1:38:XX:YY:ZZ](https://github.com/reelyactive/advlib#address)
| 10 | `1f` | ?
| 11 | `0d`| [Length of local name](https://github.com/reelyactive/advlib#local-name)
| 12| `09` | [Complete Local Name](https://github.com/reelyactive/advlib#local-name)
| 13 - 20 | `47 56 48 35 30 37 35 5f` | First part of device name "GVH5075_"
| 21 - 24 |  | Last four hex values (last two octets) of the MAC address spell out in ASCII.

#### Example of temperature/humidity advertisement
| Octets | Value if static | Description |
| :--- | :--- | :--- |
| 25 | `03` | Length of payload |
| 26 | `03` | flag for "Complete List of 16-bit UUIDs"
| 27 -28 | `88 ec` | Manufacturer Key
| 29 -31 | `02 01 05` | GAP list of 32-bit UUIDs but it is empty(?)
| 32 | | Length of payload.  For this instance it is `09`
| 33 | `ff` | Manufacture data flag
| 34 -35 | `88 ec` | Manufacturer Key
| 36 | `00` | padding?
| 37 - 39 |  | Encoded temperature and humidity
| 40 |   | Battery remaining percentage
| 41 | `00` | padding ?

### Decoding Data
The three octets are concatenated together and parsed into an integer
Example:
`03 21 5d` -> `03215d` --parse integer--> `205149`

### For positive temperature values (above 0°C/32°F):
Once we have this integer, for the temperature in Celsius, divide by 10000
```
205149 / 10000 = 20.5149°C
```

Humidity is modulus 1000 divided by 10
```
205149 % 1000 = 149
149 / 10 = 14.9% humidity
```

### For negative temperature values (below 0°C/32°F):
See [issue #2](https://github.com/Thrilleratplay/GoveeWatcher/issues/2)


### Received Signal Strength Indicator (RSSI)
There is a second advertisement signal contains the ManufacturerData Key `0x004c` and payload data `INTELLI_ROCKS`, (Govee is the brand name, the manufacture is "Shenzhen Intellirocks Tech. Co., Ltd.").  Based on the finding in [neilsheps/GoveeTemperatureAndHumidity](https://github.com/neilsheps/GoveeTemperatureAndHumidity), this relevant to the Apple iOS application.  This however provides the RSSI for the device.

### Historical data?
This is only a proof of concept for decoding BLE advertisements and do not plan on continuing on to load historical data.  Thes are done through commands sent to GATT services.


### Additional data
 * [Datasheet for Telink
BLE SoC TLSR8253F512](DS_TLSR8253-E_Datasheet for Telink BLE SoC TLSR8253.pdf)
 * [FCC.io public device data](https://fccid.io/2AQA6-H5075)
