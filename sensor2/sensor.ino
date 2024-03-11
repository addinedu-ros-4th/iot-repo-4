#include <Adafruit_Fingerprint.h>


#include <LiquidCrystal_I2C.h>

#include <Servo.h>
SoftwareSerial mySerial(2, 3);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);
LiquidCrystal_I2C dis(0x27, 16, 2);
int ID[5] = {1,2,3,4,5}; // Enter your fingerprint ID

Servo myservo; // Create servo object
const int buttonPin = 5; // pin number to which the button is connected
#define TRIG_PIN 11
#define ECHO_PIN 12
unsigned long lastDebounceTime = 0; // Last debounced time
unsigned long debounceDelay = 50; // debounce delay (ms)
int count = 0;
bool objectDetected = false;
bool tcrtDetected = false; // Flag for TCRT5000 detection
const int sensorPin = A0; // Connect the signal junction to analog pin A0
int currentServoPosition = 90; // Variable to track the current servo position

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  dis.init();
  dis.backlight();
  dis.setCursor(0, 0);
  dis.print("Place finger");
  myservo.attach(9); // Set the pin number to control the servo motor
  while (!Serial);  // For Yun/Leo/Micro/Zero/...
  delay(100);
  Serial.println("\n\nAdafruit finger detect test");
  // set the data rate for the sensor serial port
  finger.begin(57600);
  delay(5);
  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  } else {
    Serial.println("Did not find fingerprint sensor :(");
    while (1) {
      delay(1);
    }
  }
  finger.getParameters();
  finger.getTemplateCount();
  if (finger.templateCount == 0) {
    Serial.print("Sensor doesn't contain any fingerprint data. Please run the 'enroll' example.");
  }
  else {
    Serial.println("Waiting for valid finger...");
    Serial.print("Sensor contains "); Serial.print(finger.templateCount); Serial.println(" templates");
  }
}
void loop() {
   int value = getFingerprintIDez();
  for(int i=0;i<5;i++){
    if (value == ID[i]) {
      if (currentServoPosition == 0 ){
      myservo.write(90); // Rotate the servo motor to 90 degrees
      currentServoPosition = 90;
      dis.setCursor(0, 1);
      dis.print("Thank you");
      Serial.println("door is open");
      delay(2000);
      Serial.print("ID:");
      Serial.println(value);
      }
      else if (currentServoPosition == 90){
        myservo.write(0);
        currentServoPosition = 0;
        dis.setCursor(0, 1);
      dis.print("Thank you");
      Serial.println("door is close");
      delay(2000);
      Serial.print("ID:");
      Serial.println(value);
      count=0;
      }
      
    }else {
      dis.setCursor(0, 1);
      dis.print("         ");
      delay(50);
    }
    delay(50);
  }
  int sensorValue = analogRead(sensorPin); // Read the analog value from sensor
  int reading = digitalRead(buttonPin);
  long duration, distance;
  digitalWrite(TRIG_PIN, LOW); // Initialize by setting the trigger pin to LOW
  delayMicroseconds(2); // wait 2 microseconds
  digitalWrite(TRIG_PIN, HIGH); // Send a HIGH signal for 10 microseconds
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  duration = pulseIn(ECHO_PIN, HIGH); // Measure the time the echo pin goes HIGH
  distance = (duration / 2) / 29.1;
  
  
  // When an object within 10cm is detected and it was not already detected
  if (distance < 10 && !objectDetected) {
    count++; // Increase the count just once for each detection
    objectDetected = true; // Mark that an object has been detected
    Serial.print("count:");
    Serial.println(count);
  } else if (distance >= 80) {
    objectDetected = false; // Reset the flag when no object is within the detection range
  }
}


int getFingerprintIDez() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK)  return -1;
  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)  return -1;
  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)  return -1;
  return finger.fingerID;
}
