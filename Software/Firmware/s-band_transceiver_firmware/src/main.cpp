#include <Arduino.h>
#include <SPI.h>
#include "adf4351.h"
#include "serial.h"
#include "main.h"

#define SERIAL_BAUD 115200 // Serial baud rate


#define ADF_LE PIN_PC0 // Load Enable Pin for SPI communication

#define TX_AMP_ENABLE PIN_PB5 // Digital pin to enable TX Amplifier
#define RX_AMP_ENABLE PIN_PC5 // Digital pin to enable RX Amplifier

#define TX_ATTEN_LE PIN_PC1
#define TX_PHASE_LE PIN_PC2

#define ADC_CS PIN_PC3 // ADS1118 ~CS pin

#define XO_ENABLE PIN_PC6 // 10 MHz oscillator on board enable pin

#define LD PIN_PE0 // Lock Detect Pin, this is a digital input
#define RUN_LED PIN_PE1 // Processor RUN LED indicator
#define ERROR_LED PIN_PE2 // 

#define RUN_LED_MS_DELAY 


// TX ATTEN CONTROL PINS
#define C1_PIN PIN_PB0
#define C2_PIN PIN_PB1
#define C4_PIN PIN_PB2
#define C8_PIN PIN_PB3
#define C16_PIN PIN_PB4


ADF4351 adf(ADF_LE);
DAT31A dat(TX_ATTEN_LE, C1_PIN, C2_PIN, C4_PIN, C8_PIN, C16_PIN);

uint32_t freq = 100000; // Frequency in kHz
uint8_t power = 3; // 0 is min output power, 3 is max power output
uint8_t atten = 31;
bool is_rf_enabled = 1; // 0 is disabled, 1 is enabled

void setup() {
  Serial.begin(SERIAL_BAUD); // First we initialize serial communication

  // ERROR LED INDICATOR
  pinMode(ERROR_LED, OUTPUT);  // Setup ERROR LED as output pin
  digitalWrite(ERROR_LED, HIGH); // Write ERROR LED high while initializing


  // RUN LED INDICATOR
  pinMode(RUN_LED, OUTPUT);  // Setup ERROR LED as output pin
  digitalWrite(ERROR_LED, LOW); // Write ERROR LED high while initializing

  // TX AMP
  pinMode(TX_AMP_ENABLE, OUTPUT);
  digitalWrite(TX_AMP_ENABLE, LOW);

  // RX AMP
  pinMode(TX_AMP_ENABLE, OUTPUT);
  digitalWrite(TX_AMP_ENABLE, LOW);

  // OSCILLATOR ENABLE
  pinMode(XO_ENABLE, OUTPUT);
  digitalWrite(XO_ENABLE, HIGH); // By default this is on

  // Lock Detect
  pinMode(LD, INPUT);


  // Initialize ADF4351
  adf.begin();
  adf.setFrequency(freq); // Initialize Frequency
  adf.setPower(power); // Initialize Power
  adf.rfEnable(is_rf_enabled); // Initialize Output ON
  adf.writeAllRegisters(); // write all registers

  // Initialize DAT-31A
  dat.begin();
  dat.writeAtten(atten);

  // Initialize ADC

  // Initialize PHASE

  digitalWrite(ERROR_LED, LOW); // Last step is to write ERROR_LED LOW
}

void loop()
{
  unsigned long run_led_last_updated = 0; // time RUN LED as last updated
  unsigned long current_time;

  current_time = millis(); // time at start of loop

  if ((current_time - run_led_last_updated) > 1000) {
    digitalWrite(RUN_LED, !digitalRead(RUN_LED)); // toggle RUN LED to indicate processor running
    run_led_last_updated = current_time; // Update time
  }

  serialLoop();
}