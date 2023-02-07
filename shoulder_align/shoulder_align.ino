/*Shoulder correction pose for archery */


#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#include "customImu.h"

/* IMU ***************************************************************************************************/

/* Assign a unique ID to this sensor at the same time */
/*Adafruit_BNO055 bno_wrist = Adafruit_BNO055(-1, 0x28);*/

customImu bno_elbowL = customImu();
customImu bno_shoulderL = customImu();
customImu bno_shoulderR = customImu();
customImu bno_elbowR = customImu();

customImu bno_bow = customImu();

int a,b,c,d,e = 0;


//Adafruit_BNO055 bno_elbowL = Adafruit_BNO055(55);
//Adafruit_BNO055 bno_shoulderL = Adafruit_BNO055(55);
//Adafruit_BNO055 bno_shoulderR = Adafruit_BNO055(55);
//Adafruit_BNO055 bno_elbowR = Adafruit_BNO055(55);

/**************************************************************************/


/*define instatition for the i2c multiplexer, no need of library*/
/*If the pins A0, A1 and A2 from the multiplexer board are left unconnected,
then we are using the 0x70 address.*/
#define TCAADDR 0X70

#define BAUD_RATE 9600

/*array size to print the name of the imus*/
#define ARRAYSIZE 5
String names[ARRAYSIZE] = { "bno_elbowL", "bno_shoulderL", "bno_shoulderR", "bno_elbowR", "bno_bow"};


/**************************************************************************/
/* Choose bus */
/**************************************************************************/
/*function to toggle between the channels with i2c
the order is from 0 to 7 */
void tcaselect(uint8_t bus){
  
  if (bus > 7) return;

  Serial.print("TCA Port #"); Serial.println(bus);

  Wire.beginTransmission(TCAADDR);
  Serial.println(F("Ciao"));
  Wire.write(1 << bus); //send byte to select bus
  Serial.println(F("ggggggggggggggggggggggggggggggg"));
  Wire.endTransmission();
  Serial.println(bus);
}


/**************************************************************************/
/* Init of imus */
/**************************************************************************/

void init_sensor(uint8_t i, customImu bno){
  
  /*multiplex selection*/
  
  tcaselect(i);
  
  Serial.println(F("##############################"));
  // Exit from the script if the sensor is not connected
  if (!bno.begin()){
    /* There was a problem detecting the BNO055 ... check your connections */
    exit(2);  //Exit with an error to make sure the script exits in case the IMU is not connected
  }
  
  delay(10);
}

void setup() {
  Serial.begin(BAUD_RATE);
  while(!Serial);
  Wire.begin();

  Serial.println(F("##############################"));            
  Serial.println(F("Starting Initialization"));
  Serial.println(F("##############################"));

  /* Setup of the digital sensors */
  /*create a function to call for each sensor*/
  init_sensor(0, bno_elbowL);
  Serial.println(F("##############################"));
  delay(10);
  init_sensor(1, bno_shoulderL);
  delay(10);
  init_sensor(2, bno_shoulderR);
  delay(10);
  init_sensor(3, bno_elbowR);
  delay(10);
  init_sensor(4, bno_bow);
  delay(10);
    
  Serial.println();
  Serial.println(F("##############################"));
  Serial.println(F("Initialization Finished"));
  Serial.println(F("##############################"));  
  Serial.println();
  Serial.println();

}

void loop() {
  /*for each imu print in sequence datas*/
  for (int bus = 0; bus < 5; bus++) {

    tcaselect(bus);
    
    switch (bus) {
    case 0:
      a = bno_elbowL.update(a);    
      break;
    case 1:
      b = bno_shoulderL.update(b);
      break;
    case 2:
      c = bno_shoulderR.update(c); 
      break;
    case 3:
      d = bno_elbowR.update(d);
      break;
    case 4:
      e = bno_bow.update(e);
      break;
    }
    //delay(1);  // delay in between reads for stability
   }
   
}
