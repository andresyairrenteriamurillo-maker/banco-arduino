from p_base import *
CAT = 'Sonido y música'

P('Sirena de bomberos', CAT, 1, ['sirena','bomberos','ambulancia','sirena de emergencia'],
  'El zumbador sube y baja de tono como la sirena de un camión de bomberos.',
  [C('buzzer', 'Sirena', p='D8'), C('led', 'Baliza', 'rojo', a='D13')],
  '''
// Sirena de bomberos
const int SIRENA = 8;
const int BALIZA = 13;

void setup() {
  pinMode(BALIZA, OUTPUT);
}

void loop() {
  digitalWrite(BALIZA, HIGH);
  for (int f = 600; f <= 1500; f += 20) { tone(SIRENA, f); delay(8); }   // sube
  digitalWrite(BALIZA, LOW);
  for (int f = 1500; f >= 600; f -= 20) { tone(SIRENA, f); delay(8); }   // baja
}
''', 'Un ciclo for aumenta la frecuencia del sonido poco a poco y otro la disminuye. Así el tono sube y baja sin parar, como una sirena.',
  'Haz una sirena de ambulancia que alterne solo dos tonos.')

P('Escala musical', CAT, 1, ['escala musical','do re mi','notas musicales','escala'],
  'El zumbador toca la escala do, re, mi, fa, sol, la, si, do.',
  [C('buzzer', 'Parlante', p='D8')],
  '''
// Escala musical
const int PARLANTE = 8;
int notas[] = {262, 294, 330, 349, 392, 440, 494, 523};
String nombres[] = {"Do", "Re", "Mi", "Fa", "Sol", "La", "Si", "Do"};

void setup() {
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < 8; i++) {
    Serial.println(nombres[i]);
    tone(PARLANTE, notas[i], 400);
    delay(500);
  }
  delay(1500);
}
''', 'Cada nota musical es una frecuencia (vibraciones por segundo). El arreglo notas guarda las frecuencias de la escala y el arreglo nombres sus nombres, en el mismo orden.',
  'Toca la escala al revés, de do agudo a do grave.')

P('Feliz cumpleaños', CAT, 2, ['feliz cumpleanos','cancion','melodia','cumpleanos'],
  'El Arduino toca la melodía de "Feliz cumpleaños".',
  [C('buzzer', 'Parlante', p='D8'), C('led', 'Vela', 'amarillo', a='D13')],
  '''
// Feliz cumpleaños
const int PARLANTE = 8;
const int VELA = 13;
int melodia[] = {262, 262, 294, 262, 349, 330, 262, 262, 294, 262, 392, 349,
                 262, 262, 523, 440, 349, 330, 294, 466, 466, 440, 349, 392, 349};
int tiempos[] = {3, 1, 4, 4, 4, 8, 3, 1, 4, 4, 4, 8, 3, 1, 4, 4, 4, 4, 8, 3, 1, 4, 4, 4, 8};

void setup() {
  pinMode(VELA, OUTPUT);
}

void loop() {
  for (int i = 0; i < 25; i++) {
    int duracion = tiempos[i] * 110;
    digitalWrite(VELA, HIGH);
    tone(PARLANTE, melodia[i], duracion);
    delay(duracion * 0.6);
    digitalWrite(VELA, LOW);
    delay(duracion * 0.6);
  }
  delay(3000);
}
''', 'La canción se guarda en dos arreglos: la frecuencia de cada nota y cuánto dura. El LED se enciende con cada nota, como una vela que baila con la música.',
  'Escribe otra canción que conozcas cambiando los dos arreglos.')

P('Alarma de despertador', CAT, 1, ['despertador','alarma de reloj','bip bip','reloj despertador'],
  'Después de un tiempo suena un "bip-bip" de despertador hasta que presionas el botón.',
  [C('buzzer', 'Despertador', p='D8'), C('button', 'Apagar', x='D2')],
  '''
// Despertador que suena a los 10 segundos
const int ZUMBADOR = 8;
const int BOTON = 2;
const unsigned long ESPERA = 10000;
bool sonando = false;
bool apagado = false;

void setup() {
  Serial.begin(9600);
  pinMode(BOTON, INPUT_PULLUP);
  Serial.println("El despertador sonará en 10 segundos...");
}

void loop() {
  if (!apagado && millis() > ESPERA) sonando = true;
  if (sonando) {
    for (int i = 0; i < 4; i++) { tone(ZUMBADOR, 2000, 80); delay(150); }
    delay(400);
    if (digitalRead(BOTON) == LOW) {
      sonando = false; apagado = true;
      Serial.println("¡Buenos días!");
    }
  }
}
''', 'millis() dice cuánto tiempo lleva encendido el Arduino. Cuando pasa de 10 segundos, el despertador empieza a sonar en ráfagas de cuatro pitidos, hasta que se presiona el botón.',
  'Agrega un botón de "5 minutos más" que lo vuelva a programar.')

P('Tono que sube con la perilla', CAT, 1, ['tono variable','perilla de sonido','theremin de perilla','sonido con potenciometro'],
  'Al girar el potenciómetro cambia la nota del zumbador, de grave a agudo.',
  [C('pot', 'Perilla', w='A0'), C('buzzer', 'Parlante', p='D8')],
  '''
// Tono controlado con un potenciómetro
const int PERILLA = A0;
const int PARLANTE = 8;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int valor = analogRead(PERILLA);              // 0 a 1023
  int frecuencia = map(valor, 0, 1023, 200, 2000);
  tone(PARLANTE, frecuencia);
  Serial.print("Frecuencia: ");
  Serial.println(frecuencia);
  delay(50);
}
''', 'analogRead() lee la posición de la perilla como un número de 0 a 1023. map() convierte ese número a una frecuencia entre 200 y 2000 Hz.',
  'Haz que solo suenen las 8 notas de la escala según la posición de la perilla.')

P('Theremin de luz', CAT, 2, ['theremin','instrumento de luz','sonido con luz','musica con la mano'],
  'Un instrumento que se toca acercando la mano a un sensor de luz: más sombra, más grave.',
  [C('ldr', 'Sensor de luz', y='A0'), C('buzzer', 'Parlante', p='D8')],
  '''
// Theremin de luz
const int LUZ = A0;
const int PARLANTE = 8;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int luz = analogRead(LUZ);                    // más luz = número más alto
  int nota = map(luz, 0, 1023, 150, 1800);
  tone(PARLANTE, nota);
  Serial.println(nota);
  delay(30);
}
''', 'La fotorresistencia cambia su resistencia con la luz, y el Arduino lo lee en A0. Al tapar el sensor con la mano baja la luz y por lo tanto la nota.',
  'Haz que si está muy oscuro el instrumento se quede en silencio.')

P('Código Morse sonoro', CAT, 2, ['morse sonoro','telegrafo','mensaje en morse','codigo morse'],
  'El zumbador y un LED envían la palabra HOLA en código Morse.',
  [C('buzzer', 'Telégrafo', p='D8'), C('led', 'Luz', 'blanco', a='D13')],
  '''
// HOLA en código Morse
const int ZUMBADOR = 8;
const int LUZ = 13;
const int PUNTO = 150;

void senal(int duracion) {
  digitalWrite(LUZ, HIGH); tone(ZUMBADOR, 750);
  delay(duracion);
  digitalWrite(LUZ, LOW); noTone(ZUMBADOR);
  delay(PUNTO);
}

void letra(String codigo) {            // ejemplo: "...." para la H
  for (int i = 0; i < codigo.length(); i++) {
    if (codigo.charAt(i) == '.') senal(PUNTO);
    else senal(PUNTO * 3);
  }
  delay(PUNTO * 2);                    // espacio entre letras
}

void setup() {
  pinMode(LUZ, OUTPUT);
}

void loop() {
  letra("....");   // H
  letra("---");    // O
  letra(".-..");   // L
  letra(".-");     // A
  delay(2000);
}
''', 'Cada letra se escribe como un texto de puntos y rayas. La función letra() lo recorre carácter por carácter con charAt() y hace una señal corta o larga.',
  'Agrega las letras de tu nombre.')

P('Metrónomo musical ajustable', CAT, 2, ['metronomo ajustable','tempo','bpm','ritmo musical'],
  'Un metrónomo que marca el ritmo con sonido; la perilla ajusta la velocidad de 40 a 200 pulsos por minuto.',
  [C('pot', 'Velocidad', w='A0'), C('buzzer', 'Clic', p='D8'), C('led', 'Pulso', 'verde', a='D13')],
  '''
// Metrónomo ajustable
const int PERILLA = A0;
const int ZUMBADOR = 8;
const int LUZ = 13;
int tiempo = 1;

void setup() {
  Serial.begin(9600);
  pinMode(LUZ, OUTPUT);
}

void loop() {
  int bpm = map(analogRead(PERILLA), 0, 1023, 40, 200);
  int intervalo = 60000 / bpm;
  int nota = 1000;
  if (tiempo == 1) nota = 1600;          // primer tiempo más agudo
  tone(ZUMBADOR, nota, 50);
  digitalWrite(LUZ, HIGH); delay(60); digitalWrite(LUZ, LOW);
  Serial.print(bpm); Serial.println(" pulsos por minuto");
  delay(intervalo - 60);
  tiempo++;
  if (tiempo > 4) tiempo = 1;
}
''', 'La perilla elige los pulsos por minuto y el programa calcula los milisegundos entre pulsos. El primer tiempo de cada compás suena más agudo para no perder la cuenta.',
  'Agrega un interruptor para elegir compás de 3 o de 4 tiempos.')

P('Caja musical con botón', CAT, 2, ['caja musical','melodia con boton','musica al presionar','cancion de cuna'],
  'Al presionar el botón suena una canción de cuna y un LED azul acompaña cada nota.',
  [C('button', 'Dar cuerda', x='D2'), C('buzzer', 'Caja musical', p='D8'), C('led', 'Luz', 'azul', a='D13')],
  '''
// Caja musical: Estrellita, ¿dónde estás?
const int BOTON = 2;
const int PARLANTE = 8;
const int LUZ = 13;
int notas[] = {262, 262, 392, 392, 440, 440, 392, 349, 349, 330, 330, 294, 294, 262};
int largo[] = {1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2};

void setup() {
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(LUZ, OUTPUT);
}

void loop() {
  if (digitalRead(BOTON) == LOW) {
    for (int i = 0; i < 14; i++) {
      int d = largo[i] * 400;
      digitalWrite(LUZ, HIGH);
      tone(PARLANTE, notas[i], d * 0.9);
      delay(d);
      digitalWrite(LUZ, LOW);
    }
  }
}
''', 'La melodía está guardada en el arreglo notas y la duración de cada una en largo (1 = corta, 2 = larga). Solo se toca cuando el botón está presionado al inicio.',
  'Completa la canción con la segunda parte.')

P('Detector de silencio', CAT, 2, ['detector de silencio','biblioteca','ruido en clase','medidor de ruido'],
  'Un sensor de sonido vigila el salón: si hay mucho ruido se enciende una luz roja que pide silencio.',
  [C('sonido', 'Sensor de sonido', o='D2'), C('led', 'Silencio', 'verde', a='D12'), C('led', '¡Mucho ruido!', 'rojo', a='D13')],
  '''
// Detector de ruido para el salón
const int SONIDO = 2;        // DO del sensor: HIGH con ruido fuerte
const int VERDE = 12;
const int ROJO = 13;
int ruidos = 0;

void setup() {
  Serial.begin(9600);
  pinMode(SONIDO, INPUT);
  pinMode(VERDE, OUTPUT);
  pinMode(ROJO, OUTPUT);
}

void loop() {
  if (digitalRead(SONIDO) == HIGH) {
    ruidos++;
    Serial.print("Ruido detectado. Van ");
    Serial.println(ruidos);
    digitalWrite(VERDE, LOW);
    digitalWrite(ROJO, HIGH);
    delay(2000);                 // la luz roja dura 2 segundos
  } else {
    digitalWrite(ROJO, LOW);
    digitalWrite(VERDE, HIGH);
  }
}
''', 'El módulo de sonido tiene un micrófono y un comparador: cuando el ruido supera el nivel fijado con su tornillo azul, la salida DO pasa a HIGH.',
  'Cuenta los ruidos de los últimos 10 segundos y muestra una luz amarilla si son pocos.')

P('Aplauso que enciende la luz', CAT, 2, ['aplauso','clap','luz con aplauso','palmada'],
  'Una palmada enciende la lámpara y otra palmada la apaga.',
  [C('sonido', 'Micrófono', o='D2'), C('led', 'Lámpara', 'amarillo', a='D13')],
  '''
// Luz que se enciende con un aplauso
const int MICROFONO = 2;
const int LAMPARA = 13;
bool encendida = false;

void setup() {
  Serial.begin(9600);
  pinMode(MICROFONO, INPUT);
  pinMode(LAMPARA, OUTPUT);
}

void loop() {
  if (digitalRead(MICROFONO) == HIGH) {
    encendida = !encendida;
    digitalWrite(LAMPARA, encendida);
    if (encendida) Serial.println("Luz encendida");
    else Serial.println("Luz apagada");
    delay(600);                  // espera a que termine el eco del aplauso
  }
}
''', 'Cada vez que el sensor detecta un sonido fuerte, el estado de la lámpara se invierte con el operador !. La pausa de 600 ms evita que un solo aplauso cuente dos veces.',
  'Haz que se necesiten dos aplausos seguidos para encender la luz.')

P('Alarma de golpe con sirena', CAT, 2, ['alarma de golpe','vibracion alarma','proteger objeto','alarma de vitrina'],
  'Protege una caja o vitrina: si alguien la golpea o mueve, suena la sirena.',
  [C('vibracion', 'Sensor de vibración', o='D2'), C('buzzer', 'Sirena', p='D8'), C('led', 'Alerta', 'rojo', a='D13')],
  '''
// Alarma de golpe o movimiento
const int VIBRACION = 2;     // DO: HIGH cuando hay vibración
const int SIRENA = 8;
const int ALERTA = 13;

void setup() {
  Serial.begin(9600);
  pinMode(VIBRACION, INPUT);
  pinMode(ALERTA, OUTPUT);
}

void loop() {
  if (digitalRead(VIBRACION) == HIGH) {
    Serial.println("¡Movieron la caja!");
    for (int i = 0; i < 6; i++) {
      digitalWrite(ALERTA, HIGH); tone(SIRENA, 1800); delay(150);
      digitalWrite(ALERTA, LOW);  tone(SIRENA, 1200); delay(150);
    }
    noTone(SIRENA);
  }
}
''', 'El sensor de vibración tiene un resorte que hace contacto cuando lo sacuden, y su módulo entrega HIGH. Entonces el Arduino hace sonar seis ciclos de sirena.',
  'Agrega un interruptor para armar y desarmar la alarma.')
