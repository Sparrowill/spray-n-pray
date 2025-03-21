uint8_t i = 0;


void setup() {
  i = 0;
  Serial.begin(115200);
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
