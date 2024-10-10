/*연암대 스마트팜 프로젝트 master 코드입니다*/

//라이브러리 필요한 것만 추가해주세요
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
#define SUN 22 //LED
#define SC 23 //Show Case
#define SOLENOID 24 //CO2 SOLENOID
#define PUMP 25 //WATER(NT) PUMP

//토글 값
int SUN_toggle_value;
int SC_toggle_value;
int SOLENOID_toggle_value;
int PUMP_toggle_value;

//토글 핀 설정
#define SUN_toggle_pin 30
#define SC_toggle_pin 31
#define SOLENOID_toggle_pin 32
#define PUMP_toggle_pin 33

//장치 초기 설정
bool SUNSTATE = true;
bool SCSTATE = true;

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

  pinMode(SC, OUTPUT);
  digitalWrite(SC, SCSTATE);

  pinMode(SUN_toggle_pin, INPUT);
  pinMode(SC_toggle_pin, INPUT);
  pinMode(SOLENOID_toggle_pin, INPUT);
  pinMode(PUMP_toggle_pin, INPUT);
}

void loop() {
  //토글 스위치
  SUN_toggle_value = digitalRead(SUN_toggle_pin);
  SC_toggle_value = digitalRead(SC_toggle_pin);
  SOLENOID_toggle_value = digitalRead(SOLENOID_toggle_pin);
  PUMP_toggle_value = digitalRead(PUMP_toggle_pin);

  //온습도 센서읽기
  float temp_in = dht_in.readTemperature();
  float humi_in = dht_in.readHumidity();
  float temp_ex = dht_ex.readTemperature();
  float humi_ex = dht_ex.readHumidity();

  static DateTime previousTime = rtc.now();

  DateTime now = rtc.now();

  if (now.second() != previousTime.second()) {
    previousTime = now;

    Serial.print(now.year(), DEC); //0 년
    Serial.print(",");
    Serial.print(now.month(), DEC); //1 월
    Serial.print(",");
    Serial.print(now.day(), DEC); ///2 일
    Serial.print(",");
    Serial.print(now.hour(), DEC); //3 시
    Serial.print(",");
    Serial.print(now.minute(), DEC); //4 분
    Serial.print(",");
    Serial.print(now.second(), DEC); //5 초
    Serial.print(",");
    Serial.print(temp_in); //6 내부 온도
    Serial.print(",");
    Serial.print(humi_in); //7 내부 습도
    Serial.print(",");
    Serial.print(temp_ex); //8 외부 온도
    Serial.print(",");
    Serial.print(humi_ex); //9 외부 습도
    Serial.print(",");
    /*
    Serial.print(analogRead(CDS));
    Serial.print("\n");
    */

    //LED 점멸
    if (SUN_toggle_value == HIGH) {
      if (now.second() % 5 == 0) {
        SUNSTATE = !SUNSTATE; // LED 상태 변경
        digitalWrite(SUN, SUNSTATE);
      }
    } else {
      SUNSTATE = LOW;
      digitalWrite(SUN, SUNSTATE);
    }

    //액정 표시
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(temp_in);
    lcd.setCursor(0, 1);
    lcd.print(humi_in);
  }
  //쇼케이스 냉방기 작동
  if (digitalRead(SC_toggle_value) == HIGH) {
    if (temp_in >= 18) {
      digitalWrite(SC, HIGH);
    } else {
        digitalWrite(SC, LOW);
    }
  } else {
    digitalWrite(SC, LOW);
  }
}
