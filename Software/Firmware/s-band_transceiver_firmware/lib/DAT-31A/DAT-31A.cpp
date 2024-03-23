#include "DAT-31A.h"
#include "Arduino.h"

DAT31A::DAT31A(uint8_t LE_PIN, uint8_t C1_PIN, uint8_t C2_PIN, uint8_t C4_PIN, uint8_t C8_PIN, uint8_t C16_PIN) {
    CS = LE_PIN;
    C1 = C1_PIN;
    C2 = C2_PIN;
    C4 = C4_PIN;
    C8 = C8_PIN;
    C16 = C16_PIN;
}

void DAT31A::begin() {
    pinMode(CS, OUTPUT);
    digitalWrite(CS, LOW); // for latched programming, should be low while changing values

    pinMode(C1, OUTPUT);
    digitalWrite(C1, HIGH);

    pinMode(C2, OUTPUT);
    digitalWrite(C2, HIGH);

    pinMode(C4, OUTPUT);
    digitalWrite(C4, HIGH);

    pinMode(C8, OUTPUT);
    digitalWrite(C8, HIGH);

    pinMode(C16, OUTPUT);
    digitalWrite(C16, HIGH);

    digitalWrite(CS, HIGH); // Pull latch high to latch data
    digitalWrite(CS, LOW); // Pull LE low for new data

}

void DAT31A::writeAtten(uint8_t atten) {

    digitalWrite(CS, LOW); // write latch low for new data

    // Bitwise "and" operations
    digitalWrite(C1, atten & 1); 
    digitalWrite(C2, (atten & 2) >> 1); 
    digitalWrite(C4, (atten & 4) >> 2); 
    digitalWrite(C8, (atten & 8) >> 3); 
    digitalWrite(C16, (atten & 16) >> 4);

    digitalWrite(CS, HIGH); // Latch Data
    digitalWrite(CS, LOW); // Latch Data

}