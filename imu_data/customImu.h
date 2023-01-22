#include <Adafruit_BNO055.h>

// Imu with Kalman filter
class customImu: public Adafruit_BNO055{

	private:

    static const int n = 10;
    int number_of_measures;
    int counter = 0;

    //storing the measures to make compute the average
		int measures_gyro_x[n];
    int measures_gyro_y[n];
    int measures_gyro_z[n];

    int measures_accel_x[n];
    int measures_accel_y[n];
    int measures_accel_z[n];

    //gyro_x
		float K_gyro_x = 0;    // Kalman gain
    float R_gyro_x = 10.;  // Initial noise covariance                       ------------- Not updated
    float H_gyro_x = 1.;   // measurement map scalar                         ------------- Not updated
    float Q_gyro_x = 10.;  // initial esitimated covariance                  ------------- Not updated
    float P_gyro_x = 0;    // initial error measurement
    float U_hat_gyro_x = 0; // initial esitimated state
    
    //gyro_y
    float K_gyro_y = 0;    // Kalman gain
    float R_gyro_y = 10.;  // Noise covariance
    float H_gyro_y = 1.;   // measurement map scalar
    float Q_gyro_y = 10.;  // initial esitimated covariance
    float P_gyro_y = 0;    // initial error measurement
    float U_hat_gyro_y = 0; // initial esitimated state

    //gyro_z
    float K_gyro_z = 0;     // Kalman gain
    float R_gyro_z = 10.;   // Noise covariance
    float H_gyro_z = 1.;    // measurement map scalar
    float Q_gyro_z = 10.;   // initial esitimated covariance
    float P_gyro_z = 0;     // initial error measurement
    float U_hat_gyro_z = 0;  // initial esitimated state


    //accel_x
    float K_accel_x = 0;     // Kalman gain
    float R_accel_x = 10.;   // Noise covariance
    float H_accel_x = 1.;    // measurement map scalar
    float Q_accel_x = 10.;   // initial esitimated covariance
    float P_accel_x = 0;     // initial error measurement
    float U_hat_accel_x = 0;  // initial esitimated state
    
    //gyro_y
    float K_accel_y = 0;    // Kalman gain
    float R_accel_y = 10.;  // Noise covariance
    float H_accel_y = 1.;   // measurement map scalar
    float Q_accel_y = 10.;  // initial esitimated covariance
    float P_accel_y = 0;    // initial error measurement
    float U_hat_accel_y = 0; // initial esitimated state

    //gyro_z
    float K_accel_z = 0;    // Kalman gain
    float R_accel_z = 10.;  // Noise covariance
    float H_accel_z = 1.;   // measurement map scalar
    float Q_accel_z = 10.;  // initial esitimated covariance
    float P_accel_z = 0;    // initial error measurement
    float U_hat_accel_z = 0; // initial esitimated statex\

    float applyFilter();
    float getAverage();
		void output(float gyro_x, float gyro_y, float gyro_z, float accel_x, float accel_y, float accel_z);
   
	public:

    customImu(int n=10);
    void update();
};
