This project is about controlling a Mrf24j40MA module that is connected to the SPI hardware interface of a Raspberry PI.
So far it only contains the Mrf24j40 register definitions and methods to read and write most flexibly to them.
Either the register names can be used, or the direct field names within registers (consult the datasheet).
It is also possible to access register fields that reach across multiple registers (more than 8 bits).

