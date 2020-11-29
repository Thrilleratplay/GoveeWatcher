#!/usr/bin/env python3
"""Debugging information of Govee Advirtiment."""

from time import sleep
import os
import sys

from govee_advertisement import GoveeAdvertisement

from bleson.core.hci.constants import EVT_LE_ADVERTISING_REPORT  # type: ignore
from bleson.core.hci.type_converters import hex_string  # type: ignore
from bleson import get_provider, logger  # type: ignore

# Disable warnings
logger.set_level(logger.ERROR)

# Uncomment for debug log level
# logger.set_level(logger.DEBUG)

FORMAT_PRECISION = ".2f"


# ###########################################################################


def print_unknown_packet(ga) -> None:
    """Print unknown packet data."""
    msg = "Unknown packet type:"  # Govee model
    msg += "\n\tMAC:        {}"
    msg += "\n\tName:       {}"
    msg += "\n\tRSSI:       {}"
    msg += "\n\tRaw Data:   {}"
    msg += "\n"

    print(
        msg.format(
            ga.mac,
            ga.name,
            ga.rssi,
            hex_string(ga.raw_data),
        )
    )


def print_govee_data(ga) -> None:
    """Print Govee Advirtiment data."""
    msg = "{}"  # Govee model
    msg += "\n\tMAC:        {}"
    msg += "\n\tName:       {}"
    msg += "\n\tTemperature {}C / {}F"
    msg += "\n\tHumidity:   {}%"
    msg += "\n\tBattery:    {}%"
    msg += "\n\tRSSI:       {}"
    msg += "\n\tGAP_FLAGS:  {}"
    msg += "\n\tMFG_data:   {}"
    msg += "\n\tGovee data: {}"
    msg += "\n\tRaw Data:   {}"
    msg += "\n"

    print(
        msg.format(
            ga.model,
            ga.mac,
            ga.name,
            format(ga.temperature, FORMAT_PRECISION),
            format(((ga.temperature * 1.8) + 32), FORMAT_PRECISION),
            ga.humidity,
            ga.battery,
            ga.rssi,
            ga.flags,
            hex_string(ga.mfg_data),
            ga.packet,
            hex_string(ga.raw_data),
        ),
    )


def handle_meta_event(hci_packet) -> None:
    """Handle recieved BLE data."""
    # If recieved BLE packet is of type ADVERTISING_REPORT
    if hci_packet.subevent_code == EVT_LE_ADVERTISING_REPORT:
        ga = GoveeAdvertisement(hci_packet.data)

        # If mfg data information is defined
        if ga.packet is not None:
            print_govee_data(ga)
        else:
            print_unknown_packet(ga)


# ###########################################################################


adapter = get_provider().get_adapter()
adapter._handle_meta_event = handle_meta_event

try:
    while True:
        adapter.start_scanning()
        sleep(2)
        adapter.stop_scanning()
except KeyboardInterrupt:
    try:
        adapter.stop_scanning()
        sys.exit(0)
    except SystemExit:
        adapter.stop_scanning()
        os._exit(0)
