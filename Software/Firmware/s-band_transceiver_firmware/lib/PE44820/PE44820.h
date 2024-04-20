#ifndef _PE44820_h
#define _PE44820_h

#include <Arduino.h>
#include <SPI.h>

union REGISTER{
    struct {
        uint8_t ADDR : 4;
        bool OPT : 1;
        uint8_t PHASE : 8;
        uint8_t DONTCARE : 3;
    } bits;
    struct {
        uint8_t BYTE0;
        uint8_t BYTE1;

    } bytes;
    uint16_t word;
};

class PE44820 {
    public:
        void begin();
        void writeRegister();
        void setPhase(uint8_t phase);
        PE44820(uint8_t LE);

        REGISTER REG;

        uint8_t CS;
        const uint32_t SCLK       = 2000000;///< SPI SCLK frequency
};

#endif