#!/usr/bin/env python3

from time import sleep
from bleson import get_provider, Observer, UUID16
from bleson.logger import log, set_level, ERROR, DEBUG

# Disable warnings
set_level(ERROR)

# # Uncomment for debug log level
set_level(DEBUG)

# https://macaddresschanger.com/bluetooth-mac-lookup/A4%3AC1%3A38
# OUI Prefix	Company
# A4:C1:38	Telink Semiconductor (Taipei) Co. Ltd.
GOVEE_BT_MAC_OUI_PREFIX = "A4:C1:38"

H5075_UPDATE_UUID16 = UUID16(0xec88)

govee_devices = {}

# ###########################################################################
FORMAT_PRECISION = ".2f"


# Decode H5075 Temperature into degrees Celcius
def decode_temp_in_c(encoded_data):
    return format((encoded_data/10000), FORMAT_PRECISION)


# Decode H5075 Temperature into degrees Fahrenheit
def decode_temp_in_f(encoded_data):
    return format((((encoded_data/10000) * 1.8) + 32), FORMAT_PRECISION)


# Decode H5075 percent humidity
def decode_humidity(encoded_data):
    return format(((encoded_data % 1000) / 10), FORMAT_PRECISION)


# On BLE advertisement callback
def on_advertisement(advertisement):
    log.debug(advertisement)

    if advertisement.address.address.startswith(GOVEE_BT_MAC_OUI_PREFIX):
        mac = advertisement.address.address

        if mac not in govee_devices:
            govee_devices[mac] = {}
        if H5075_UPDATE_UUID16 in advertisement.uuid16s:
            # TODO:  there must be a proper way to discode
            name = advertisement.name.split("'")[1]
            encoded_data = int(advertisement.mfg_data.hex()[6:12], 16)

            govee_devices[mac]["address"] = mac
            govee_devices[mac]["name"] = name
            govee_devices[mac]["mfg_data"] = advertisement.mfg_data
            govee_devices[mac]["data"] = encoded_data

            govee_devices[mac]["tempInC"] = decode_temp_in_c(encoded_data)
            govee_devices[mac]["tempInF"] = decode_temp_in_f(encoded_data)
            govee_devices[mac]["humidity"] = decode_humidity(encoded_data)

        if advertisement.rssi is not None and advertisement.rssi != 0:
            govee_devices[mac]["rssi"] = advertisement.rssi

        log.debug(govee_devices[mac])

# ###########################################################################


adapter = get_provider().get_adapter()

observer = Observer(adapter)
observer.on_advertising_data = on_advertisement


observer.start()
sleep(3)
observer.stop()


for govee_device in govee_devices.values():
    print(f"{govee_device['name']} ({govee_device['address']}) - {govee_device['tempInC']}C / {govee_device['tempInF']}F  - Humidity: {govee_device['humidity']}%")
    print(f"{govee_device['name']} ({govee_device['address']}) - RSSI: {govee_device['rssi']}")
