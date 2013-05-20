<<<<<<< HEAD
RaspPI going IEEE802.15.4
=========================

COPYRIGHT (C) 2013 Jasper Buesch. All rights reserved.

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License V2 as published by the Free Software Foundation.

LIABILITY
This program is distributed for educational purposes only and is no way suitable for any particular application, especially commercial. There is no implied suitability so use at your own risk!


Description
-----------
This project is about controlling a Mrf24j40MA module (802.15.4 radio) that is connected to the SPI hardware interface of a Raspberry PI.
So far it only contains the Mrf24j40 register definitions and methods to read and write most flexibly to them.
Either the register names can be used, or the direct field names within registers (consult the datasheet).
It is also possible to access register fields that reach across multiple registers (more than 8 bits).

The mrf24j40_spi requires an SPI Python extension. The original sources can be found at https://github.com/lthiery/SPI-Py.
=======
This project is about controlling an Mrf24j40MA module that is connected to the SPI hardware interface of a Raspberry PI.
So far it only contains the Mrf24j40 register definitions and methods to read and write most flexible to them.
Either the register names can be used, or the field names within registers (consult the datasheet).
It is also possible to access register field that reach across multiple registers (more than 8 bits).
>>>>>>> Added method to readout rxfifo

My cleaned fork https://github.com/mstaflex/SPI-Py.
