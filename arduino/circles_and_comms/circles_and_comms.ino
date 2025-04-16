#include "circle.h"
#define NUM_CIRCLES 5

#define START_BUTTON_PIN 26  //Active Low
#define START_BUTTON_LIGHT 27
#define START_BUTTON_FLASH_RATE 500

#define PUMP_RELAY_PIN 48

#define MAX_CIRCLE_SWAPS 100  // Needs verifying / tweaking with below
#define MAX_TIMER 4           //s - max time spent on each array, multiply by MAX_CIRCLE_SWAPS for maximum game time.

#define TARGET_CHECK_INTERVAL 350  // Effectively the marker of how long the game will last, how often do we add points for on-target

#define MAX_SCORE 100

// Define 5 circles
Circle topLeft = Circle(8, 9, 10, 11, 13);
Circle topRight = Circle(14, 15, 16, 17, 49);
Circle bottomLeft = Circle(4, 5, 6, 7, 12);
Circle bottomRight = Circle(18, 19, 20, 21, 50);
Circle middle = Circle(23, 22, 2, 3, 51);

Circle circles[NUM_CIRCLES] = { topLeft, topRight, bottomLeft, bottomRight, middle };

void (*resetFunc)(void) = 0;
// Deal with reset button push


void setup() {
  // Set up the Serial Comms
  Serial.begin(115200);
  Serial.println();  //There to clear the buffer in the python
  //Set up the Start Button
  pinMode(START_BUTTON_PIN, INPUT_PULLUP);
  pinMode(START_BUTTON_LIGHT, OUTPUT);
  pinMode(PUMP_RELAY_PIN, OUTPUT);

  bool startButtonLightState = HIGH;
  digitalWrite(START_BUTTON_LIGHT, startButtonLightState);

  for (uint8_t i = 0; i < NUM_CIRCLES; i++) {
    circles[i].set_pins();
    circles[i].stop_leds();
  }

  uint32_t timestamp = millis();
  uint8_t i = 0;
  // Wait for the start button to be pushed
  while (digitalRead(START_BUTTON_PIN)) {
    //Flash the button (non blocking)
    if ((millis() - timestamp) > START_BUTTON_FLASH_RATE) {
      timestamp = millis();
      startButtonLightState = !startButtonLightState;
      digitalWrite(START_BUTTON_LIGHT, startButtonLightState);
    }
  }
  randomSeed(analogRead(A2));
  Serial.println("RESET");
  delay(1000);
  digitalWrite(START_BUTTON_LIGHT, LOW);
  digitalWrite(PUMP_RELAY_PIN, HIGH);

  Serial.println("COUNTDOWN_5");
  delay(1000);
  Serial.println("COUNTDOWN_4");
  delay(1000);
  Serial.println("COUNTDOWN_3");
  delay(1000);
  Serial.println("COUNTDOWN_2");
  delay(1000);
  Serial.println("COUNTDOWN_1");
  delay(1000);
  Serial.println("COUNTDOWN_0");
  delay(1000);
  //reset();
}

void loop() {
  // Generate a random array for circle swapping
  circleVars circleOrder[MAX_CIRCLE_SWAPS] = {};
  uint8_t nums[5] = {0};
  for (uint8_t i = 0; i < MAX_CIRCLE_SWAPS; i++) {
    // Chooses a random number between 0 and NUM_CIRCLES-1 for the circle to do
    circleOrder[i].circlePosition = random(0, NUM_CIRCLES);
    // Check the number isn;t the same as the last one
    while (i > 0 && circleOrder[i].circlePosition == circleOrder[i - 1].circlePosition) {
      circleOrder[i].circlePosition = random(0, NUM_CIRCLES);
      // Will only exit once the ranom number is new.
    }
    // Chose a random number between 1 and MAX_TIMER for the circle to stay for
    circleOrder[i].circleTime = random(2, MAX_TIMER + 1);
    //  Serial.println("Circle: " + String(circleOrder[i].circlePosition) + ", Time on Circle: " + String(circleOrder[i].circleTime));
    nums[circleOrder[i].circlePosition]+=1;
  }

  for(uint8_t j =0; j<5;j++){
    Serial.println("Number of " +String(j) + "'s = " + String(nums[j]));
  }
  uint8_t score = 0;
  uint8_t currentCircle = 0;
  while (1) {

    Circle activeCircle = circles[circleOrder[currentCircle].circlePosition];
    uint32_t circleStartTime = millis();
    uint32_t onTargetTimer = millis();

    // While the game hasn't timed out
    while (currentCircle < MAX_CIRCLE_SWAPS) {

      // Handle reset requests
      if (!digitalRead(START_BUTTON_PIN)) {
        //Reset requested
        Serial.println("RESET");
        digitalWrite(PUMP_RELAY_PIN, LOW);

        delay(1000);
        resetFunc();
      }

      // If we have been on the current circle for the set time
      if (millis() - circleStartTime > ((circleOrder[currentCircle].circleTime) * 1000)) {
        // turn off any leds
        activeCircle.stop_leds();
        // Move to new circle
        currentCircle++;
        activeCircle = circles[circleOrder[currentCircle].circlePosition];
        circleStartTime = millis();
      }
      // If enough tim ehas passed that we can check for on-target water again
      if (millis() - onTargetTimer > TARGET_CHECK_INTERVAL) {
        // If the water is on target
        onTargetTimer = millis();
        if (activeCircle.get_switch_pin_state()) {
          delay(100);  //TODO non blocking
          // update score
          score++;
          Serial.println(String(score));
          if (score >= MAX_SCORE) {
            activeCircle.stop_leds();
            break;
            //Game over
          }
        }
      }
      // Will do non-blocking timer on the back end to handle the LED timings
      activeCircle.swap_leds();
    }
    delay(100);
    Serial.end();
    //Game over
    digitalWrite(PUMP_RELAY_PIN, LOW);
    resetFunc();
  }
}
