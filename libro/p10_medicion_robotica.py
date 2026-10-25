from p_base import *
CAT = 'Medición y ciencia'

P('Voltímetro de 0 a 5 V', CAT, 1, ['voltimetro','medir voltaje','voltios','multimetro'],
  'El Arduino mide el voltaje de la perilla y lo muestra en voltios con dos decimales.',
  [C('pot', 'Perilla (voltaje a medir)', w='A0')],
  '''
void setup() {
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(A0);
  float voltios = lectura * 5.0 / 1023.0;
  Serial.print("Lectura: "); Serial.print(lectura);
  Serial.print("   Voltaje: "); Serial.print(voltios, 2); Serial.println(" V");
  delay(500);
}
''', 'El convertidor del Arduino divide 5 V en 1024 partes. Multiplicando por 5 y dividiendo por 1023 se pasa del número al voltaje real.',
  'Muestra una alerta si el voltaje pasa de 4 V.', notas=['Nunca midas más de 5 V directamente en una entrada analógica.'])

P('Voltímetro con pantalla LCD', CAT, 2, ['voltimetro lcd','medidor de voltaje lcd','barra de voltaje'],
  'Muestra el voltaje en la LCD con una barra que crece.',
  [C('pot', 'Perilla', w='A0'), C('lcd', 'Pantalla LCD')],
  LCD_INC + '''
void setup() {
  lcd.init(); lcd.backlight();
}

void loop() {
  float v = analogRead(A0) * 5.0 / 1023.0;
  int barras = v * 16 / 5;
  lcd.setCursor(0, 0); lcd.print("Voltaje: "); lcd.print(v, 2); lcd.print(" V ");
  lcd.setCursor(0, 1);
  for (int i = 0; i < 16; i++) lcd.print(i < barras ? "#" : " ");
  delay(200);
}
''', 'La barra tiene 16 casillas: 5 V las llena todas. El número de casillas encendidas es proporcional al voltaje.',
  'Haz que suene un pitido al llegar a 5 V.')

P('Amperímetro con ACS712 y LCD', CAT, 3, ['amperimetro','corriente lcd','acs712 lcd','medidor de corriente'],
  'Mide la corriente que pasa por el sensor ACS712 y la muestra en la LCD.',
  [C('acs712', 'Sensor de corriente', o='A0'), C('lcd', 'Pantalla LCD')],
  LCD_INC + '''
void setup() {
  lcd.init(); lcd.backlight();
  lcd.print("Amperimetro");
  delay(1000);
}

void loop() {
  long suma = 0;
  for (int i = 0; i < 50; i++) suma += analogRead(A0);
  float v = suma / 50.0 * 5.0 / 1023.0;
  float a = (v - 2.5) / 0.185;
  lcd.clear();
  lcd.print("I = "); lcd.print(a, 2); lcd.print(" A");
  lcd.setCursor(0, 1); lcd.print("Vout = "); lcd.print(v, 2);
  delay(500);
}
''', 'Se toman 50 lecturas y se promedian para que el número no salte. El ACS712 de 5 A cambia 0,185 V por cada amperio.',
  'Muestra también la corriente máxima medida.')

P('Termómetro con máximo y mínimo', CAT, 2, ['maxima y minima','registro de temperatura','temperatura extrema'],
  'Guarda la temperatura más alta y la más baja desde que se encendió.',
  [C('lm35', 'Sensor LM35', o='A0'), C('button', 'Borrar', x='D2')],
  '''
float maxima = -100, minima = 200;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  float t = analogRead(A0) * 500.0 / 1023.0;
  if (t > maxima) maxima = t;
  if (t < minima) minima = t;
  if (digitalRead(2) == LOW) { maxima = t; minima = t; }
  Serial.print("Ahora: "); Serial.print(t, 1);
  Serial.print("  Máx: "); Serial.print(maxima, 1);
  Serial.print("  Mín: "); Serial.println(minima, 1);
  delay(1000);
}
''', 'Las variables empiezan con valores imposibles para que la primera lectura las reemplace. Luego solo cambian si aparece un valor mayor o menor.',
  'Guarda también a qué segundo ocurrió el máximo.')

P('Cronómetro para experimentos', CAT, 2, ['cronometro','medir tiempo','experimento de fisica','caida libre'],
  'Un botón inicia y otro detiene el cronómetro, con precisión de milésimas de segundo.',
  [C('button', 'Iniciar', x='D2'), C('button', 'Detener', x='D3'), C('led', 'Corriendo', 'verde', a='D13')],
  '''
unsigned long inicio = 0;
bool corriendo = false;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP); pinMode(3, INPUT_PULLUP); pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(2) == LOW && !corriendo) { inicio = millis(); corriendo = true; digitalWrite(13, HIGH); }
  if (digitalRead(3) == LOW && corriendo) {
    corriendo = false; digitalWrite(13, LOW);
    float seg = (millis() - inicio) / 1000.0;
    Serial.print("Tiempo: "); Serial.print(seg, 3); Serial.println(" s");
  }
}
''', 'millis() cuenta los milisegundos desde que el Arduino se encendió. La resta entre el final y el inicio da la duración exacta.',
  'Usa dos sensores de obstáculos como barreras de inicio y llegada.')

P('Medidor de velocidad con dos sensores', CAT, 3, ['velocimetro','medir velocidad','fotopuerta','carro de juguete'],
  'Dos sensores infrarrojos separados 20 cm miden cuánto tarda un carrito en pasar y calculan su velocidad.',
  [C('obstaculo', 'Sensor de entrada', o='D2'), C('obstaculo', 'Sensor de salida', o='D3'), C('buzzer', 'Pitido', p='D8')],
  '''
const float DISTANCIA = 0.20;            // metros entre sensores

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT); pinMode(3, INPUT);
  Serial.println("Pasa el carrito por los sensores");
}

void loop() {
  if (digitalRead(2) == LOW) {
    unsigned long t0 = millis();
    while (digitalRead(3) == HIGH && millis() - t0 < 5000) {}
    float seg = (millis() - t0) / 1000.0;
    if (seg < 5) {
      float vel = DISTANCIA / seg;
      Serial.print("Velocidad: "); Serial.print(vel, 2); Serial.println(" m/s");
      tone(8, 1500, 150);
    }
    delay(1000);
  }
}
''', 'Velocidad = distancia ÷ tiempo. El primer sensor arranca el conteo y el segundo lo detiene; si en 5 segundos no pasa nada, se descarta.',
  'Convierte el resultado a km/h (multiplica por 3,6).')

P('Medidor de estatura', CAT, 2, ['estatura','medir altura','cuanto mido','sonar altura'],
  'El sensor ultrasónico en el techo mide la distancia a la cabeza y calcula la estatura.',
  [C('sonar', 'Sensor ultrasónico', t='D7', e='D6'), C('button', 'Medir', x='D2'), C('buzzer', 'Pitido', p='D8')],
  '''
const int ALTO_SENSOR = 220;             // cm del piso al sensor

long medir() {
  digitalWrite(7, LOW); delayMicroseconds(2);
  digitalWrite(7, HIGH); delayMicroseconds(10); digitalWrite(7, LOW);
  long cm = pulseIn(6, HIGH) / 58;
  return cm;
}

void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT); pinMode(6, INPUT); pinMode(2, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(2) == LOW) {
    long estatura = ALTO_SENSOR - medir();
    tone(8, 1500, 150);
    Serial.print("Tu estatura: "); Serial.print(estatura); Serial.println(" cm");
    delay(1000);
  }
}
''', 'El sensor mide la distancia de él hasta la cabeza. Restando eso de la altura a la que está el sensor se obtiene la estatura.',
  'Calcula el promedio de estatura del salón.')

P('Contador de vueltas con imán', CAT, 2, ['contador de vueltas','revoluciones','rpm','bicicleta'],
  'Un imán en la rueda pasa frente al sensor Hall; el Arduino cuenta vueltas y calcula las RPM.',
  [C('hall', 'Sensor Hall', o='D2'), C('led', 'Pulso', 'amarillo', a='D13')],
  '''
int vueltas = 0;
bool antes = HIGH;
unsigned long ultimoReporte = 0;
int vueltasAntes = 0;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT); pinMode(13, OUTPUT);
}

void loop() {
  bool ahora = digitalRead(2);
  if (antes == HIGH && ahora == LOW) { vueltas++; digitalWrite(13, HIGH); }
  else digitalWrite(13, LOW);
  antes = ahora;
  if (millis() - ultimoReporte >= 5000) {
    int rpm = (vueltas - vueltasAntes) * 12;   // 5 s × 12 = 1 minuto
    Serial.print("Vueltas: "); Serial.print(vueltas); Serial.print("   RPM: "); Serial.println(rpm);
    vueltasAntes = vueltas; ultimoReporte = millis();
  }
}
''', 'Cada vez que el imán pasa, la salida baja a LOW: eso es una vuelta. Las vueltas de 5 segundos multiplicadas por 12 dan las vueltas por minuto.',
  'Con el diámetro de la rueda, calcula los kilómetros recorridos.')

P('Experimento: luz y distancia', CAT, 2, ['experimento de luz','intensidad luminosa','ley inversa','ciencia'],
  'Mide cómo cambia la luz que recibe la fotorresistencia al alejar una linterna, y guarda los datos.',
  [C('ldr', 'Fotorresistencia', y='A0'), C('sonar', 'Sensor de distancia', t='D7', e='D6'), C('button', 'Tomar dato', x='D2')],
  '''
int dato = 0;

long medir() {
  digitalWrite(7, LOW); delayMicroseconds(2);
  digitalWrite(7, HIGH); delayMicroseconds(10); digitalWrite(7, LOW);
  long cm = pulseIn(6, HIGH) / 58;
  return cm;
}

void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT); pinMode(6, INPUT); pinMode(2, INPUT_PULLUP);
  Serial.println("dato, distancia_cm, luz");
}

void loop() {
  if (digitalRead(2) == LOW) {
    dato++;
    Serial.print(dato); Serial.print(", "); Serial.print(medir()); Serial.print(", "); Serial.println(analogRead(A0));
    delay(500);
  }
}
''', 'Los datos salen separados por comas: se pueden copiar a una hoja de cálculo y hacer una gráfica. Así se trabaja en un laboratorio de ciencias.',
  'Grafica tus datos y describe qué pasa con la luz al duplicar la distancia.')

P('Detector de terremotos (sismógrafo)', CAT, 2, ['sismografo','terremoto','temblor','alerta sismica'],
  'Cuenta las vibraciones por segundo; si son muchas, activa la alerta sísmica.',
  [C('vibracion', 'Sensor de vibración', o='D2'), C('buzzer', 'Alerta', p='D8'), C('led', 'Sismo', 'rojo', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT); pinMode(13, OUTPUT);
}

void loop() {
  int golpes = 0;
  unsigned long inicio = millis();
  while (millis() - inicio < 1000) {
    if (digitalRead(2) == HIGH) golpes++;
    delay(10);
  }
  Serial.print("Intensidad: "); Serial.println(golpes);
  if (golpes > 30) {
    Serial.println("¡ALERTA SÍSMICA!");
    for (int i = 0; i < 10; i++) { digitalWrite(13, HIGH); tone(8, 2200, 100); delay(150); digitalWrite(13, LOW); delay(100); }
  }
}
''', 'Un golpe aislado no es un sismo. Por eso se cuentan las vibraciones durante un segundo: solo una vibración sostenida activa la alerta.',
  'Muestra la intensidad con 3 LED (débil, medio, fuerte).')

CAT = 'Robótica y vehículos'

P('Carro que esquiva obstáculos', CAT, 3, ['carro evasor','robot esquiva obstaculos','robot autonomo','carrito'],
  'Un robot de dos motores avanza y, si encuentra algo a menos de 20 cm, gira para esquivarlo.',
  [C('sonar', 'Sensor ultrasónico', t='D7', e='D6'), C('motor', 'Motor izquierdo', p='D5'), C('motor', 'Motor derecho', p='D3')],
  '''
long medir() {
  digitalWrite(7, LOW); delayMicroseconds(2);
  digitalWrite(7, HIGH); delayMicroseconds(10); digitalWrite(7, LOW);
  long cm = pulseIn(6, HIGH) / 58;
  return cm;
}

void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT); pinMode(6, INPUT);
  pinMode(5, OUTPUT); pinMode(3, OUTPUT);
}

void loop() {
  long d = medir();
  if (d > 20) {
    analogWrite(5, 200); analogWrite(3, 200);       // adelante
  } else {
    Serial.println("Obstáculo: girando");
    analogWrite(5, 200); analogWrite(3, 0);         // gira a la derecha
    delay(600);
  }
  delay(50);
}
''', 'Para girar, un motor sigue andando y el otro se detiene. Así funcionan los robots con dos ruedas motrices (tracción diferencial).',
  'Haz que el robot retroceda antes de girar (necesitas un puente H como el L298N).',
  notas=['Un motor real no se conecta directo al pin: se usa un transistor o un módulo L298N.'], extra=['Chasis de robot con 2 ruedas', 'Portapilas de 4 AA'])

P('Robot seguidor de luz', CAT, 3, ['seguidor de luz','robot linterna','fototropismo','robot ldr'],
  'Dos fotorresistencias funcionan como ojos: el robot gira hacia el lado con más luz.',
  [C('ldr', 'Ojo izquierdo', y='A0'), C('ldr', 'Ojo derecho', y='A1'), C('motor', 'Motor izquierdo', p='D5'), C('motor', 'Motor derecho', p='D6')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(5, OUTPUT); pinMode(6, OUTPUT);
}

void loop() {
  int izq = analogRead(A0), der = analogRead(A1);
  if (izq > der + 50) { analogWrite(5, 80); analogWrite(6, 200); }        // más luz a la izquierda
  else if (der > izq + 50) { analogWrite(5, 200); analogWrite(6, 80); }   // más luz a la derecha
  else { analogWrite(5, 180); analogWrite(6, 180); }
  delay(50);
}
''', 'Para girar a la izquierda, la rueda izquierda va más despacio que la derecha. El margen de 50 evita que el robot tiemble cuando las dos luces son casi iguales.',
  'Haz que se detenga si hay demasiada luz (llegó a la meta).', notas=['Los motores se manejan con transistores o con un L298N.'], extra=['Chasis de robot con 2 ruedas'])

P('Robot seguidor de línea', CAT, 3, ['seguidor de linea','robot linea negra','sensor infrarrojo linea','competencia de robotica'],
  'Dos sensores infrarrojos miran el piso y el robot corrige su rumbo para seguir una línea negra.',
  [C('obstaculo', 'Sensor IR izquierdo', o='D2'), C('obstaculo', 'Sensor IR derecho', o='D4'), C('motor', 'Motor izquierdo', p='D5'), C('motor', 'Motor derecho', p='D6')],
  '''
void setup() {
  pinMode(2, INPUT); pinMode(4, INPUT);
  pinMode(5, OUTPUT); pinMode(6, OUTPUT);
}

void loop() {
  bool izqBlanco = digitalRead(2) == LOW;   // el blanco refleja la luz
  bool derBlanco = digitalRead(4) == LOW;
  if (izqBlanco && derBlanco) { analogWrite(5, 180); analogWrite(6, 180); }   // línea al centro
  else if (!izqBlanco) { analogWrite(5, 0); analogWrite(6, 180); }           // la línea está a la izquierda
  else if (!derBlanco) { analogWrite(5, 180); analogWrite(6, 0); }           // la línea está a la derecha
}
''', 'El blanco refleja la luz infrarroja y el negro la absorbe. Si un sensor ve negro, el robot gira hacia ese lado para volver a centrar la línea.',
  'Agrega un sensor ultrasónico para detenerse si hay algo en el camino.', notas=['Los motores se manejan con transistores o con un L298N.'], extra=['Cinta aislante negra para la pista'])

P('Grúa con joystick', CAT, 3, ['grua','joystick servos','pinza','brazo grua'],
  'Una grúa: el joystick gira la base (servo 1) y sube o baja el brazo (servo 2); el botón abre y cierra la pinza.',
  [C('joystick', 'Joystick', x='A0', y='A1', s='D2'), C('servo', 'Base', s='D9'), C('servo', 'Brazo', s='D10'), C('servo', 'Pinza', s='D11'), C('supply', 'Fuente 5 V para servos')],
  SERVO_INC + '''Servo base, brazo, pinza;
bool cerrada = false;

void setup() {
  base.attach(9); brazo.attach(10); pinza.attach(11);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  base.write(map(analogRead(A0), 0, 1023, 0, 180));
  brazo.write(map(analogRead(A1), 0, 1023, 30, 150));
  if (digitalRead(2) == LOW) {
    cerrada = !cerrada;
    pinza.write(cerrada ? 90 : 10);
    delay(300);
  }
  delay(20);
}
''', 'Con map() cada eje del joystick se convierte en un ángulo. El botón del joystick (al presionarlo hacia abajo) alterna la pinza entre abierta y cerrada.',
  'Graba una secuencia de movimientos y repítela sola.', notas=['Tres servos consumen mucho: usa una fuente externa de 5 V con GND común.'])

P('Semáforo para pista de carritos', CAT, 2, ['largada','semaforo de carreras','formula 1','salida de carrera'],
  'Un semáforo de largada como en la Fórmula 1: 3 luces rojas se encienden y al apagarse... ¡salida!',
  [C('button', 'Iniciar', x='D2'), C('led', 'Rojo 1', 'rojo', a='D11'), C('led', 'Rojo 2', 'rojo', a='D12'), C('led', 'Rojo 3', 'rojo', a='D13'), C('led', 'Salida', 'verde', a='D10'), C('buzzer', 'Pito', p='D8')],
  '''
void setup() {
  pinMode(2, INPUT_PULLUP);
  for (int p = 10; p <= 13; p++) pinMode(p, OUTPUT);
  randomSeed(analogRead(A5));
}

void loop() {
  if (digitalRead(2) == HIGH) return;
  for (int p = 11; p <= 13; p++) { digitalWrite(p, HIGH); tone(8, 600, 150); delay(1000); }
  delay(random(500, 3000));             // espera al azar
  for (int p = 11; p <= 13; p++) digitalWrite(p, LOW);
  digitalWrite(10, HIGH); tone(8, 1500, 600);
  delay(3000);
  digitalWrite(10, LOW);
}
''', 'La espera al azar antes de la salida evita que los corredores adivinen el momento: hay que reaccionar a la luz.',
  'Agrega dos botones para detectar quién salió antes de tiempo.')

P('Radar de barrido con aviso de cercanía', CAT, 3, ['radar','sonar giratorio','barrido','servo sonar'],
  'El servo gira el sensor ultrasónico de lado a lado y el monitor muestra la distancia en cada ángulo, como un radar.',
  [C('servo', 'Base del radar', s='D9'), C('sonar', 'Sensor ultrasónico', t='D7', e='D6'), C('buzzer', 'Alerta', p='D8')],
  SERVO_INC + '''Servo radar;

long medir() {
  digitalWrite(7, LOW); delayMicroseconds(2);
  digitalWrite(7, HIGH); delayMicroseconds(10); digitalWrite(7, LOW);
  long cm = pulseIn(6, HIGH) / 58;
  return cm;
}

void barrer(int desde, int hasta, int paso) {
  for (int a = desde; a != hasta; a += paso) {
    radar.write(a);
    delay(30);
    long d = medir();
    Serial.print(a); Serial.print(" grados: "); Serial.print(d); Serial.println(" cm");
    if (d < 15) tone(8, 2000, 40);
  }
}

void setup() {
  Serial.begin(9600);
  radar.attach(9);
  pinMode(7, OUTPUT); pinMode(6, INPUT);
}

void loop() {
  barrer(0, 180, 10);
  barrer(180, 0, -10);
}
''', 'La función barrer() recibe desde dónde, hasta dónde y de a cuánto girar. Se usa dos veces: de ida y de vuelta.',
  'Muestra en la LCD el ángulo del objeto más cercano.')

P('Robot mascota que reacciona', CAT, 2, ['robot mascota','robot emocional','mascota electronica','tamagotchi'],
  'Una mascota robot: si la acaricias (sensor táctil) mueve la cola y canta; si alguien se acerca mucho, se asusta.',
  [C('tactil', 'Cabeza (táctil)', o='D2'), C('sonar', 'Ojos (ultrasonido)', t='D7', e='D6'), C('servo', 'Cola', s='D9'), C('buzzer', 'Voz', p='D8'), C('rgb', 'Corazón', r='D3', g='D5', b='D11')],
  SERVO_INC + '''Servo cola;

long medir() {
  digitalWrite(7, LOW); delayMicroseconds(2);
  digitalWrite(7, HIGH); delayMicroseconds(10); digitalWrite(7, LOW);
  long cm = pulseIn(6, HIGH) / 58;
  return cm;
}

void color(int r, int g, int b) { analogWrite(3, r); analogWrite(5, g); analogWrite(11, b); }

void setup() {
  cola.attach(9);
  pinMode(2, INPUT); pinMode(7, OUTPUT); pinMode(6, INPUT);
}

void loop() {
  if (digitalRead(2) == HIGH) {                  // feliz
    color(0, 255, 0);
    for (int i = 0; i < 3; i++) { cola.write(60); tone(8, 1200, 80); delay(200); cola.write(120); tone(8, 1600, 80); delay(200); }
  } else if (medir() < 10) {                     // asustado
    color(255, 0, 0); tone(8, 300, 300); cola.write(90); delay(500);
  } else {                                       // tranquilo
    color(0, 0, 120); cola.write(90);
  }
  delay(100);
}
''', 'El robot tiene tres «estados de ánimo», cada uno con su color, sonido y movimiento. Elegir entre estados con if / else if es la base de muchos robots y videojuegos.',
  'Agrega un estado "aburrido" si nadie lo toca en 30 segundos.')
