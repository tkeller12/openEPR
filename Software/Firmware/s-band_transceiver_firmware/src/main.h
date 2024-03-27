#include <Arduino.h>
#include <SPI.h>
#include "adf4351.h"
#include "DAT-31A.h"
#include "ADS1118.h"
#include "PE44820.h"
#include "serial.h"

#ifndef main_h
#define main_h

#define TX_AMP_ENABLE PIN_PB5 // Digital pin to enable TX Amplifier
#define RX_AMP_ENABLE PIN_PC5 // Digital pin to enable RX Amplifier

extern ADF4351 adf;
extern DAT31A dat;
extern ADS1118 adc;
extern PE44820 ps;
extern uint32_t freq; // Frequency in kHz
extern uint8_t power; // Power, 0 to 3, 0 is min, 3 is max
extern uint8_t atten; // TX atten, 0 to 31
extern uint8_t phase; // TX phase 0 to 255
extern bool is_rf_enabled; // 0 is disabled, 1 is enabled
extern bool is_tx_amp_enabled;
extern bool is_rx_amp_enabled;


#endif