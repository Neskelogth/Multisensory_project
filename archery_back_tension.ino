/*Shoulder correction pose for archery */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>



/* IMU ***************************************************************************************************/

/* Set the delay between fresh samples */
static const unsigned long BNO055_PERIOD_MILLISECS = 100; // E.g. 4 milliseconds per sample for 250 Hz
#define BNO055_PERIOD_MICROSECS 100.0e3f //= 1000 * PERIOD_MILLISECS;
static uint32_t BNO055_last_read = 0;

/* Assign a unique ID to this sensor at the same time */
/*Adafruit_BNO055 bno_wrist = Adafruit_BNO055(-1, 0x28);*/
Adafruit_BNO055 bno_elbowL = Adafruit_BNO055(55);
Adafruit_BNO055 bno_shoulderL = Adafruit_BNO055(55);
Adafruit_BNO055 bno_shoulderR = Adafruit_BNO055(55);
Adafruit_BNO055 bno_elbowR = Adafruit_BNO055(55);


/**************************************************************************/


/*define instatition for the i2c multiplexer, no need of library*/
/*If the pins A0, A1 and A2 from the multiplexer board are left unconnected,
then we are using the 0x70 address.*/
#define TCAADDR 0X70

#define BAUD_RATE 9600

/*array size to print the name of the imus*/
#define ARRAYSIZE 4
String names[ARRAYSIZE] = { "bno_elbowL", "bno_shoulderL", "bno_shoulderR", "bno_elbowR" };


/**************************************************************************/
/* Choose bus */
/**************************************************************************/
/*function to toggle between the channels with i2c
the order is from 0 to 7 */
void tcaselect(uint8_t bus){
  
  if (bus > 7) return;

  Serial.print("TCA Port #"); Serial.println(bus);

  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << bus); //send byte to select bus
  Wire.endTransmission();
  Serial.println(bus);
}


/**************************************************************************/
/* Init of imus */
/**************************************************************************/
void init_sensor(uint8_t i, Adafruit_BNO055 bno){
  /*multiplex selection*/
  tcaselect(i);

  Serial.println("Sensor initializing..."); Serial.println("");
  
  /* Initialize the sensor */
  if(!bno.begin()){
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print(F("BNO055 "));
    Serial.print(names[i]); 
    Serial.println(F(" NOT detected"));
    while(1);
  }
  
  delay(1000);
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
  delay(10);
  init_sensor(1, bno_shoulderL);
  delay(10);
  init_sensor(2, bno_shoulderR);
  delay(10);
  init_sensor(3, bno_elbowR);
  delay(10);
    
  Serial.println();
  Serial.println(F("##############################"));
  Serial.println(F("Initialization Finished"));
  Serial.println(F("##############################"));  
  Serial.println();
  Serial.println();
  
  //filtering sensor by taking an averaging every 10 measures
  
  //init counter
  a,b,c,d = 0;
  
  //init avg
  avg_a = 0;
  avg_b = 0;
  avg_c = 0;
  avd_d = 0;

}

void loop() {
  /*for each imu print in sequence datas*/
  

  for (int bus = 0; bus < 4; bus++) {

    tcaselect(bus);

    if (micros() - BNO055_last_read >= BNO055_PERIOD_MICROSECS) {
    BNO055_last_read += BNO055_PERIOD_MICROSECS;

    sensors_event_t orientationData;

    switch (bus) {
    case 0:
      
      a += 1;
      avg_a += orientationData.orientation.y;
      
      if (a % 10 == 0){
      bno_wrist.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
      Serial.print("elbowL y = ");
      Serial.print(avg_a/10 * 1000);
      avg_a = 0;
      }
      
      break;
    case 1:
      
      b += 1;
      avg_b += orientationData.orientation.y;
      
      if (b % 10 == 0){
      bno_shoulderL.getEvent(&angVelData, Adafruit_BNO055::VECTOR_GYROSCOPE);
      Serial.print("shoulderL y = ");
      Serial.print(avg_b/10 * 1000);
      avg_b = 0;
      }
      
      break;
    case 2:
    
      c += 1;
      avg_c += orientationData.orientation.y;
    
      if (c % 10 == 0){
      bno_shoulderR.getEvent(&angVelData, Adafruit_BNO055::VECTOR_GYROSCOPE);
      Serial.print("shoulderR y = ");
      Serial.print(avg_c/10 * 1000 );
      avg_c = 0;
      }
      
      break;
    case 3:
      
      d += 1;
      avg_d += orientationData.orientation.y;
      
      if (d % 10 == 0){
      bno_elbowR.getEvent(&angVelData, Adafruit_BNO055::VECTOR_GYROSCOPE);
      Serial.print("elbowR y = ");
      Serial.println(avg_d/10 * 1000);
      avg_d = 0;
      }
      
      break;
    }
    delay(1);  // delay in between reads for stability
   }
   delay(1);
  }

}
