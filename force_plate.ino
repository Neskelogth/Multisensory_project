/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/

int init_time = 5000;

float init_fsrA = 0;
float init_fsrB = 0;
float init_fsrC = 0;
float init_fsrD = 0;
float init_fsrE = 0;
float init_fsrF = 0;
float init_fsrG = 0;
float init_fsrH = 0;

float taraA=0.5656;
float taraC=0.6219;
float taraE=0.5605;
float taraG=0.5556;

const float VCC = 5;
const float R_DIV  = 10000.0;
const int avg_size = 10;

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

  Serial.println(analogRead(A0));


  fsrA = analogRead(A0) * VCC / 1023.0;
  fsrC = analogRead(A1) * VCC / 1023.0;
  fsrE = analogRead(A2) * VCC / 1023.0;
  fsrG = analogRead(A3) * VCC / 1023.0;

  Serial.println(fsrA);
  Serial.println(fsrC);
  Serial.println(fsrE);
  Serial.println(fsrG);

  float fsrRA = R_DIV * (VCC / fsrA - 1.0);
  float fsrRC = R_DIV * (VCC / fsrC - 1.0);
  float fsrRE = R_DIV * (VCC / fsrE - 1.0);
  float fsrRG = R_DIV * (VCC / fsrG - 1.0);

  float fsrCA = 1.0 / fsrRA;
  float fsrCC = 1.0 / fsrRC;
  float fsrCE = 1.0 / fsrRE;
  float fsrCG = 1.0 / fsrRG;

  Serial.println(force(fsrRA, fsrCA));
  Serial.println(force(fsrRC, fsrCC));
  Serial.println(force(fsrRE, fsrCE));
  Serial.println(force(fsrRG, fsrCG));

  float fsrFA = force(fsrRA, fsrCA)*taraA/1000*9.81;
  float fsrFC = force(fsrRC, fsrCC)*taraC/1000*9.81;
  float fsrFE = force(fsrRE, fsrCE)*taraE/1000*9.81;
  float fsrFG = force(fsrRG, fsrCG)*taraG/1000*9.81;
 
  float x = (fsrFC*0.60 + fsrFE*0.60 - (7.1*9.81*0.60/2))/(63*9.81);
  float y = (fsrFA*0.60 + fsrFC*0.60 - (7.1*9.81*0.60/2))/(63*9.81);

  //float x = (fsrFC*0.60 + fsrFD*0.60 + fsrFE*0.60 + fsrFB*0.60/2 + fsrFF*0.60/2 )/(63*9.81);
  //float y = (fsrFA*0.60 + fsrFB*0.60 + fsrFC*0.60 + fsrFD*0.60/2 + fsrFH*0.60/2 )/(63*9.81);

  // print out the value you read:
  String text = "A: ";
  text = text + fsrFA;
  text = text + " C: "; 
  text = text + fsrFC;  
  text = text + " E: ";
  text = text + fsrFE;
  text = text + " G: "; 
  text = text + fsrFG;
  Serial.println(text);
  Serial.print("X = ");
  Serial.println(x);
  Serial.print("Y = ");
  Serial.println(y);

  delay(1000);  // delay in between reads for stability
}
