#include "Particle.h"

namespace {
constexpr pin_t GREEN_LED = D2;
constexpr pin_t YELLOW_LED = D5;
constexpr pin_t RED_LED = D3;

void setOutputs(bool red, bool yellow, bool green) {
    digitalWrite(RED_LED, red ? HIGH : LOW);
    digitalWrite(YELLOW_LED, yellow ? HIGH : LOW);
    digitalWrite(GREEN_LED, green ? HIGH : LOW);
}

int setLed(String value) {
    value.toLowerCase();

    if (value == "green") {
        setOutputs(false, false, true);
    } else if (value == "yellow") {
        setOutputs(false, true, false);
    } else if (value == "red") {
        setOutputs(true, false, false);
    } else if (value == "off") {
        setOutputs(false, false, false);
    } else {
        return -1;
    }
    return 1;
}
}  // namespace

void setup() {
    pinMode(GREEN_LED, OUTPUT);
    pinMode(YELLOW_LED, OUTPUT);
    pinMode(RED_LED, OUTPUT);
    setOutputs(false, false, false);
    Particle.function("set_led", setLed);
}

void loop() {
}
