from p_base import *
FP_NOTE = 'Las huellas se registran antes con el ejemplo «enroll» de Adafruit Fingerprint. En el simulador ya están guardadas las huellas 1, 2 y 3.'
RFID_NOTE = 'Para usar tu tarjeta, mira su código en el monitor serie y cámbialo en el programa.'

P('Doble factor: tarjeta y huella', 'Seguridad y control de acceso', 3, ['doble factor','tarjeta y huella','rfid huella','alta seguridad'],
  'Para abrir se necesitan dos cosas: primero la tarjeta autorizada y luego una huella registrada.',
  [C('rfid', 'Lector RFID', s='D10', r='D9'), C('huella', 'Lector de huellas', t='D2', r='D3'), C('led', 'Abierto', 'verde', a='D7'), C('buzzer', 'Pitido', p='D8')],
  RFID_INC + FP_INC + RFID_READ + FP_READ + '''bool tarjetaOk = false;
unsigned long cuando = 0;

void setup() {
  Serial.begin(9600);
  SPI.begin(); rfid.PCD_Init();
  finger.begin(57600);
  pinMode(7, OUTPUT);
  Serial.println("Paso 1: acerque la tarjeta");
}

void loop() {
  if (!tarjetaOk) {
    int r = leerTarjeta();
    if (r == 1) { tarjetaOk = true; cuando = millis(); tone(8, 1500, 100); Serial.println("Paso 2: ponga su dedo (10 s)"); }
    if (r == 0) tone(8, 300, 400);
    return;
  }
  int id = leerHuella();
  if (id > 0) {
    Serial.println("Acceso concedido");
    digitalWrite(7, HIGH); delay(3000); digitalWrite(7, LOW);
    tarjetaOk = false;
  } else if (id == 0 || millis() - cuando > 10000) {
    Serial.println("Acceso negado: empiece de nuevo");
    tone(8, 300, 600);
    tarjetaOk = false;
  }
}
''', 'Los bancos usan «doble factor»: algo que tienes (la tarjeta) y algo que eres (tu huella). Después de la tarjeta hay 10 segundos para poner el dedo; si no, todo vuelve a empezar.',
  'Agrega un teclado para una clave como tercer factor.', notas=[FP_NOTE, RFID_NOTE])

P('Alarma antirrobo para bicicleta', 'Seguridad y control de acceso', 2, ['alarma de bicicleta','alarma de moto','inclinacion alarma','antirrobo'],
  'Si alguien mueve o inclina la bicicleta estando la alarma armada, suena la sirena.',
  [C('inclinacion', 'Sensor de inclinación', o='D2'), C('switch', 'Armar alarma', x='D3'), C('buzzer', 'Sirena', p='D8'), C('led', 'Armada', 'rojo', a='D13')],
  '''
void setup() {
  pinMode(2, INPUT); pinMode(3, INPUT_PULLUP); pinMode(13, OUTPUT);
}

void loop() {
  bool armada = digitalRead(3) == LOW;
  digitalWrite(13, armada);
  if (armada && digitalRead(2) == HIGH) {
    for (int i = 0; i < 15; i++) { tone(8, 2000); delay(120); tone(8, 1300); delay(120); }
    noTone(8);
  }
}
''', 'El interruptor arma o desarma la alarma. Solo cuando está armada, un cambio en el sensor de inclinación dispara la sirena.',
  'Usa una tarjeta RFID para armar y desarmar.')

P('Contador de productos en banda', 'Medición y ciencia', 2, ['banda transportadora','contar objetos','sensor de obstaculos contador','fabrica'],
  'Como en una fábrica: el sensor infrarrojo cuenta cada producto que pasa y cada 10 suena un aviso de caja llena.',
  [C('obstaculo', 'Sensor IR', o='D2'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Caja llena', p='D8')],
  LCD_INC + '''int productos = 0;
bool antes = HIGH;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT);
  lcd.print("Productos: 0");
}

void loop() {
  bool ahora = digitalRead(2);
  if (antes == HIGH && ahora == LOW) {
    productos++;
    int cajas = productos / 10;
    lcd.clear();
    lcd.print("Productos: "); lcd.print(productos);
    lcd.setCursor(0, 1); lcd.print("Cajas: "); lcd.print(cajas);
    if (productos % 10 == 0) tone(8, 1500, 500);
  }
  antes = ahora;
}
''', 'Se cuenta solo el instante en que aparece el objeto (cambio de HIGH a LOW). La división entera entre 10 da las cajas completas y el residuo % dice si se acaba de llenar una.',
  'Agrega un servo que desvíe un producto de cada diez para control de calidad.')

P('Alcancía que cuenta monedas', 'Medición y ciencia', 2, ['alcancia','contar monedas','ahorro','banco de monedas'],
  'Cada moneda que cae interrumpe el sensor infrarrojo; la alcancía cuenta el ahorro en pesos.',
  [C('obstaculo', 'Sensor IR', o='D2'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Clinc', p='D8')],
  LCD_INC + '''long ahorro = 0;
const int VALOR = 500;                    // todas las monedas de 500

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT);
  lcd.print("Ahorro: $0");
}

void loop() {
  if (digitalRead(2) == LOW) {
    ahorro += VALOR;
    tone(8, 2500, 60);
    lcd.clear(); lcd.print("Ahorro: $"); lcd.print(ahorro);
    lcd.setCursor(0, 1); lcd.print(ahorro >= 10000 ? "Meta cumplida!" : "Sigue ahorrando");
    delay(300);
  }
}
''', 'Se usa long porque el ahorro puede pasar de 32 767, el número más grande que cabe en un int del Arduino UNO.',
  'Pon una meta con el teclado.')

P('Piano táctil de 3 notas', 'Sonido y música', 1, ['piano tactil','touch piano','sensor tactil musica'],
  'Tres sensores táctiles son las teclas de un pequeño piano.',
  [C('tactil', 'Do', o='D2'), C('tactil', 'Mi', o='D3'), C('tactil', 'Sol', o='D4'), C('buzzer', 'Parlante', p='D8')],
  '''
int notas[] = {262, 330, 392};

void setup() {
  for (int i = 2; i <= 4; i++) pinMode(i, INPUT);
}

void loop() {
  bool suena = false;
  for (int i = 0; i < 3; i++) {
    if (digitalRead(2 + i) == HIGH) { tone(8, notas[i]); suena = true; }
  }
  if (!suena) noTone(8);
}
''', 'El sensor táctil detecta el dedo sin necesidad de presionar. Cada sensor está asociado a una frecuencia del arreglo notas.',
  'Agrega una cuarta tecla y toca una canción.')

P('Monitor del clima con LCD y ventilador', 'Temperatura y clima', 3, ['clima lcd','temperatura humedad pantalla','dht11 lcd ventilador'],
  'La LCD muestra temperatura y humedad; el ventilador se enciende solo si hace calor.',
  [C('dht11', 'Sensor DHT11', d='D2'), C('lcd', 'Pantalla LCD'), C('motor', 'Ventilador', p='D6')],
  DHT_INC + LCD_INC + '''
void setup() {
  dht.begin();
  lcd.init(); lcd.backlight();
  pinMode(6, OUTPUT);
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (isnan(t) || isnan(h)) { lcd.clear(); lcd.print("Error sensor"); delay(2000); return; }
  bool calor = t > 28;
  digitalWrite(6, calor);
  lcd.clear();
  lcd.print("T: "); lcd.print(t, 1); lcd.print(" C");
  lcd.setCursor(0, 1); lcd.print("H: "); lcd.print(h, 0); lcd.print("%"); lcd.print(calor ? " VENT ON" : "");
  delay(2000);
}
''', 'isnan() revisa si la lectura falló (por ejemplo, un cable suelto) para mostrar un error en vez de números raros.',
  'Agrega un LED azul que avise si la humedad pasa del 80 %.')

P('Indicador de gas en LCD', 'Hogar y ambiente', 2, ['gas lcd','nivel de gas pantalla','mq2 lcd'],
  'La LCD muestra el nivel de gas con una barra y la palabra SEGURO o PELIGRO.',
  [C('gas', 'Sensor MQ-2', o='A0'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Alarma', p='D8')],
  LCD_INC + '''
void setup() {
  lcd.init(); lcd.backlight();
}

void loop() {
  int g = analogRead(A0);
  int barras = map(g, 0, 1023, 0, 16);
  lcd.clear();
  lcd.print(g > 400 ? "PELIGRO " : "SEGURO  "); lcd.print(g);
  lcd.setCursor(0, 1);
  for (int i = 0; i < barras; i++) lcd.print("#");
  if (g > 400) tone(8, 2000, 200);
  delay(500);
}
''', 'map() convierte la lectura (0 a 1023) en un número de casillas (0 a 16) para dibujar la barra.',
  'Guarda el valor más alto registrado.')

P('Nivel de tanque en LCD', 'Hogar y ambiente', 2, ['tanque lcd','nivel de agua pantalla','porcentaje tanque'],
  'La LCD muestra el porcentaje de agua del tanque y avisa cuando está casi vacío.',
  [C('nivel', 'Sensor de nivel', o='A0'), C('lcd', 'Pantalla LCD'), C('led', 'Casi vacío', 'rojo', a='D13')],
  LCD_INC + '''
void setup() {
  lcd.init(); lcd.backlight();
  pinMode(13, OUTPUT);
}

void loop() {
  int porc = constrain(map(analogRead(A0), 0, 650, 0, 100), 0, 100);
  lcd.clear();
  lcd.print("Tanque: "); lcd.print(porc); lcd.print(" %");
  lcd.setCursor(0, 1);
  if (porc < 15) { lcd.print("Casi vacio!"); digitalWrite(13, HIGH); }
  else { lcd.print("Nivel normal"); digitalWrite(13, LOW); }
  delay(1000);
}
''', 'constrain() asegura que el porcentaje nunca quede por debajo de 0 ni por encima de 100, aunque el sensor dé un valor raro.',
  'Agrega la bomba con relé para llenar el tanque.')

P('Detector de objetos con sensor IR', 'Distancia y movimiento', 1, ['sensor de obstaculos','infrarrojo','detector ir','objeto cerca'],
  'El sensor infrarrojo detecta si hay algo delante y enciende un LED.',
  [C('obstaculo', 'Sensor IR', o='D2'), C('led', 'Objeto', 'rojo', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT); pinMode(13, OUTPUT);
}

void loop() {
  bool hayAlgo = digitalRead(2) == LOW;
  digitalWrite(13, hayAlgo);
  if (hayAlgo) Serial.println("Objeto detectado");
  delay(200);
}
''', 'El sensor emite luz infrarroja (invisible) y mira si rebota. Si hay algo delante, la salida baja a LOW. El tornillo azul del sensor ajusta la distancia.',
  'Agrega un pitido que suene al detectar el objeto.')

P('Mano que saluda al acercarte', 'Servos y motores', 1, ['saludo automatico','mano robot','servo ir','hola'],
  'Cuando alguien se acerca, una mano de cartón en el servo saluda de lado a lado.',
  [C('obstaculo', 'Sensor IR', o='D2'), C('servo', 'Mano', s='D9')],
  SERVO_INC + '''Servo mano;

void setup() {
  pinMode(2, INPUT);
  mano.attach(9); mano.write(90);
}

void loop() {
  if (digitalRead(2) == LOW) {
    for (int i = 0; i < 3; i++) { mano.write(50); delay(250); mano.write(130); delay(250); }
    mano.write(90);
    delay(1000);
  }
}
''', 'El servo va de 50 a 130 grados tres veces, como una mano que saluda, y vuelve al centro.',
  'Haz que diga "hola" con una melodía en el buzzer.', extra=['Mano recortada en cartón'])
