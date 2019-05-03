#include <Sparki.h>
#define NO_LCD // disables the LCD, frees up 3088 Bytes Flash Memory, 1k RAM
#define NO_ACCEL // disables the Accelerometer, frees up 598 Bytes Flash Memory
#define NO_MAG // disables the Magnetometer, frees up 2500 Bytes Flash Memory
const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

unsigned long timeLeft = 0;
unsigned long timeRight = 0;
unsigned long timeForward = 0;
unsigned long timeBackward = 0;

int period = 1000;
int periodStop = 800;
int ultraPeriod = 10000;
boolean commandOnce;
int fastPeriod = 500;
int IRleft;
int IRright;
int IRthreshold;

char messageFromPC[buffSize] = {0};
char messageTwo[buffSize] = {0};
int barkfreq = 0;
int red = 0;
int blue = 0;
int green = 0;
int datacase;
int movecase;
int ultracase;
int head;
int angleServo;
unsigned long timeUltra = 0;
//int period = 2000;
unsigned long timeNow = 0;
String distance;
String angle;

void setup()
{
  Serial1.begin(9600);
}

void loop()
{
  getDataPC();
  selectData();
  edgeAvoidance();

}
void getDataPC() {
  if (Serial1.available()) {

    char x = Serial1.read();

    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }

    if (readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) {
      bytesRecvd = 0;
      readInProgress = true;
    }
  }
}

void parseData() {



  char * strtokIndx; // this is used by strtok() as an index

  strtokIndx = strtok(inputBuffer, ",");
  strcpy(messageFromPC, strtokIndx);

  strtokIndx = strtok(NULL, ",");
  datacase = atoi(strtokIndx);
  
  strtokIndx = strtok(NULL, ",");
  barkfreq = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ",");
  red = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ",");
  green = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ",");
  blue = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ",");
  ultracase = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ",");
  head = atoi(strtokIndx);

}

void selectData() {
  switch (datacase) {
    case 1:
      updateMovementFree();
      break;

    case 2:
      updateGripper();
      break;

    case 3:
      updateLED();
      break;

    case 4:
      updateBeep();
      break;
    
    case 5:
      updateUltrasonic();
      break;
    
    case 6:
      updateHead();
      break;
  }
}

void updateHead() {

  commandOnce = true;
  if (commandOnce) {
    sparki.servo(map(head, 0, 180, -90, 90));
    datacase = 1;
    strcpy(messageFromPC, "STOPM");
  }
  }
  


void updateMovementFree() {
  if (strcmp(messageFromPC, "STOPM") == 0) {
    sparki.moveStop();

  }
  else if (strcmp(messageFromPC, "UP") == 0) {
        sparki.moveForward();
      }


  else if (strcmp(messageFromPC, "DOWN") == 0) {
        sparki.moveBackward();
      }

  else if (strcmp(messageFromPC, "LEFT") == 0) {
        sparki.moveLeft();
  }

  else if (strcmp(messageFromPC, "RIGHT") == 0) {
        sparki.moveRight();
      }
}


void updateGripper() {

  if (strcmp(messageFromPC, "OPEN") == 0) {
    sparki.gripperOpen();
    delay(10);

  }

  else if (strcmp(messageFromPC, "CLOSE") == 0) {
    sparki.gripperClose();
    delay(10);
  }

  else if (strcmp(messageFromPC, "STOP") == 0) {
    sparki.gripperStop();
    delay(10);

  }
}

void updateLED() {

  if (strcmp(messageFromPC, "LED") == 0) {
    sparki.RGB(red, green , blue);
  }
}


void updateBeep() {
  if (strcmp(messageFromPC, "BEEP") == 0) {
    sparki.beep(barkfreq);
  }
}

void updateUltrasonic() {
  switch(ultracase){
    case 1:
      sweepUltrasonic();
      break;
    case 2:
      captureUltrasonic();
      break;
  }
}

void sweepUltrasonic() {
  commandOnce = true;

if (commandOnce) {

  for (int i = 0; i <= 180; i += 10) {
    angleServo = map(i, 0, 180, -90, 90);
    sparki.servo(angleServo);
    distance = sparki.ping();
    angle = String(i);
    Serial1.print("c");
    Serial1.print(angle);
    Serial1.print("c");
    Serial1.print("a");
    Serial1.print(distance);
    Serial1.println("a");
    
  }
  sparki.servo(0);
  datacase = 1;
  strcpy(messageFromPC, "STOPM");
  }
  
  }
void captureUltrasonic() {
  commandOnce = true;
  if (commandOnce) {
    Serial1.println(sparki.ping());
    datacase = 1;
    strcpy(messageFromPC, "STOPM");
  }
}
void edgeAvoidance() {
  IRleft = sparki.edgeLeft();
  IRright = sparki.edgeRight();
  IRthreshold = 200;
  if (IRleft < IRthreshold || IRright < IRthreshold) {
    sparki.moveBackward(5);
  }
}



