#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";
// duration for output
int time = 1;
// initial command
int command = 0;

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(110);
  radio.setDataRate(RF24_2MBPS);
  radio.stopListening();
}
void loop() {
  //receive command
  if (Serial.available() > 0) {
    command = Serial.read();
  }
  else {
    reset();
  }
  send_command(command, time);
}

void right(int time) {
  const char text[] = "right";
  radio.write(&text, sizeof(text));
  delay(time);
}

void left(int time) {
  const char text[] = "left";
  radio.write(&text, sizeof(text));
  delay(time);
}

void forward(int time) {
  const char text[] = "forward";
  radio.write(&text, sizeof(text));
  delay(time);
}

void reverse(int time) {
  const char text[] = "reverse";
  radio.write(&text, sizeof(text));
  delay(time);
}

void reset() {
  const char text[] = "stop";
  radio.write(&text, sizeof(text));
}

void send_command(int command, int time) {
  switch (command) {
    //reset command
    case 0: reset(); break;

    // single command
    case 1: forward(time); break;
    case 2: reverse(time); break;
    case 3: right(time); break;
    case 4: left(time); break;

    //combination command
    //     case 6: forward_right(time); break;
    //     case 7: forward_left(time); break;
    //     case 8: reverse_right(time); break;
    //     case 9: reverse_left(time); break;

    default: Serial.print("Invalid Command\n");
  }
}

