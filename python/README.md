# Govee Watcher (Python)
Proof of concept bluetooth broadcast decoder from Govee H5075 Thermometer Hygrometer using [Bleson](https://github.com/TheCellule/python-bleson).


*NOTE*: Only tested on Linux

## Requirements
  * Python 3
  * sudo privileges


## Install
Clone or download this repo.
```shell
  sudo pip3 install bleson
```

## Usage
In a terminal:
```shell
  sudo python goveeWatcher.py
```
It will collect information for 3 seconds and print the values for each device in the format:

```
GVH5075_XXXX (A4:C1:38:XX:XX:XX) - 20.52C / 68.93F  - Humidity: 15.00%
GVH5075_XXXX (A4:C1:38:XX:XX:XX) - RSSI: -62
```
