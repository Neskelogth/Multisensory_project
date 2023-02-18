/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/

int init_time = 5000;

const float VCC = 5;
const float R_DIV  = 10000.0;
const int avg_size = 10;

float taraA;
float taraC;
float taraE;
float taraG;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  while(millis()<init_time){
  }

  float fsrA = 0;
  float fsrC = 0;
  float fsrE = 0;
  float fsrG = 0;

  fsrA = analogRead(A0) * VCC / 1023.0;
  fsrC = analogRead(A1) * VCC / 1023.0;
  fsrE = analogRead(A2) * VCC / 1023.0;
  fsrG = analogRead(A3) * VCC / 1023.0;

  float fsrRA = R_DIV * (VCC / fsrA - 1.0);
  float fsrRC = R_DIV * (VCC / fsrC - 1.0);
  float fsrRE = R_DIV * (VCC / fsrE - 1.0);
  float fsrRG = R_DIV * (VCC / fsrG - 1.0);

  float fsrCA = 1.0 / fsrRA;
  float fsrCC = 1.0 / fsrRC;
  float fsrCE = 1.0 / fsrRE;
  float fsrCG = 1.0 / fsrRG;

  float fsrWA = force(fsrRA, fsrCA);
  float fsrWC = force(fsrRC, fsrCC);
  float fsrWE = force(fsrRE, fsrCE);
  float fsrWG = force(fsrRG, fsrCG);

  taraA = 1775/fsrWA;
  taraC = 1775/fsrWC;
  taraE = 1775/fsrWE;
  taraG = 1775/fsrWG;

}

float force(float resistance, float conduttance){
  // Use the two FSR guide graphs to approximate the force
  float fsrForce = 0;

  if (resistance <= 400) 
      fsrForce = (conduttance - 0.00075) / 0.00000032639;
    else
      fsrForce =  conduttance / 0.000000642857;

  return fsrForce;
}


// the loop routine runs over and over again forever:
void loop() {
  float fsrA = 0;
  float fsrC = 0;
  float fsrE = 0;
  float fsrG = 0;
  
  fsrA = analogRead(A0) * VCC / 1023.0;
  fsrC = analogRead(A1) * VCC / 1023.0;
  fsrE = analogRead(A2) * VCC / 1023.0;
  fsrG = analogRead(A3) * VCC / 1023.0;

  float fsrRA = R_DIV * (VCC / fsrA - 1.0);
  float fsrRC = R_DIV * (VCC / fsrC - 1.0);
  float fsrRE = R_DIV * (VCC / fsrE - 1.0);
  float fsrRG = R_DIV * (VCC / fsrG - 1.0);

  float fsrCA = 1.0 / fsrRA;
  float fsrCC = 1.0 / fsrRC;
  float fsrCE = 1.0 / fsrRE;
  float fsrCG = 1.0 / fsrRG;

  float fsrFA = force(fsrRA, fsrCA)*taraA/1000*9.81;
  float fsrFC = force(fsrRC, fsrCC)*taraC/1000*9.81;
  float fsrFE = force(fsrRE, fsrCE)*taraE/1000*9.81;
  float fsrFG = force(fsrRG, fsrCG)*taraG/1000*9.81;
 
  float x = (fsrFC*0.60 + fsrFE*0.60 - (7.1*9.81*0.60/2))/(63*9.81);
  float y = (fsrFA*0.60 + fsrFC*0.60 - (7.1*9.81*0.60/2))/(63*9.81);

  // print out the value you read:
  Serial.print("X = ");
  Serial.print(x*1000);
  Serial.print(" Y = ");
  Serial.println(y*1000);
}
