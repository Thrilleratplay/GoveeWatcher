# Govee Watcher
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

## usage
In a terminal:
```shell
  node index.js
```
It may take a few seconds before devices are discovered.


## TODO:
  * Explain the decoding
  * determine battery percentage
  * determine how/if negative temeratures are transmitted
  * better filtering of output
     * Use Bluetooth LE GATT instead of continuously scanning
  * proofread and correct embarrassing spelling
