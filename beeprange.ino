void beeprange(int range,int del){

  for(int i=0;i<range;i++){
    beep();
    delay(del);
  }
}

void beepnumber(){
  beep();           // Generate the default “beep” signal 
  sleep(1000); 
  beep(1);      // Generate type 1 of beep signal 
  sleep(1000);
  beep(2);      // Generate type 2 of beep signal
  sleep(1000);
  beep(3);      // Generate type 3 of beep signal
  sleep(1000);
}
