# Govee Watcher (Node.js)
Proof of concept bluetooth broadcast decoder from Govee H5075 Thermometer Hygrometer using [Bluez](http://www.bluez.org/) on Linux

## Requirements
  * Bluetooth permissions for user
  * Bluez installed on Linux
  * Node.js (tested with v12)


## Install
*NOTE*: Linux only

Clone or download this repo.
```shell
  npm install
```

## Usage
In a terminal:
```shell
  node index.js
```
*NOTE*: It may take a few seconds before devices are discovered.

## How does it work?
This essentially opens a bash terminal, runs `bluetoothctl scan on` and parses the data when there is an update from a BLE advertisement.

When the data contains the "ManufacturerData Key" `0xec88`, the associated "ManufacturerData Value" contains temperature and humidity data in hex.  [Decoding is decribed here](../README.md).
