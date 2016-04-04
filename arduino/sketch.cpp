#include <Smartcar.h>

#define SPEED 200

#define BAUDRATE 115200

#define PROX_TRIGGER_PIN 6
#define PROX_ECHO_PIN 7
SR04 PROX;

#define ENC_LEFT_PIN 2
Odometer ENC_LEFT;

#define ENC_RIGHT_PIN 3
Odometer ENC_RIGHT;

DCMotors MOTORS(STANDARD);

Gyroscope GYRO(10);

void setup() {
  Serial.begin(BAUDRATE);

  ENC_LEFT.attach(ENC_LEFT_PIN);
  ENC_RIGHT.attach(ENC_RIGHT_PIN);
  ENC_LEFT.begin();
  ENC_RIGHT.begin();

  PROX.attach(PROX_TRIGGER_PIN, PROX_ECHO_PIN);

  MOTORS.init();

  GYRO.attach();
  GYRO.begin();
}

float gyro(int samples) {
  float value = 0;
  for (int i = 0; i < samples; i++) {
    value += GYRO.getAngularDisplacement();
    GYRO.update();
    delayMicroseconds(10);
  }
  return value / samples;
}

void turn(int target, int speed) {
  GYRO.calibrate(10);
  
  float zero = gyro(4);
  float value;
  
  MOTORS.setMotorSpeed(speed, -speed);
  
  do {
    value = abs(zero - gyro(4));
  } while (value < target);

  MOTORS.setMotorSpeed(0, 0);
}

void loop() {
  GYRO.update();
  
  if (Serial.available()) {
    char in = Serial.read();
    switch (in) {
      case 'l':
        turn(10, SPEED);
        break;
      case 'r':
        turn(10, -SPEED);
        break;
      case 'f':
        MOTORS.setMotorSpeed(SPEED, SPEED);
        break;
      case 'b':
        MOTORS.setMotorSpeed(-SPEED, -SPEED);
        break;
      case 's':
        MOTORS.setMotorSpeed(0, 0);
        break;
    }
  }
}
