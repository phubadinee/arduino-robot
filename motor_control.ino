void Stop(){
  motor(1,0);
  motor(2,0);
  motor(3,0);
  motor(4,0);
}

void Forword(int Speed,int d){
  motor(1,Speed);
  motor(2,Speed-d);
  motor(3,Speed);
  motor(4,Speed-d);
}

void Backword(int Speed){
  motor(1,-Speed);
  motor(2,-Speed);
  motor(3,-Speed);
  motor(4,-Speed);
}

void Turnleft(int Speed){
  motor(1,-Speed);
  motor(2,Speed);
  motor(3,-Speed);
  motor(4,Speed);
}

void Turnright(int Speed){
  motor(1,Speed);
  motor(2,-Speed);
  motor(3,Speed);
  motor(4,-Speed);
}

void Sideleft(int Speed){
  motor(1,-Speed);
  motor(2,Speed);
  motor(3,Speed);
  motor(4,-Speed);
}

void Sideright(int Speed){
  motor(1,Speed);
  motor(2,-Speed);
  motor(3,-Speed);
  motor(4,Speed);
}

void Diagonalleft(int Speed){
  motor(1,0);
  motor(2,100);
  motor(3,100);
  motor(4,0);
}

void Diagonalright(int Speed){
  motor(1,100);
  motor(2,0);
  motor(3,0);
  motor(4,100);
}
