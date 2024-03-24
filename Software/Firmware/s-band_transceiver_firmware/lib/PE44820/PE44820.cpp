#include "PE44820.h"
#include <Arduino.h>

PE44820::PE44820(uint8_t LE) {
    CS = LE;
}

void PE44820::begin() {
    pinMode(CS, OUTPUT);
    digitalWrite(CS, HIGH);
    SPI.begin();
    // NOTE: Confirm Mode is correct
    SPI.beginTransaction(SPISettings(SCLK, MSBFIRST, SPI_MODE0));
}

void PE44820::writeRegister() {
    SPI.setDataMode(SPI_MODE0);
    digitalWrite(CS, LOW);
    SPI.transfer16(REG.word);
    digitalWrite(CS, HIGH);
}

void PE44820::setPhase(uint8_t phase) {
    REG.bits.PHASE = phase;
    writeRegister();
}