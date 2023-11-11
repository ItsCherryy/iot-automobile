//Arduino Sketch for Arduino Uno
#include <Servo.h>
#include <Stepper.h>
#include <SoftwareSerial.h>
#define echoPin 3
#define trigPin 2
#define servoPin 6
#define ledPin 7
#define ldrPin A0
#define stepsPerRev 2048
#define motSpeed 10
#define RX 0
#define TX 1

long duration;
int distance;
Servo servo;
int aut;
int mvm = 0;
int trn = 35;
unsigned long timer = millis();
Stepper stepper(stepsPerRev,8,10,9,11);
SoftwareSerial espSer(RX,TX);


void setup() {
    pinMode(trigPin,OUTPUT);
    pinMode(echoPin,INPUT);
    pinMode(ldrPin,INPUT);
    pinMode(ledPin,OUTPUT);
    servo.attach(servoPin);
    stepper.setSpeed(motSpeed);
    Serial.begin(9600);
    espSer.begin(9600);
}
void loop() {
    if(espSer.available()>0){
        aut = espSer.readStringUntil(',').toInt();
        if(aut == 2){
            int lgt = espSer.readStringUntil(';').toInt();
            digitalWrite(ledPin,(lgt) ? HIGH:LOW);
        }else{
            mvm = espSer.readStringUntil(',').toInt();
            trn = espSer.readStringUntil(';').toInt();
        }
        espSer.readString();
    }
    turns();
    stepper.step(mvm);
    sensor();
}
void turns(){
    int servo_angle = servo.read();
    if(trn > servo_angle){
        while(servo_angle != trn){
            servo.write(servo_angle);
            delay(10);
            servo_angle += 1;
        }
    }else{
        while(servo_angle != trn){
            servo.write(servo_angle);
            delay(10);
            servo_angle -= 1;
        }
    }
}
void sensor(){
    digitalWrite(trigPin,LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin,HIGH);
    delayMicroseconds(5);
    digitalWrite(trigPin,LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 /2;
    int ldr = analogRead(ldrPin);
    Serial.println(String(distance) + " " + String(ldr));
}