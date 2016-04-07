
// Mega interrupt pins: 2, 3, 18, 19, 20, 21
#define MIC_0 18
#define MIC_1 19
#define MIC_2 20

// cm in microseconds at 20C 1 atm
const long speedOfSound = 0.03432;

// Forward
const float mic0xPos = 0.0;
const float mic0yPos = 1.0;

// Back right
const float mic1xPos = 0.5;
const float mic1yPos = -0.5;

// Back left
const float mic2xPos = -0.5;
const float mic2yPos = 0.5;

// Last activation of the microphone
unsigned long micTimes[] = {0, 0, 0};
// Contains timing differences
// 0 = 0 -> 1
// 1 = 1 -> 2
// 2 = 2 -> 0
long micDiffs[] = {0, 0, 0};

// Time in micros between which microphones time out
unsigned long micTimeOut = 1000;

// replaces getDistance()
// 0 = 0 -> 1
// 1 = 1 -> 2
// 2 = 2 -> 0
unsigned long micDistances[] = {0, 0, 0};

unsigned long lastTime = 0;

void setup() {
  attachInterrupt(MIC_0, triggerMic0, RISING);
  attachInterrupt(MIC_1, triggerMic1, RISING);
  attachInterrupt(MIC_2, triggerMic2, RISING);
  
  micDistances[0] = (mic0xPos, mic1xPos, mic0yPos, mic1yPos);
  micDistances[1] = (mic1xPos, mic2xPos, mic1yPos, mic2yPos);
  micDistances[2] = (mic2xPos, mic0xPos, mic2yPos, mic0yPos);

}

void loop() {
  // If at least one microphone has been activated
  // begin counting to timeout
  if(lastTime == 0 && (micTimes[0] || micTimes[1] || micTimes[2]))
  {
    lastTime = micros();
  }
  
  // If timeout reached, reset mic values
  if(micros() - lastTime > micTimeOut)
  {
    resetMicValues();
  }
    
  // If all mics activated before timeout, calculate direction.
  if(micTimes[0] && micTimes[1] && micTimes[2])
  {
    // Get the differences in timing
    // 0 = 0 -> 1
    // 1 = 1 -> 2
    // 2 = 2 -> 0
    micDiffs[0] = micTimes[1] - micTimes[0];
    micDiffs[1] = micTimes[2] - micTimes[1];
    micDiffs[2] = micTimes[0] - micTimes[2];
    
    findDirection();
    
    resetMicValues();
  }
}

void resetMicValues()
{
  micTimes[0] = 0;
  micTimes[1] = 0;
  micTimes[2] = 0;
    
  lastTime = 0;
}

void findDirection()
{
  //todo
}

// Maybe declare as consts to save on processing
float getDistance(float x1, float x2, float y1, float y2)
{
  return sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2));
}

long timeToCm(long microseconds)
{
  return microseconds * speedOfSound;
}

// Interrupts
void triggerMic0()
{
  micTimes[0] = micros();
}
void triggerMic1()
{
  micTimes[1] = micros();
}
void triggerMic2()
{
  micTimes[2] = micros();
}
