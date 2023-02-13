/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/

int init_time = 5000;
int init_LF = 0;
int init_RF = 0;
int init_LB = 0;
int init_RB = 0;

const float VCC = 3.3;
const float R_DIV  = 10000.0;
const int avg_size = 10;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

float force(float resistance, float conduttance){
  // Use the two FSR guide graphs to approximate the force
  float fsrForce = 0;

  if (resistance <= 600) 
      fsrForce = (conduttance - 0.00075) / 0.00000032639;
    else
      fsrForce =  conduttance / 0.000000642857;

  return fsrForce;
}

// the loop routine runs over and over again forever:
void loop() {
  float fsrA = 0;
  float fsrB = 0;
  float fsrC = 0;
  float fsrD = 0;
  float fsrE = 0;
  float fsrF = 0;
  float fsrG = 0;
  float fsrH = 0;

  // read the input on analog pins
  for(int i=0; i < avg_size; i++){
    fsrA += analogRead(A0) * VCC / 1023.0;
    fsrB += analogRead(A4) * VCC / 1023.0;
    fsrC += analogRead(A1) * VCC / 1023.0;
    fsrD += analogRead(A5) * VCC / 1023.0;
    fsrE += analogRead(A2) * VCC / 1023.0;
    fsrF += analogRead(A6) * VCC / 1023.0;
    fsrG += analogRead(A3) * VCC / 1023.0;
    fsrH += analogRead(A7) * VCC / 1023.0;
    delay(10);
  }

  fsrA /= avg_size;
  fsrB /= avg_size;
  fsrC /= avg_size;
  fsrD /= avg_size;
  fsrE /= avg_size;
  fsrF /= avg_size;
  fsrG /= avg_size;
  fsrH /= avg_size;

  Serial.println(fsrA);
  Serial.println(fsrB);
  Serial.println(fsrC);
  Serial.println(fsrD);
  Serial.println(fsrE);
  Serial.println(fsrF);
  Serial.println(fsrG);

  float fsrRA = R_DIV * (VCC / fsrA - 1.0);
  float fsrRB = R_DIV * (VCC / fsrB - 1.0);
  float fsrRC = R_DIV * (VCC / fsrC - 1.0);
  float fsrRD = R_DIV * (VCC / fsrD - 1.0);
  float fsrRE = R_DIV * (VCC / fsrE - 1.0);
  float fsrRF = R_DIV * (VCC / fsrF - 1.0);
  float fsrRG = R_DIV * (VCC / fsrG - 1.0);
  float fsrRH = R_DIV * (VCC / fsrH - 1.0);

  float fsrCA = 1.0 / fsrRA;
  float fsrCB = 1.0 / fsrRB;
  float fsrCC = 1.0 / fsrRC;
  float fsrCD = 1.0 / fsrRD;
  float fsrCE = 1.0 / fsrRE;
  float fsrCF = 1.0 / fsrRF;
  float fsrCG = 1.0 / fsrRG;
  float fsrCH = 1.0 / fsrRH;

  float fsrFA = force(fsrRA, fsrCA)/1000*9.8;
  float fsrFB = force(fsrRB, fsrCB)/1000*9.8;
  float fsrFC = force(fsrRC, fsrCC)/1000*9.8;
  float fsrFD = force(fsrRD, fsrCD)/1000*9.8;
  float fsrFE = force(fsrRE, fsrCE)/1000*9.8;
  float fsrFF = force(fsrRF, fsrCF)/1000*9.8;
  float fsrFG = force(fsrRG, fsrCG)/1000*9.8;
  float fsrFH = force(fsrRH, fsrCH)/1000*9.8;
 
  float x = (fsrFC*0.75 + fsrFD*0.75 + fsrFE*0.75 + fsrFB*0.75/2 + fsrFF*0.75/2 - (11.1*9.81*0.75/2))/(63*9.81);
  float y = (fsrFA*0.75 + fsrFB*0.75 + fsrFC*0.75 + fsrFD*0.75/2 + fsrFH*0.75/2 - (11.1*9.81*0.75/2))/(63*9.81);

  // print out the value you read:
  String text = "A: ";
  text = text + fsrFA;
  text = text + " B: ";
  text = text + fsrFB; 
  text = text + " C: "; 
  text = text + fsrFC;  
  text = text + " D: ";
  text = text + fsrFD;
  text = text + " E: ";
  text = text + fsrFE;
  text = text + " F: ";
  text = text + fsrFF; 
  text = text + " G: "; 
  text = text + fsrFG;  
  text = text + " H: ";
  text = text + fsrFH;
  Serial.println(text);
  Serial.print("X = ");
  Serial.println(x);
  Serial.print("Y = ");
  Serial.println(y);

  delay(1000);  // delay in between reads for stability
}
