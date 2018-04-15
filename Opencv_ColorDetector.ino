#include<SoftwareSerial.h>
SoftwareSerial bt(2,3);//Rx then TX
#define pc Serial

void glow(String led){
  String reds="",greens="",blues="";
  int red=0,green=0,blue=0;
  int cc=0;//Comma Counter
  char c;
  for(int i=0;i<led.length();i++){
    c=led.charAt(i);
    if(c!=','){
      if(cc==0){
        reds+=c;
      }
      else if(cc==1){
        greens+=c;
      }
      else if(cc==2){
        blues+=c;
      }
      }
    
    else{
      ++cc;
    }
  }
  red=reds.toInt();
  if(red>180){//Hard Coding the Color offset (Depends on the led used)
    red=255;
  }
  green=greens.toInt();
  blue=blues.toInt()*0.65;
  if(blue<30){
    blue=0;
  }

  pc.print(red);
  pc.print(":");
  pc.print(green);
  pc.print(":");
  pc.print(blue);
  pc.print(":");

  analogWrite(9,blue);
  analogWrite(11,red);
  analogWrite(10,green);
}

void setup() {
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);

  pc.begin(9600);
  pc.println("PC connected ");
  bt.begin(9600);
  pc.println("Bluetooth Stable");
  bt.setTimeout(200);
}

String data;

void loop() {
  if(bt.available()){
    data=bt.readString();
    glow(data);
    pc.println("\n");
  }

}

