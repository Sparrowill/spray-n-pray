
void reset() {
  // Deal with reset button push
  Serial.println("RESET");
  setup();
}




void setup() {
  delay(500);
  // Set up the Serial Comms
  Serial.begin(115200);
  // //Set up the Start Button
  // pinMode(START_BUTTON_PIN, INPUT_PULLUP);
  // pinMode(START_BUTTON_LIGHT, OUTPUT);
  // bool startButtonLightState = HIGH;
  // digitalWrite(START_BUTTON_LIGHT, startButtonLightState);
  delay(2000);

  uint32_t timestamp = millis();
  // // Wait for the start button to be pushed
  // while (digitalRead(START_BUTTON_PIN)) {
  //   //Flash the button (non blocking)
  //   if ((millis() - timestamp) > START_BUTTON_FLASH_RATE) {
  //     timestamp = millis();
  //     startButtonLightState = !startButtonLightState;
  //     digitalWrite(START_BUTTON_LIGHT, startButtonLightState);
  //   }
  // }
  // digitalWrite(START_BUTTON_LIGHT, LOW);

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
}

void loop() {

  uint8_t score = 0;
  while (1) {
    Serial.println(String(score));
    score+=20;
    delay(1000);
    if (score > 100) {
      reset();
    }
  }
}
