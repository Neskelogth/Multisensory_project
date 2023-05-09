int init_time = 5000;

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  while(millis()<init_time){
  }

}

void loop() {
  // analog read of the force sensors
  int fsr0 = analogRead(A0);
  int fsr1 = analogRead(A1);
  int fsr2 = analogRead(A2);
  int fsr3 = analogRead(A3);

  // communication of the force sensor outputs
  Serial.print("FSR0 = ");
  Serial.print(fsr0);
  Serial.print(" FSR1 = ");
  Serial.print(fsr1);
  Serial.print(" FSR2 = ");
  Serial.print(fsr2);
  Serial.print(" FSR3 = ");
  Serial.println(fsr3);

}
