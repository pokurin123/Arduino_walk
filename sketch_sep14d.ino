//#define elements 2 //カンマで区切るデータの最大項目数
//String data_string; //シリアルで受け取る全文字列
//char *p; //文字列をカンマで分割するstrtok処理で使うポインタ
//String p_string; //上記ポインタで区切った文字列の仮格納用
//String data_array[elements]; //カンマ分割されたstrデータを格納する
////String li_data[elements];
int ledPin_right=2;
int ledPin_left=4;

void setup() {
  pinMode(ledPin_right, OUTPUT); 
  pinMode(ledPin_left, OUTPUT); 
  Serial.begin(9600); //シリアルを開く
  Serial.println("ready");
}

void loop() {
  if( Serial.available()){
    char ch = Serial.read();
    if(ch == '0'){
      digitalWrite(ledPin_right,1);
      digitalWrite(ledPin_left,1);
    } else if(ch == '1'){
      digitalWrite(ledPin_right,0);
      digitalWrite(ledPin_left,1);
    } else if(ch == '2'){
      digitalWrite(ledPin_right,1);
      digitalWrite(ledPin_left,0);
    } else if(ch == '3'){
      digitalWrite(ledPin_right,0);
      digitalWrite(ledPin_left,0);
    }
  }
}
