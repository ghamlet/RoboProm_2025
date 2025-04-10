#include "DxlMaster2.h"
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Regexp.h>
#define UDP_PORT 8888

byte mac[] = { 
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED 
};

IPAddress ip(192, 168, 42, 128);
IPAddress target(192, 168, 42, 120);

unsigned int localPort = 8888; 
unsigned int UDPremotePort = 8888; 

EthernetUDP Udp;

uint8_t data = 0;
uint8_t protocol = 1;
uint8_t id = 42;
uint8_t test = 0;

void setup() {
  DxlMaster.begin(57600);
  Serial.begin(115200);
  
  Ethernet.init(10); 

  for(uint8_t i = 0; i < 4; i++){
    mac[i] = ip[i];
  }

  Ethernet.begin(mac, ip); 
  Udp.begin(localPort);

  // for(uint8_t i =0; i < 70; i++){
  //   DxlMaster.read(1, i, 3, test);
  //   if(test != 0){
  //     Serial.println(test);
  //   }
  // }
}

void loop() {
  if (receiveUDP()){
    DxlMaster.write(protocol, id, 25, 1);
    delay(100);
    DxlMaster.read(protocol, id, 27, data);
    Serial.println(data);

    String mes = String(data);
    sendUDP(mes, target);
  }
}

bool receiveUDP(){
  int packetSize = Udp.parsePacket();
  if(packetSize > 0){
    char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    MatchState ms;
    ms.Target(packetBuffer);
    Serial.print(packetBuffer);
    char result = ms.Match("get_sonar_data", 0);
    if(result == REGEXP_MATCHED){
      return true;
      packetBuffer[UDP_TX_PACKET_MAX_SIZE] = 0;
    }
    packetBuffer[UDP_TX_PACKET_MAX_SIZE] = 0;
  }
  return false;
}

void sendUDP(String str, IPAddress ip){
  char out[str.length() + 1];
  str.toCharArray(out, str.length() + 1);
  Udp.beginPacket(ip, UDPremotePort);
  Udp.write(out);
  Udp.endPacket();
}
