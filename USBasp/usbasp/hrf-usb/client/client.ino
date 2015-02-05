#define chclient 1 // номер клиента 1...
#define timeoutper 400 // таймаут запросов от сервера.
#define timesend 400 // интервал отправки данных,для обычных датчиков можно установить время выше.

#include <SPI.h>
#include "DHT.h"

DHT dht;

#include "nRF24L01.h"
#include "RF24.h"

unsigned long time1=0;
unsigned long time2=0;

#define RELE_1 13 //
#define RELE_2 7

// Set up nRF24L01 radio on SPI bus plus pins 9 & 10
RF24 radio(9,10);

// 0 -прием , 1 -передача
const uint64_t pipes[2] = { 0xF0F0F0F0E1LL,0xF0F0F0F0D2LL};

// структура принятых данных.МЕНЯТЬ НЕЛЬЗЯ
typedef struct{
byte identifier;
byte val1;
byte val2;
byte val3;
byte val4;
}
nf0;
nf0 servernf;

// структура отправляемых данных.Изменяемые данные.
//Размер структуры должен быть не больше 32 байт !
typedef struct{
  byte identifier;// номер передатчика.МЕНЯТЬ НЕЛЬЗЯ

  int Analog;
  boolean test_data;
  int Error_Message; // счетчик ошибок
  long count;// счетчик передач для контроля качества канала
 float temperature_Sensor;// передаём температуру.
 float Humidity_Sensor;// передаём влажность
}
nf1;
nf1 clientnf;

void setup() {

dht.setup(3); // DHT датчик на пине 3

pinMode(RELE_1, OUTPUT);

pinMode(RELE_2, OUTPUT);

radio.begin();

// выбор скорости
//  radio.setDataRate(RF24_250KBPS);
  radio.setDataRate(RF24_1MBPS);
//  radio.setDataRate(RF24_2MBPS);
   
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(25); //тут установка канала
  radio.setCRCLength(RF24_CRC_16);

// radio.setAutoAck(false); // выключить аппаратное потверждение

radio.setRetries(15,15);

radio.openWritingPipe(pipes[1]); // Открываем канал передачи
radio.openReadingPipe(1,pipes[0]); // Открываем канал приема  

}

byte errorstate;

void loop() {


//---------------------------------для чтения сенсоров--------------------------
  if ((millis()-time1) >= 1000) {  // обновляем сенсоры раз в секунду (1000млс)
//  тут будут опросы сенсоров

  
clientnf.temperature_Sensor = dht.getTemperature();
clientnf.Humidity_Sensor = dht.getHumidity();

     time1 = millis();      
  }
  
  // Заполнение структуры данными
  clientnf.identifier = chclient;

  clientnf.Analog=analogRead(0); //пример передачи int данных
  
if (clientnf.count <= 2147483646)  clientnf.count++; // счетчик передач для контроля качества канала
  else clientnf.count = 0;
  
  // Заполнение структуры данными

//***********************************************************************************/
  if ((millis() - time2) >= timesend || errorstate !=0) {  
  radio.stopListening();
  bool ok = radio.write( &clientnf, sizeof(clientnf) );
  radio.startListening();
 
  unsigned long started_waiting_at = millis();
  bool timeout = false;
  while ( ! radio.available() && ! timeout )
  
  if (millis() - started_waiting_at > timeoutper ) timeout = true;


  if ( timeout ) {
  //  счетчик ошибок
  clientnf.Error_Message++;
  errorstate++; // счетчик ошибок для повтора
  }
  else {
    radio.read( &servernf, sizeof(servernf) );
    errorstate=0;
}
if (errorstate>=10) errorstate=0; // не более 10 попыток для повтора
//**********************************************************************************/


if (servernf.identifier == chclient) { // выполнение команд с сервера,
//если данные предназначены для этого клиента:

// val1= 10 -значит дергаем пинами, val2 - номер пина, val3 - состояние пина
// не забудте установить режим OUTPUT для нужных пинов.
// nRF-USB write 1 10 7 1 1 - что значит установить на 7 выводе логический уровень 1
    if (servernf.val1==10) digitalWrite(servernf.val2,servernf.val3);
   
// val1= 11 -значит управляем ШИМ пинами, val2 - номер пина, val3 - уровень 0..255.
// не забудте установить режим OUTPUT для нужных пинов.
// ШИМ возможен только на некоторых пинах !!
    if (servernf.val1==11) analogWrite(servernf.val2,servernf.val3);

}

    time2 = millis();      
  }

} // конец loop