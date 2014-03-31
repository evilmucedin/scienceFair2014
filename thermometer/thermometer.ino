#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into pin 3 on the Arduino
#define ONE_WIRE_BUS 3

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

void discoverOneWireDevices()
{
  byte addr[8];
  
  Serial.print("Looking for 1-Wire devices...\n\r");
  while (oneWire.search(addr))
  {
    Serial.print("\n\rFound \'1-Wire\' device with address:\n\r");
    for (byte i = 0; i < 8; ++i)
    {
      Serial.print("0x");
      if (addr[i] < 16)
      {
        Serial.print('0');
      }
      Serial.print(addr[i], HEX);
      if (i < 7)
      {
        Serial.print(", ");
      }
    }
    if (OneWire::crc8(addr, 7) != addr[7])
    {
      Serial.print("CRC is not valid!\n");
      return;
    }
  }
  Serial.print("\n\r\n\rThat's it.\r\n");
  oneWire.reset_search();
  return;
}

DeviceAddress thermometer1 = { 0x28, 0x12, 0x45, 0x3C, 0x05, 0x00, 0x00, 0x7F };
DeviceAddress thermometer2 = { 0x28, 0xE6, 0x42, 0x4D, 0x05, 0x00, 0x00, 0xA7 };

void setup()
{
  // start serial port
  Serial.begin(9600);

  discoverOneWireDevices();

  // Start up the library
  sensors.begin();

  // set the resolution to 10 bit (good enough?)
  sensors.setResolution(thermometer1, 12);
  sensors.setResolution(thermometer2, 12);
}

void printTemperature(DeviceAddress deviceAddress)
{
  float tempC = sensors.getTempC(deviceAddress);
  if (tempC == -127.00)
  {
    Serial.print("Error getting temperature");
  }
  else
  {
    Serial.print("\t");
    Serial.print(tempC);
    Serial.print("\t");
    Serial.print(DallasTemperature::toFahrenheit(tempC));
  }
}

void loop()
{
  delay(1000);
  sensors.requestTemperatures();
 
  Serial.print("1");
  printTemperature(thermometer1);
  Serial.print("\n\r2");
  printTemperature(thermometer2);
  Serial.print("\n\r");
  Serial.print("\n\r");
} 
