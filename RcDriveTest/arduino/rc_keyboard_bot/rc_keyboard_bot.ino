#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Adafruit_NeoPixel.h>

#define in1 6
#define in2 7
#define in3 8
#define in4 9

RF24 radio(22, 23); // CE, CSN
const byte address[6] = "00001";
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(8, 2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels1 = Adafruit_NeoPixel(3, 40, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_2MBPS);
  radio.setChannel(110);
  radio.startListening();
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pixels.begin();
  pixels1.begin();
}

void loop() {
  headlight();
  //  if (!radio.available())
  //    noRadio();
  if (radio.available()) {
    char text[32];
    radio.read(&text, sizeof(text));
    Serial.println(text);
    if (strcmp("forward", text) == 0)
      forward();
    else if (strcmp("reverse", text) == 0)
      reverse();
    else if (strcmp("right", text) == 0)
      right();
    else if (strcmp("left", text) == 0)
      left();
    else if (strcmp("stop", text) == 0)
      stop();
    else {
      Serial.print(text);
      Serial.print("Don't come here");
    }
  }
}
void forward() {
  Serial.println("forward");
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  digitalWrite(14, HIGH);
  setcolor(0, 255, 0);
}
void reverse() {
  Serial.println("reverse");
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  digitalWrite(16, HIGH);
  setcolor(255, 255, 255);
}
void right() {
  Serial.println("right");
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  digitalWrite(14, HIGH);
  digitalWrite(15, HIGH);
  setcolor(0, 255, 255);
}
void left() {
  Serial.println("left");
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  digitalWrite(16, HIGH);
  digitalWrite(15, HIGH);
  setcolor(255, 0, 255);
}
void stop() {
  Serial.println("stop");
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  digitalWrite(15, HIGH);
  setcolor(255, 0, 0);
}

void setcolor(int x , int y, int z) {
  for (int j = 0; j < 8; j++) {
    pixels.setPixelColor(j, pixels.Color(x, y, z));
    pixels.show();
  }
}
void headlight() {
  for (int j = 0; j < 3; j++) {
    pixels1.setPixelColor(j, pixels1.Color(255, 255, 255));
    pixels1.show();
  }
}

