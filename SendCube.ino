void SendCube(int Position) {

  if (Position == 1) {
    degreebase = 35;
    degreefront = 110;
    degreeup = 20;
  }

  else if (Position == 2) {
    degreebase = 63;
    degreefront = 110;
    degreeup = 20;
  }
  else if (Position == 3) {
    degreebase = 90;
    degreefront = 110;
    degreeup = 20;
  }
  else if (Position == 4) {
    degreebase = 115;
    degreefront = 110;
    degreeup = 20;
  }
  else if (Position == 5) {
    degreebase = 143;
    degreefront = 110;
    degreeup = 20;
  }

  beeprange(1, 100);

  defult();

  //หยิบ
  Hand(150); delay(500);

  Base(degreebase); delay(500);
  Frontback(degreefront); delay(500);
  Updown(degreeup); delay(500);
  Hand(180); delay(500);               //Hand Close

  //  //หัน
  Updown(100); delay(500);
  for (int i = degreebase; i > 0; i--) {
    Base(i);
    delay(5);
  }
  delay(500);               //Position to Town
  Updown(80); delay(500);
  Hand(115); delay(500);              //Hand Open
  Updown(100); delay(500);

  for (int i = 40; i < 90; i++) {
    Base(i);
    delay(5);
  }
  defult();
}

void MotorSend(int i) {
  Stop(); 
  Sideright(30);delay(3500);
  Stop();
  SendCube(i);
  Sideleft(30);delay(3500);
  Stop();
  

}
