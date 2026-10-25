from p_base import *
CAT = 'Juegos'

P('Simón dice de 3 colores', CAT, 3, ['simon dice','juego de memoria','secuencia de colores','memoria'],
  'El Arduino muestra una secuencia de luces que crece cada ronda; repítela con los botones sin equivocarte.',
  [C('led', 'Rojo', 'rojo', a='D11'), C('led', 'Verde', 'verde', a='D12'), C('led', 'Azul', 'azul', a='D13'),
   C('button', 'Botón rojo', x='D2'), C('button', 'Botón verde', x='D3'), C('button', 'Botón azul', x='D4'), C('buzzer', 'Sonido', p='D8')],
  '''
int secuencia[20];
int largo = 0;
int leds[] = {11, 12, 13};
int botones[] = {2, 3, 4};
int tonos[] = {440, 660, 880};

void mostrar(int c) {
  digitalWrite(leds[c], HIGH); tone(8, tonos[c], 300); delay(400);
  digitalWrite(leds[c], LOW); delay(150);
}

int esperarBoton() {
  while (true) {
    for (int i = 0; i < 3; i++) {
      if (digitalRead(botones[i]) == LOW) { mostrar(i); return i; }
    }
  }
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 3; i++) { pinMode(leds[i], OUTPUT); pinMode(botones[i], INPUT_PULLUP); }
  randomSeed(analogRead(A5));
}

void loop() {
  secuencia[largo] = random(3);
  largo++;
  Serial.print("Ronda "); Serial.println(largo);
  for (int i = 0; i < largo; i++) mostrar(secuencia[i]);
  for (int i = 0; i < largo; i++) {
    if (esperarBoton() != secuencia[i]) {
      Serial.print("Perdiste. Llegaste a la ronda "); Serial.println(largo);
      tone(8, 150, 1000); delay(1500);
      largo = 0;
      return;
    }
  }
  delay(600);
}
''', 'La secuencia se guarda en un arreglo y crece un color en cada ronda. Luego el programa espera tus botones y los compara uno por uno con lo guardado.',
  'Agrega un cuarto color y un récord.')

P('Adivina el número', CAT, 2, ['adivina el numero','numero secreto','juego de adivinar','mayor o menor'],
  'El Arduino piensa un número del 1 al 9; escríbelo en el teclado y te dice si es mayor o menor.',
  [C('keypad', 'Teclado', **KP_PINS), C('led', 'Más alto', 'amarillo', a='D11'), C('led', 'Más bajo', 'azul', a='D12'), C('led', 'Correcto', 'verde', a='D13')],
  KP_INC + '''int secreto, intentos = 0;

void setup() {
  Serial.begin(9600);
  pinMode(11, OUTPUT); pinMode(12, OUTPUT); pinMode(13, OUTPUT);
  randomSeed(analogRead(A5));
  secreto = random(1, 10);
  Serial.println("Pensé un número del 1 al 9");
}

void loop() {
  char t = teclado.getKey();
  if (t < '1' || t > '9') return;
  int n = t - '0';
  intentos++;
  digitalWrite(11, LOW); digitalWrite(12, LOW);
  if (n < secreto) { Serial.println("Es más alto"); digitalWrite(11, HIGH); }
  else if (n > secreto) { Serial.println("Es más bajo"); digitalWrite(12, HIGH); }
  else {
    Serial.print("¡Correcto! en "); Serial.print(intentos); Serial.println(" intentos");
    digitalWrite(13, HIGH); delay(2000); digitalWrite(13, LOW);
    secreto = random(1, 10); intentos = 0;
  }
}
''', 'Restar el carácter \'0\' convierte la tecla en número: \'7\' − \'0\' = 7. Cada intento enciende la luz que da la pista.',
  'Amplía el juego del 1 al 99 usando dos teclas.')

P('Ruleta de la suerte', CAT, 1, ['ruleta','ruleta de leds','suerte','girar'],
  'Presiona el botón y la luz gira por 5 LED cada vez más lento hasta detenerse en uno al azar.',
  [C('button', 'Girar', x='D2'), C('led', 'L1', 'rojo', a='D9'), C('led', 'L2', 'amarillo', a='D10'), C('led', 'L3', 'verde', a='D11'),
   C('led', 'L4', 'azul', a='D12'), C('led', 'L5', 'blanco', a='D13'), C('buzzer', 'Clic', p='D8')],
  '''
void setup() {
  pinMode(2, INPUT_PULLUP);
  for (int p = 9; p <= 13; p++) pinMode(p, OUTPUT);
  randomSeed(analogRead(A5));
}

void loop() {
  if (digitalRead(2) == HIGH) return;
  int vueltas = random(15, 30);
  int pausa = 30;
  for (int i = 0; i < vueltas; i++) {
    int p = 9 + i % 5;
    digitalWrite(p, HIGH); tone(8, 1500, 10); delay(pausa);
    digitalWrite(p, LOW);
    pausa += 10;
  }
  digitalWrite(9 + (vueltas - 1) % 5, HIGH);
  delay(2000);
  digitalWrite(9 + (vueltas - 1) % 5, LOW);
}
''', 'La pausa crece en cada paso, por eso la ruleta frena poco a poco. El número de vueltas es aleatorio, así nadie sabe dónde parará.',
  'Asigna un premio a cada color y muéstralo en el monitor.')

P('Piedra, papel o tijera', CAT, 2, ['piedra papel tijera','juego contra el arduino','jankenpo'],
  'Elige con un botón y el Arduino elige al azar; el monitor dice quién ganó.',
  [C('button', 'Piedra', x='D2'), C('button', 'Papel', x='D3'), C('button', 'Tijera', x='D4'), C('led', 'Ganaste', 'verde', a='D12'), C('led', 'Perdiste', 'rojo', a='D13')],
  '''
String nombre[] = {"Piedra", "Papel", "Tijera"};

void setup() {
  Serial.begin(9600);
  for (int b = 2; b <= 4; b++) pinMode(b, INPUT_PULLUP);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
  randomSeed(analogRead(A5));
}

void loop() {
  int yo = -1;
  for (int b = 0; b < 3; b++) if (digitalRead(2 + b) == LOW) yo = b;
  if (yo < 0) return;
  int ard = random(3);
  Serial.print("Tú: "); Serial.print(nombre[yo]); Serial.print("  Arduino: "); Serial.println(nombre[ard]);
  if (yo == ard) Serial.println("Empate");
  else if ((yo + 1) % 3 == ard) { Serial.println("Ganó el Arduino"); digitalWrite(13, HIGH); }
  else { Serial.println("¡Ganaste!"); digitalWrite(12, HIGH); }
  delay(1500);
  digitalWrite(12, LOW); digitalWrite(13, LOW);
}
''', 'Truco matemático: cada opción pierde contra la siguiente (piedra < papel < tijera < piedra). Por eso (yo + 1) % 3 es la opción que te gana.',
  'Lleva el marcador del juego al mejor de 5.')

P('Contador de puntos para partido', CAT, 2, ['marcador','partido','puntos','scoreboard','lcd marcador'],
  'Un marcador para dos equipos: cada botón suma un punto y la LCD muestra el resultado.',
  [C('lcd', 'Pantalla LCD'), C('button', 'Equipo A', x='D2'), C('button', 'Equipo B', x='D3'), C('button', 'Reiniciar', x='D4'), C('buzzer', 'Pito', p='D8')],
  LCD_INC + '''int a = 0, b = 0;

void mostrar() {
  lcd.clear();
  lcd.print("Equipo A: "); lcd.print(a);
  lcd.setCursor(0, 1); lcd.print("Equipo B: "); lcd.print(b);
}

void setup() {
  lcd.init(); lcd.backlight();
  for (int p = 2; p <= 4; p++) pinMode(p, INPUT_PULLUP);
  mostrar();
}

void loop() {
  if (digitalRead(2) == LOW) { a++; tone(8, 1200, 100); mostrar(); delay(300); }
  if (digitalRead(3) == LOW) { b++; tone(8, 900, 100); mostrar(); delay(300); }
  if (digitalRead(4) == LOW) { a = 0; b = 0; tone(8, 400, 400); mostrar(); delay(300); }
}
''', 'Cada botón cambia su contador y vuelve a dibujar la pantalla. El delay evita que una sola pulsación sume varios puntos.',
  'Haz que suene una fanfarria cuando un equipo llegue a 10.')

P('Juego de puntería con luz', CAT, 2, ['punteria','linterna','tiro al blanco','laser'],
  'Ilumina la fotorresistencia con una linterna en menos de 3 segundos cada vez que se encienda el LED.',
  [C('ldr', 'Blanco (LDR)', y='A0'), C('led', 'Señal', 'rojo', a='D13'), C('buzzer', 'Sonido', p='D8')],
  '''
int puntos = 0;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  randomSeed(analogRead(A5));
}

void loop() {
  delay(random(1000, 4000));
  digitalWrite(13, HIGH);
  unsigned long inicio = millis();
  bool acerto = false;
  while (millis() - inicio < 3000) {
    if (analogRead(A0) > 800) { acerto = true; break; }
  }
  digitalWrite(13, LOW);
  if (acerto) { puntos++; tone(8, 1800, 200); Serial.print("¡Blanco! Puntos: "); Serial.println(puntos); }
  else { tone(8, 200, 400); Serial.println("Fallaste"); }
}
''', 'El juego espera un tiempo al azar, enciende la señal y mide si la luz de la linterna llega a tiempo. La instrucción break sale del while antes de terminar los 3 segundos.',
  'Reduce el tiempo disponible a medida que suman puntos.')

P('Carrera de botones para dos', CAT, 2, ['carrera de botones','quien presiona mas','duelo','velocidad de dedos'],
  'Dos jugadores presionan su botón lo más rápido posible durante 10 segundos; gana quien más veces lo presione.',
  [C('button', 'Jugador 1', x='D2'), C('button', 'Jugador 2', x='D3'), C('led', 'Gana 1', 'rojo', a='D12'), C('led', 'Gana 2', 'azul', a='D13'), C('buzzer', 'Salida', p='D8')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP); pinMode(3, INPUT_PULLUP);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  Serial.println("¡Ya!");
  tone(8, 1000, 500);
  int c1 = 0, c2 = 0;
  bool antes1 = HIGH, antes2 = HIGH;
  unsigned long inicio = millis();
  while (millis() - inicio < 10000) {
    bool ahora1 = digitalRead(2), ahora2 = digitalRead(3);
    if (antes1 == HIGH && ahora1 == LOW) c1++;
    if (antes2 == HIGH && ahora2 == LOW) c2++;
    antes1 = ahora1; antes2 = ahora2;
    delay(5);
  }
  Serial.print("Jugador 1: "); Serial.print(c1); Serial.print("  Jugador 2: "); Serial.println(c2);
  digitalWrite(12, c1 > c2); digitalWrite(13, c2 > c1);
  delay(5000);
  digitalWrite(12, LOW); digitalWrite(13, LOW);
}
''', 'Para contar pulsaciones (no el tiempo que se mantiene presionado) se compara el estado de antes con el de ahora: solo cuenta el cambio de HIGH a LOW.',
  'Muestra la cuenta en una LCD mientras juegan.')

P('Dado doble con LCD', CAT, 1, ['dos dados','dado lcd','parques','juego de mesa'],
  'Presiona el botón y la pantalla muestra dos dados y su suma, ideal para el parqués.',
  [C('lcd', 'Pantalla LCD'), C('button', 'Lanzar', x='D2'), C('buzzer', 'Sonido', p='D8')],
  LCD_INC + '''
void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT_PULLUP);
  randomSeed(analogRead(A5));
  lcd.print("Presiona lanzar");
}

void loop() {
  if (digitalRead(2) == HIGH) return;
  for (int i = 0; i < 8; i++) { tone(8, 600 + i * 100, 30); delay(60); }
  int d1 = random(1, 7), d2 = random(1, 7);
  lcd.clear();
  lcd.print("Dados: "); lcd.print(d1); lcd.print(" y "); lcd.print(d2);
  lcd.setCursor(0, 1); lcd.print("Suma: "); lcd.print(d1 + d2);
  if (d1 == d2) lcd.print(" PAR!");
  delay(500);
}
''', 'random(1, 7) da un número del 1 al 6 (el 7 no se incluye). Si los dos dados son iguales, en el parqués se llama "par" y se vuelve a tirar.',
  'Cuenta cuántos pares han salido.')

P('Esquiva obstáculos en la LCD', CAT, 3, ['juego lcd','esquivar','dinosaurio','saltar'],
  'Un muñeco corre en la LCD: presiona el botón para saltar los obstáculos que vienen.',
  [C('lcd', 'Pantalla LCD'), C('button', 'Saltar', x='D2'), C('buzzer', 'Sonido', p='D8')],
  LCD_INC + '''int obst = 15, puntos = 0;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  bool arriba = digitalRead(2) == LOW;
  lcd.clear();
  lcd.setCursor(1, arriba ? 0 : 1); lcd.print("o");
  lcd.setCursor(obst, 1); lcd.print("#");
  lcd.setCursor(10, 0); lcd.print(puntos);
  if (obst == 1 && !arriba) {
    tone(8, 150, 800);
    lcd.clear(); lcd.print("Perdiste! "); lcd.print(puntos);
    delay(2000);
    puntos = 0; obst = 15;
    return;
  }
  obst--;
  if (obst < 0) { obst = 15; puntos++; tone(8, 1500, 30); }
  delay(250);
}
''', 'El obstáculo (#) avanza una columna hacia la izquierda en cada vuelta. Si llega a la columna del muñeco y este no está saltando, el juego termina.',
  'Aumenta la velocidad cada 5 puntos.')

P('Tirar la moneda', CAT, 1, ['cara o sello','moneda','decidir al azar'],
  'Para decidir algo: presiona el botón y se enciende "cara" o "sello" al azar.',
  [C('button', 'Lanzar', x='D2'), C('led', 'Cara', 'amarillo', a='D12'), C('led', 'Sello', 'blanco', a='D13')],
  '''
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP); pinMode(12, OUTPUT); pinMode(13, OUTPUT);
  randomSeed(analogRead(A5));
}

void loop() {
  if (digitalRead(2) == LOW) {
    for (int i = 0; i < 10; i++) { digitalWrite(12, i % 2); digitalWrite(13, (i + 1) % 2); delay(80); }
    int r = random(2);
    digitalWrite(12, r == 0); digitalWrite(13, r == 1);
    Serial.println(r == 0 ? "Cara" : "Sello");
    delay(1000);
  }
}
''', 'random(2) da 0 o 1 con la misma probabilidad. El parpadeo alternado antes del resultado simula la moneda girando en el aire.',
  'Lanza 100 monedas y cuenta cuántas caras salen. ¿Se acerca a 50?')

P('Laberinto con joystick', CAT, 3, ['laberinto','joystick lcd','mover personaje','juego joystick'],
  'Mueve una estrella por la LCD con el joystick hasta llegar a la meta.',
  [C('lcd', 'Pantalla LCD'), C('joystick', 'Joystick', x='A0', y='A1', s='D2'), C('buzzer', 'Sonido', p='D8')],
  LCD_INC + '''int x = 0, y = 0;
int metaX = 15, metaY = 1;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT_PULLUP);
  randomSeed(analogRead(A5));
}

void loop() {
  int jx = analogRead(A0), jy = analogRead(A1);
  if (jx > 800 && x < 15) x++;
  if (jx < 200 && x > 0) x--;
  if (jy > 800) y = 1;
  if (jy < 200) y = 0;
  lcd.clear();
  lcd.setCursor(metaX, metaY); lcd.print("M");
  lcd.setCursor(x, y); lcd.print("*");
  if (x == metaX && y == metaY) {
    tone(8, 1800, 300);
    lcd.clear(); lcd.print("Llegaste!"); delay(1500);
    metaX = random(16); metaY = random(2); x = 0; y = 0;
  }
  delay(150);
}
''', 'El joystick son dos perillas: cerca de 0 o de 1023 significa que se movió a un lado. La estrella solo avanza si no se sale de la pantalla.',
  'Agrega un cronómetro para ver cuánto tardas.')

P('Juego de equilibrio con inclinación', CAT, 2, ['equilibrio','no lo inclines','pulso firme','inclinacion juego'],
  'Mantén el sensor derecho el mayor tiempo posible; si se inclina, pierdes.',
  [C('inclinacion', 'Sensor de inclinación', o='D2'), C('buzzer', 'Sonido', p='D8'), C('led', 'Perdiste', 'rojo', a='D13')],
  '''
unsigned long inicio;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT); pinMode(13, OUTPUT);
  inicio = millis();
}

void loop() {
  if (digitalRead(2) == HIGH) {
    unsigned long segundos = (millis() - inicio) / 1000;
    Serial.print("Aguantaste "); Serial.print(segundos); Serial.println(" segundos");
    digitalWrite(13, HIGH); tone(8, 200, 800); delay(2000);
    digitalWrite(13, LOW);
    inicio = millis();
  }
}
''', 'El sensor de inclinación tiene una bolita metálica: al inclinarse cambia la salida. El tiempo aguantado se calcula con millis().',
  'Pon el sensor sobre una cuchara y haz carreras con él.')

P('Pregunta y respuesta con botones', CAT, 2, ['concurso','trivia','preguntas','quiz'],
  'Un concurso de preguntas en el monitor serie: responde con los botones A o B.',
  [C('button', 'Opción A', x='D2'), C('button', 'Opción B', x='D3'), C('led', 'Correcto', 'verde', a='D12'), C('led', 'Incorrecto', 'rojo', a='D13'), C('buzzer', 'Sonido', p='D8')],
  '''
String preguntas[] = {"¿Cuántos pines digitales tiene el Arduino UNO? A) 14  B) 20",
                      "¿Qué mide un LM35? A) Luz  B) Temperatura",
                      "¿Ley de Ohm? A) V = I x R  B) V = I + R"};
int correctas[] = {0, 1, 0};
int n = 0, puntos = 0;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP); pinMode(3, INPUT_PULLUP);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
  Serial.println(preguntas[0]);
}

void loop() {
  int r = -1;
  if (digitalRead(2) == LOW) r = 0;
  if (digitalRead(3) == LOW) r = 1;
  if (r < 0) return;
  if (r == correctas[n]) { puntos++; digitalWrite(12, HIGH); tone(8, 1500, 200); }
  else { digitalWrite(13, HIGH); tone(8, 200, 400); }
  delay(1000); digitalWrite(12, LOW); digitalWrite(13, LOW);
  n++;
  if (n == 3) { Serial.print("Puntaje final: "); Serial.print(puntos); Serial.println(" de 3"); n = 0; puntos = 0; }
  Serial.println(preguntas[n]);
}
''', 'Las preguntas y sus respuestas correctas están en dos arreglos con el mismo orden. La variable n indica en qué pregunta vamos.',
  'Escribe 5 preguntas de otra materia.')

P('Reloj de ajedrez', CAT, 2, ['reloj de ajedrez','temporizador por turnos','ajedrez'],
  'Cada jugador tiene 60 segundos; al terminar su jugada presiona su botón y corre el tiempo del otro.',
  [C('lcd', 'Pantalla LCD'), C('button', 'Jugador 1', x='D2'), C('button', 'Jugador 2', x='D3'), C('buzzer', 'Fin', p='D8')],
  LCD_INC + '''long t1 = 60000, t2 = 60000;
int turno = 1;
unsigned long antes;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(2, INPUT_PULLUP); pinMode(3, INPUT_PULLUP);
  antes = millis();
}

void loop() {
  unsigned long ahora = millis();
  if (turno == 1) t1 -= ahora - antes; else t2 -= ahora - antes;
  antes = ahora;
  if (digitalRead(2) == LOW && turno == 1) turno = 2;
  if (digitalRead(3) == LOW && turno == 2) turno = 1;
  int s1 = t1 / 1000;
  int s2 = t2 / 1000;
  lcd.setCursor(0, 0); lcd.print("J1: "); lcd.print(s1); lcd.print(" s  ");
  lcd.setCursor(0, 1); lcd.print("J2: "); lcd.print(s2); lcd.print(" s  ");
  if (t1 <= 0 || t2 <= 0) {
    lcd.clear(); lcd.print(t1 <= 0 ? "Gana jugador 2" : "Gana jugador 1");
    tone(8, 600, 1500); delay(4000);
    t1 = 60000; t2 = 60000; turno = 1; antes = millis();
  }
  delay(100);
}
''', 'En cada vuelta se resta el tiempo transcurrido solo al jugador que tiene el turno. Así funcionan los relojes de los torneos de ajedrez.',
  'Agrega 2 segundos de bonificación por jugada.')
