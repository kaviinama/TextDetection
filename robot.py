import easygopigo3 as easy
import sys
from gopigo3 import FirmwareVersionError

#############################################
# Here are functions related to GoPiGo. # 
#############################################

#try to connect to the GoPiGo3
try:
    gopigo=easy.EasyGoPiGo3()
    gopigo.reset_all()
except IOError:
    print("GoPiGo3 robot not detected")
    sys.exit(1)
    
#try to connect to the distance sensor
try:
    distance_sensor = gopigo.init_distance_sensor()
except IOError:
    print("DistanceSensor couldn't be found")
    sys.exit(1)
except FirmwareVersionError:
    print("GoPiGo3 board needs to be updated")
    sys.exit(1)
except Exception:
    print("Unknown error occurred while instantiating GoPiGo3")
    sys.exit(1)  



#reads distance sensor and returns distance in cm 
def read_distance_sensor():
    distance_cm=distance_sensor.read()
    return  distance_cm




        
 