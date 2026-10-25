from p_base import *
CAT = 'Hogar y ambiente'

P('Detector de fuga de gas en la cocina', CAT, 2, ['fuga de gas','cocina segura','mq2 alarma','detector de gas'],
  'El sensor MQ-2 vigila el aire de la cocina: si sube el gas, suena la alarma y se enciende el extractor.',
  [C('gas', 'Sensor de gas MQ-2', o='A0'), C('buzzer', 'Alarma', p='D8'), C('motor', 'Extractor', p='D6'), C('led', 'Peligro', 'rojo', a='D13')],
  '''
const int GAS = A0, LIMITE = 400;

void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT); pinMode(6, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  int nivel = analogRead(GAS);
  Serial.print("Gas: "); Serial.println(nivel);
  if (nivel > LIMITE) {
    digitalWrite(13, HIGH); digitalWrite(6, HIGH);
    tone(8, 2000, 200);
  } else {
    digitalWrite(13, LOW); digitalWrite(6, LOW);
  }
  delay(300);
}
''', 'El MQ-2 cambia su resistencia cuando hay gas o humo, y el Arduino lo lee como un número de 0 a 1023. Por encima del límite se enciende la alarma y el extractor saca el aire.',
  'Haz que la alarma siga sonando 10 segundos aunque el gas ya haya bajado.',
  notas=['El MQ-2 necesita calentarse 1 o 2 minutos antes de dar lecturas confiables.'])

P('Detector de incendio con llama', CAT, 1, ['sensor de llama','detector de fuego','incendio llama','fuego'],
  'Si el sensor ve una llama, suena la alarma de incendio.',
  [C('llama', 'Sensor de llama', o='D2'), C('buzzer', 'Alarma', p='D8'), C('led', 'Fuego', 'rojo', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT); pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(2) == LOW) {           // LOW = hay llama
    Serial.println("¡FUEGO!");
    digitalWrite(13, HIGH);
    tone(8, 2500, 150); delay(200);
    tone(8, 1500, 150); delay(200);
  } else {
    digitalWrite(13, LOW);
  }
}
''', 'El sensor de llama ve la luz infrarroja del fuego. Su salida DO baja a LOW cuando detecta una llama, por eso se pregunta por LOW.',
  'Agrega una bomba de agua que se encienda con el fuego.')

P('Bomba contra incendios automática', CAT, 3, ['bomba contra incendio','apagar fuego','rociador','sprinkler'],
  'Un rociador automático: si hay fuego, el relé enciende la bomba de 12 V hasta que la llama se apaga.',
  [C('llama', 'Sensor de llama', o='D2'), C('relay', 'Relé de la bomba', i='D7'), C('pump12', 'Bomba de agua 12 V'), C('supply12', 'Fuente 12 V'), C('buzzer', 'Alarma', p='D8')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT); pinMode(7, OUTPUT);
}

void loop() {
  if (digitalRead(2) == LOW) {
    Serial.println("Fuego: rociando agua");
    digitalWrite(7, HIGH);
    tone(8, 2000, 100);
  } else {
    digitalWrite(7, LOW);
  }
  delay(200);
}
''', 'La bomba trabaja a 12 V, así que el Arduino la controla con un relé. Mientras el sensor siga viendo la llama, la bomba sigue encendida.',
  'Deja la bomba encendida 5 segundos más después de que se apague el fuego.',
  notas=['La bomba va con su propia fuente de 12 V a través del relé; nunca la conectes al Arduino.'], extra=['Manguera delgada y recipiente con agua'])

P('Luz de pasillo con sensor de movimiento', CAT, 1, ['luz de pasillo','luz con movimiento','pir luz','escalera'],
  'Al pasar alguien, la luz del pasillo se enciende 10 segundos.',
  [C('pir', 'Sensor PIR', o='D2'), C('led', 'Luz del pasillo', 'blanco', a='D13')],
  '''
unsigned long ultimo = 0;

void setup() {
  pinMode(2, INPUT); pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(2) == HIGH) ultimo = millis();
  if (millis() - ultimo < 10000 && ultimo > 0) digitalWrite(13, HIGH);
  else digitalWrite(13, LOW);
}
''', 'Cada vez que el PIR detecta movimiento se guarda la hora en ultimo. La luz queda encendida mientras no hayan pasado 10 segundos desde el último movimiento.',
  'Haz que solo funcione de noche con una fotorresistencia.')

P('Luz nocturna inteligente', CAT, 2, ['luz nocturna','luz de noche con movimiento','ldr pir','ahorro de energia'],
  'La luz se enciende solo si es de noche y hay alguien pasando: así se ahorra energía.',
  [C('ldr', 'Fotorresistencia', y='A0'), C('pir', 'Sensor PIR', o='D2'), C('led', 'Luz', 'amarillo', a='D9')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT); pinMode(9, OUTPUT);
}

void loop() {
  int luz = analogRead(A0);
  bool oscuro = luz < 300;
  bool alguien = digitalRead(2) == HIGH;
  if (oscuro && alguien) { digitalWrite(9, HIGH); delay(5000); }
  else digitalWrite(9, LOW);
}
''', 'El operador && exige que las dos condiciones se cumplan a la vez: oscuridad y movimiento. Si falta cualquiera, la luz queda apagada.',
  'En vez de encender de golpe, usa analogWrite para que la luz suba despacio.')

P('Aplausos que encienden la luz', CAT, 2, ['aplauso luz','clap switch','encender con aplauso','sensor de sonido luz'],
  'Un aplauso enciende la luz y otro la apaga.',
  [C('sonido', 'Sensor de sonido', o='D2'), C('led', 'Lámpara', 'amarillo', a='D13')],
  '''
bool encendida = false;

void setup() {
  pinMode(2, INPUT); pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(2) == HIGH) {
    encendida = !encendida;
    digitalWrite(13, encendida);
    delay(500);                          // ignora el eco del aplauso
  }
}
''', 'El signo ! invierte el valor: si estaba encendida pasa a apagada y al revés. El delay de medio segundo evita que el mismo aplauso cuente dos veces.',
  'Haz que se necesiten dos aplausos seguidos para cambiar.')

P('Lámpara táctil', CAT, 1, ['lampara tactil','touch lampara','tocar para encender','ttp223'],
  'Toca el sensor para cambiar la lámpara entre apagada, baja, media y alta.',
  [C('tactil', 'Sensor táctil', o='D2'), C('led', 'Lámpara', 'blanco', a='D9')],
  '''
int nivel = 0;
int brillo[] = {0, 60, 150, 255};

void setup() {
  pinMode(2, INPUT); pinMode(9, OUTPUT);
}

void loop() {
  if (digitalRead(2) == HIGH) {
    nivel = (nivel + 1) % 4;
    analogWrite(9, brillo[nivel]);
    delay(400);
  }
}
''', 'El operador % (residuo) hace que el nivel vuelva a 0 después del 3. Con analogWrite en un pin PWM (~9) se logran brillos intermedios.',
  'Agrega un quinto nivel que haga parpadear la lámpara.')

P('Alarma de inundación', CAT, 1, ['inundacion','alarma de agua','nivel de agua alarma','sotano'],
  'Si el agua sube en el piso o el sótano, suena una alarma.',
  [C('nivel', 'Sensor de nivel de agua', o='A0'), C('buzzer', 'Alarma', p='D8'), C('led', 'Agua', 'azul', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  int agua = analogRead(A0);
  Serial.print("Agua: "); Serial.println(agua);
  if (agua > 200) { digitalWrite(13, HIGH); tone(8, 1800, 300); }
  else digitalWrite(13, LOW);
  delay(500);
}
''', 'El sensor de nivel tiene pistas metálicas: cuanto más mojadas, más corriente pasa y mayor es el número leído.',
  'Haz que el pitido sea más rápido cuanto más agua haya.')

P('Llenado automático de tanque con bomba', CAT, 3, ['llenar tanque','bomba tanque','control de nivel','tinaco'],
  'La bomba llena el tanque cuando el agua baja del 20 % y se apaga al llegar al 80 %.',
  [C('nivel', 'Sensor de nivel', o='A0'), C('relay', 'Relé de la bomba', i='D7'), C('pump12', 'Bomba de agua 12 V'), C('supply12', 'Fuente 12 V')],
  '''
bool llenando = false;

void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT);
}

void loop() {
  int porc = map(analogRead(A0), 0, 650, 0, 100);
  if (porc < 20) llenando = true;
  if (porc > 80) llenando = false;
  digitalWrite(7, llenando);
  Serial.print("Tanque: "); Serial.print(porc); Serial.println(llenando ? "%  llenando" : "%");
  delay(500);
}
''', 'Hay dos límites distintos (20 % y 80 %). Así la bomba no se prende y apaga a cada rato, sino que llena el tanque completo de una vez. Esto se llama histéresis.',
  'Muestra el nivel del tanque en una LCD.', notas=['La bomba usa la fuente de 12 V a través del relé.'])

P('Tendedero que avisa la lluvia', CAT, 2, ['tendedero','ropa lluvia','aviso de lluvia','recoger ropa'],
  'Si empieza a llover, suena un aviso para recoger la ropa y un servo cubre el tendedero.',
  [C('lluvia', 'Sensor de lluvia', o='A0'), C('servo', 'Techo', s='D9'), C('buzzer', 'Aviso', p='D8')],
  SERVO_INC + '''Servo techo;

void setup() {
  Serial.begin(9600);
  techo.attach(9); techo.write(0);
}

void loop() {
  int seco = analogRead(A0);              // 1023 seco, baja con agua
  if (seco < 600) {
    techo.write(120);
    tone(8, 1000, 200);
    Serial.println("¡Está lloviendo! Techo cerrado");
  } else {
    techo.write(0);
  }
  delay(1000);
}
''', 'El sensor de lluvia da un número alto cuando está seco. Cuando le caen gotas el número baja; por debajo de 600 el servo cierra el techo.',
  'Avisa solo una vez, no cada segundo.')

P('Ventilador de dos velocidades', CAT, 2, ['ventilador dos velocidades','ventilador automatico','temperatura motor','lm35 motor'],
  'Si hace calor el ventilador gira despacio; si hace mucho calor, a toda velocidad.',
  [C('lm35', 'Sensor LM35', o='A0'), C('motor', 'Ventilador', p='D6')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(6, OUTPUT);
}

void loop() {
  float temp = analogRead(A0) * 500.0 / 1023.0;
  Serial.print("Temperatura: "); Serial.println(temp, 1);
  if (temp > 32) analogWrite(6, 255);
  else if (temp > 27) analogWrite(6, 130);
  else analogWrite(6, 0);
  delay(1000);
}
''', 'El LM35 entrega 10 mV por cada grado. La fórmula convierte el número leído en °C, y según la temperatura se elige la velocidad con analogWrite.',
  'Agrega una tercera velocidad intermedia.')

P('Calentador con relé y termostato', CAT, 3, ['termostato','calentador','relé temperatura','calefaccion'],
  'Un termostato: el relé enciende el calentador por debajo de 22 °C y lo apaga por encima de 25 °C.',
  [C('dht11', 'Sensor DHT11', d='D2'), C('relay', 'Relé del calentador', i='D7'), C('led', 'Calentando', 'rojo', a='D13')],
  DHT_INC + '''bool calentando = false;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(7, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  float t = dht.readTemperature();
  if (isnan(t)) return;
  if (t < 22) calentando = true;
  if (t > 25) calentando = false;
  digitalWrite(7, calentando); digitalWrite(13, calentando);
  Serial.print(t, 1); Serial.println(calentando ? " °C - calentando" : " °C");
  delay(2000);
}
''', 'Como en el tanque, se usan dos límites para que el relé no se active y desactive a cada rato. Así funcionan los termostatos de las neveras y los hornos.',
  'Muestra la temperatura deseada en una LCD y cámbiala con botones.',
  notas=['Si vas a usar un calentador de 110 V, pide ayuda a un adulto o electricista: es corriente peligrosa.'])

P('Monitor de humedad para el baño', CAT, 2, ['humedad baño','extractor humedad','moho','dht11 motor'],
  'Si la humedad del baño pasa del 70 %, se enciende el extractor para evitar el moho.',
  [C('dht11', 'Sensor DHT11', d='D2'), C('motor', 'Extractor', p='D6')],
  DHT_INC + '''
void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(6, OUTPUT);
}

void loop() {
  float h = dht.readHumidity();
  if (isnan(h)) return;
  Serial.print("Humedad: "); Serial.print(h, 0); Serial.println(" %");
  digitalWrite(6, h > 70 ? HIGH : LOW);
  delay(2000);
}
''', 'El DHT11 mide la humedad relativa del aire. La expresión «condición ? A : B» elige A si la condición es verdadera y B si no.',
  'Agrega un LED que avise cuando el aire está muy seco (menos de 30 %).')

P('Recordatorio para regar la planta', CAT, 1, ['regar planta','planta sedienta','humedad de suelo led','maceta'],
  'La maceta avisa con luz roja cuando la tierra está seca y con verde cuando está bien.',
  [C('suelo', 'Sensor de humedad de suelo', o='A0'), C('led', 'Seca', 'rojo', a='D12'), C('led', 'Bien', 'verde', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  int lectura = analogRead(A0);          // alto = seco
  int humedad = map(lectura, 1000, 350, 0, 100);
  Serial.print("Humedad de la tierra: "); Serial.print(humedad); Serial.println(" %");
  digitalWrite(12, humedad < 30);
  digitalWrite(13, humedad >= 30);
  delay(1000);
}
''', 'El sensor de suelo da números altos cuando la tierra está seca. Con map() se convierte a un porcentaje fácil de entender.',
  'Haz que el LED rojo parpadee cuando la tierra esté muy seca (menos de 10 %).')

P('Cortina que abre con el sol', CAT, 2, ['cortina automatica','abrir con el sol','servo ldr','despertador de luz'],
  'Al amanecer el servo abre la cortina y al anochecer la cierra.',
  [C('ldr', 'Fotorresistencia', y='A0'), C('servo', 'Cortina', s='D9')],
  SERVO_INC + '''Servo cortina;

void setup() {
  Serial.begin(9600);
  cortina.attach(9);
}

void loop() {
  int luz = analogRead(A0);
  if (luz > 600) cortina.write(180);     // de día: abierta
  if (luz < 300) cortina.write(0);       // de noche: cerrada
  Serial.println(luz);
  delay(1000);
}
''', 'Entre 300 y 600 la cortina no se mueve: así no se abre y cierra con cada nube que pasa.',
  'Agrega un botón para abrirla a mano.')

P('Timbre con luz para personas sordas', CAT, 1, ['timbre visual','timbre con luz','accesibilidad','sordos'],
  'Al tocar el timbre, además del sonido parpadea una luz brillante, útil para personas con discapacidad auditiva.',
  [C('button', 'Timbre', x='D2'), C('buzzer', 'Sonido', p='D8'), C('led', 'Luz', 'blanco', a='D13')],
  '''
void setup() {
  pinMode(2, INPUT_PULLUP); pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(2) == LOW) {
    for (int i = 0; i < 6; i++) {
      digitalWrite(13, HIGH); tone(8, 1200, 120); delay(150);
      digitalWrite(13, LOW); delay(150);
    }
  }
}
''', 'La tecnología también sirve para incluir: el mismo aviso llega por dos sentidos, el oído y la vista.',
  'Agrega una vibración (motor) para quien está dormido.')

P('Pastillero con recordatorio', CAT, 2, ['pastillero','recordatorio de medicina','abuelos','alarma de medicina'],
  'Cada cierto tiempo suena un aviso para tomar la medicina; se apaga al presionar el botón.',
  [C('button', 'Ya la tomé', x='D2'), C('buzzer', 'Aviso', p='D8'), C('led', 'Medicina', 'azul', a='D13')],
  '''
const unsigned long CADA = 20000;        // 20 s para probar (8 horas = 28800000)
unsigned long ultima = 0;
bool avisando = false;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP); pinMode(13, OUTPUT);
}

void loop() {
  if (millis() - ultima > CADA) avisando = true;
  if (avisando) {
    digitalWrite(13, HIGH); tone(8, 1500, 100); delay(500);
    digitalWrite(13, LOW); delay(500);
    if (digitalRead(2) == LOW) { avisando = false; ultima = millis(); Serial.println("Medicina tomada"); }
  }
}
''', 'Con millis() se mide el tiempo sin detener el programa. Cuando pasan los milisegundos de CADA, empieza el aviso hasta que alguien presiona el botón.',
  'Cuenta cuántas dosis se han tomado en el día.')

P('Medidor de calidad del aire con semáforo', CAT, 2, ['calidad del aire','contaminacion','semaforo del aire','humo'],
  'Un semáforo indica si el aire está limpio (verde), regular (amarillo) o contaminado (rojo).',
  [C('gas', 'Sensor MQ-2', o='A0'), C('led', 'Limpio', 'verde', a='D11'), C('led', 'Regular', 'amarillo', a='D12'), C('led', 'Contaminado', 'rojo', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(11, OUTPUT); pinMode(12, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  int aire = analogRead(A0);
  Serial.print("Aire: "); Serial.println(aire);
  digitalWrite(11, aire < 250);
  digitalWrite(12, aire >= 250 && aire < 450);
  digitalWrite(13, aire >= 450);
  delay(500);
}
''', 'Cada LED recibe el resultado de una comparación: verdadero enciende, falso apaga. Solo una de las tres comparaciones es verdadera a la vez.',
  'Abre una ventana (servo) cuando el aire esté contaminado.')

P('Medidor de consumo de un aparato', CAT, 3, ['consumo electrico','medir corriente','acs712','cuanto gasta'],
  'Con el sensor ACS712 se mide cuánta corriente consume un aparato y se calcula su potencia.',
  [C('acs712', 'Sensor de corriente ACS712', o='A0'), C('led', 'Consumo alto', 'rojo', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  float voltios = analogRead(A0) * 5.0 / 1023.0;
  float amperios = (voltios - 2.5) / 0.185;
  if (amperios < 0) amperios = -amperios;
  float vatios = amperios * 12.0;        // aparato de 12 V
  Serial.print("Corriente: "); Serial.print(amperios, 2);
  Serial.print(" A   Potencia: "); Serial.print(vatios, 1); Serial.println(" W");
  digitalWrite(13, amperios > 2.0);
  delay(1000);
}
''', 'Sin corriente, el ACS712 entrega 2,5 V. Por cada amperio la salida cambia 0,185 V. La potencia es voltaje por corriente (P = V × I).',
  'Calcula cuánta energía (W·h) se ha gastado desde que se encendió.',
  notas=['La carga que se mide pasa por los dos tornillos azules del sensor. No midas aparatos de 110 V sin supervisión.'])

P('Casa inteligente con menú en LCD', CAT, 3, ['casa inteligente','domotica','smart home','panel de control'],
  'Un panel de la casa: la LCD muestra la temperatura y la luz, y con dos botones se encienden la sala y el ventilador.',
  [C('lcd', 'Pantalla LCD'), C('lm35', 'Sensor LM35', o='A0'), C('ldr', 'Fotorresistencia', y='A1'), C('button', 'Sala', x='D2'), C('button', 'Ventilador', x='D3'),
   C('led', 'Luz de la sala', 'amarillo', a='D12'), C('motor', 'Ventilador', p='D6')],
  LCD_INC + '''bool sala = false, venti = false;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT_PULLUP); pinMode(3, INPUT_PULLUP);
  pinMode(12, OUTPUT); pinMode(6, OUTPUT);
}

void loop() {
  if (digitalRead(2) == LOW) { sala = !sala; delay(300); }
  if (digitalRead(3) == LOW) { venti = !venti; delay(300); }
  digitalWrite(12, sala); digitalWrite(6, venti);
  int temp = analogRead(A0) * 500.0 / 1023;
  int luz = map(analogRead(A1), 0, 1023, 0, 100);
  lcd.setCursor(0, 0); lcd.print("T:"); lcd.print(temp); lcd.print("C Luz:"); lcd.print(luz); lcd.print("%  ");
  lcd.setCursor(0, 1); lcd.print(sala ? "Sala ON " : "Sala OFF"); lcd.print(venti ? " Ven ON " : " Ven OFF");
  delay(200);
}
''', 'Es una pequeña domótica: sensores para leer la casa, botones para dar órdenes y una pantalla para ver todo. Los espacios al final de cada texto borran restos de números anteriores.',
  'Haz que el ventilador se encienda solo si la temperatura pasa de 30 °C.')
