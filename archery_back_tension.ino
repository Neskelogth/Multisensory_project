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
}


void setup() {
  
  Serial.begin(BAUD_RATE);
  while(!Serial);
  Wire.begin();

  /* Setup of the digital sensors */
  /*create a function to call for each sensor*/
  init_sensor(0, bno_elbowL);
  delay(5);
  init_sensor(1, bno_shoulderL);
  delay(5);
  init_sensor(2, bno_shoulderR);
  delay(5);
  init_sensor(3, bno_elbowR);
  delay(5);
  init_sensor(4, bno_bow);
  delay(5);

}

void loop() {
  
  /*for each imu print in sequence datas*/
  //EULER is in degrees

  for (int bus = 0; bus < 5; bus++) {

    tcaselect(bus);

    switch (bus) {

     /*
     x = Yaw, y = Roll, z = pitch 
     
     The Yaw values are between 0° to +360°
     The Roll values are between -90° and +90°
     The Pitch values are between -180° and +180°
    */ 
    
    case 0:
      sensors_event_t event0;
      bno_elbowL.getEvent(&event0, Adafruit_BNO055::VECTOR_EULER);
      Serial.print("Imu: elbowL = ");
      Serial.print(event0.orientation.x*1000);
      break;
      
    case 1:
      sensors_event_t event1;
      bno_shoulderL.getEvent(&event1, Adafruit_BNO055::VECTOR_EULER);
      Serial.print(" shoulderL = ");
      Serial.print(event1.orientation.x*1000);
      break;
      
    case 2:
      sensors_event_t event2;
      bno_shoulderR.getEvent(&event2,  Adafruit_BNO055::VECTOR_EULER);  
      Serial.print(" shoulderR = ");
      Serial.print(event2.orientation.x*1000);
      break;
      
    case 3:
      sensors_event_t event3;
      bno_elbowR.getEvent(&event3,  Adafruit_BNO055::VECTOR_EULER);
      Serial.print(" elbowR = ");
      Serial.println(event3.orientation.x*1000);
      break;

    case 4:
      sensors_event_t event4;
      bno_bow.getEvent(&event4,  Adafruit_BNO055::VECTOR_EULER);
      Serial.print("Bow: x = ");
      Serial.print(event4.orientation.x*1000);
      Serial.print(" y = ");
      Serial.print(event4.orientation.y*1000);
      Serial.print(" z = ");
      Serial.println(event4.orientation.z*1000);   
      break;
      
    }
    delay(1);  // delay in between reads for stability
   }

}
