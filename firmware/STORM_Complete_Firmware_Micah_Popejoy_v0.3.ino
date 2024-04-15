#include <Servo.h>

//define motor 1 (LEFT) related pins
#define IN1 10
#define IN2 9
#define ENA 11

//define motor 2 (RIGHT) related pins
#define IN3 8
#define IN4 7
#define ENB 6

// Define the encoder pins
#define ENCA 4 // White
#define ENCB 5 // Yellow

// Define Servo Pins
#define turret 1
#define height 2

// Define magnet pin
#define magnet 0

/* Stick values for controlling the motors and servos. ML_ST controls the left motor and turret servo,
   MR_SH controls the right motor and height servo */
float ML_SH = 0;
float MR_ST = 0;

/* Boolean value that determines if we are controlling the servos or the motors */
int controlState;

/* Direction is determined by the sign of the pwr values in loop() */
int dirL;
int dirR;

/* Holds the Serial data received from Pi */
char buffer[9];

/* SERVO GLOBAL VARS */

// Servo Objects
Servo turretServo;
Servo heightServo;

// Servo Position Vars
int turretPosition = 90;
int heightPosition = 150;
// int pastYPosition = turretPosition;
// int pastXPosition = heightPosition;


void setup() {
  pinMode(magnet, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  turretServo.attach(1);
  heightServo.attach(2);
  turretServo.write(turretPosition);
  heightServo.write(heightPosition);
  Serial.begin(115200);
}

void loop() {
  //Serial.print("Data: ");
  /*
  Serial.println(buffer[0]);
  Serial.print(buffer[1]);
  Serial.print(buffer[2]);
  Serial.print(buffer[3]);
  Serial.print(buffer[4]);
  Serial.print(buffer[5]);
  Serial.print(buffer[6]);
  Serial.print(buffer[7]);
  Serial.print(buffer[8]);
  Serial.print(buffer[9]);
  */
  
  
  if (Serial.available() >= 9) {
    
    Serial.readBytes(buffer, 9);
    // Copy buffer data into the controlMoters and the Stick values
    memcpy(&controlState, &buffer[0], sizeof(char));
    memcpy(&ML_SH, &buffer[5], sizeof(float));
    memcpy(&MR_ST, &buffer[1], sizeof(float));
    
    if (controlState == 0) {
      /* MOTOR CODE */
      // Determine direction from power values
      if (ML_SH > 0) {
        dirL = 1;
      }
      else if (ML_SH < 0) {
        dirL = -1;
      }
      if (MR_ST > 0) {
        dirR = 1;
      }
      else if (MR_ST < 0) {
        dirR = -1;
      }

      // Set left motor
      setMotor(dirL, (int)fabs(ML_SH), ENA, IN1, IN2);
      // Serial.println(fabs(ML_SH));
      // Set right motor
      setMotor(dirR, (int)fabs(MR_ST), ENB, IN3, IN4);
    }
    else if (controlState == 1) {
      /* SERVO CODE */
      MR_ST = map((int)MR_ST, -255, 255, -1000, 1000);
      ML_SH = map((int)ML_SH, -255, 255, -1000, 1000);
      
      double heightPosIncrement = 0.002 * fabs(MR_ST);
      // Calculate Turret (Y) position
      if (MR_ST < 0) {
        if (turretPosition >= 180) {
          turretPosition = 180;
        }
        else {
          turretPosition = turretPosition + (int)heightPosIncrement;
        }
      }
      else if (MR_ST > 0) {
        if (turretPosition <= 0) {
          turretPosition = 0;
        }
        else {
          turretPosition = turretPosition - (int)heightPosIncrement;
        }
      }

      double turretPosIncrement = 0.002 * fabs(ML_SH);
      // Calculate Height (X) position
      if (ML_SH > 0) {
        if (heightPosition >= 180) {
          heightPosition = 180;
        }
        else {
          heightPosition = heightPosition + (int)turretPosIncrement;
        }
      }
      else if (ML_SH < 0) {
        if (heightPosition <= 0) {
          heightPosition = 0;
        }
        else {
          heightPosition = heightPosition - (int)turretPosIncrement;
        }
      }
      
      // Record the current position as the pastPosition
        // pastYPosition = turretPosition;
        // pastXPosition = heightPosition;
      turretServo.write(turretPosition);
      heightServo.write(heightPosition);
    }
    // Set the magnet to high
    else if (controlState == 2) {
      digitalWrite(magnet, HIGH);
    }
    // Set the magnet to low
    else if (controlState == 3) {
      digitalWrite(magnet, LOW);
    }


    // Serial.print("y value = ");
    // Serial.print(MR_ST);
    // Serial.print(", x value = ");
    // Serial.print(ML_SH);
    // Serial.print(", Turret Position = ");
    // Serial.print(turretPosition);
    // Serial.print(", Height position = ");
    // Serial.print(heightPosition);
    // Serial.println();
    
  
  }
}

void setMotor(int dir, int pwmVal, int pwm, int in1, int in2) {
  analogWrite(pwm, pwmVal);
  if (dir == 1) { // set to clockwise
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else if (dir == -1) { // Set to counter-clockwise
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }
  else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }
}