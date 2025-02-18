const int ledPins[] = {2, 3, 4, 5, 6};
const int buzzerPin = 7;

void setup() {
    Serial.begin(9600);
    for (int i = 0; i < 5; i++) {
        pinMode(ledPins[i], OUTPUT);
    }
    pinMode(buzzerPin, OUTPUT);
}

void loop() {
    if (Serial.available()) {
        char command = Serial.read();
        
        for (int i = 0; i < 5; i++) {
            digitalWrite(ledPins[i], LOW);
        }
        digitalWrite(buzzerPin, LOW);
        
        if (command == 'H') {
            for (int i = 0; i < 5; i++) {
                digitalWrite(ledPins[i], HIGH);
            }
            digitalWrite(buzzerPin, HIGH);
        } else if (command >= '1' && command <= '5') {
            int ledIndex = command - '1';
            digitalWrite(ledPins[ledIndex], HIGH);
        }
    }
}