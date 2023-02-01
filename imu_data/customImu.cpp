#include "customImu.h"
#include <Adafruit_BNO055.h>

void customImu::output(float gyro_x, float gyro_y, float gyro_z){

    if (this-> counter == this-> number_of_measures){

      this-> counter = 0;
      
      Serial.print("Gyro: x = ");
      Serial.print(this-> U_hat_gyro_x);
      Serial.print(" y = ");
      Serial.print(this-> U_hat_gyro_y);
      Serial.print(" z = ");
      Serial.println(this-> U_hat_gyro_z);
    }
}


void customImu::update(){

    //Getting the data
    imu::Vector<3> euler = this-> getVector(Adafruit_BNO055::VECTOR_EULER);

    int roll = (int) (euler.x() * 1000);
    int pitch = (int) (euler.y() * 1000);
    int yaw = (int) (euler.z() * 1000);

    // Saving the data
    this-> measures_gyro_x[this-> counter] = roll;
    this-> measures_gyro_y[this-> counter] = pitch;
    this-> measures_gyro_z[this-> counter] = yaw;

    // Incrementing the counter and checking if the number of iteration was reached
    this-> counter = this-> counter + 1;
    int num = this-> number_of_measures;

    if(this-> counter == num){

      // Average the measurements
      int avg_gyro_x = 0;
      int avg_gyro_y = 0;
      int avg_gyro_z = 0;
      
      for(int i = 0; i < num; i++){
        
        avg_gyro_x += this-> measures_gyro_x[i];
        avg_gyro_y += this-> measures_gyro_y[i];
        avg_gyro_z += this-> measures_gyro_z[i];
      }
      /*
      avg_gyro_x /= num;
      avg_gyro_y /= num;
      avg_gyro_z /= num;
      */
      
      // gyro filtering
      this-> K_gyro_x = (this-> P_gyro_x * this-> H_gyro_x) / (this-> H_gyro_x * this-> P_gyro_x * this-> H_gyro_x + this-> R_gyro_x); //updating Kalman gain
      this-> U_hat_gyro_x = this-> K_gyro_x * (avg_gyro_x - this-> H_gyro_x * this-> U_hat_gyro_x);
      this-> P_gyro_x = (1 - this-> K_gyro_x * this-> H_gyro_x) * this-> P_gyro_x + this-> Q_gyro_x;

      this-> K_gyro_y = (this-> P_gyro_y * this-> H_gyro_y) / (this-> H_gyro_y * this-> P_gyro_y * this-> H_gyro_y + this-> R_gyro_y); //updating Kalman gain
      this-> U_hat_gyro_y = this-> K_gyro_y * (avg_gyro_y - this-> H_gyro_y * this-> U_hat_gyro_y); 
      this-> P_gyro_y = (1 - this-> K_gyro_y * this-> H_gyro_y) * this-> P_gyro_y + this-> Q_gyro_y;

      this-> K_gyro_z = (this-> P_gyro_z * this-> H_gyro_z) / (this-> H_gyro_z * this-> P_gyro_z * this-> H_gyro_z + this-> R_gyro_z); //updating Kalman gain
      this-> U_hat_gyro_z = this-> K_gyro_z * (avg_gyro_z - this-> H_gyro_z * this-> U_hat_gyro_z); 
      this-> P_gyro_z = (1 - this-> K_gyro_z * this-> H_gyro_z) * this-> P_gyro_z + this-> Q_gyro_z;

      this-> output(avg_gyro_x, avg_gyro_y, avg_gyro_z);
    }
    
}
