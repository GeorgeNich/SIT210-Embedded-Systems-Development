#!/usr/bin/env python3
"""Read and classify illuminance from a BH1750-compatible I2C sensor."""

import time
from pathlib import Path
import sys

from smbus2 import SMBus

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from projects.common.logic import classify_lux  # noqa: E402

DEVICE_ADDRESS = 0x23
ONE_TIME_LOW_RES_MODE = 0x23
I2C_BUS_NUMBER = 1


def read_lux(bus: SMBus, address: int = DEVICE_ADDRESS) -> float:
    data = bus.read_i2c_block_data(address, ONE_TIME_LOW_RES_MODE, 2)
    raw_value = data[1] + (256 * data[0])
    return raw_value / 1.2


def main() -> None:
    with SMBus(I2C_BUS_NUMBER) as bus:
        while True:
            lux = read_lux(bus)
            print(f"{lux:.1f} lux - {classify_lux(lux)}")
            time.sleep(0.25)


if __name__ == "__main__":
    main()
