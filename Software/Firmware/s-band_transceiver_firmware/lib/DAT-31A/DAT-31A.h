#ifndef _DAT_31A_h
#define _DAT_31A_h

#include <Arduino.h>

class DAT31A {
    public:
        uint8_t CS;
        uint8_t C1;
        uint8_t C2;
        uint8_t C4;
        uint8_t C8;
        uint8_t C16;
        void begin();
        void writeAtten(uint8_t atten);
        DAT31A(uint8_t LE_PIN, uint8_t C1_PIN, uint8_t C2_PIN, uint8_t C4_PIN, uint8_t C8_PIN, uint8_t C16_PIN); // constructor
};

#endif
