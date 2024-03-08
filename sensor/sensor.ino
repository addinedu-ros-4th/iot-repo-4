#include <Servo.h>

Servo myservo; // Create servo object
const int buttonPin = 3; // pin number to which the button is connected
int buttonState; // current button state
int lastButtonState = LOW; // Last button state (initial value is LOW)
#define TRIG_PIN 11
#define ECHO_PIN 12
unsigned long lastDebounceTime = 0; // Last debounced time
unsigned long debounceDelay = 50; // debounce delay (ms)
int count = 0;
bool objectDetected = false;
bool tcrtDetected = false; // Flag for TCRT5000 detection
const int sensorPin = A0; // Connect the signal junction to analog pin A0
int currentServoPosition = 0; // Variable to track the current servo position

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  myservo.attach(9); // Set the pin number to control the servo motor
}

void loop() {
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

  // If the button state is different from the last read state, reset the debounce timer.
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
      // If the button is pressed and the servo is at 0 degrees
      if (currentServoPosition == 90 && buttonState == HIGH) {
        myservo.write(0); // Rotate the servo motor to 90 degrees
        currentServoPosition = 0; // Update the servo position variable
        Serial.println("door is open."); // Since we're closing the door at 90 degrees
        count = 0;
      }
    }
  }

  if (currentServoPosition == 0 &&sensorValue <= 980 && !tcrtDetected) {
    myservo.write(90); // Rotate the servo motor to 0 degrees once per TCRT5000 detection
    currentServoPosition = 90; // Update the servo position variable
    Serial.println("door is close."); // Now opening the door at 0 degrees
    tcrtDetected = true;
  } else if (sensorValue > 980) {
    tcrtDetected = false; // Reset the TCRT5000 detection flag
  }
  
  // When an object within 10cm is detected and it was not already detected
  if (distance < 10 && !objectDetected) {
    count++; // Increase the count just once for each detection
    objectDetected = true; // Mark that an object has been detected
    Serial.print("count:");
    Serial.println(count);
  } else if (distance >= 80) {
    objectDetected = false; // Reset the flag when no object is within the detection range
  }

  // Update the current read state to the last state.
  lastButtonState = reading;
}
