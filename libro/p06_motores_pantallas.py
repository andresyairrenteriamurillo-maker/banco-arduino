from p_base import *
CAT = 'Servos y motores'

P('Barrido de servo', CAT, 1, ['barrido de servo','servo basico','mover servo de lado a lado','limpiaparabrisas basico'],
  'El servo gira de 0 a 180 grados y regresa, una y otra vez.',
  [C('servo', 'Servo', s='D9')],
  SERVO_INC + '''Servo motor;

void setup() {
  motor.attach(9);
}

void loop() {
  for (int a = 0; a <= 180; a++) { motor.write(a); delay(10); }
  for (int a = 180; a >= 0; a--) { motor.write(a); delay(10); }
}
''', 'Un servo no gira libremente como un motor normal: va al ángulo exacto que le indiques. Avanzando de grado en grado se ve un movimiento suave.',
  'Haz que el barrido sea solo entre 30 y 150 grados.')

P('Puerta automática con botón', CAT, 1, ['puerta automatica','abrir puerta con boton','servo puerta','porton'],
  'Al presionar el botón la puerta (servo) se abre, espera 3 segundos y se cierra.',
  [C('button', 'Abrir', x='D2'), C('servo', 'Puerta', s='D9'), C('led', 'Puerta abierta', 'verde', a='D13')],
  SERVO_INC + '''Servo puerta;
const int BOTON = 2, LUZ = 13;

void setup() {
  puerta.attach(9);
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(LUZ, OUTPUT);
  puerta.write(0);           // cerrada
}

void loop() {
  if (digitalRead(BOTON) == LOW) {
    digitalWrite(LUZ, HIGH);
    puerta.write(90);        // abierta
    delay(3000);
    puerta.write(0);
    digitalWrite(LUZ, LOW);
  }
}
''', 'El servo representa el brazo que mueve la puerta: 0 grados es cerrada y 90 grados abierta. El LED verde avisa mientras está abierta.',
  'Haz que la puerta se cierre despacio, de grado en grado.')

P('Alimentador de mascotas con temporizador', CAT, 2, ['alimentador de mascotas','comida para perro','dispensador de comida','alimentador automatico'],
  'Cada cierto tiempo el servo abre la compuerta para soltar comida, y un pitido llama a la mascota.',
  [C('servo', 'Compuerta', s='D9'), C('buzzer', 'Llamado', p='D8'), C('button', 'Dar comida ya', x='D2')],
  SERVO_INC + '''Servo compuerta;
const unsigned long CADA = 20000;   // 20 s para probar (en la vida real: 8 horas)
unsigned long ultima = 0;

void servir() {
  tone(8, 1000, 200); delay(300); tone(8, 1300, 200);
  compuerta.write(80);   // abrir
  delay(1000);
  compuerta.write(0);    // cerrar
  ultima = millis();
  Serial.println("Comida servida");
}

void setup() {
  Serial.begin(9600);
  compuerta.attach(9);
  compuerta.write(0);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  if (millis() - ultima > CADA || digitalRead(2) == LOW) servir();
}
''', 'La función servir() hace todo el proceso: pitido, abrir, esperar y cerrar. Se llama cuando pasa el tiempo programado o cuando se presiona el botón.',
  'Cuenta cuántas porciones se han servido en el día.')

P('Limpiaparabrisas con sensor de lluvia', CAT, 2, ['limpiaparabrisas','lluvia y servo','plumillas','carro inteligente'],
  'Cuando el sensor detecta lluvia, el servo mueve el limpiaparabrisas; más lluvia, más rápido.',
  [C('lluvia', 'Sensor de lluvia', o='A0'), C('servo', 'Limpiaparabrisas', s='D9')],
  SERVO_INC + '''Servo plumilla;

void setup() {
  Serial.begin(9600);
  plumilla.attach(9);
}

void loop() {
  int lectura = analogRead(A0);          // seca ≈ 1020, mojada < 500
  if (lectura < 900) {
    int espera = map(lectura, 300, 900, 3, 15);   // más agua: menos espera
    espera = constrain(espera, 3, 15);
    for (int a = 0; a <= 150; a += 3) { plumilla.write(a); delay(espera); }
    for (int a = 150; a >= 0; a -= 3) { plumilla.write(a); delay(espera); }
  } else {
    plumilla.write(0);
  }
}
''', 'La placa del sensor tiene pistas separadas: el agua las une y baja la lectura analógica. Con menos lectura, el programa usa menos espera entre pasos y el servo va más rápido.',
  'Agrega un LED que indique si está lloviendo.')

P('Motor con botón de encendido', CAT, 1, ['motor con boton','encender motor','ventilador con boton'],
  'Un botón enciende y apaga un pequeño motor de ventilador.',
  [C('button', 'Encender', x='D2'), C('motor', 'Motor', p='D6')],
  '''
// Motor con botón de encendido
const int BOTON = 2, MOTOR = 6;
bool girando = false;
int anterior = HIGH;

void setup() {
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(MOTOR, OUTPUT);
}

void loop() {
  int ahora = digitalRead(BOTON);
  if (anterior == HIGH && ahora == LOW) {
    girando = !girando;
    if (girando) analogWrite(MOTOR, 200);
    else analogWrite(MOTOR, 0);
    delay(50);
  }
  anterior = ahora;
}
''', 'Es el mismo interruptor de un toque de la lámpara, pero ahora controla un motor con analogWrite() para poder elegir su velocidad.',
  'Agrega dos velocidades: un toque lenta, dos toques rápida.',
  notas=['Usa un transistor TIP120 y un diodo para conectar el motor en la vida real.'])

P('Bandera que saluda', CAT, 1, ['bandera','saludo con servo','mano que saluda','robot saluda'],
  'Un servo con una banderita la agita tres veces cada vez que presionas el botón.',
  [C('button', 'Saludar', x='D2'), C('servo', 'Brazo de la bandera', s='D9')],
  SERVO_INC + '''Servo brazo;

void setup() {
  brazo.attach(9);
  pinMode(2, INPUT_PULLUP);
  brazo.write(90);
}

void loop() {
  if (digitalRead(2) == LOW) {
    for (int i = 0; i < 3; i++) {
      brazo.write(50); delay(250);
      brazo.write(130); delay(250);
    }
    brazo.write(90);
  }
}
''', 'Alternando entre 50 y 130 grados el brazo se mueve de un lado al otro. Un ciclo for repite el movimiento tres veces.',
  'Haz que salude automáticamente cuando el PIR detecte a alguien.')

P('Reloj de arena con servo', CAT, 2, ['reloj de arena','temporizador con servo','aguja','minutero'],
  'Un servo funciona como aguja de un temporizador de 30 segundos: avanza poco a poco y al final suena una alarma.',
  [C('button', 'Iniciar', x='D2'), C('servo', 'Aguja', s='D9'), C('buzzer', 'Alarma', p='D8')],
  SERVO_INC + '''Servo aguja;
const int SEGUNDOS = 30;

void setup() {
  aguja.attach(9);
  pinMode(2, INPUT_PULLUP);
  aguja.write(0);
}

void loop() {
  if (digitalRead(2) == LOW) {
    for (int s = 0; s <= SEGUNDOS; s++) {
      aguja.write(map(s, 0, SEGUNDOS, 0, 180));   // la aguja avanza
      delay(1000);
    }
    for (int i = 0; i < 5; i++) { tone(8, 2000, 150); delay(300); }
    aguja.write(0);
  }
}
''', 'map() reparte los 180 grados del servo entre los 30 segundos: la aguja avanza 6 grados por segundo y llega al final justo cuando termina el tiempo.',
  'Usa una perilla para elegir la duración entre 10 y 60 segundos.')

P('Ventilador oscilante', CAT, 2, ['ventilador oscilante','ventilador que gira','oscilar','ventilador de pie'],
  'Un motor hace de ventilador y un servo lo gira de lado a lado para repartir el aire.',
  [C('motor', 'Aspas', p='D6'), C('servo', 'Oscilación', s='D9'), C('switch', 'Encendido', x='D2')],
  SERVO_INC + '''Servo giro;
int angulo = 45, paso = 1;

void setup() {
  giro.attach(9);
  pinMode(2, INPUT_PULLUP);
  pinMode(6, OUTPUT);
}

void loop() {
  if (digitalRead(2) == LOW) {          // interruptor activado
    analogWrite(6, 220);
    angulo += paso;
    if (angulo >= 135 || angulo <= 45) paso = -paso;   // cambiar de sentido
    giro.write(angulo);
    delay(30);
  } else {
    analogWrite(6, 0);
  }
}
''', 'La variable paso vale 1 o −1. Al llegar a un extremo se le cambia el signo y el servo empieza a moverse hacia el otro lado.',
  'Agrega una perilla para regular la velocidad de las aspas.')

P('Compuerta de riego con servo', CAT, 2, ['compuerta','riego con servo','valvula con servo','canal de agua'],
  'Si la tierra está seca, un servo abre la compuerta del agua; si está húmeda, la cierra.',
  [C('suelo', 'Sensor de humedad de suelo', o='A0'), C('servo', 'Compuerta', s='D9'), C('led', 'Regando', 'azul', a='D13')],
  SERVO_INC + '''Servo compuerta;

void setup() {
  Serial.begin(9600);
  compuerta.attach(9);
  pinMode(13, OUTPUT);
}

void loop() {
  int humedad = analogRead(A0);       // seco ≈ 1000, mojado ≈ 350
  Serial.println(humedad);
  if (humedad > 700) {                // tierra seca
    compuerta.write(90);
    digitalWrite(13, HIGH);
  } else if (humedad < 500) {         // tierra húmeda
    compuerta.write(0);
    digitalWrite(13, LOW);
  }
  delay(500);
}
''', 'Entre 500 y 700 el programa no cambia nada: deja la compuerta como estaba. Ese "espacio muerto" evita que la compuerta se abra y cierre sin parar.',
  'Muestra el porcentaje de humedad en una LCD.')

P('Seguidor de movimiento con servo', CAT, 3, ['cabeza que sigue','ojo robot','seguir a una persona','camara que sigue'],
  'Un servo gira hacia la izquierda o la derecha según cuál de dos sensores PIR detecte movimiento.',
  [C('pir', 'PIR izquierdo', o='D2'), C('pir', 'PIR derecho', o='D3'), C('servo', 'Cabeza', s='D9')],
  SERVO_INC + '''Servo cabeza;

void setup() {
  cabeza.attach(9);
  pinMode(2, INPUT); pinMode(3, INPUT);
  cabeza.write(90);
}

void loop() {
  bool izquierda = digitalRead(2) == HIGH;
  bool derecha = digitalRead(3) == HIGH;
  if (izquierda && !derecha) cabeza.write(150);
  else if (derecha && !izquierda) cabeza.write(30);
  else if (izquierda && derecha) cabeza.write(90);
  delay(200);
}
''', 'Con dos sensores apuntando a lados distintos, el programa compara cuál detecta movimiento y gira el servo hacia ese lado. Si los dos detectan, mira al centro.',
  'Haz que vuelva al centro si no hay movimiento durante 5 segundos.')

P('Mano robótica de un dedo', CAT, 2, ['mano robotica','dedo robot','flexion','protesis'],
  'Una perilla dobla y estira un dedo robótico movido por un servo, como una prótesis sencilla.',
  [C('pot', 'Control del dedo', w='A0'), C('servo', 'Dedo', s='D9'), C('led', 'Agarre', 'verde', a='D13')],
  SERVO_INC + '''Servo dedo;

void setup() {
  dedo.attach(9);
  pinMode(13, OUTPUT);
}

void loop() {
  int angulo = map(analogRead(A0), 0, 1023, 0, 160);
  dedo.write(angulo);
  digitalWrite(13, angulo > 120);     // el LED avisa cuando el dedo está cerrado
  delay(15);
}
''', 'Es la misma idea del servo con perilla, aplicada a un dedo hecho de cartón y un hilo atado al servo. El LED indica cuándo la mano está cerrada.',
  'Usa dos servos y dos perillas para mover dos dedos.',
  extra=['Cartón, pitillos e hilo para el dedo'])

P('Semáforo con barrera de tren', CAT, 3, ['paso a nivel','tren','barrera de tren','cruce ferroviario'],
  'Al detectar el tren, se encienden luces rojas intermitentes, suena una campana y baja la barrera.',
  [C('sonar', 'Detector del tren', t='D7', e='D6'), C('servo', 'Barrera', s='D9'), C('led', 'Luz izquierda', 'rojo', a='D12'), C('led', 'Luz derecha', 'rojo', a='D13'), C('buzzer', 'Campana', p='D8')],
  SERVO_INC + '''Servo barrera;
const int TRIG = 7, ECHO = 6;

long medir() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10); digitalWrite(TRIG, LOW);
  long cm = pulseIn(ECHO, HIGH) / 58;
  return cm;
}

void setup() {
  barrera.attach(9);
  barrera.write(90);                 // levantada
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  if (medir() < 30) {                // viene el tren
    barrera.write(0);                // bajar
    while (medir() < 30) {
      digitalWrite(12, HIGH); digitalWrite(13, LOW); tone(8, 900, 150); delay(400);
      digitalWrite(12, LOW); digitalWrite(13, HIGH); delay(400);
    }
    digitalWrite(13, LOW);
    delay(1500);
    barrera.write(90);               // subir cuando pasó
  }
}
''', 'Mientras el tren sigue frente al sensor, las dos luces rojas se alternan y la campana suena. Cuando ya pasó, la barrera vuelve a subir.',
  'Agrega una luz verde para los carros cuando la vía esté libre.')

CAT = 'Pantallas'

P('Hola mundo en la LCD', CAT, 1, ['hola mundo lcd','primer lcd','pantalla lcd basica','escribir en pantalla'],
  'Escribe un saludo en la pantalla LCD y un contador de segundos.',
  [C('lcd', 'Pantalla LCD')],
  LCD_INC + '''
void setup() {
  lcd.init();          // arranca la pantalla
  lcd.backlight();     // enciende la luz de fondo
  lcd.setCursor(0, 0); // columna 0, fila 0
  lcd.print("Hola, mundo!");
}

void loop() {
  lcd.setCursor(0, 1);
  lcd.print("Segundos: ");
  lcd.print(millis() / 1000);
  delay(200);
}
''', 'La LCD tiene 2 filas de 16 caracteres. setCursor() elige dónde escribir y print() escribe texto o números. millis() / 1000 da los segundos desde el encendido.',
  'Escribe tu nombre en la primera fila.')

P('Cronómetro con LCD y botones', CAT, 2, ['cronometro','cronometro lcd','medir tiempo','carrera'],
  'Un cronómetro con dos botones: iniciar/pausar y reiniciar. Muestra minutos, segundos y décimas.',
  [C('button', 'Iniciar / pausar', x='D2'), C('button', 'Reiniciar', x='D3'), C('lcd', 'Pantalla LCD')],
  LCD_INC + '''bool corriendo = false;
unsigned long acumulado = 0, inicio = 0;
int anterior = HIGH;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT_PULLUP); pinMode(3, INPUT_PULLUP);
  lcd.print("Cronometro");
}

void loop() {
  int ahora = digitalRead(2);
  if (anterior == HIGH && ahora == LOW) {
    if (corriendo) acumulado += millis() - inicio;
    else inicio = millis();
    corriendo = !corriendo;
    delay(50);
  }
  anterior = ahora;
  if (digitalRead(3) == LOW) { corriendo = false; acumulado = 0; }
  unsigned long t = acumulado;
  if (corriendo) t += millis() - inicio;
  int minutos = t / 60000;
  int segundos = (t / 1000) % 60;
  int decimas = (t / 100) % 10;
  lcd.setCursor(0, 1);
  if (minutos < 10) lcd.print("0");
  lcd.print(minutos); lcd.print(":");
  if (segundos < 10) lcd.print("0");
  lcd.print(segundos); lcd.print("."); lcd.print(decimas); lcd.print("   ");
  delay(50);
}
''', 'El tiempo se guarda en milisegundos. Para mostrarlo se separa en minutos, segundos y décimas con divisiones y el operador %, que da el residuo de una división.',
  'Agrega un tercer botón para guardar tiempos de vuelta.')

P('Mensaje que se desplaza', CAT, 2, ['mensaje desplazable','marquesina','texto en movimiento','letrero'],
  'Un letrero luminoso: el mensaje recorre la pantalla de derecha a izquierda.',
  [C('lcd', 'Pantalla LCD')],
  LCD_INC + '''String mensaje = "                Bienvenidos al laboratorio de Arduino!                ";
int pos = 0;

void setup() {
  lcd.init(); lcd.backlight();
  lcd.setCursor(0, 1);
  lcd.print("  ING. ARDUINO");
}

void loop() {
  lcd.setCursor(0, 0);
  lcd.print(mensaje.substring(pos, pos + 16));   // 16 letras desde pos
  pos++;
  if (pos > mensaje.length() - 16) pos = 0;
  delay(250);
}
''', 'substring() toma un pedazo del texto: 16 letras a partir de la posición pos. Como pos aumenta en cada vuelta, el pedazo visible se corre y parece que el texto se mueve.',
  'Escribe el mensaje del día de tu colegio.')

P('Contador de personas en el aula', CAT, 2, ['aforo','cupo del aula','contador de entrada y salida','capacidad maxima'],
  'Dos botones (entra / sale) llevan la cuenta de personas en el aula y avisan si se supera el cupo.',
  [C('button', 'Entra', x='D2'), C('button', 'Sale', x='D3'), C('lcd', 'Pantalla LCD'), C('led', 'Cupo lleno', 'rojo', a='D13')],
  LCD_INC + '''const int CUPO = 30;
int personas = 0;

void mostrar() {
  lcd.clear();
  lcd.print("Personas: "); lcd.print(personas);
  lcd.setCursor(0, 1);
  if (personas >= CUPO) lcd.print("CUPO LLENO");
  else { lcd.print("Libres: "); lcd.print(CUPO - personas); }
  digitalWrite(13, personas >= CUPO);
}

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT_PULLUP); pinMode(3, INPUT_PULLUP); pinMode(13, OUTPUT);
  mostrar();
}

void loop() {
  if (digitalRead(2) == LOW) { personas++; mostrar(); delay(300); }
  if (digitalRead(3) == LOW && personas > 0) { personas--; mostrar(); delay(300); }
}
''', 'La función mostrar() solo se llama cuando cambia la cuenta, así la pantalla no parpadea. Se revisa que personas sea mayor que 0 antes de restar.',
  'Cambia los botones por dos sensores infrarrojos en la puerta.')

P('Dado con pantalla', CAT, 1, ['dado lcd','dado en pantalla','numero al azar en pantalla'],
  'Presiona el botón y la LCD muestra el resultado de un dado de 6 caras.',
  [C('button', 'Lanzar', x='D2'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Sonido', p='D8')],
  LCD_INC + '''
void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT_PULLUP);
  lcd.print("Presiona el boton");
}

void loop() {
  if (digitalRead(2) == LOW) {
    for (int i = 0; i < 8; i++) {          // animación
      lcd.setCursor(0, 1); lcd.print("Rodando... "); lcd.print(random(1, 7));
      tone(8, 600 + i * 80, 40);
      delay(80);
    }
    int dado = random(1, 7);
    lcd.clear();
    lcd.print("Salio el:");
    lcd.setCursor(7, 1);
    lcd.print(dado);
    delay(500);
  }
}
''', 'La animación muestra números al azar con sonidos que suben, y al final se escribe el resultado definitivo centrado en la segunda fila.',
  'Haz un dado de 20 caras para juegos de rol.')

P('Nombre en la pantalla OLED', CAT, 2, ['oled','nombre en oled','pantalla oled basica','dibujar en pantalla'],
  'Escribe tu nombre en una pantalla OLED y dibuja un marco alrededor.',
  [C('oled', 'Pantalla OLED')],
  '''
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.drawRect(0, 0, 128, 64, SSD1306_WHITE);   // marco
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(16, 16);
  display.print("Hola,");
  display.setCursor(16, 36);
  display.print("Ana!");
  display.display();                                // mostrar lo dibujado
}

void loop() {
}
''', 'La OLED tiene 128 × 64 puntos. Primero se dibuja todo en la memoria (marco y texto) y display() lo envía a la pantalla de una sola vez.',
  'Dibuja una carita feliz con círculos.')

P('Reloj de juego de mesa', CAT, 2, ['reloj de ajedrez','turnos','reloj de dos jugadores','ajedrez'],
  'Un reloj de ajedrez: cada jugador tiene 2 minutos y presiona su botón al terminar su turno.',
  [C('button', 'Jugador 1', x='D2'), C('button', 'Jugador 2', x='D3'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Tiempo agotado', p='D8')],
  LCD_INC + '''long tiempo1 = 120000, tiempo2 = 120000;   // 2 minutos cada uno
int turno = 1;
unsigned long ultimo = 0;

void escribir(int fila, String nombre, long t) {
  lcd.setCursor(0, fila);
  int seg = t / 1000;
  int minutos = seg / 60;
  int resto = seg % 60;
  lcd.print(nombre); lcd.print(minutos); lcd.print(":");
  if (resto < 10) lcd.print("0");
  lcd.print(resto); lcd.print("  ");
}

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT_PULLUP); pinMode(3, INPUT_PULLUP);
  ultimo = millis();
}

void loop() {
  unsigned long ahora = millis();
  if (turno == 1) tiempo1 -= ahora - ultimo;
  else tiempo2 -= ahora - ultimo;
  ultimo = ahora;
  if (turno == 1 && digitalRead(2) == LOW) turno = 2;
  if (turno == 2 && digitalRead(3) == LOW) turno = 1;
  escribir(0, "Jugador 1: ", max(tiempo1, 0));
  escribir(1, "Jugador 2: ", max(tiempo2, 0));
  if (tiempo1 <= 0 || tiempo2 <= 0) {
    tone(8, 400, 1000);
    while (true) delay(1000);          // fin del juego
  }
  delay(100);
}
''', 'Solo el reloj del jugador que tiene el turno se descuenta. Cada vuelta del loop() resta el tiempo que pasó desde la vuelta anterior.',
  'Agrega 2 segundos de bonificación por cada jugada.')

P('Termómetro e higrómetro en OLED', CAT, 3, ['oled dht11','clima en oled','pantalla del clima'],
  'Muestra la temperatura y la humedad con números grandes en la pantalla OLED.',
  [C('dht11', 'Sensor DHT11', d='D2'), C('oled', 'Pantalla OLED')],
  DHT_INC + '''#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
  dht.begin();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);  display.print("Temperatura");
  display.setCursor(0, 34); display.print("Humedad");
  display.setTextSize(2);
  display.setCursor(0, 12); display.print(t, 0); display.print(" C");
  display.setCursor(0, 46); display.print(h, 0); display.print(" %");
  display.display();
  delay(2000);
}
''', 'setTextSize() cambia el tamaño de la letra: los títulos van pequeños (1) y los números grandes (2) para leerlos de lejos.',
  'Dibuja una barra que crezca con la humedad.')

P('Votación electrónica', CAT, 2, ['votacion','urna electronica','elecciones','votar'],
  'Tres botones para votar por tres candidatos; la LCD muestra los resultados al presionar el botón de cierre.',
  [C('button', 'Candidato A', x='D2'), C('button', 'Candidato B', x='D3'), C('button', 'Candidato C', x='D4'), C('button', 'Ver resultados', x='D5'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Confirmación', p='D8')],
  LCD_INC + '''int votos[] = {0, 0, 0};
String nombres[] = {"A", "B", "C"};

void setup() {
  lcd.init(); lcd.backlight();
  for (int p = 2; p <= 5; p++) pinMode(p, INPUT_PULLUP);
  lcd.print("Vote por A, B o C");
}

void loop() {
  for (int i = 0; i < 3; i++) {
    if (digitalRead(2 + i) == LOW) {
      votos[i]++;
      tone(8, 1200, 150);
      lcd.setCursor(0, 1); lcd.print("Voto registrado ");
      delay(1500);
      lcd.setCursor(0, 1); lcd.print("                ");
    }
  }
  if (digitalRead(5) == LOW) {
    lcd.clear();
    for (int i = 0; i < 3; i++) { lcd.print(nombres[i]); lcd.print(":"); lcd.print(votos[i]); lcd.print(" "); }
    delay(4000);
    lcd.clear(); lcd.print("Vote por A, B o C");
  }
}
''', 'Los votos se guardan en un arreglo: votos[0] es el candidato A, votos[1] el B y votos[2] el C. Los botones están en los pines 2, 3 y 4, por eso se usa 2 + i.',
  'Muestra quién va ganando.')

P('Calculadora de suma con teclado', CAT, 3, ['calculadora','sumar con teclado','teclado y lcd','operaciones'],
  'Escribe dos números con el teclado, presiona A para sumar y la LCD muestra el resultado.',
  [C('keypad', 'Teclado', **KP_PINS), C('lcd', 'Pantalla LCD')],
  KP_INC + LCD_INC + '''String numero1 = "", numero2 = "";
bool segundo = false;

void setup() {
  lcd.init(); lcd.backlight();
  lcd.print("Calculadora +");
}

void loop() {
  char tecla = teclado.getKey();
  if (!tecla) return;
  if (tecla >= '0' && tecla <= '9') {
    if (segundo) numero2 += tecla;
    else numero1 += tecla;
  } else if (tecla == 'A') {               // el signo +
    segundo = true;
  } else if (tecla == '#') {               // igual
    long r = numero1.toInt() + numero2.toInt();
    lcd.clear(); lcd.print(numero1 + "+" + numero2 + "=");
    lcd.setCursor(0, 1); lcd.print(r);
    numero1 = ""; numero2 = ""; segundo = false;
    return;
  } else if (tecla == '*') {               // borrar
    numero1 = ""; numero2 = ""; segundo = false;
  }
  lcd.clear();
  lcd.print(numero1);
  if (segundo) { lcd.print("+"); lcd.print(numero2); }
}
''', 'Los números se van armando como texto, tecla por tecla. Al presionar # se convierten a número con toInt() y se suman. La tecla A hace de signo más y * borra.',
  'Agrega resta con la tecla B y multiplicación con la C.')

P('Mi tarjeta de presentación en LCD', CAT, 1, ['tarjeta de presentacion','datos personales','mostrar informacion'],
  'La pantalla muestra, una tras otra, varias líneas con tus datos: nombre, curso y gusto favorito.',
  [C('lcd', 'Pantalla LCD')],
  LCD_INC + '''String lineas[] = {"Me llamo:", "Ana Martinez", "Curso:", "Noveno B", "Me gusta:", "la robotica!"};

void setup() {
  lcd.init(); lcd.backlight();
}

void loop() {
  for (int i = 0; i < 6; i += 2) {      // de dos en dos
    lcd.clear();
    lcd.print(lineas[i]);
    lcd.setCursor(0, 1);
    lcd.print(lineas[i + 1]);
    delay(2000);
  }
}
''', 'Los textos están en un arreglo de String. El ciclo los toma de dos en dos: el primero va en la fila de arriba y el segundo en la de abajo.',
  'Agrega dos pantallas más con tu comida y tu deporte favoritos.')
