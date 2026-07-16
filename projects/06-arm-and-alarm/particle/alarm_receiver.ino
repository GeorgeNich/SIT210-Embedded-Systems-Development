#include "Particle.h"

namespace {
constexpr pin_t STATUS_LED = D7;
constexpr unsigned long BLINK_ON_MS = 500;
constexpr unsigned long BLINK_OFF_MS = 500;
constexpr int BLINK_COUNT = 4;

bool alarmPatternActive = false;
int completedBlinks = 0;
bool ledOn = false;
unsigned long nextTransitionMs = 0;

int handleAlarm(String value) {
    value.toLowerCase();
    if (value != "alert") {
        return -1;
    }

    Particle.publish("alarm/triggered", "proximity threshold crossed", PRIVATE);
    alarmPatternActive = true;
    completedBlinks = 0;
    ledOn = true;
    digitalWrite(STATUS_LED, HIGH);
    nextTransitionMs = millis() + BLINK_ON_MS;
    return 1;
}

void updateAlarmPattern() {
    if (!alarmPatternActive || millis() < nextTransitionMs) {
        return;
    }

    ledOn = !ledOn;
    digitalWrite(STATUS_LED, ledOn ? HIGH : LOW);

    if (ledOn) {
        nextTransitionMs = millis() + BLINK_ON_MS;
    } else {
        ++completedBlinks;
        if (completedBlinks >= BLINK_COUNT) {
            alarmPatternActive = false;
            digitalWrite(STATUS_LED, LOW);
        } else {
            nextTransitionMs = millis() + BLINK_OFF_MS;
        }
    }
}
}  // namespace

void setup() {
    pinMode(STATUS_LED, OUTPUT);
    digitalWrite(STATUS_LED, LOW);
    Particle.function("alarm", handleAlarm);
}

void loop() {
    updateAlarmPattern();
}
