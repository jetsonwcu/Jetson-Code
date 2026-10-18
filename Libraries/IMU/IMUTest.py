import IMULibrary
import time

imu = IMULibrary.IMU()
imu.EnableSensors(True, [IMU.Sensor.ACCELEROMETER, IMU.Sensor.GYROSCOPE, IMU.Sensor.MAGNETOMETER])

while 1:
    print("Acceleration: ", imu.GetSensorData(IMU.Sensor.ACCELEROMETER))
    print("Gyroscope: ", imu.GetSensorData(IMU.Sensor.GYROSCOPE))
    print("Magnetometer: ", imu.GetSensorData(IMU.Sensor.MAGNETOMETER))
    sleep(1)