
from mrf24j40_spi import Mrf24j40Spi
import time

class Mrf24j40Radio(object):

    def __init__(self):
        self.spi = Mrf24j40Spi()
        self.spi.openSPI()

    def init_radio(self):
        # 0x07 - Perform a software Reset. Bit is auto-reset
        self.spi.write("SOFTRST", 0x07)
        # 0x98 - Initialize FIFOEN = 1 and TXONTS = 0x6.
        self.spi.write("PACON2", 0x98)
        # 0x95 - Initialize RFSTBL = 0x9.
        self.spi.write("TXSTBL", 0x95)
        # 0x03 - Initialize RFOPT = 0x03.
        self.spi.write("RFCON0", 0x03)
        # 0x01 - Initialize VCOOPT = 0x02.
        self.spi.write("RFCON1", 0x01)
        # 0x80 - Enable PLL (PLLEN = 1).
        self.spi.write("RFCON2", 0x80)
        # 0x90 - Initialize TXFIL = 1 and 20MRECVR = 1.
        self.spi.write("RFCON6", 0x90)
        # 0x80 - Initialize SLPCLKSEL = 0x2 (100 kHz Internal oscillator).
        self.spi.write("RFCON7", 0x80)
        # 0x10 - Initialize RFVCO = 1.
        self.spi.write("RFCON8", 0x10)
        # 0x21 - Initialize CLKOUTEN = 1 and SLPCLKDIV = 0x01.
        self.spi.write("SLPCON1", 0x21)

        self.spi.write("PANCOORD", 1)
        self.spi.write("COORD", 1)
        self.spi.write("PROMI", 1)
        self.spi.write("MACMINBE", 1)  # csma backoff exponent

        self.spi.write("BO", 15)
        self.spi.write("SO", 15)

        # 11. BBREG2 (0x3A) = 0x80 - Set CCA mode to ED.
        self.spi.write("BBREG2", 0x80)
        # 12. CCAEDTH = 0x60 - Set CCA ED threshold.
        self.spi.write("CCAEDTH", 0x60)
        # 13. BBREG6 (0x3E) = 0x40 - Set appended RSSI value to RXFIFO.
        self.spi.write("BBREG6", 0x40)

        self.spi.write("RXIE", 0)
        self.spi.write("TXNIE", 0)
        # rising edge indicated interrupt signal to pic
        self.spi.write("SLPCON0", 0x02)
        # rising edge indicated interrupt signal to pic
        self.spi.write("CHANNEL", 0)

        self.spi.write("RFCON3", 0x00)
        # 0x04 - Reset RF state machine.
        self.spi.write("RFCTL", 0x04)
        self.spi.write("RFCTL", 0x00)

    def check_int_reg(self):
        int_reg = self.spi.read("INTSTAT")
        return int_reg

    def readout_rxfifo(self):
        self.spi.write("RXDECINV", 1)
        num = self.spi.read(0x300)
        read_bytes = []
        for i in range(0, num + 2):
            read_bytes.append(self.spi.read(0x300 + i))
        self.spi.write("RXDECINV", 0)
        return read_bytes


if __name__ == '__main__':
    radio = Mrf24j40Radio()
    radio.init_radio()
    while True:
        if radio.check_int_reg():
            print radio.readout_rxfifo()
        time.sleep(0.1)











