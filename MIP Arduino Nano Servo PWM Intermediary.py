// Receives pulse width (in microseconds) from Raspberry Pi via UART (D0/RX)
// Outputs servo PWM signal on D9
// Baud: 9600. Send commands like "1500\n" (500–2500 us)
// Anthropic Claude Opus 4.6 was utilized for the purposes of code generation, debugging, and optimization.

#include <Servo.h>

Servo servo;
const int SERVO_PIN = 9;
String inputBuffer = "";

void setup() {
  Serial.begin(9600);
  servo.attach(SERVO_PIN);
  servo.writeMicroseconds(1500); // neutral on startup
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      inputBuffer.trim();
      if (inputBuffer.length() > 0) {
        int pulseWidth = inputBuffer.toInt();
        if (pulseWidth >= 500 && pulseWidth <= 2500) {
          servo.writeMicroseconds(pulseWidth);
          Serial.print("OK:");
          Serial.println(pulseWidth);
        } else {
          Serial.println("ERR:out_of_range");
        }
      }
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }
}
