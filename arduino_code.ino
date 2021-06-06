#include <LiquidCrystal_I2C.h>



#include <DHT.h>

#include <Wire.h> // Library for I2C communication
#include <LiquidCrystal_I2C.h> // Library for LCD

//Constants
#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
#define HALL_SENSOR      3
#define LED      13
DHT dht(DHTPIN, DHTTYPE); // Initialize DHT sensor for normal 16mhz Arduino

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 20, 4);

//Variables
float hum;  //Stores humidity value
float temp; //Stores temperature value

void setup()
{
  pinMode(LED, OUTPUT);
  pinMode(HALL_SENSOR, INPUT);
  digitalWrite(LED, LOW);
    Serial.begin(9600);
    lcd.init();
  lcd.backlight();
    dht.begin();
}

void loop()
{
    //Read data and store it to variables hum and temp
    hum = dht.readHumidity();
    temp= dht.readTemperature();
     digitalWrite(LED, !digitalRead(HALL_SENSOR));
    
    //Print temp and humidity values to serial monitor
    lcd.setCursor(0, 0); 
    lcd.print("Temp:");
    lcd.print(temp);
    Serial.print(String(temp));
    Serial.print(", ");
    Serial.print(String(hum));
    Serial.print(",");
    Serial.print(String(digitalRead(HALL_SENSOR)));
    Serial.println(",");
    delay(2000); //Delay 2 sec.
}
