#include "circle.h"
#define NUM_CIRCLES 5

#define START_BUTTON_PIN 26  //Active Low
#define START_BUTTON_LIGHT 27
#define START_BUTTON_FLASH_RATE 500

#define MAX_CIRCLE_SWAPS 200  // Needs verifying / tweaking with below
#define TIME_ON_CIRCLE 3000   //ms - time spent on each array, multiply by MAX_CIRCLE_SWAPS for maximum game time.

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
  //Set up the Start Button
  pinMode(START_BUTTON_PIN, INPUT_PULLUP);
  pinMode(START_BUTTON_LIGHT, OUTPUT);
  bool startButtonLightState = HIGH;
  digitalWrite(START_BUTTON_LIGHT, startButtonLightState);

  for (uint8_t i = 0; i < NUM_CIRCLES; i++) {
    circles[i].set_pins();
    circles[i].stop_leds();
  }

  uint32_t timestamp = millis();
  // Wait for the start button to be pushed
  while (digitalRead(START_BUTTON_PIN)) {
    //Flash the button (non blocking)
    if ((millis() - timestamp) > START_BUTTON_FLASH_RATE) {
      timestamp = millis();
      startButtonLightState = !startButtonLightState;
      digitalWrite(START_BUTTON_LIGHT, startButtonLightState);
    }
  }
  digitalWrite(START_BUTTON_LIGHT, LOW);

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
  uint8_t circleOrder[MAX_CIRCLE_SWAPS] = {};
  for (uint8_t i = 0; i < MAX_CIRCLE_SWAPS; i++) {
    // Chooses a random number between 0 and NUM_CIRCLES-1
    circleOrder[i] = random(0, NUM_CIRCLES);
  }

  uint8_t score = 0;
  uint8_t currentCircle = 0;
  while (1) {

    Circle activeCircle = circles[circleOrder[currentCircle]];
    //activeCircle.set_pins();
    uint32_t circleStartTime = millis();
    while (1) {
      // If we have been on the current circle for the set
      if (millis() - circleStartTime > TIME_ON_CIRCLE) {
        // turn off any leds
        activeCircle.stop_leds();
        // Move to new circle
        currentCircle++;
        break;
      }
      // If the water is on target
      if (activeCircle.get_switch_pin_state()) {
        delay(100);
        // update score
        score++;
        Serial.println(String(score));
        if (score > MAX_SCORE) {
          activeCircle.stop_leds();
          delay(5000);
          Serial.println("RESET");
          delay(1000);
          resetFunc();
          //Game over, reset
          //reset();
        }
      }
      // Will do non-blocking timer on the back end to handle the LED timings
      activeCircle.swap_leds();
    }

    if (currentCircle >= MAX_CIRCLE_SWAPS) {
      Serial.println("RESET");
      delay(1000);
      resetFunc();

      break;
    }
  }
}
