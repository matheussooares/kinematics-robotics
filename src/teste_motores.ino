#include <Servo.h>


Servo junta_1;
Servo junta_2;
Servo junta_3;
Servo junta_4;


void setup() {
  junta_1.attach(6);
  junta_2.attach(7);
  junta_3.attach(8);
  junta_4.attach(9);

  Serial.begin(9600);
}

void loop() {

  junta_1.write(0);

  delay(1000);

  junta_1.write(179);

  delay(1000);

  junta_1.write(0);

  delay(1000);

// JUNTA 2
  junta_2.write(0);

  delay(1000);
  
  junta_2.write(179);

  delay(1000);

  junta_2.write(0);

  delay(1000);

//JUNTA 3
  junta_3.write(0);

  delay(1000);
  
  junta_3.write(179);
  
  delay(1000);

  junta_3.write(0);

  delay(1000);

//JUNTA 4
  junta_4.write(0);

  delay(1000);
  
  junta_4.write(179);

  delay(1000);

  junta_4.write(0);

  delay(1000);

}
