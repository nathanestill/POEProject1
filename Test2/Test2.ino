#include <Servo.h>

Servo panservo;
Servo tiltservo;

int pos1 = 0;
int pos2 = 0;

const int analogInPin = A0;
int sensorValue = 0;
void setup() {
  panservo.attach(9);
  tiltservo.attach(10);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  for (pos1 = 60; pos1 <= 120; pos1 += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    panservo.write(pos1);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
    for (pos2 = 50; pos2 <= 130; pos2 += 2) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      tiltservo.write(pos2);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
      printReadings(analogInPin, pos1, pos2); // prints all of the readings to the python script to visualize it
      delay(15);
    }
    pos1 = pos1 + 1;
    panservo.write(pos1);
    delay(15);
    for (pos2 = 130; pos2 >= 50; pos2 -= 2) { // goes from 180 degrees to 0 degrees
      tiltservo.write(pos2);  // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
      printReadings(analogInPin, pos1, pos2); // prints all of the readings to the python script to visualize it
      delay(15);
    }
  }
}
void printReadings(int analogInPin, int pos1, int pos2) {
  sensorValue = analogRead(analogInPin); // gets the raw sensor value
  // map it to the range of the analog out:
  int distance = 129.97 * exp(-0.004 * sensorValue) * 100; // converts the value into a distance (multiplied by 100 to make it an int)
  // communicates the distance and angles to the python script:
  Serial.print(distance); Serial.print(",");
  Serial.print(pos1); Serial.print(",");
  Serial.println(pos2);
}
