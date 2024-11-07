from ensurepip import bootstrap
import sensors.BME280 as BME280   #Atmospheric Pressure/Temperature and humidity
import sensors.LTR390 as LTR390  #UV
import sensors.TSL2591 as TSL2591 #LIGHT
import sensors.SGP40 as SGP40
import smbus2
from dataclasses import dataclass, asdict
from kafka import KafkaProducer
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all log messages
    format='[%(asctime)s] %(levelname)s: %(message)s',
)
MPU_VAL_WIA = 0x71
MPU_ADD_WIA = 0x75
ICM_VAL_WIA = 0xEA
ICM_ADD_WIA = 0x00
ICM_SLAVE_ADDRESS = 0x68
bus = smbus2.SMBus(bus=1)
bme280 = BME280.BME280()
bme280.get_calib_param()
light = TSL2591.TSL2591()
uv = LTR390.LTR390()
sgp = SGP40.SGP40()

print("TSL2591 Light I2C address:0X29")
print("LTR390 UV I2C address:0X53")
print("SGP40 VOC I2C address:0X59")
print("bme280 T&H I2C address:0X76")

@dataclass
class DataOutput():
    msg_time: str
    pressure: int
    temp: int
    hum: int
    lux:float
    uvs:int

producer = KafkaProducer(bootstrap_servers="10.100.102.54:9092", request_timeout_ms = 10000)
try:
    while True:
        bme: list = bme280.readData()

        # setup all values from sensors
        pressure = round(number=bme[0], ndigits=2) 
        temp = round(number=bme[1], ndigits=2) 
        hum = round(number=bme[2], ndigits=2)
        lux = round(number=light.Lux(), ndigits=2)
        uvs = uv.UVS()

        sensor_data = DataOutput(
            msg_time= str(datetime.now()),
            pressure=pressure,
            temp= temp,
            hum= hum,
            lux=lux,
            uvs=uvs
        )

        future = producer.send(topic="sensor-input", value=json.dumps(asdict(obj=sensor_data)).encode('utf-8'))
        # producer.send(topic="sensors", value=json.dumps("testtest").encode('utf-8'))
        # result = future.get(timeout=10)  # Wait for confirmation
        print("Message sent:", sensor_data)
        # producer.send('sensors', value=b'Hello from Python producer')
        # producer.flush()
except KeyboardInterrupt:
    exit()
