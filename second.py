import time
import smbus
import datetime

def temperatureConversion(msb, lsb):
    tmp = ((msb << 8) | lsb)
    return -45 + 175 * (int(str(tmp), 10) / (pow(2, 16) - 1))


def humidityConversion(msb, lsb):
    tmp = ((msb << 8) | lsb)
    return -45 + 175 * (int(str(tmp), 10) / (pow(2, 16) - 1))


i2c = smbus.SMBus(1)
i2cAddress = 0x45

i2c.write_byte_data(i2cAddress, 0x21, 0x30)

time.sleep(1)

while True:
    i2c.write_byte_data(i2cAddress, 0xE0, 0x00)
    data = i2c.read_i2c_block_data(i2cAddress, 0x00, 6)

    print(str(datetime.datetime.now()))
    print(str('{:.5g}'.format(temperatureConversion(data[0], data[1]))) + "C")
    print(str('{:.5g}'.format(humidityConversion(data[3],data[4]))) + "%")
    print('------------------------------')
    time.sleep(1)

