#include "Particle.h"

namespace {
constexpr pin_t PHOTORESISTOR_PIN = A4;
constexpr pin_t LED_PIN = D7;
constexpr int LIGHT_THRESHOLD = 50;  // Calibrate for the actual circuit and room.
constexpr unsigned long SAMPLE_INTERVAL_MS = 2000;
bool previousBright = false;
bool hasPreviousState = false;
}  // namespace

void setup() {
    pinMode(PHOTORESISTOR_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    const int reading = analogRead(PHOTORESISTOR_PIN);
    const bool isBright = reading > LIGHT_THRESHOLD;

    digitalWrite(LED_PIN, isBright ? HIGH : LOW);

    if (!hasPreviousState || isBright != previousBright) {
        const char* eventName = isBright
            ? "light_exposure/high"
            : "light_exposure/low";
        const String data = String::format("reading=%d", reading);
        Particle.publish(eventName, data, PRIVATE);
        previousBright = isBright;
        hasPreviousState = true;
    }

    delay(SAMPLE_INTERVAL_MS);
}
