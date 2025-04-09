#include <Ethernet.h> 
#include <Regexp.h>
#include <EthernetUdp.h>

#define red_led 2
#define orange_led 3
#define green_led 4
#define blue_led 5

//МАС-адрес
byte mac[] = { 
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED 
};

//IP-адрес
IPAddress ip(192, 168, 42, 129);

int led_state = 0;

//Порт
unsigned int localPort = 8000; 
unsigned int UDPremotePort = 8888; 

EthernetUDP Udp;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);     
  Ethernet.init(10);   
  Ethernet.begin(mac, ip); 
  Udp.begin(localPort);

}

void loop() {
  // put your main code here, to run repeatedly:
  recieveUDP();
}

void recieveUDP(){
  int packetSize = Udp.parsePacket();
  if(packetSize > 0){
    char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    MatchState ms;
    ms.Target(packetBuffer);
    Serial.print(packetBuffer);
    char result = ms.Match("id:(%d+):state:(%d+)", 0);
    char m[20];
    if(result == REGEXP_MATCHED){
      ms.GetMatch(m);
      Serial.println("id: " + String(ms.GetCapture(m, 0)));
      Serial.println("state: " + String(ms.GetCapture(m, 1)));
      led_state = atoi(ms.GetCapture(m, 1));
      changeLed(led_state);
    }
    packetBuffer[UDP_TX_PACKET_MAX_SIZE] = 0;
  }
}

void changeLed(int state){
  switch (state){
    case 0: // orange off - command recieved
      digitalWrite(orange_led, LOW);
      digitalWrite(blue_led, LOW);
      digitalWrite(red_led, LOW);
      digitalWrite(green_led, LOW);
    case 1: // брак - красный
      digitalWrite(red_led, HIGH);
      digitalWrite(orange_led, LOW);
      digitalWrite(green_led, LOW);
      digitalWrite(blue_led, LOW);// 2 - красный , 3- оранжевый, 4 - зеленый, 5 - синий 
      break;
    case 2: // orange - wait command
      digitalWrite(orange_led, HIGH);
      digitalWrite(red_led, LOW);
      digitalWrite(green_led, LOW);
      digitalWrite(blue_led, LOW);
      break;
    case 3: // hrupkaya - green 
      digitalWrite(green_led, HIGH);
      digitalWrite(orange_led, LOW);
      digitalWrite(red_led, LOW);
      digitalWrite(blue_led, LOW);
      break; 
    case 4: // not xrupkaya
      digitalWrite(blue_led, HIGH);
      digitalWrite(orange_led, LOW);
      digitalWrite(green_led, LOW);
      digitalWrite(red_led, LOW);
      break;
    case 5: // green&blue - not thing 
      digitalWrite(blue_led, HIGH);
      digitalWrite(green_led, HIGH);
      digitalWrite(orange_led, LOW);
      digitalWrite(red_led, LOW);
      break;
    
  }
}
