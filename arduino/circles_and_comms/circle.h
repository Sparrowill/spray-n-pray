#ifndef CIRCLE_H
#define CIRCLE_H

#include <Arduino.h>

#define NUM_LED_PINS 4
#define LED_FLASH_TIME 150  //ms - The amount of time each LED colour will be on for

class Circle {
public:
  Circle(uint8_t led1, uint8_t led2, uint8_t led3, uint8_t led4, uint8_t switchPin);
  void set_pins();
  void swap_leds();
  void stop_leds();
  bool get_switch_pin_state();

private:
  uint8_t _leds[NUM_LED_PINS] = {};
  uint8_t _switchPin = 0;
  uint8_t _ledCounter = 0;
  uint32_t _ledTimer = 0;
};

struct circleVars {
  uint8_t circlePosition;
  uint8_t circleTime;
};




#endif  //CIRCLE_H