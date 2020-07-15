#include <AFMotor.h>
#include <Servo.h>

#define DOWN  150
#define CENTER 85
#define UP      5

#define SHIFT  5
#define CTRL   150
// RG YB
AF_Stepper top_stepper(200, 2);
AF_Stepper left_stepper(200, 1);

Servo head;
Servo tail;
 
int top_step;
int left_step;
 
int past_top_step;
int past_left_step;
 
void setup() {
  Serial.begin(9600);
  
  head.attach(9);
  tail.attach(10);
  
  head.write(85);
  tail.write(85);
  
  top_step  = 0;
  left_step = 0;
 
  past_top_step  = 0;
  past_left_step = 0;
}
 
void loop() {
  if (!Serial.available()) return;
 
  String s = Serial.readString();
  String top, left;
  char* c = &s[0];
  bool comma = true;
  
  while(*c) {
    char *now_c = c;
    c++;
    
    if (*now_c == ',') {
      comma = !comma;
      if (comma == true) {
        top_step  = atoi(top.c_str());
        left_step = atoi(left.c_str());
  
        top  = "";
        left = "";
  
        Serial.println(top_step);
        Serial.println(left_step);
        
        move(top_stepper,  &past_top_step,  top_step);
        move(left_stepper, &past_left_step, left_step);
        key_press();
        key_release();
        continue;
      }
      continue;
    }

    if (*now_c == '.') {
      key_hold(SHIFT);
      continue;
    }

    if (*now_c == ' ' || *c == 0) {
      top_step  = atoi(top.c_str());
      left_step = atoi(left.c_str());

      top  = "";
      left = "";

      Serial.println(top_step);
      Serial.println(left_step);
      
      move(top_stepper,  &past_top_step,  top_step);
      move(left_stepper, &past_left_step, left_step);
      key_press();
      key_release();
      continue;
    }
    
    if (comma == true)
      top.concat(*now_c);
    else
      left.concat(*now_c);
  }

  move(top_stepper,  &past_top_step,  0);
  move(left_stepper, &past_left_step, 0);
}
 
void move(AF_Stepper stepper, int *past_step, int now_step) {
  int step_direction;
  if (*past_step < now_step) {
    step_direction = FORWARD;
  } else {
    step_direction = BACKWARD;
  }
  
  for (int i=0; i<abs(*past_step-now_step); i++) {
    stepper.step(1, step_direction, DOUBLE);
    delay(20);
  }
 
  *past_step = now_step;
}

void key_press() {
  head.write(DOWN);
  delay(300);
  
  head.write(CENTER);
  delay(300);
}

void key_hold(int SPECIAL_KEY) {
  tail.write(SPECIAL_KEY);
  delay(300);
}

void key_release() {
  tail.write(CENTER);
  delay(300);
}

