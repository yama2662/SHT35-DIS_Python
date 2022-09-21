import time
import smbus
import datetime

def temperatureConversion(msb, lsb):
    tmp = ((msb << 8) | lsb)
    return -45 + 175 * (int(str(tmp), 10) / (pow(2, 16) - 1))


def humidityConversion(msb, lsb):
    tmp = ((msb << 8) | lsb)
    return -45 + 175 * (int(str(tmp), 10) / (pow(2, 16) - 1))

def averageDisplay(temperature, humidity):
    print(str(datetime.datetime.now()))
    print( str('{:.4g}'.format(sum(temperature)/len(temperature))) + "C" )
    print( str('{:.4g}'.format(sum(humidity)/len(humidity))) + "%" )
    print('------------------------------')


i2c = smbus.SMBus(1)
i2cAddress = 0x45

i2c.write_byte_data(i2cAddress, 0x20, 0x32)

time.sleep(1)

temperature = []
humidity = []

old_time = datetime.datetime.now()
now_time = old_time

while True:
    i2c.write_byte_data(i2cAddress, 0xE0, 0x00)
    data = i2c.read_i2c_block_data(i2cAddress, 0x00, 6)
    now_time = datetime.datetime.now()

    if now_time.minute != old_time.minute:
        averageDisplay(temperature, humidity)

        old_time = now_time
        temperature = []
        humidity = []

    else:
        temperature.append(temperatureConversion(data[0], data[1]))
        humidity.append(humidityConversion(data[3], data[4]))

    time.sleep(2)
