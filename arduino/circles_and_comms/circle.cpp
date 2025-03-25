#include "circle.h"

Circle::Circle(uint8_t led1, uint8_t led2, uint8_t led3, uint8_t led4, uint8_t switchPin) {
  _leds[0] = led1;
  _leds[1] = led2;
  _leds[2] = led3;
  _leds[3] = led4;
  uint8_t _switchPin = switchPin;
}

void Circle::set_pins() {
  for (uint8_t i = 0; i < NUM_LED_PINS; i++) {
    pinMode(_leds[i], OUTPUT);
    digitalWrite(_leds[i], LOW);
  }
  pinMode(_switchPin, INPUT);
  _ledTimer = millis();
}

void Circle::swap_leds() {
  // If the leds were last swapped more than LED_FLASH_TIME ago
  if (millis() - _ledTimer > LED_FLASH_TIME) {
    _ledTimer = millis();
    //Turn off current ones
    digitalWrite(_leds[_ledCounter], LOW);
    // Increment LED counter (or reset to 0)
    if (_ledCounter >= (NUM_LED_PINS - 1)) {
      _ledCounter = 0;
    } else {
      _ledCounter += 1;
    }
    //Turn on new LEDs
    digitalWrite(_leds[_ledCounter], HIGH);
  }
}

void Circle::stop_leds() {
  for (uint8_t i = 0; i < NUM_LED_PINS; i++) {
    digitalWrite(_leds[i], LOW);
  }
}



bool Circle::get_switch_pin_state() {
  return digitalRead(_switchPin);
}