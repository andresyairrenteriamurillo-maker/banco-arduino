from p_base import *

TM_INC = '#include <TM1637Display.h>\nTM1637Display display(2, 3);   // CLK en D2, DIO en D3\n'
MX_INC = '#include <LedControl.h>\nLedControl matriz = LedControl(12, 11, 10, 1);   // DIN, CLK, CS\n'
NP_INC = '#include <Adafruit_NeoPixel.h>\nAdafruit_NeoPixel anillo(12, 6, NEO_GRB + NEO_KHZ800);   // 12 LED en D6\n'
RTC_INC = '#include <RTClib.h>\nRTC_DS3231 rtc;   // SDA en A4, SCL en A5\n'
BT_INC = '#include <SoftwareSerial.h>\nSoftwareSerial bt(10, 11);   // TXD del HC-05 en D10, RXD en D11\n'
IR_INC = '#include <IRremote.hpp>\nconst int RECEPTOR = 11;\n'
DS_INC = '#include <OneWire.h>\n#include <DallasTemperature.h>\nOneWire oneWire(2);\nDallasTemperature sensores(&oneWire);\n'
HX_INC = '#include <HX711.h>\nHX711 balanza;   // DT en D3, SCK en D2\n'
SEGS_PINS = dict(a='D2', b='D3', c='D4', d='D5', e='D6', f='D7', g='D8', h='D9')

P('Contador en display de 7 segmentos', 'Pantallas', 2, ['7 segmentos','display de 7 segmentos','contador 0 a 9','digito'],
  'El display cuenta del 0 al 9, un número por segundo, encendiendo los segmentos correctos.',
  [C('seg7', 'Display de 7 segmentos', **SEGS_PINS)],
  '''
// Cada fila dice qué segmentos (a, b, c, d, e, f, g) se encienden para cada número
const byte DIGITOS[10][7] = {
  {1,1,1,1,1,1,0}, {0,1,1,0,0,0,0}, {1,1,0,1,1,0,1}, {1,1,1,1,0,0,1}, {0,1,1,0,0,1,1},
  {1,0,1,1,0,1,1}, {1,0,1,1,1,1,1}, {1,1,1,0,0,0,0}, {1,1,1,1,1,1,1}, {1,1,1,1,0,1,1}
};
const int PINES[7] = {2, 3, 4, 5, 6, 7, 8};   // a, b, c, d, e, f, g

void mostrar(int n) {
  for (int s = 0; s < 7; s++) digitalWrite(PINES[s], DIGITOS[n][s]);
}

void setup() {
  for (int s = 0; s < 7; s++) pinMode(PINES[s], OUTPUT);
  pinMode(9, OUTPUT);   // punto
}

void loop() {
  for (int n = 0; n < 10; n++) {
    mostrar(n);
    delay(1000);
  }
}
''', 'Un display de 7 segmentos son 7 LED en forma de 8. La tabla DIGITOS guarda, para cada número, cuáles se encienden (1) y cuáles no (0).',
  'Agrega un botón que sume uno cada vez que lo presionas.', notas=['En la vida real cada segmento lleva una resistencia de 220 Ω.'], extra=['8 resistencias de 220 Ω'])

P('Contador de visitas con display TM1637', 'Pantallas', 2, ['tm1637','4 digitos','contador de visitas','marcador'],
  'Cada vez que alguien presiona el botón, el display de 4 dígitos suma uno.',
  [C('tm1637', 'Display de 4 dígitos', c='D2', d='D3'), C('button', 'Contar', x='D4'), C('buzzer', 'Pitido', p='D8')],
  TM_INC + '''int visitas = 0;

void setup() {
  display.setBrightness(5);
  pinMode(4, INPUT_PULLUP);
  display.showNumberDec(0);
}

void loop() {
  if (digitalRead(4) == LOW) {
    visitas++;
    display.showNumberDec(visitas);
    tone(8, 1500, 60);
    delay(300);
  }
}
''', 'La librería TM1637Display se encarga de encender los segmentos: con showNumberDec() basta con darle el número.',
  'Agrega un segundo botón para restar.')

P('Cronómetro en display TM1637', 'Pantallas', 2, ['cronometro display','minutos y segundos','tm1637 reloj'],
  'Un cronómetro que muestra minutos y segundos con los dos puntos en el medio, como un reloj.',
  [C('tm1637', 'Display de 4 dígitos', c='D2', d='D3'), C('button', 'Iniciar / parar', x='D4')],
  TM_INC + '''bool corriendo = false;
unsigned long inicio = 0, acumulado = 0;

void setup() {
  display.setBrightness(7);
  pinMode(4, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(4) == LOW) {
    if (corriendo) acumulado += millis() - inicio;
    else inicio = millis();
    corriendo = !corriendo;
    delay(300);
  }
  unsigned long total = acumulado + (corriendo ? millis() - inicio : 0);
  int segundos = total / 1000;
  int minutos = segundos / 60;
  int mmss = minutos * 100 + segundos % 60;
  display.showNumberDecEx(mmss, 0b01000000, true);   // con los dos puntos
  delay(50);
}
''', 'El número 0412 se ve como 04:12. Con showNumberDecEx() y 0b01000000 se encienden los dos puntos del centro.',
  'Agrega un botón para volver a cero.')

P('Reloj digital con DS3231 y TM1637', 'Pantallas', 3, ['reloj digital','reloj','ds3231','hora en display'],
  'Un reloj de verdad: el DS3231 guarda la hora y el display la muestra con los dos puntos parpadeando.',
  [C('ds3231', 'Reloj DS3231'), C('tm1637', 'Display de 4 dígitos', c='D2', d='D3')],
  RTC_INC + TM_INC + '''
void setup() {
  Serial.begin(9600);
  display.setBrightness(5);
  if (!rtc.begin()) Serial.println("No encuentro el reloj");
  // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));   // quita las // una vez para poner la hora
}

void loop() {
  DateTime ahora = rtc.now();
  int hhmm = ahora.hour() * 100 + ahora.minute();
  bool puntos = ahora.second() % 2 == 0;
  display.showNumberDecEx(hhmm, puntos ? 0b01000000 : 0, true);
  delay(200);
}
''', 'El DS3231 tiene una pila: sigue contando la hora aunque desconectes el Arduino. rtc.now() la entrega con hour(), minute() y second().',
  'Agrega un zumbador que suene como alarma a una hora fija.', notas=['Para poner el reloj en hora, quita una vez las // de la línea rtc.adjust y sube el programa.'])

P('Carita feliz en matriz 8×8', 'Pantallas', 2, ['carita','matriz','8x8','emoji','dibujo con leds'],
  'La matriz de 64 LED dibuja una carita feliz y luego una triste, una y otra vez.',
  [C('max7219', 'Matriz 8×8', d='D12', c='D11', s='D10')],
  MX_INC + '''byte feliz[8] = {B00111100, B01000010, B10100101, B10000001, B10100101, B10011001, B01000010, B00111100};
byte triste[8] = {B00111100, B01000010, B10100101, B10000001, B10011001, B10100101, B01000010, B00111100};

void dibujar(byte img[]) {
  for (int fila = 0; fila < 8; fila++) matriz.setRow(0, fila, img[fila]);
}

void setup() {
  matriz.shutdown(0, false);    // despertar la matriz
  matriz.setIntensity(0, 8);    // brillo de 0 a 15
  matriz.clearDisplay(0);
}

void loop() {
  dibujar(feliz);
  delay(1500);
  dibujar(triste);
  delay(1500);
}
''', 'Cada fila de la imagen es un byte de 8 bits: cada 1 es un LED encendido. B00111100 enciende los 4 LED del centro.',
  'Dibuja un corazón y haz que parpadee.')

P('Flecha que se mueve en la matriz', 'Pantallas', 2, ['animacion','flecha','matriz animada','letrero'],
  'Una flecha recorre la matriz de izquierda a derecha, como un letrero luminoso.',
  [C('max7219', 'Matriz 8×8', d='D12', c='D11', s='D10'), C('pot', 'Velocidad', w='A0')],
  MX_INC + '''byte flecha[8] = {B00010000, B00110000, B01111111, B11111111, B01111111, B00110000, B00010000, B00000000};

void setup() {
  matriz.shutdown(0, false);
  matriz.setIntensity(0, 6);
}

void loop() {
  for (int x = -8; x < 8; x++) {
    for (int fila = 0; fila < 8; fila++) {
      int v = flecha[fila];
      if (x < 0) v = v << -x; else v = v >> x;
      matriz.setRow(0, fila, v & 255);
    }
    delay(map(analogRead(A0), 0, 1023, 40, 300));
  }
}
''', 'Mover los bits a la derecha (>>) desplaza el dibujo. La perilla cambia la pausa entre pasos, es decir, la velocidad.',
  'Haz que la flecha vaya y vuelva.')

P('Arcoíris en anillo NeoPixel', 'Luces y LED', 2, ['neopixel','arcoiris','anillo led','ws2812'],
  'Los 12 LED del anillo muestran todos los colores del arcoíris girando sin parar.',
  [C('neopixel', 'Anillo NeoPixel', i='D6')],
  NP_INC + '''long tono = 0;

void setup() {
  anillo.begin();
  anillo.setBrightness(80);
}

void loop() {
  for (int i = 0; i < 12; i++) {
    long h = tono + i * 65536 / 12;
    anillo.setPixelColor(i, anillo.ColorHSV(h));
  }
  anillo.show();
  tono += 1024;
  delay(30);
}
''', 'ColorHSV() convierte un tono (0 a 65535) en un color. Cada LED recibe un tono distinto y, al sumar un poco cada vez, el arcoíris gira.',
  'Usa un potenciómetro para cambiar la velocidad del giro.')

P('Ruleta de colores NeoPixel', 'Juegos', 2, ['ruleta neopixel','ruleta de colores','juego de luces'],
  'Presiona el botón: una luz gira por el anillo, frena poco a poco y se detiene en un color al azar.',
  [C('neopixel', 'Anillo NeoPixel', i='D6'), C('button', 'Girar', x='D2'), C('buzzer', 'Clic', p='D8')],
  NP_INC + '''
void setup() {
  anillo.begin();
  anillo.setBrightness(90);
  pinMode(2, INPUT_PULLUP);
  randomSeed(analogRead(A5));
}

void loop() {
  if (digitalRead(2) == HIGH) return;
  int pasos = random(24, 40), pausa = 20;
  for (int k = 0; k < pasos; k++) {
    anillo.clear();
    anillo.setPixelColor(k % 12, anillo.ColorHSV((k % 12) * 5461));
    anillo.show();
    tone(8, 1500, 8);
    delay(pausa);
    pausa += 6;
  }
  delay(2000);
}
''', 'La luz avanza un LED en cada paso y la pausa crece: por eso frena. Cada posición tiene su propio color.',
  'Asigna un premio a cada color.')

P('Motor paso a paso que gira 90°', 'Servos y motores', 2, ['paso a paso','stepper','28byj','girar angulo exacto'],
  'Cada vez que presionas el botón, el motor paso a paso gira exactamente un cuarto de vuelta.',
  [C('stepper', 'Motor paso a paso', a='D8', b='D9', c='D10', d='D11'), C('button', 'Girar', x='D2')],
  '''#include <Stepper.h>
const int PASOS_VUELTA = 2048;
Stepper motor(PASOS_VUELTA, 8, 10, 9, 11);   // IN1, IN3, IN2, IN4

void setup() {
  motor.setSpeed(12);   // vueltas por minuto
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(2) == LOW) {
    motor.step(PASOS_VUELTA / 4);   // 90 grados
  }
}
''', 'El 28BYJ-48 da 2048 pasos por vuelta: 512 pasos son 90°. A diferencia del servo, puede dar vueltas completas sin límite.',
  'Haz que con otro botón gire al revés (pasos negativos).', notas=['El orden en el código es IN1, IN3, IN2, IN4: así lo necesita este motor.'])

P('Carro adelante y atrás con L298N', 'Robótica y vehículos', 2, ['l298n','puente h','carro robot','sentido de giro'],
  'El motor avanza, frena y retrocede; la perilla controla la velocidad.',
  [C('l298n', 'Driver con motor', e='D5', a='D7', b='D8'), C('pot', 'Velocidad', w='A0')],
  '''
const int ENA = 5, IN1 = 7, IN2 = 8;

void mover(int sentido, int velocidad) {
  digitalWrite(IN1, sentido > 0 ? HIGH : LOW);
  digitalWrite(IN2, sentido < 0 ? HIGH : LOW);
  analogWrite(ENA, velocidad);
}

void setup() {
  Serial.begin(9600);
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
}

void loop() {
  int vel = map(analogRead(A0), 0, 1023, 0, 255);
  Serial.println("Adelante");  mover(1, vel);  delay(2000);
  Serial.println("Detenido");  mover(0, 0);    delay(800);
  Serial.println("Atrás");     mover(-1, vel); delay(2000);
  mover(0, 0); delay(800);
}
''', 'El L298N es un puente H: IN1 e IN2 deciden hacia dónde gira el motor y ENA, con analogWrite, qué tan rápido.',
  'Agrega un segundo motor para hacer un carro de dos ruedas.', notas=['En la vida real el motor se alimenta con pilas por los bornes del L298N y su GND se une con el del Arduino.'], extra=['Portapilas de 4 AA o batería de 9 V'])

P('Ventilador de mano con velocidad', 'Servos y motores', 1, ['ventilador','helice','l9110','velocidad del ventilador'],
  'Un ventilador con hélice cuya velocidad se regula con una perilla; un interruptor cambia el sentido.',
  [C('ventilador', 'Ventilador', a='D5', b='D6'), C('pot', 'Velocidad', w='A0'), C('switch', 'Sentido', x='D2')],
  '''
void setup() {
  pinMode(5, OUTPUT); pinMode(6, OUTPUT);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  int vel = map(analogRead(A0), 0, 1023, 0, 255);
  if (digitalRead(2) == HIGH) { analogWrite(5, vel); analogWrite(6, 0); }
  else { analogWrite(5, 0); analogWrite(6, vel); }
  delay(50);
}
''', 'El módulo L9110 tiene dos entradas: si INA recibe PWM e INB está en 0, gira hacia un lado; al revés, hacia el otro.',
  'Haz que el ventilador se encienda solo si hace calor (LM35).')

P('Luces con control remoto', 'Botones e interruptores', 2, ['control remoto','infrarrojo','irremote','luces con control'],
  'Con el control remoto de TV: el 1 enciende la luz roja, el 2 la verde, el 3 la azul y el 0 las apaga.',
  [C('irrx', 'Receptor IR', s='D11'), C('led', 'Roja', 'rojo', a='D4'), C('led', 'Verde', 'verde', a='D5'), C('led', 'Azul', 'azul', a='D6')],
  IR_INC + '''
void setup() {
  Serial.begin(9600);
  IrReceiver.begin(RECEPTOR);
  pinMode(4, OUTPUT); pinMode(5, OUTPUT); pinMode(6, OUTPUT);
}

void loop() {
  if (IrReceiver.decode()) {
    int tecla = IrReceiver.decodedIRData.command;
    Serial.print("Código: 0x"); Serial.println(tecla, HEX);
    if (tecla == 0x0C) digitalWrite(4, !digitalRead(4));   // botón 1
    if (tecla == 0x18) digitalWrite(5, !digitalRead(5));   // botón 2
    if (tecla == 0x5E) digitalWrite(6, !digitalRead(6));   // botón 3
    if (tecla == 0x16) { digitalWrite(4, LOW); digitalWrite(5, LOW); digitalWrite(6, LOW); }   // botón 0
    IrReceiver.resume();
  }
}
''', 'Cada botón del control envía un código distinto por luz infrarroja. El programa lo lee con decode() y decide qué LED cambiar.',
  'Usa los botones + y − para subir y bajar el brillo de un LED.', notas=['Si tu control es diferente, mira sus códigos en el monitor serie y cámbialos en el programa.'])

P('Encender un LED desde el celular (Bluetooth)', 'Hogar y ambiente', 2, ['bluetooth','celular','app','hc-05','domotica'],
  'Desde una app de Bluetooth en el celular: envía 1 para encender la luz y 0 para apagarla.',
  [C('hc05', 'Bluetooth HC-05', t='D10', r='D11'), C('led', 'Luz', 'amarillo', a='D13')],
  BT_INC + '''
void setup() {
  bt.begin(9600);
  pinMode(13, OUTPUT);
  bt.println("Hola! Envia 1 o 0");
}

void loop() {
  if (bt.available()) {
    char letra = bt.read();
    if (letra == '1') { digitalWrite(13, HIGH); bt.println("Luz encendida"); }
    if (letra == '0') { digitalWrite(13, LOW);  bt.println("Luz apagada"); }
  }
}
''', 'El HC-05 recibe por radio lo que manda el celular y se lo pasa al Arduino como si fuera el monitor serie. Con bt.println() el Arduino le responde.',
  'Agrega un relé para encender una lámpara de verdad.', notas=['En el celular usa una app como «Serial Bluetooth Terminal». La clave del HC-05 suele ser 1234.'])

P('Termómetro sumergible con LCD', 'Temperatura y clima', 2, ['ds18b20','temperatura del agua','termometro de piscina','acuario'],
  'La sonda DS18B20 mide la temperatura del agua y la LCD la muestra; si se calienta mucho, suena un aviso.',
  [C('ds18b20', 'Sonda DS18B20', d='D2'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Aviso', p='D8')],
  DS_INC + LCD_INC + '''
void setup() {
  sensores.begin();
  lcd.init(); lcd.backlight();
}

void loop() {
  sensores.requestTemperatures();
  float t = sensores.getTempCByIndex(0);
  lcd.clear();
  lcd.print("Agua: "); lcd.print(t, 1); lcd.print(" C");
  lcd.setCursor(0, 1);
  if (t > 40) { lcd.print("Muy caliente!"); tone(8, 1500, 200); }
  else lcd.print("Temperatura ok");
  delay(1000);
}
''', 'El DS18B20 habla por un solo cable (OneWire). requestTemperatures() pide la medida y getTempCByIndex(0) la entrega en °C.',
  'Úsalo para controlar el calentador de un acuario con un relé.', notas=['Entre el cable amarillo (DATA) y 5V va una resistencia de 4,7 kΩ.'], extra=['Resistencia de 4,7 kΩ'])

P('Balanza de cocina con LCD', 'Medición y ciencia', 3, ['balanza','bascula','peso','hx711','celda de carga'],
  'Una balanza digital: pon algo encima y la LCD muestra su peso en gramos. Un botón pone la balanza en cero (tara).',
  [C('hx711', 'Balanza HX711', d='D3', k='D2'), C('lcd', 'Pantalla LCD'), C('button', 'Tara', x='D4')],
  HX_INC + LCD_INC + '''
void setup() {
  lcd.init(); lcd.backlight();
  pinMode(4, INPUT_PULLUP);
  balanza.begin(3, 2);
  balanza.set_scale(420);   // número de calibración
  balanza.tare();           // poner en cero
}

void loop() {
  if (digitalRead(4) == LOW) { balanza.tare(); delay(300); }
  float gramos = balanza.get_units(5);
  lcd.clear();
  lcd.print("Peso:");
  lcd.setCursor(0, 1); lcd.print(gramos, 0); lcd.print(" g");
  delay(300);
}
''', 'La celda de carga se dobla un poquito con el peso y el HX711 mide ese cambio. set_scale() convierte la lectura en gramos y tare() resta el peso del plato.',
  'Muestra también el peso en libras.', notas=['El número de calibración (420) cambia en cada celda: pesa algo conocido y ajústalo.'])

P('Altímetro con barómetro BMP280', 'Medición y ciencia', 2, ['altimetro','barometro','bmp280','presion atmosferica','altura'],
  'El BMP280 mide la presión del aire y calcula a qué altura sobre el mar estás.',
  [C('bmp280', 'Barómetro BMP280'), C('lcd', 'Pantalla LCD')],
  '''#include <Adafruit_BMP280.h>
''' + LCD_INC + '''Adafruit_BMP280 bmp;

void setup() {
  Serial.begin(9600);
  lcd.init(); lcd.backlight();
  if (!bmp.begin(0x76)) lcd.print("Sin barometro");
}

void loop() {
  float presion = bmp.readPressure() / 100.0;     // hPa
  float altura = bmp.readAltitude(1013.25);       // metros
  lcd.clear();
  lcd.print(presion, 1); lcd.print(" hPa");
  lcd.setCursor(0, 1); lcd.print(altura, 0); lcd.print(" m");
  Serial.print("Temperatura: "); Serial.println(bmp.readTemperature(), 1);
  delay(1000);
}
''', 'Mientras más alto subes, menos aire hay encima y la presión baja. Con esa idea readAltitude() calcula la altura.',
  'Lleva el altímetro a un edificio y mide la altura de cada piso.')

P('Menú con perilla rotatoria', 'Botones e interruptores', 3, ['encoder','codificador rotatorio','menu','ky-040'],
  'Gira la perilla para recorrer un menú en la LCD y presiónala para elegir una opción.',
  [C('encoder', 'Perilla rotatoria', c='D2', d='D3', s='D4'), C('lcd', 'Pantalla LCD'), C('led', 'Luz', 'verde', a='D13')],
  LCD_INC + '''String opciones[] = {"Encender luz", "Apagar luz", "Parpadear"};
int opcion = 0;
int antes = HIGH;

void mostrar() {
  lcd.clear(); lcd.print("Menu:");
  lcd.setCursor(0, 1); lcd.print("> "); lcd.print(opciones[opcion]);
}

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT); pinMode(3, INPUT); pinMode(4, INPUT);
  pinMode(13, OUTPUT);
  mostrar();
}

void loop() {
  int clk = digitalRead(2);
  if (clk != antes && clk == LOW) {
    if (digitalRead(3) != clk) opcion = (opcion + 1) % 3;   // derecha
    else opcion = (opcion + 2) % 3;                         // izquierda
    mostrar();
  }
  antes = clk;
  if (digitalRead(4) == LOW) {
    if (opcion == 0) digitalWrite(13, HIGH);
    if (opcion == 1) digitalWrite(13, LOW);
    if (opcion == 2) for (int i = 0; i < 6; i++) { digitalWrite(13, i % 2); delay(200); }
    delay(300);
  }
}
''', 'El codificador da pulsos en CLK y DT. Cuando CLK baja, si DT es distinto, giró a la derecha; si es igual, a la izquierda. Así funcionan las perillas de los equipos de sonido.',
  'Agrega una cuarta opción al menú.')

P('Semáforo con módulo de 3 luces', 'Luces y LED', 1, ['modulo semaforo','semaforo','luces de transito'],
  'Un semáforo armado con el módulo que ya trae los tres LED y sus resistencias.',
  [C('semaforo', 'Módulo semáforo', r='D9', y='D10', v='D11')],
  '''
const int ROJO = 9, AMARILLO = 10, VERDE = 11;

void luz(int r, int a, int v, int tiempo) {
  digitalWrite(ROJO, r); digitalWrite(AMARILLO, a); digitalWrite(VERDE, v);
  delay(tiempo);
}

void setup() {
  pinMode(ROJO, OUTPUT); pinMode(AMARILLO, OUTPUT); pinMode(VERDE, OUTPUT);
}

void loop() {
  luz(0, 0, 1, 4000);   // verde
  luz(0, 1, 0, 1500);   // amarillo
  luz(1, 0, 0, 4000);   // rojo
}
''', 'La función luz() recibe qué luces encender y cuánto tiempo, así el loop() queda corto y fácil de leer.',
  'Agrega un botón de peatón.')

P('Alarma con barrera láser', 'Seguridad y control de acceso', 2, ['barrera laser','alarma laser','rayo laser','mision imposible'],
  'Un rayo láser apunta al receptor. Si alguien atraviesa el rayo, suena la alarma.',
  [C('laser', 'Láser', s='D7'), C('laserrx', 'Receptor láser', o='D2'), C('buzzer', 'Alarma', p='D8'), C('led', 'Alarma', 'rojo', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT); pinMode(2, INPUT); pinMode(13, OUTPUT);
  digitalWrite(7, HIGH);   // encender el láser
}

void loop() {
  if (digitalRead(2) == LOW) {        // el rayo se cortó
    Serial.println("¡Intruso cruzó el rayo!");
    for (int i = 0; i < 10; i++) { digitalWrite(13, HIGH); tone(8, 2200, 100); delay(150); digitalWrite(13, LOW); delay(100); }
  }
}
''', 'El receptor da HIGH mientras le llega la luz del láser. Si una persona pasa, el rayo se corta, la salida baja a LOW y se activa la alarma.',
  'Cuenta cuántas personas cruzan la barrera.', notas=['Nunca mires el láser directamente ni lo apuntes a los ojos.', 'En el simulador desmarca «Le llega el rayo láser» para simular que alguien lo corta.'])

P('Alcoholímetro con semáforo', 'Medición y ciencia', 2, ['alcoholimetro','alcohol','mq-3','aliento'],
  'Sopla cerca del sensor MQ-3: verde si no hay alcohol, amarillo si hay poco y rojo si hay mucho.',
  [C('mq3', 'Sensor MQ-3', o='A0'), C('led', 'Bien', 'verde', a='D11'), C('led', 'Cuidado', 'amarillo', a='D12'), C('led', 'Peligro', 'rojo', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(11, OUTPUT); pinMode(12, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  int alcohol = analogRead(A0);
  Serial.print("Alcohol: "); Serial.println(alcohol);
  digitalWrite(11, alcohol < 300);
  digitalWrite(12, alcohol >= 300 && alcohol < 600);
  digitalWrite(13, alcohol >= 600);
  delay(500);
}
''', 'El MQ-3 cambia su resistencia con el vapor de alcohol. Es un sensor educativo: no reemplaza a un alcoholímetro de la policía.',
  'Agrega una LCD que muestre un mensaje para cada nivel.', notas=['El MQ-3 necesita calentarse unos minutos antes de medir.'])

P('Monitor de pulso cardiaco', 'Medición y ciencia', 3, ['pulso','ritmo cardiaco','latidos','pulsaciones'],
  'Pon el dedo en el sensor: un LED parpadea con cada latido y el monitor muestra las pulsaciones por minuto.',
  [C('pulso', 'Sensor de pulso', o='A0'), C('led', 'Latido', 'rojo', a='D13'), C('buzzer', 'Bip', p='D8')],
  '''
const int UMBRAL = 600;
bool arriba = false;
unsigned long ultimo = 0;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  int senal = analogRead(A0);
  if (senal > UMBRAL && !arriba) {          // empieza un latido
    arriba = true;
    unsigned long ahora = millis();
    if (ultimo > 0) {
      int lpm = 60000 / (ahora - ultimo);
      Serial.print("Pulso: "); Serial.print(lpm); Serial.println(" lpm");
    }
    ultimo = ahora;
    digitalWrite(13, HIGH); tone(8, 1000, 30);
  }
  if (senal < UMBRAL - 50) { arriba = false; digitalWrite(13, LOW); }
}
''', 'Con cada latido llega más sangre al dedo y la señal sube. Midiendo el tiempo entre dos picos se calculan las pulsaciones por minuto: 60000 ÷ milisegundos.',
  'Muestra el pulso en una LCD y avisa si pasa de 120.', notas=['Es un proyecto educativo: no sirve para diagnósticos médicos.'])

P('Detector de metales', 'Medición y ciencia', 1, ['detector de metales','inductivo','metal','buscar metales'],
  'Acerca un objeto de metal a la punta del sensor inductivo: suena un pitido y se enciende la luz.',
  [C('inductivo', 'Sensor inductivo', o='D2'), C('buzzer', 'Pitido', p='D8'), C('led', 'Metal', 'amarillo', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT); pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(2) == LOW) {
    Serial.println("¡Metal detectado!");
    digitalWrite(13, HIGH); tone(8, 1800, 100); delay(150);
  } else {
    digitalWrite(13, LOW);
  }
}
''', 'El sensor inductivo crea un campo magnético en su punta; cuando entra un metal el campo cambia y la salida pasa a LOW.',
  'Cuenta cuántas latas pasan por una banda.', notas=['Los sensores inductivos reales suelen trabajar a 12 V; existen versiones de 5 V para Arduino.'])

P('Alarma de puerta con contacto magnético', 'Seguridad y control de acceso', 1, ['sensor de puerta','reed','contacto magnetico','alarma de puerta'],
  'Un imán en la puerta y el contacto reed en el marco: si la puerta se abre, suena la alarma.',
  [C('reed', 'Contacto magnético', o='D2'), C('buzzer', 'Alarma', p='D8'), C('led', 'Abierta', 'rojo', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT); pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(2) == HIGH) {         // el imán se alejó: puerta abierta
    digitalWrite(13, HIGH);
    tone(8, 2000, 150); delay(300);
  } else {
    digitalWrite(13, LOW);
  }
}
''', 'Dentro del reed hay dos láminas que se juntan con el imán. Con la puerta cerrada el imán está cerca (LOW); al abrirla, la salida pasa a HIGH.',
  'Agrega un teclado para desactivar la alarma con clave.', notas=['En el simulador, desmarca «Imán cerca» para abrir la puerta.'])

P('Riego con electroválvula', 'Hogar y ambiente', 3, ['electrovalvula','riego por goteo','valvula','riego automatico'],
  'El sensor capacitivo vigila la tierra: cuando está seca, el relé abre la electroválvula y pasa el agua.',
  [C('suelocap', 'Sensor de humedad', o='A0'), C('relay', 'Relé de la válvula', i='D7'), C('valve12', 'Electroválvula 12 V'), C('supply12', 'Fuente 12 V')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT);
}

void loop() {
  int lectura = analogRead(A0);                 // seco ≈ 620, mojado ≈ 290
  int humedad = map(lectura, 620, 290, 0, 100);
  Serial.print("Humedad: "); Serial.print(humedad); Serial.println(" %");
  if (humedad < 30) digitalWrite(7, HIGH);      // abrir el agua
  if (humedad > 60) digitalWrite(7, LOW);       // cerrar el agua
  delay(1000);
}
''', 'La electroválvula es una llave de agua eléctrica de 12 V. El relé la abre por debajo del 30 % y la cierra por encima del 60 %.',
  'Muestra la humedad en una LCD.', notas=['La válvula va con su fuente de 12 V a través del relé.'], extra=['Manguera y conexión a un tanque elevado'])

P('Ventilador de 12 V por temperatura', 'Temperatura y clima', 2, ['ventilador 12v','termistor','ntc','enfriar'],
  'El termistor NTC mide la temperatura; si pasa de 30 °C, el relé enciende un ventilador de 12 V.',
  [C('ntc', 'Termistor NTC', o='A0'), C('relay', 'Relé del ventilador', i='D7'), C('fan12', 'Ventilador 12 V'), C('supply12', 'Fuente 12 V')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT);
}

void loop() {
  int lectura = analogRead(A0);
  float r = 10000.0 * lectura / (1023.0 - lectura);                     // resistencia del NTC
  float c = 1.0 / (log(10000.0 / r) / 3950.0 + 1.0 / 298.15) - 273.15;  // fórmula Beta
  Serial.print("Temperatura: "); Serial.println(c, 1);
  digitalWrite(7, c > 30 ? HIGH : LOW);
  delay(1000);
}
''', 'El termistor cambia su resistencia con la temperatura. La «fórmula Beta» convierte esa resistencia en grados Celsius.',
  'Haz que el ventilador siga 1 minuto encendido después de bajar la temperatura.')

P('Calidad del agua: turbidez y pH', 'Medición y ciencia', 3, ['calidad del agua','turbidez','ph','agua potable'],
  'Dos sondas revisan el agua: la turbidez dice qué tan sucia está y el pH si es ácida o alcalina.',
  [C('turbidez', 'Sensor de turbidez', o='A0'), C('ph', 'Sensor de pH', o='A1'), C('led', 'Agua buena', 'verde', a='D12'), C('led', 'Agua mala', 'rojo', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  int claridad = analogRead(A0);                     // limpia ≈ 860
  float voltios = analogRead(A1) * 5.0 / 1023.0;
  float ph = 7 - (voltios - 2.5) / 0.18;
  Serial.print("Claridad: "); Serial.print(claridad);
  Serial.print("   pH: "); Serial.println(ph, 1);
  bool buena = claridad > 700 && ph > 6.5 && ph < 8.5;
  digitalWrite(12, buena); digitalWrite(13, !buena);
  delay(1000);
}
''', 'El agua para tomar debe ser clara y tener un pH entre 6,5 y 8,5. El programa revisa las dos condiciones a la vez con &&.',
  'Agrega el sensor TDS para medir las sales disueltas.', notas=['La sonda de pH real se calibra con soluciones de pH 4 y 7.'])

P('Guante robótico con sensor de flexión', 'Robótica y vehículos', 2, ['guante','flexion','mano robotica','servo con dedo'],
  'Al doblar el dedo con el sensor de flexión, el servo de una mano robótica se dobla igual.',
  [C('flex', 'Sensor de flexión', o='A0'), C('servo', 'Dedo robótico', s='D9')],
  SERVO_INC + '''Servo dedo;

void setup() {
  dedo.attach(9);
}

void loop() {
  int f = analogRead(A0);                       // derecho ≈ 300, doblado ≈ 720
  int angulo = constrain(map(f, 300, 720, 0, 180), 0, 180);
  dedo.write(angulo);
  delay(20);
}
''', 'El sensor de flexión aumenta su resistencia al doblarse. map() traduce esa lectura en un ángulo para el servo.',
  'Usa cinco sensores y cinco servos para una mano completa.', extra=['Guante de tela', 'Resistencia de 47 kΩ'])

P('Tapete que enciende la tira de LED', 'Hogar y ambiente', 2, ['tapete','fsr','presion','tira led','luz de bienvenida'],
  'Al pisar el tapete con el sensor de fuerza, se enciende una tira de LED de 12 V durante 10 segundos.',
  [C('fsr', 'Sensor de fuerza', o='A0'), C('relay', 'Relé de la tira', i='D7'), C('strip12', 'Tira de LED 12 V'), C('supply12', 'Fuente 12 V')],
  '''
unsigned long pisado = 0;

void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT);
}

void loop() {
  int fuerza = analogRead(A0);
  if (fuerza > 200) pisado = millis();
  bool encendida = pisado > 0 && millis() - pisado < 10000;
  digitalWrite(7, encendida);
  delay(100);
}
''', 'Cada pisada guarda la hora en pisado. La tira queda encendida mientras no hayan pasado 10 segundos desde la última pisada.',
  'Cuenta cuántas personas entran.')

P('Grúa con electroimán', 'Robótica y vehículos', 1, ['electroiman','grua magnetica','iman electrico','recoger metal'],
  'Mientras mantienes presionado el botón, el electroimán levanta clips y tornillos.',
  [C('electroiman', 'Electroimán', s='D7'), C('button', 'Atraer', x='D2')],
  '''
void setup() {
  pinMode(7, OUTPUT);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  digitalWrite(7, digitalRead(2) == LOW ? HIGH : LOW);
}
''', 'Un electroimán es una bobina de cable: con corriente se vuelve imán y sin corriente suelta lo que tenía.',
  'Monta el electroimán en un servo para mover las piezas de un lugar a otro.')

P('Luz con radar de presencia', 'Hogar y ambiente', 1, ['radar','rcwl-0516','presencia','luz automatica'],
  'El radar RCWL-0516 detecta a las personas incluso detrás de una puerta de madera y enciende la luz.',
  [C('radar', 'Radar de presencia', o='D2'), C('ledpow', 'Lámpara', s='D9')],
  '''
unsigned long ultimo = 0;

void setup() {
  pinMode(2, INPUT); pinMode(9, OUTPUT);
}

void loop() {
  if (digitalRead(2) == HIGH) ultimo = millis();
  if (ultimo > 0 && millis() - ultimo < 8000) analogWrite(9, 255);
  else analogWrite(9, 0);
}
''', 'El radar envía ondas de radio y nota cuando algo se mueve. A diferencia del PIR, atraviesa plástico y madera.',
  'Haz que la luz se apague poco a poco.')

P('Tacómetro con fotointerruptor', 'Medición y ciencia', 2, ['tacometro','rpm','fotointerruptor','contar vueltas'],
  'Una rueda con un agujero pasa por la ranura del sensor; el Arduino cuenta las vueltas por minuto.',
  [C('ranura', 'Fotointerruptor', o='D2'), C('lcd', 'Pantalla LCD')],
  LCD_INC + '''int vueltas = 0;
bool antes = LOW;
unsigned long inicio = 0;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT);
}

void loop() {
  bool ahora = digitalRead(2);
  if (ahora == HIGH && antes == LOW) vueltas++;
  antes = ahora;
  if (millis() - inicio >= 3000) {
    int rpm = vueltas * 20;            // 3 s × 20 = 1 minuto
    lcd.clear(); lcd.print("RPM: "); lcd.print(rpm);
    lcd.setCursor(0, 1); lcd.print("Vueltas: "); lcd.print(vueltas);
    vueltas = 0; inicio = millis();
  }
}
''', 'Cada vez que la rueda tapa la ranura, la salida sube a HIGH: eso es una vuelta. Las vueltas de 3 segundos por 20 dan las RPM.',
  'Muestra la velocidad en km/h de una bicicleta.')

P('Bastón que vibra cerca de obstáculos', 'Distancia y movimiento', 2, ['baston inteligente','vibracion','ciegos','obstaculos','accesibilidad'],
  'Un bastón para personas ciegas: el motor vibra más fuerte cuanto más cerca está un obstáculo.',
  [C('sonar', 'Sensor de distancia', t='D7', e='D6'), C('vibmotor', 'Motor de vibración', s='D5')],
  '''
long medir() {
  digitalWrite(7, LOW); delayMicroseconds(2);
  digitalWrite(7, HIGH); delayMicroseconds(10); digitalWrite(7, LOW);
  long cm = pulseIn(6, HIGH) / 58;
  return cm;
}

void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT); pinMode(6, INPUT); pinMode(5, OUTPUT);
}

void loop() {
  long d = medir();
  int fuerza = 0;
  if (d < 100) fuerza = map(d, 0, 100, 255, 60);
  analogWrite(5, fuerza);
  Serial.print(d); Serial.println(" cm");
  delay(100);
}
''', 'La tecnología puede ayudar a las personas: aquí la distancia se convierte en vibración, algo que se siente sin necesidad de ver.',
  'Agrega un zumbador que pite cuando el obstáculo esté a menos de 30 cm.')
