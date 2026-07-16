#include "Particle.h"
#include "Adafruit_DHT_Particle.h"

namespace {
constexpr pin_t DHT_PIN = D5;
constexpr int DHT_TYPE = DHT11;
constexpr unsigned long SAMPLE_INTERVAL_MS = 15000;
DHT dht(DHT_PIN, DHT_TYPE);
}  // namespace

void setup() {
    Serial.begin(9600);
    dht.begin();
    Particle.publish("telemetry/status", "DHT11 started", PRIVATE);
    delay(2000);
}

void loop() {
    const float temperatureC = dht.getTempCelcius();

    if (isnan(temperatureC)) {
        Serial.println("DHT11 read failed");
        delay(SAMPLE_INTERVAL_MS);
        return;
    }

    Serial.printf("Temperature: %.1f C\n", temperatureC);
    Particle.publish("temperature_c", String::format("%.1f", temperatureC), PRIVATE);
    delay(SAMPLE_INTERVAL_MS);
}
