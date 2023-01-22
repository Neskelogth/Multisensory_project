#include "customImu.h"

const long BAUD_RATE = 115200;
const int n = 10;
customImu f(n);

void setup() {
  
  // put your setup code here, to run once:
  Serial.begin(BAUD_RATE);

  // Exit from the script if the sensor is not connected
  if (!f.begin()){
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    exit(2);  //Exit with an error to make sure the script exits in case the IMU is not connected
  }
}

void loop() {

   f.update();
}
