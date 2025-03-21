uint8_t i = 0;


void setup() {
  i = 0;
  delay(3000);
  Serial.begin(115200);
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
  Serial.println(String(i));
  delay(500);
  i++;

  if (i > 100) {
    delay(3000);
    Serial.println("RESET");
    setup();
  }
}
