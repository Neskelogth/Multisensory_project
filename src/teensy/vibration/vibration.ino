int const BAUDRATE = 9600;
int vibra_1 = 1;
int vibra_2 = 3;
int vibra_3 = 5;
int vibra_4 = 7;

void setup() {
  Serial.begin(BAUDRATE);
  Serial.setTimeout(10);

  pinMode(vibra_1, OUTPUT);
  pinMode(vibra_2, OUTPUT);
  pinMode(vibra_3, OUTPUT);
  pinMode(vibra_4, OUTPUT);
}

void loop() {
  if (Serial.available() > 0){
    String str = Serial.readString();
    
    if (str[0] == '1'){
    digitalWrite(vibra_1, HIGH);
    }else{
      digitalWrite(vibra_1, LOW);
    }
    
    if (str[1] == '1'){
    digitalWrite(vibra_2, HIGH);
    }else{
      digitalWrite(vibra_2, LOW);
    }
    
    if (str[2] == '1'){
    digitalWrite(vibra_3, HIGH);
    }else{
      digitalWrite(vibra_3, LOW);
    }
    
    if (str[3] == '1'){
    digitalWrite(vibra_4, HIGH);
    }else{
      digitalWrite(vibra_4, LOW);
    }
  }
}
