// Arduino Sketch for ESP 32
#include "WiFi.h"
#include <HTTPClient.h>
#define RXD2 16
#define TXD2 17

const char* ssid = "";
const char* password = "";
String url = "http://192.168.68.108/data";
String cmd = "";


void setup()
{
    Serial.begin(9600);
    Serial2.begin(9600,SERIAL_8N1,RXD2,TXD2);
    WiFi.begin(ssid,password);
}
void loop()
{
    delay(2000);
    if ((WiFi.status() == WL_CONNECTED)){
        HTTPClient http;
        bool http_conn = http.begin(url);
        int httpCode = http.GET();
        // httpCode will be negative on error
        if(httpCode > 0) {
            // file found at server
            if(httpCode == HTTP_CODE_OK) {
                String payload = http.getString();
                if(Serial2.availableForWrite()>payload.length()){
                    int siz = payload.length()+1;
                    char stri[siz];
                    payload.toCharArray(stri,siz);
                    if(cmd != payload){
                        Serial2.write(stri,siz);
                        Serial2.flush();
                        Serial.println(stri);
                        cmd = payload;
                    }
                }else{
                    Serial2.flush();
                }
            }
        }
        http.end();
    }
}