void receiveEvent(int howmany) {
  while (Wire.available() > 1) {
    dataCommand[0] = Wire.read();
    dataCommand[1] = Wire.read();
    dataCommand[2] = Wire.read();
    dataCommand[3] = Wire.read();
    
  }
}

void requestEvent() {
  Wire.write(dataSend, 3);
}
