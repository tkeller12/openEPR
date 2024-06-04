#include <Arduino.h>
#include <SPI.h>
#include "serial.h"
#include "main.h"

#define SERIAL_BAUD 115200 // Serial baud rate

#define ADF_LE PIN_PC0 // ADF4351 Load Enable Pin for SPI communication

// #define TX_AMP_ENABLE PIN_PB5 // Digital pin to enable TX Amplifier
// #define RX_AMP_ENABLE PIN_PC5 // Digital pin to enable RX Amplifier

#define TX_ATTEN_LE PIN_PC1 // TX Digital Attenuator load enable pin
#define TX_PHASE_LE PIN_PC2 // TX Phase Shifter load enable pin

#define ADC_CS PIN_PC3 // ADS1118 ~CS pin

#define XO_ENABLE PIN_PC6 // 10 MHz oscillator on board enable pin

#define RUN_LED PIN_PE1 // Processor RUN LED indicator
#define ERROR_LED PIN_PE2 // ERROR Led

#define RUN_LED_MS_DELAY 500


// TX ATTEN CONTROL PINS
#define C1_PIN PIN_PB0
#define C2_PIN PIN_PB1
#define C4_PIN PIN_PB2
#define C8_PIN PIN_PB3
#define C16_PIN PIN_PB4


ADF4351 adf(ADF_LE);
DAT31A dat(TX_ATTEN_LE, C1_PIN, C2_PIN, C4_PIN, C8_PIN, C16_PIN);
ADS1118 adc(ADC_CS);
PE44820 ps(TX_PHASE_LE);

//uint32_t freq = 1000000; // Frequency in kHz
uint32_t freq = 200000; // Frequency in kHz
//uint32_t freq = 347500; // Frequency in kHz
uint8_t power = 3; // 0 is min output power, 3 is max power output
uint8_t atten = 31;
uint8_t phase = 0;
bool is_rf_enabled = 1; // 0 is disabled, 1 is enabled
bool is_tx_amp_enabled = 0; // 0 is disabled, 1 is enabled
bool is_rx_amp_enabled = 0; // 0 is disabled, 1 is enabled
float adc_reading = 0;

unsigned long run_led_last_updated = 0; // time RUN LED as last updated

void setup() {
  Serial.begin(SERIAL_BAUD); // First we initialize serial communication

  // ERROR LED INDICATOR
  pinMode(ERROR_LED, OUTPUT);  // Setup ERROR LED as output pin
  digitalWrite(ERROR_LED, HIGH); // Write ERROR LED high while initializing

  // RUN LED INDICATOR
  pinMode(RUN_LED, OUTPUT);  // Setup ERROR LED as output pin
  digitalWrite(ERROR_LED, LOW); // Write ERROR LED high while initializing

  // TX AMP
  // pinMode(TX_AMP_ENABLE, OUTPUT); // Don't do this, it causes an issue with SPI communication...
  PORTB_DIR |= 0b100000; // SET PIN_B5 to output
  digitalWrite(TX_AMP_ENABLE, is_tx_amp_enabled);

  // RX AMP
  pinMode(RX_AMP_ENABLE, OUTPUT);
  digitalWrite(RX_AMP_ENABLE, is_tx_amp_enabled);

  // OSCILLATOR ENABLE
  pinMode(XO_ENABLE, OUTPUT);
  digitalWrite(XO_ENABLE, HIGH); // By default this is on

  // Lock Detect
  pinMode(LD, INPUT);

  // Initialize ADF4351
  adf.begin();
  adf.setFrequency(freq); // Initialize Frequency
  adf.setPower(power); // Initialize Power
  adf.setPower(power, 1); // Initialize Power
  adf.rfEnable(is_rf_enabled); // Initialize Output ON
  adf.rfEnable(is_rf_enabled, 1); // Initialize Output ON
  adf.writeAllRegisters(); // write all registers

  // Now we go through Procedure
  delay(10); // Allow ADF to lock
  //adf.REG1.bits.PHASE_ADJUST = 0; 
  //adf.writeAllRegisters(); // write all registers
  delay(10); // Allow ADF to lock

  //adf.writeRegister(0x580005);
  //adf.writeRegister(0x3500FC);


  // Initialize DAT-31A
  dat.begin();
  dat.writeAtten(atten);

  // Initialize PHASE
  ps.begin();
  ps.setPhase(0);

  // Initialize ADC
  adc.begin();
  adc.setSamplingRate(adc.RATE_860SPS);
  adc.setInputSelected(adc.DIFF_0_1);
  adc.setFullScaleRange(adc.FSR_4096);
  adc.setContinuousMode();
  adc_reading = adc.getMilliVolts();

  digitalWrite(ERROR_LED, LOW); // Last step is to write ERROR_LED LOW
}

void loop()
{
  unsigned long current_time;
  static uint16_t phase_ix; // for testing

  current_time = millis(); // time at start of loop

  if ((current_time - run_led_last_updated) > RUN_LED_MS_DELAY) {
    digitalWrite(RUN_LED, !digitalRead(RUN_LED)); // toggle RUN LED to indicate processor running
    run_led_last_updated = current_time; // Update time
  }

  serialLoop();

  phase_ix += 100;
  if (phase_ix > 1000) {
    phase_ix = 0;
  }
  adf.phase(phase_ix);
  //adf.phase(10);
  adf.writeRegister(adf.REG1.word);
  adf.writeRegister(adf.REG0.word);
  //adf.writeAllRegisters();
  delay(1000); // delay ms
}