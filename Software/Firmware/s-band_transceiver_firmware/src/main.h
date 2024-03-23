#include <Arduino.h>
#include <SPI.h>
#include "adf4351.h"
#include "DAT-31A.h"
#include "serial.h"

#ifndef main_h
#define main_h

extern ADF4351 adf;
extern DAT31A dat;
extern uint32_t freq; // Frequency in kHz
extern uint8_t power; // Power, 0 to 3, 0 is min, 3 is max
extern uint8_t atten; // TX atten, 0 to 31
extern bool is_rf_enabled; // 0 is disabled, 1 is enabled

#endif