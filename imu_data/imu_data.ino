#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

const long BAUD_RATE = 115200;
Adafruit_BNO055 bno = Adafruit_BNO055(55);
/*******************************************************************************************************
 *  To set correctly                                                                                   *
 *******************************************************************************************************/
const int threshold = 1;

float prev_x;
float prev_y;
float prev_z;
float current_x;
float current_y;
float current_z;
int counter;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD_RATE);

  // Exit from the script if the sensor is not connected
  if (!bno.begin()){
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    exit(2);  //Exit with an error to make sure the script exits in case the IMU is not connected
   }
  // Initialize variables
  counter = 0;
  prev_x = 0;
  prev_y = 0;
  prev_z = 0;
}

void loop() {
  // Take sensor data
  sensors_event_t orientationData , angVelocityData , linearAccelData, magnetometerData, accelerometerData, gravityData;
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  // Update previous measurements
  prev_x = current_x;
  prev_y = current_y;
  prev_z = current_z;

  //If this is the first loop, save the current measurements
  if (counter == 0){
    counter ++;
    current_x = orientationData.orientation.x;
    current_y = orientationData.orientation.y;
    current_z = orientationData.orientation.z;
  }else{
      //If the difference in position with the previous 
      if (abs(orientationData.orientation.x - prev_x) > threshold){
          current_x = orientationData.orientation.x;
          Serial.print("\n Euler x= ");
          Serial.print(current_x);
      }else{
        current_x = prev_x;
      }

      if (abs(orientationData.orientation.y - prev_y) > threshold){
          current_y = orientationData.orientation.y;
          Serial.print("\n Euler y= ");
          Serial.print(current_y);
      }else{
        current_y = prev_y;
      }

      if (abs(orientationData.orientation.z - prev_z) > threshold){
          current_z = orientationData.orientation.z;
          Serial.print("\n Euler z= ");
          Serial.print(current_z);
      }else{
        current_z = prev_z;
      }
      
  }  
}
