#include "customImu.h"
#include <Adafruit_BNO055.h>

void customImu::output(float gyro_x, float gyro_y, float gyro_z, float accel_x, float accel_y, float accel_z){

    if (this-> counter == this-> number_of_measures){

      this-> counter = 0;
      
      Serial.print("Gyro: x = ");
      Serial.print(this-> U_hat_gyro_x);
      Serial.print(" y = ");
      Serial.print(this-> U_hat_gyro_y);
      Serial.print(" z = ");
      Serial.print(this-> U_hat_gyro_z);
      Serial.print(" Accel: x = ");
      Serial.print(this-> U_hat_accel_x);
      Serial.print(" y = ");
      Serial.print(this-> U_hat_accel_y);
      Serial.print(" z = ");
      Serial.print(this-> U_hat_accel_z);
      Serial.print(" measures= ");
      Serial.println(this-> number_of_measures);
    }
}


void customImu::update(){

    // Getting the data
    sensors_event_t event;
    this-> getEvent(& event);

    int roll = (int) event.orientation.roll * 1000;          // x
    int pitch = (int) event.orientation.pitch * 1000;        // y
    int heading = (int) event.orientation.heading * 1000;    // z

    int accel_x = (int) event.acceleration.x * 1000;
    int accel_y = (int) event.acceleration.y * 1000;
    int accel_z = (int) event.acceleration.z * 1000;

    // Saving the data
    this-> measures_gyro_x[this-> counter] = roll;
    this-> measures_gyro_y[this-> counter] = pitch;
    this-> measures_gyro_z[this-> counter] = heading;

    this-> measures_accel_x[this-> counter] = accel_x;
    this-> measures_accel_y[this-> counter] = accel_y;
    this-> measures_accel_z[this-> counter] = accel_z;

    // Incrementing the counter and checking if the number of iteration was reached
    this-> counter = this-> counter + 1;
    int num = this-> number_of_measures;

    if(this-> counter == num){

      // Average the measurements
      int avg_gyro_x = 0;
      int avg_gyro_y = 0;
      int avg_gyro_z = 0;

      int avg_accel_x = 0;
      int avg_accel_y = 0;
      int avg_accel_z = 0;
      
      for(int i = 0; i < num; i++){
        
        avg_gyro_x += this-> measures_gyro_x[i];
        avg_gyro_y += this-> measures_gyro_y[i];
        avg_gyro_z += this-> measures_gyro_z[i];

        avg_accel_x += this-> measures_accel_x[i];
        avg_accel_y += this-> measures_accel_y[i];
        avg_accel_z += this-> measures_accel_z[i];
      }
      /*
      avg_gyro_x /= num;
      avg_gyro_y /= num;
      avg_gyro_z /= num;

      avg_accel_x /= num;
      avg_accel_y /= num;
      avg_accel_z /= num;
      */
      // gyro filtering
      this-> K_gyro_x = (this-> P_gyro_x * this-> H_gyro_x) / (this-> H_gyro_x * this-> P_gyro_x * this-> H_gyro_x + this-> R_gyro_x); //updating Kalman gain
      this-> U_hat_gyro_x = this-> K_gyro_x * (avg_gyro_x - this-> H_gyro_x * this-> U_hat_gyro_x); //is U the prev_measure? should make sense
      this-> P_gyro_x = (1 - this-> K_gyro_x * this-> H_gyro_x) * this-> P_gyro_x + this-> Q_gyro_x;

      this-> K_gyro_y = (this-> P_gyro_y * this-> H_gyro_y) / (this-> H_gyro_y * this-> P_gyro_y * this-> H_gyro_y + this-> R_gyro_y); //updating Kalman gain
      this-> U_hat_gyro_y = this-> K_gyro_y * (avg_gyro_y - this-> H_gyro_y * this-> U_hat_gyro_y); //is U the prev_measure? should make sense
      this-> P_gyro_y = (1 - this-> K_gyro_y * this-> H_gyro_y) * this-> P_gyro_y + this-> Q_gyro_y;

      this-> K_gyro_z = (this-> P_gyro_z * this-> H_gyro_z) / (this-> H_gyro_z * this-> P_gyro_z * this-> H_gyro_z + this-> R_gyro_z); //updating Kalman gain
      this-> U_hat_gyro_z = this-> K_gyro_z * (avg_gyro_z - this-> H_gyro_z * this-> U_hat_gyro_z); //is U the prev_measure? should make sense
      this-> P_gyro_z = (1 - this-> K_gyro_z * this-> H_gyro_z) * this-> P_gyro_z + this-> Q_gyro_z;


      // accel filtering
      this-> K_accel_x = (this-> P_accel_x * this-> H_accel_x) / (this-> H_accel_x * this-> P_accel_x * this-> H_accel_x + this-> R_accel_x); //updating Kalman gain
      this-> U_hat_accel_x = this-> K_accel_x * (avg_accel_x - this-> H_accel_x * this-> U_hat_accel_x); //is U the prev_measure? should make sense
      this-> P_accel_x = (1 - this-> K_accel_x * this-> H_accel_x) * this-> P_accel_x + this-> Q_accel_x;

      this-> K_accel_y = (this-> P_accel_y * this-> H_accel_y) / (this-> H_accel_y * this-> P_accel_y * this-> H_accel_y + this-> R_accel_y); //updating Kalman gain
      this-> U_hat_accel_y = this-> K_accel_y * (avg_accel_y - this-> H_accel_y * this-> U_hat_accel_y); //is U the prev_measure? should make sense
      this-> P_accel_y = (1 - this-> K_accel_y * this-> H_accel_y) * this-> P_accel_y + this-> Q_accel_y;

      this-> K_accel_z = (this-> P_accel_z * this-> H_accel_z) / (this-> H_accel_z * this-> P_accel_z * this-> H_accel_z + this-> R_accel_z); //updating Kalman gain
      this-> U_hat_accel_z = this-> K_accel_z * (avg_accel_z - this-> H_accel_z * this-> U_hat_accel_z); //is U the prev_measure? should make sense
      this-> P_accel_z = (1 - this-> K_accel_z * this-> H_accel_z) * this-> P_accel_z + this-> Q_accel_z;


      this-> output(avg_gyro_x, avg_gyro_y, avg_gyro_z, avg_accel_x, avg_accel_y, avg_accel_z);
    }
    
}
