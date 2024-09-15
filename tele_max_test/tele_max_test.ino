



#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
//#include <DHT.h>

// Replace with your network credentials
const char* ssid = "vivo 1935";
const char* password = "Greeshma5";

// Initialize Telegram BOT
#define BOTtoken "6408474114:AAHYuxxTXZH3wKG1uuGntyVd0qaJfT5eiv4" // your Bot Token
#define CHAT_ID "1828030153" // Replace with your chat ID

//// DHT11 sensor pin
//#define DHTPIN D4
//#define DHTTYPE DHT11

//// Initialize the DHT sensor
//DHT dht(DHTPIN, DHTTYPE);

X509List cert(TELEGRAM_CERTIFICATE_ROOT);
WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);

MAX30105 particleSensor;

const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;

float beatsPerMinute;
int beatAvg;

void setup() {
  Serial.begin(115200);
  Serial.println("Initializing...");

  configTime(0, 0, "pool.ntp.org");

  client.setTrustAnchors(&cert);

  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  bot.sendMessage(CHAT_ID, "Bot started up", "");

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }
  Serial.println("Place your index finger on the sensor with steady pressure.");
  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeGreen(0);

//  // Initialize DHT sensor
//  dht.begin();
}

void loop() {
//  // Read LM35 temperature
//  float temperature = dht.readTemperature();
//  float humidity = dht.readHumidity();

  // Read MAX30105 IR value
  long irValue = particleSensor.getIR();

  if (checkForBeat(irValue) == true) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    beatsPerMinute = 60 / (delta / 1000.0);

    if (beatsPerMinute < 255 && beatsPerMinute > 20) {
      rates[rateSpot++] = (byte)beatsPerMinute;
      rateSpot %= RATE_SIZE;

      beatAvg = 0;
      for (byte x = 0; x < RATE_SIZE; x++) {
        beatAvg += rates[x];
      }
      beatAvg /= RATE_SIZE;
    }
  }

  // Print data to serial monitor
//  Serial.print("Temperature: ");
//  Serial.print(temperature);
//  Serial.print(" °C, Humidity: ");
//  Serial.print(humidity);
  Serial.print(". IR Value: ");
  Serial.print(irValue);
  Serial.print(", BPM: ");
  Serial.print(beatsPerMinute);
  Serial.print(", Avg BPM: ");
  Serial.print(beatAvg);

  if (irValue < 50000) {
    Serial.print(" No finger?");
  }

  if (beatAvg > 75 && irValue > 50000) {
    bot.sendMessage(CHAT_ID, "High BPM!", "");
//    break;
  }

//  for (int i =0; i< 100; i++){
//    if (beatAvg > 80){
//      bot.sendMessage(CHAT_ID, "High BPM!", "");
//      break;
//    }
//  }
//
  if (beatAvg > 80 && irValue > 50000 ) {
    bot.sendMessage(CHAT_ID, "person has fallen!", "");
    delay(100);
  }

  Serial.println();

  //delay(100);
}
