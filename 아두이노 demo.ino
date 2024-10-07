/*연암대 스마트팜 프로젝트 데모 코드입니다
코드 수정시 날짜와 수정내용을 함께 적어주세요!!!!*/

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

  if (now.second() != previousTime.second()) { //1초를 주기로 동작
    previousTime = now;

    float temp_in = dht_in.readTemperature();
    float humi_in = dht_in.readHumidity();
    float temp_ex = dht_ex.readTemperature();
    float humi_ex = dht_ex.readHumidity();
    
    //파이썬 시리얼 데이터
    Serial.print(now.year(), DEC); //0번 '년'
    Serial.print(",");
    //데이터 split을 콤마(,)로 구분하니까 Serial.print(",'); 를 꼭 써주세요 20204,10,7,18.5,60.0,20.5,60.0......
    Serial.print(now.month(), DEC); //1번 '월'
    Serial.print(",");
    Serial.print(now.day(), DEC); //2번 '일'
    Serial.print(",");
    Serial.print(now.hour(), DEC); //3번 '시'
    Serial.print(",");
    Serial.print(now.minute(), DEC); //4번 '분'
    Serial.print(",");
    Serial.print(now.second(), DEC); //5번 '초'
    Serial.print(",");
    Serial.print(temp_in); //6번 '내부 온도'
    Serial.print(",");
    Serial.print(humi_in); //7번 '내부 습도'
    Serial.print(",");
    Serial.print(temp_ex); //8번 '외부 온도'
    Serial.print(",");
    Serial.print(humi_ex); //9번 외부 습도'
    Serial.print(",");
    Serial.print(analogRead(CDS)); //10번 '조도센서 값'
    Serial.print("\n"); //줄바꿈
    
    //LED 토글
    if (now.second() % 5 == 0) { //2024-10-7 5초로 설정되어있습니다.
    SUNSTATE = !SUNSTATE;
    digitalWrite(SUN, SUNSTATE);
    }
    //lcd 화면 표시
    lcd.setCursor(0, 0); //2024-10-7 내부 온습도만 출력됩니다.
    lcd.print(temp_in);
    lcd.setCursor(0, 1);
    lcd.print(humi_in);
    lcd.clear();
  }
  /* 20204-10-7 CC는 쇼케이스 냉방기의 예명으로 가코드만 작성된 형태입니다 기능X
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
  */
}
