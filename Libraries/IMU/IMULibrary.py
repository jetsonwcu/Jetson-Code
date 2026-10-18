import sys
import busio
import board
from enum import Enum

import adafruit_bno08x

class IMU:
    i2c = None
    imu = None
    
    #The type of sensor being accessed.
    class Sensor(Enum):
        ACCELEROMETER = adafruit_bno08x.BNO_REPORT_ACCELEROMETER
        GYROSCOPE = adafruit_bno08x.BNO_REPORT_GYROSCOPE
        MAGNETOMETER = adafruit_bno08x.BNO_REPORT_MAGNETOMETER
        LINEAR_ACCELERATION = adafruit_bno08x.BNO_REPORT_LINEAR_ACCELERATION
        ROTATION_VECTOR = adafruit_bno08x.BNO_REPORT_ROTATION_VECTOR
        GRAVITY = adafruit_bno08x.BNO_REPORT_GRAVITY
        
        GAME_ROTATION_VECTOR = adafruit_bno08x.BNO_REPORT_GAME_ROTATION_VECTOR
        GEOMAGNETIC_ROTATION_VECTOR = adafruit_bno08x.BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR
        STEP_COUNTER = adafruit_bno08x.BNO_REPORT_STEP_COUNTER
        RAW_ACCELEROMETER = adafruit_bno08x.BNO_REPORT_RAW_ACCELEROMETER
        RAW_GYROSCOPE = adafruit_bno08x.BNO_REPORT_RAW_GYROSCOPE
        RAW_MAGNETOMETER = adafruit_bno08x.BNO_REPORT_RAW_MAGNETOMETER
        SHAKE_DETECTOR = adafruit_bno08x.BNO_REPORT_SHAKE_DETECTOR
        STABILITY_CLASSIFIER = adafruit_bno08x.BNO_REPORT_STABILITY_CLASSIFIER
        ACTIVITY_CLASSIFIER = adafruit_bno08x.BNO_REPORT_ACTIVITY_CLASSIFIER
        GYRO_INTEGRATED_ROTATION_VECTOR = adafruit_bno08x.BNO_REPORT_GYRO_INTEGRATED_ROTATION_VECTOR
    
    
    #Internal
    def __init__(self):

        try:
            self.i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
        except BaseException as e:
            print(e)
            sys.exit("I2C bus failed to initialize.")
            
        try:
            self.imu = BNO08X_I2C(i2c)
        except BaseException as e:
            print(e)
            sys.exit("IMU failed to initialize.")
        
        #Library already does initialize and reset.
        #self.Calibrate() TODO How is device supposed to be oriented when calibrating?


    #Meta
    
    #Hard and soft resets the IMU until it is online.
    def Initialize(self):
        self.imu.initialize()

    #Resets the IMU through hardware.
    def ResetHard(self):
        self.imu.hard_reset()
    
    #Resets the IMU using software commands.
    def ResetSoft(self):
        self.imu.soft_reset()

    #Calibrates the IMU.
    def Calibrate(self):
        self.imu.begin_calibration()
        #TODO What is the correct return value?
        while self.imu.calibration_status != 0:
            pass

    #Saves the calibration data to on chip memory.
    def SaveCalibration(self):
        self.imu.save_calibration_data()
        
    #Enables or disables a given Sensor enum on the IMU.
    def EnableSensor(self, state: bool, feature: Sensor):
        if state == true:
            self.imu.enable_feature(feature)
        else:
            self.imu.disable_feature(feature)
            
    #Enables or disables a list of sensors.
    def EnableSensors(self, state: bool, features: [Sensor]):
        for feature in features:
            EnableSensor(state, feature)


    #Sensor Data
    
    #TODO Use single function instead.
    def GetSensorData(self, sensor: Sensor):
        
        match sensor:
            case Sensor.ACCELEROMETER:
                return self.imu.acceleration #Optional[float, float, float] (X,Y,Z) (meters/second^2)
            case Sensor.GYROSCOPE:
                return self.imu.gyro #Optional[float, float, float] (X,Y,Z) (Radians/second)
            case Sensor.MAGNETOMETER:
                return self.imu.magnetic #Optional[float, float, float] (X,Y,Z)
            case Sensor.LINEAR_ACCELERATION:
                return self.imu.linear_acceleration #Optional[float, float, float]
            #TODO The rest of the sensor data.
            case _:
                print("Sensor not found.")
                return None
