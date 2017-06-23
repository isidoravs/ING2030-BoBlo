#include "HX711.h"
#include <Servo.h> 

HX711 scale;
 
Servo myservo;  

int angulo = 90; //angulo de giro del servo
int boton=8;//pin del boton

void setup() {
  Serial.begin(38400);
  scale.begin(A1, A0);

  myservo.attach(9);  //Pin del servo
  pinMode(boton,INPUT);
  myservo.write(0);

  scale.set_scale(-436.6);    // this value is obtained by calibrating the scale with known weights; see the README for details
  scale.tare();               // reset the scale to 0

}

void loop() {
  Serial.println(scale.get_units(), 0);

  scale.power_down();             // put the ADC in sleep mode
  delay(500);
  scale.power_up();

  if(Serial.available()){ // only send data back if data has been sent
    if(Serial.read() == 100){ // entrego señal de d
      myservo.write(angulo);     
      delay(500);
      myservo.write(0); 
      Serial.println("Exito");
    }
  }
}
