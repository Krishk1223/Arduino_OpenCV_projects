#include <LiquidCrystal.h>

/*
 The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K variable resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)
*/

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2; //circuit setup
LiquidCrystal lcd(rs, en, d4, d5, d6, d7); // lcd initialised 
char incomingData; // pySerial data incoming
const int BAUD_RATE = 9600;

void setup() {
  // put your setup code here, to run once:
  lcd.begin(16, 2);
  Serial.begin(BAUD_RATE);
  lcd.setCursor(0,0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){ // if incoming data recieved to arduino then condition is true
    incomingData = Serial.read(); // read data 
    if (incomingData == 's'){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Sad :(");
    }
    else if (incomingData == 'n'){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Neutral :|");
    }
    else if (incomingData == 'h'){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Happy :)");
    }
    else {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Not sure");
    }
  }

}
