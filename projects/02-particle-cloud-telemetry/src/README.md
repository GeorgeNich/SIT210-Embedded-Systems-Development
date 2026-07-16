# Particle Cloud Telemetry Source

## Files

| File | Description |
|---|---|
| [`dht_temperature_webhook.ino`](dht_temperature_webhook.ino) | Reads DHT11 temperature and publishes a private `temperature_c` event |
| [`light_exposure_ifttt.ino`](light_exposure_ifttt.ino) | Reads a photoresistor and publishes bright/dark state changes |

## Configuration Points

### DHT example

```cpp
constexpr pin_t DHT_PIN = D5;
constexpr int DHT_TYPE = DHT11;
constexpr unsigned long SAMPLE_INTERVAL_MS = 15000;
```

The source requires the `Adafruit_DHT_Particle` library.

### Light example

```cpp
constexpr pin_t PHOTORESISTOR_PIN = A4;
constexpr pin_t LED_PIN = D7;
constexpr int LIGHT_THRESHOLD = 50;
```

`LIGHT_THRESHOLD` is installation-specific and should be calibrated using observed readings.

## Cloud Setup

The source publishes private events. Webhook or IFTTT configuration belongs in the Particle Console and external service dashboards rather than in committed source code.
