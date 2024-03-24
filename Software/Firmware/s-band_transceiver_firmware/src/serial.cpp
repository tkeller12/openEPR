#include "Arduino.h"
#include "main.h"
#include "serial.h"
String serialString = "";

void serialLoop() {
  int8_t whitespaceIndex;
  String serialCommand;
  String serialData;
  uint32_t serialValue;
  char incomingChar;
  //uint8_t incomingByte;
  bool serialQuery;

  if (Serial.available() > 0){
    incomingChar = Serial.read(); // Read 1 byte
    //incomingChar = Serial.readString(); // This will read until timeout, instead you should only read 1 byte
    serialString += incomingChar; // Append to string
    //serialString.concat(incomingChar); // Alternative method

    //Serial.println(serialString); // Uncomment for troubleshooting
  }

  if (serialString.endsWith("\n")){
    serialString.trim(); // Remove whitespace and newline
    serialString.toLowerCase(); // Convert to Lower case
    whitespaceIndex = serialString.indexOf(" "); // Find index of space
    serialCommand = serialString.substring(0,whitespaceIndex); // Command is 1st part
    serialData = serialString.substring(whitespaceIndex); // Data is 2nd part
    serialQuery = serialCommand.endsWith("?"); // Queries have question mark
    serialValue = serialData.toInt(); // Convert data to integer

    if (serialQuery) {
      serialCommand.remove(serialCommand.lastIndexOf("?")); // Remove "?"
    }
    serialString = "";  //reset string

    if (serialCommand == "*IDN") { // should thick check for "?"?
      Serial.println('openEPR,S-Band Transceiver,v0.1.0');
    }
    else if (serialCommand == "freq"){
      if (serialQuery) {
        Serial.println(freq);
      }
      else if ((serialValue >= 35000) && (serialValue <= 4400000)) {
        freq = serialValue;
        adf.setFrequency(freq);
      }
    }
    else if (serialCommand == "power"){
      if (serialQuery) {
        Serial.println(power);
      }
      else if((serialValue >= 0) && (serialValue <= 3)) {
          power = serialValue;
          adf.setPower(power);                  
      }
    }
    else if (serialCommand == "rfenable"){
      if (serialQuery) {
        Serial.println(is_rf_enabled);
      }
      else if ((serialValue == 0) || (serialValue == 1)) {
        is_rf_enabled = serialValue;
        adf.rfEnable(is_rf_enabled);
      }
    }
    else if (serialCommand == "adc"){
      if (serialQuery) {
        Serial.println(String(adc.getMilliVolts(),4));
      }
      else if (serialData == "tx"){
        adc.setInputSelected(adc.AIN_0);
      }
      else if (serialData == "rx"){
        adc.setInputSelected(adc.AIN_1);
      }
      else if (serialData == "diff"){
        adc.setInputSelected(adc.DIFF_0_1);
      }
    }
    else if (serialCommand == "atten"){
      if (serialQuery) {
        Serial.println(atten);
      }
      else if (serialValue < 32) {
        dat.writeAtten(atten);
      }
    }
  }


}