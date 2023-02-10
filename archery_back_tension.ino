/*Shoulder correction pose for archery 2023 */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/* IMU ***************************************************************************************************/

/* Set the delay between fresh samples */
//Euler measure goes at 100Hz
static const unsigned long BNO055_PERIOD_MILLISECS = 1; // E.g. 4 milliseconds per sample for 250 Hz
#define BNO055_PERIOD_MICROSECS 100.0e3f // = 1000 * PERIOD_MILLISECS;
static uint32_t BNO055_last_read = 0;

/* Assign a unique ID to this sensor at the same time */

Adafruit_BNO055 bno_elbowL = Adafruit_BNO055(55);
Adafruit_BNO055 bno_shoulderL = Adafruit_BNO055(55);
Adafruit_BNO055 bno_shoulderR = Adafruit_BNO055(55);
Adafruit_BNO055 bno_elbowR = Adafruit_BNO055(55);
Adafruit_BNO055 bno_bow = Adafruit_BNO055(55);

//define vector to take angles from imu sensors
imu::Vector<3> euler0;
imu::Vector<3> euler1;
imu::Vector<3> euler2;
imu::Vector<3> euler3;
imu::Vector<3> euler4;


/**************************************************************************/


/*define instatition for the i2c multiplexer, no need of library*/
/*If the pins A0, A1 and A2 from the multiplexer board are left unconnected,
then we are using the 0x70 address.*/
#define TCAADDR 0X70

#define BAUD_RATE 9600

/**************************************************************************/
/* Choose bus */
/**************************************************************************/
/*function to toggle between the channels with i2c
the order is from 0 to 7 */
void tcaselect(uint8_t bus){
  
  if (bus > 7) return;
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << bus); //send byte to select bus
  Wire.endTransmission();
}


/**************************************************************************/
/* Init of imus */
/**************************************************************************/
void init_sensor(uint8_t i, Adafruit_BNO055 bno){
  
  /*multiplex selection*/
  tcaselect(i);

  //Serial.println("Sensor initializing..."); Serial.println("");
  
  /* Initialize the sensor */
  if(!bno.begin()){
    /* There was a problem detecting the BNO055 ... check your connections */
    /*Serial.print(F("BNO055 "));
    Serial.print(names[i]); 
    Serial.println(F(" NOT detected"));*/
    while(1);
  }
  
  delay(1000);
}


void setup() {
  
  Serial.begin(BAUD_RATE);
  while(!Serial);
  Wire.begin();

  /* Setup of the digital sensors */
  /*create a function to call for each sensor*/
  init_sensor(0, bno_elbowL);
  delay(10);
  init_sensor(1, bno_shoulderL);
  delay(10);
  init_sensor(2, bno_shoulderR);
  delay(10);
  init_sensor(3, bno_elbowR);
  delay(10);
  init_sensor(4, bno_bow);
  delay(10);

}

void loop() {
  
  /*for each imu print in sequence datas*/
  //EULER is in degrees

  for (int bus = 0; bus < 5; bus++) {

    tcaselect(bus);

    switch (bus) {
    case 0:
      euler0 = bno_elbowL.getVector(Adafruit_BNO055::VECTOR_EULER);
      Serial.print("Imu: elbowL = ");
      Serial.print(euler0.y()*1000);
      break;
      
    case 1:
      euler1 = bno_shoulderL.getVector(Adafruit_BNO055::VECTOR_EULER);
      Serial.print(" shoulderL = ");
      Serial.print(euler1.y()*1000);
      break;
      
    case 2:
    
      euler2 = bno_shoulderR.getVector(Adafruit_BNO055::VECTOR_EULER);
      Serial.print(" shoulderR = ");
      Serial.print(euler2.y()*1000);
      break;
      
    case 3:
      
      euler3 = bno_elbowR.getVector(Adafruit_BNO055::VECTOR_EULER);
      Serial.print(" elbowR = ");
      Serial.println(euler3.y()*1000);
      break;

    case 4:
      
      euler4 = bno_bow.getVector(Adafruit_BNO055::VECTOR_EULER);
      Serial.print("Bow: x = ");
      Serial.print(euler4.x()*1000);
      Serial.print(" y = ");
      Serial.print(euler4.y()*1000);
      Serial.print(" z = ");
      Serial.println(euler4.z()*1000);
      
      break;
      
    }
    //delay(1);  // delay in between reads for stability
   }

}
