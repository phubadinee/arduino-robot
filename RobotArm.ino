//Hand = 4               180หุบ
//FrontBack = 3          ค่าน้อย = หลัง | ค่ามาก = หน้า
//UpDown =  2            ค่ามาก = ขึ้น     60
//Base = 1

void Hand(int degree) {
  servo(4, degree);
}

void Updown(int degree) {
  servo(2, degree);
}

void Frontback(int degree) {
  servo(3, degree);
}

void Base(int degree) {
  servo(1, degree);
}


void defult() {
  Hand(180);
  Frontback(70);
  Updown(70);
  Base(90);
}
