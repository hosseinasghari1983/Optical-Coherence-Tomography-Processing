#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  pinMode(2,OUTPUT);
  pinMode(13,OUTPUT);
}

void loop() {
  if (Serial.available()) {
    digitalWrite(13,HIGH);
    digitalWrite(2,HIGH);
    delay(1);
    digitalWrite(2,LOW);
    digitalWrite(13,LOW);
    while(Serial.available()){
      Serial.read();
    }
  }
}