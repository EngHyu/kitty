import http.requests.*;
import processing.serial.*;

Serial arduino;
GetRequest get, delete;
JSONArray jsons;
void setup() {
  arduino = new Serial(this, Serial.list()[1], 9600);
  get     = new GetRequest("http://192.168.2.12:5000/catch/");
  get.addHeader("user_id", "2989227905");
  
  delete  = new GetRequest("http://192.168.2.12:5000/catch/delete/");
  delete.addHeader("user_id", "2989227905");
}

void draw() {
  get.send();
  String jsons_string = get.getContent();
  
  try {
    jsons = parseJSONArray(jsons_string);
    println(jsons_string);
  } catch (Exception  e) {
    delay(1000);
    return;
  }
  
  int index = jsons.getJSONObject(0).getInt("index");
  delete.addHeader("index", str(index));
  delete.send();
  
  send("-42,579,");
  for (int i=1; i<jsons.size(); i++) {
    JSONObject from_server = jsons.getJSONObject(i);
    String     to_serial   = get(from_server);
    send(to_serial);
    delay(200);
  }
  send("-108,29,");
  delay(500);
}
/*

*/
String get(JSONObject from_server) {
  String to_serial = 
  int(430 - from_server.getInt("top") / 9.8 * 4) * -1
  + "," 
  + int(1550 - from_server.getInt("left") / 30 * 15.3)
  + ",";
  println(to_serial);
  return to_serial;
}

void send(String to_serial) {
  for (int i=0; i<to_serial.length(); i++) {
    int ascii = to_serial.charAt(i);
    arduino.write(ascii);
  }
}