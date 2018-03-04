import oscP5.*;
import netP5.*;
String firstValue;
String secondValue;
  
OscP5 oscP5;
NetAddress myRemoteLocation;

void setup() {
  size(800, 400);
  frameRate(25);
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this,1234);

  myRemoteLocation = new NetAddress("127.0.0.1", 5005);
}


void draw() {
  background(0); 
   if(firstValue != null){
    textAlign(CENTER);
    fill(255);
    stroke(255);
    textSize(80);
    text(firstValue, width/2, height/2+80);
    text(secondValue, width/2, height/2-80);
    
   }
}

void mousePressed() {
  OscMessage myMessage = new OscMessage("/matt");
  
  myMessage.add(5);

  oscP5.send(myMessage, myRemoteLocation); 
  print("sent message");
}

void oscEvent(OscMessage theOscMessage) {  
  if(theOscMessage.checkAddrPattern("/isadora/1")==true) {
    firstValue = theOscMessage.get(0).stringValue();
    println(" values:"+ firstValue);
    return;
  } 
  if(theOscMessage.checkAddrPattern("/isadora/2")==true) {
    secondValue = theOscMessage.get(0).stringValue();
    println(" values:"+ secondValue);
    return;
  }
  println("### received an osc message. with address pattern "+theOscMessage.addrPattern());
}