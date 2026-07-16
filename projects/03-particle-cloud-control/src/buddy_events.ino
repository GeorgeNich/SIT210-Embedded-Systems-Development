#include "Particle.h"

namespace {
constexpr pin_t WAVE_LED = D2;
constexpr pin_t PAT_LED = D5;
constexpr unsigned long WAVE_MS = 300;
constexpr unsigned long PAT_MS = 1000;
constexpr char EVENT_NAME[] = "Deakin_RIOT_SIT210_Photon_Buddy";

void blink(pin_t pin, int repetitions, unsigned long intervalMs) {
    for (int i = 0; i < repetitions; ++i) {
        digitalWrite(pin, HIGH);
        delay(intervalMs);
        digitalWrite(pin, LOW);
        delay(intervalMs);
    }
}

void handleBuddyEvent(const char* event, const char* data) {
    if (data == nullptr) {
        return;
    }

    if (strcmp(data, "wave") == 0) {
        blink(WAVE_LED, 3, WAVE_MS);
    } else if (strcmp(data, "pat") == 0) {
        blink(PAT_LED, 10, PAT_MS);
    }
}
}  // namespace

void setup() {
    pinMode(WAVE_LED, OUTPUT);
    pinMode(PAT_LED, OUTPUT);
    Particle.subscribe(EVENT_NAME, handleBuddyEvent);
}

void loop() {
}
