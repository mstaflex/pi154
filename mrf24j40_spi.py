#    This file contains routines to access the registers of the mrf24j40 in a flexible way.
#    It uses the Python SPI extension written by Louis Thiery (sources: https://github.com/lthiery/SPI-Py)

#    Copyright (C) 2013  Jasper Buesch

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Jasper Buesch; jasper.buesch@gmail.com


from mrf24j40_registers import register_fields, short_addr_registers, long_addr_registers
import spi


class Mrf24j40Spi(object):

    def __init__(self):
        self.short_write_mask = 0x01
        self.long_write_mask = 0x10
        self.long_addr_bit = 0x80

    def openSPI(self):
        status = spi.openSPI()

    def closeSPI(self):
        status = spi.closeSPI()

    def _write_register(self, reg, value):
        """Writes the entire register, identified by its name  (datasheet)."""
        if reg in short_addr_registers:
            reg_addr = short_addr_registers[reg]
            bytes = [((reg_addr << 1) + self.short_write_mask), value]
        else:
            if reg in long_addr_registers:
                reg_addr = long_addr_registers[reg]
            else:
                reg_addr = reg
            bytes = []
            bytes.append((reg_addr >> 3) + self.long_addr_bit)
            bytes.append(((reg_addr << 5) & 0xE0) + self.long_write_mask)
            bytes.append(value)
        spi.transfer(tuple(bytes))

    def _read_register(self, reg):
        """Reads the entire register, identified by its name (datasheet)."""
        if reg in short_addr_registers:
            reg_addr = short_addr_registers[reg]
            bytes = [(reg_addr << 1), 0]
            result = spi.transfer(tuple(bytes))
            return result[1]
        else:
            if reg in long_addr_registers:
                reg_addr = long_addr_registers[reg]
            else:
                reg_addr = reg
            bytes = []
            bytes.append((reg_addr >> 3) + self.long_addr_bit)
            bytes.append((reg_addr << 5) & 0xE0)
            bytes.append(0)
            result = spi.transfer(tuple(bytes))
            return result[2]

    def _write_register_field(self, name, value):
        """Writes sub-register field, identified by its name (datasheet).
        These fields are defined in 'mrf24j40_registers' and can comprise of single bits, or
        several bits across multiple registers. For their names consult the datasheet."""
        reg_field_descr = register_fields[name]
        for dic in reg_field_descr:
            register = dic['register']
            shift = dic['shift']
            bits = dic['bits']
            reg_data = self._read_register(register)
            mask = sum([1 << i for i in range(0, bits)]) << shift
            reg_data = (255 - mask) & reg_data  # zero the masked range
            reg_data |= (value << shift) & mask
            self._write_register(register, reg_data)
            value = (value >> bits)  # shift the bits for this field away

    def _read_register_field(self, name):
        """Reads sub-register field, identified by its name (datasheet).
        These fields are defined in 'mrf24j40_registers' and can comprise of single bits, or
        several bits across multiple registers. For their names consult the datasheet."""
        reg_field_descr = register_fields[name]
        return_value = 0
        return_shift = 0
        for dic in reg_field_descr:
            register = dic['register']
            shift = dic['shift']
            bits = dic['bits']
            reg_data = self._read_register(register)
            mask = sum([1 << i for i in range(0, bits)]) << shift
            reg_data = reg_data & mask
            reg_data = reg_data >> shift
            return_value += reg_data << return_shift
            return_shift += bits
        return return_value

    def write(self, name, value):
        """Convenient function to write either to registers of sub-register fields."""
        if name in register_fields.keys():
            self._write_register_field(name, value)
        else:
            self._write_register(name, value)

    def read(self, name):
        """Convenient function to read either to registers of sub-register fields."""
        if name in register_fields.keys():
            return self._read_register_field(name)
        else:
            return self._read_register(name)


if __name__ == '__main__':
    """The driver is usually used by other program parts.
    The following lines are for debug purposes only."""
    driver = Mrf24j40Spi()
    driver.openSPI()

    print driver.write("SADR", 0x5511)
    print bin(driver.read("SADR"))
    print bin(driver.read("SADRH"))
    print bin(driver.read("SADRL"))
    print bin(driver.read(0x300))
