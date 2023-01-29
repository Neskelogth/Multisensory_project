float circleX = 0;
float circleY = 0;
int circleSize = 80;
int XLIM = 400;
int YLIM = 400;
int CENTER_X = XLIM/2;
int CENTER_Y = YLIM/2;
float DISTANCE_THRESHOLD = (XLIM/2)*0.15;

float distance;

import controlP5.*; 
import oscP5.*;
import netP5.*;
  
OscP5 oscP5;
NetAddress myRemoteLocation;

void settings() {
  size(XLIM, YLIM);
  
  oscP5 = new OscP5(this,5006); 
  //myRemoteLocation = new NetAddress("127.0.0.1",12000);
}

void draw() {
  background(0, 256, 256);
  
  //strokeWeight(2);
  //stroke(0);
  //fill(255);
  //rect(-1, -1, 2, 2);
  
  fill(0);
  stroke(0);
  ellipse(CENTER_X, CENTER_Y, circleSize, circleSize);
  
  
  
  distance = dist(circleX, circleY, CENTER_X, CENTER_Y);
  println(distance);
  if (distance <= DISTANCE_THRESHOLD) {
    fill(0, 255, 0);
    stroke(0);
    ellipse(circleX, circleY, circleSize, circleSize);
  } else {
    fill(255, 0, 0);
    stroke(0);
    ellipse(circleX, circleY, circleSize, circleSize);
  }
}

void oscEvent(OscMessage theOscMessage) {
  if(theOscMessage.checkAddrPattern("/x") == true) {
    float x = theOscMessage.get(0).floatValue();
    circleX = CENTER_X*(1+x);
    //if (distance <= DISTANCE_THRESHOLD){
    //  circleX = CENTER_X;
    //}
  }
  if(theOscMessage.checkAddrPattern("/y") == true) {
    float y = theOscMessage.get(0).floatValue();
    circleY = CENTER_Y*(1+y);
    //if (distance <= DISTANCE_THRESHOLD){
    //  circleY = CENTER_Y;
    //  println("ylet");
    //}
  }
  distance = dist(circleX, circleY, CENTER_X, CENTER_Y);
  if (distance <= DISTANCE_THRESHOLD){
      circleY = CENTER_Y;
      circleX = CENTER_X;
    }
    //position = OSCvalue;
    //return;
  /* process the received data here */
  //float receivedData = theOscMessage.get(0).floatValue();
  //println("received data: " + receivedData);
  return;
}

//void mouseDragged() {
//  circleX = map(mouseX, 0, width, -1, 1);
//  circleY = map(mouseY, 0, height, -1, 1);
//}
