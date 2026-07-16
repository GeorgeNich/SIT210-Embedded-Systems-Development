#include "Particle.h"

namespace {
constexpr pin_t LED_PIN = D7;
constexpr unsigned long UNIT_MS = 250;
constexpr const char* MESSAGE = "GEORGE";

const char* morseFor(char value) {
    switch (tolower(value)) {
        case 'a': return ".-";   case 'b': return "-...";
        case 'c': return "-.-."; case 'd': return "-..";
        case 'e': return ".";    case 'f': return "..-.";
        case 'g': return "--.";  case 'h': return "....";
        case 'i': return "..";   case 'j': return ".---";
        case 'k': return "-.-";  case 'l': return ".-..";
        case 'm': return "--";   case 'n': return "-.";
        case 'o': return "---";  case 'p': return ".--.";
        case 'q': return "--.-"; case 'r': return ".-.";
        case 's': return "...";  case 't': return "-";
        case 'u': return "..-";  case 'v': return "...-";
        case 'w': return ".--";  case 'x': return "-..-";
        case 'y': return "-.--"; case 'z': return "--..";
        default: return nullptr;
    }
}

void setLed(bool on, unsigned long durationMs) {
    digitalWrite(LED_PIN, on ? HIGH : LOW);
    delay(durationMs);
}

void signalSymbol(char symbol) {
    const unsigned long onTime = symbol == '-' ? 3 * UNIT_MS : UNIT_MS;
    setLed(true, onTime);
    setLed(false, UNIT_MS);  // Space between parts of one letter.
}

void signalCharacter(char value) {
    const char* code = morseFor(value);
    if (code == nullptr) {
        delay(7 * UNIT_MS);
        return;
    }

    for (const char* symbol = code; *symbol != '\0'; ++symbol) {
        signalSymbol(*symbol);
    }
    delay(2 * UNIT_MS);  // Existing one-unit gap + two units = letter gap.
}

void signalMessage(const char* message) {
    for (const char* value = message; *value != '\0'; ++value) {
        if (*value == ' ') {
            delay(4 * UNIT_MS);  // Completes a seven-unit word gap.
        } else {
            signalCharacter(*value);
        }
    }
}
}  // namespace

void setup() {
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    signalMessage(MESSAGE);
    delay(7 * UNIT_MS);
}
