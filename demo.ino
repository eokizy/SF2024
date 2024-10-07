#include <OneWire.h>
#include <RTClib.h>
#include <DHT.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

//센서 핀 번호
#define DHTPIN_in 2
#define DHTPIN_ex 3
#define CDS 2
#define DS18B20 5

//센서 초기 설정
OneWire ds(DS18B20);
#define DHTTYPE DHT22

//장치 핀 번호
int SUN = 22;

//장치 초기 설정
bool SUNSTATE = true;

DHT dht_in(DHTPIN_in, DHTTYPE);
DHT dht_ex(DHTPIN_ex, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);
RTC_DS3231 rtc;

void setup() {
  Serial.begin(9600);

  lcd.init();
  lcd.backlight();

  dht_in.begin();
  dht_ex.begin();

  rtc.begin();
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));

  pinMode(SUN, OUTPUT);
  digitalWrite(SUN, SUNSTATE);
}

void loop() {

  static DateTime previousTime = rtc.now();

  DateTime now = rtc.now();

  if (now.second() != previousTime.second()) {
    previousTime = now;

    float temp_in = dht_in.readTemperature();
    float humi_in = dht_in.readHumidity();
    float temp_ex = dht_ex.readTemperature();
    float humi_ex = dht_ex.readHumidity();

    Serial.print(now.year(), DEC);
    Serial.print(",");
    Serial.print(now.month(), DEC);
    Serial.print(",");
    Serial.print(now.day(), DEC);
    Serial.print(",");
    Serial.print(now.hour(), DEC);
    Serial.print(",");
    Serial.print(now.minute(), DEC);
    Serial.print(",");
    Serial.print(now.second(), DEC);
    Serial.print(",");
    Serial.print(temp_in);
    Serial.print(",");
    Serial.print(humi_in);
    Serial.print(",");
    Serial.print(temp_ex);
    Serial.print(",");
    Serial.print(humi_ex);
    Serial.print(",");
    Serial.print(analogRead(CDS));
    Serial.print("\n");

    if (now.second() % 5 == 0) {
    SUNSTATE = !SUNSTATE; // LED 상태 변경
    digitalWrite(SUN, SUNSTATE);
    }
    //lcd
    lcd.setCursor(0, 0);
    lcd.print(temp_in);
    lcd.setCursor(0, 1);
    lcd.print(humi_in);
    lcd.clear();
  }
  if (digitalRead(switch) == HIGH) {
    if (temp_in >= 18) {
      digitalWrite(CC = HIGH);
      Serial.print(1);
      } else {
        digitalWrite(CC = LOW);
      }
    } else {
      digitalWrite(CC = LOW);
    }
}
