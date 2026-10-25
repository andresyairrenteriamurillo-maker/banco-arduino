from p_base import *
CAT = 'Luces y LED'

P('Mi primer LED parpadeante', CAT, 1, ['parpadeo','blink','primer led','led parpadeante'],
  'Un LED se enciende y se apaga cada medio segundo: el "Hola mundo" de Arduino.',
  [C('led', 'LED rojo', 'rojo', a='D13')],
  '''
// Mi primer LED parpadeante
const int LED = 13;          // el LED está en el pin 13

void setup() {
  pinMode(LED, OUTPUT);      // el pin 13 será una salida
}

void loop() {
  digitalWrite(LED, HIGH);   // enciende el LED (5 V)
  delay(500);                // espera medio segundo
  digitalWrite(LED, LOW);    // apaga el LED (0 V)
  delay(500);
}
''', 'En setup() el pin 13 se configura como salida. En loop(), que se repite para siempre, el pin se pone en HIGH (5 V) y luego en LOW (0 V), con una pausa entre cada cambio.',
  'Cambia los dos delay() para que el LED parpadee el doble de rápido.')

P('Señal de auxilio SOS', CAT, 1, ['sos','morse','auxilio','senal de auxilio'],
  'El LED envía el mensaje SOS en código Morse: tres destellos cortos, tres largos y tres cortos.',
  [C('led', 'Luz de auxilio', 'blanco', a='D13')],
  '''
// SOS en código Morse
const int LED = 13;

void destello(int duracion) {
  digitalWrite(LED, HIGH);
  delay(duracion);
  digitalWrite(LED, LOW);
  delay(200);                // pausa entre destellos
}

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  for (int i = 0; i < 3; i++) destello(200);   // S: tres cortos
  for (int i = 0; i < 3; i++) destello(600);   // O: tres largos
  for (int i = 0; i < 3; i++) destello(200);   // S: tres cortos
  delay(1500);               // pausa antes de repetir
}
''', 'La función destello() enciende el LED el tiempo que le indiquemos. Un ciclo for la repite tres veces con destellos cortos (puntos) y tres con destellos largos (rayas).',
  'Escribe tu nombre en código Morse con destellos cortos y largos.')

P('Faro de barco', CAT, 1, ['faro','faro de barco','destello','baliza'],
  'Un LED amarillo imita un faro: un destello muy rápido cada dos segundos.',
  [C('led', 'Luz del faro', 'amarillo', a='D12')],
  '''
// Faro de barco
const int FARO = 12;

void setup() {
  pinMode(FARO, OUTPUT);
}

void loop() {
  digitalWrite(FARO, HIGH);
  delay(80);                 // destello muy corto
  digitalWrite(FARO, LOW);
  delay(150);
  digitalWrite(FARO, HIGH);
  delay(80);                 // segundo destello
  digitalWrite(FARO, LOW);
  delay(2000);               // larga pausa: así lo reconocen los barcos
}
''', 'Cada faro real tiene su propio ritmo de destellos para que los marineros lo reconozcan. Aquí el ritmo es: dos destellos cortos y una pausa de dos segundos.',
  'Inventa el ritmo de tu propio faro con tres destellos.')

P('Luz de vela', CAT, 1, ['vela','llama de vela','luz de vela','parpadeo aleatorio'],
  'Un LED amarillo cambia su brillo al azar para parecer la llama de una vela.',
  [C('led', 'Llama', 'amarillo', a='D9')],
  '''
// Luz de vela: brillo al azar
const int LLAMA = 9;         // pin con PWM (~) para regular el brillo

void setup() {
  pinMode(LLAMA, OUTPUT);
}

void loop() {
  int brillo = random(80, 256);     // número al azar entre 80 y 255
  analogWrite(LLAMA, brillo);       // brillo de 0 (apagado) a 255 (máximo)
  delay(random(40, 120));           // espera también al azar
}
''', 'analogWrite() regula el brillo con PWM: el pin se enciende y apaga muy rápido, y el ojo ve un brillo intermedio. random() da números al azar, que imitan el temblor de una llama.',
  'Agrega un segundo LED rojo para que la vela tenga dos colores.')

P('LED que respira', CAT, 1, ['respira','respiracion','fade','desvanecer','brillo suave'],
  'El brillo del LED sube y baja suavemente, como si respirara.',
  [C('led', 'LED azul', 'azul', a='D9')],
  '''
// LED que respira
const int LED = 9;           // pin con PWM (~)

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  for (int b = 0; b <= 255; b += 5) {   // sube el brillo
    analogWrite(LED, b);
    delay(20);
  }
  for (int b = 255; b >= 0; b -= 5) {   // baja el brillo
    analogWrite(LED, b);
    delay(20);
  }
}
''', 'Dos ciclos for cambian el brillo de 5 en 5: el primero de 0 a 255 y el segundo de 255 a 0. Como cada paso dura 20 ms, el cambio se ve suave.',
  'Haz que respire más lento cambiando el delay a 40 ms.')

P('Luces de policía', CAT, 1, ['policia','luces de policia','patrulla','sirena de luces'],
  'Un LED rojo y uno azul se alternan como las luces de una patrulla.',
  [C('led', 'Luz roja', 'rojo', a='D12'), C('led', 'Luz azul', 'azul', a='D11')],
  '''
// Luces de policía
const int ROJO = 12;
const int AZUL = 11;

void destellar(int pin) {
  for (int i = 0; i < 3; i++) {     // tres destellos rápidos
    digitalWrite(pin, HIGH);
    delay(60);
    digitalWrite(pin, LOW);
    delay(60);
  }
}

void setup() {
  pinMode(ROJO, OUTPUT);
  pinMode(AZUL, OUTPUT);
}

void loop() {
  destellar(ROJO);
  destellar(AZUL);
}
''', 'La función destellar() recibe el número de pin y hace tres destellos rápidos. Llamándola primero con el rojo y después con el azul se logra el efecto de patrulla.',
  'Agrega un zumbador que suene con cada destello.')

P('Semáforo básico', CAT, 1, ['semaforo basico','semaforo de tres luces','transito'],
  'Tres LED funcionan como un semáforo: verde, amarillo y rojo con sus tiempos.',
  [C('led', 'Rojo', 'rojo', a='D12'), C('led', 'Amarillo', 'amarillo', a='D11'), C('led', 'Verde', 'verde', a='D10')],
  '''
// Semáforo básico
const int ROJO = 12;
const int AMARILLO = 11;
const int VERDE = 10;

void luz(int r, int a, int v, int tiempo) {
  digitalWrite(ROJO, r);
  digitalWrite(AMARILLO, a);
  digitalWrite(VERDE, v);
  delay(tiempo);
}

void setup() {
  pinMode(ROJO, OUTPUT);
  pinMode(AMARILLO, OUTPUT);
  pinMode(VERDE, OUTPUT);
}

void loop() {
  luz(LOW, LOW, HIGH, 4000);   // verde 4 segundos
  luz(LOW, HIGH, LOW, 1500);   // amarillo 1,5 segundos
  luz(HIGH, LOW, LOW, 4000);   // rojo 4 segundos
}
''', 'La función luz() decide qué LED se enciende y cuánto tiempo. El loop() repite la secuencia verde, amarillo y rojo, como un semáforo real.',
  'Agrega una fase en la que el verde parpadea antes del amarillo.')

P('Semáforo de dos vías', CAT, 2, ['semaforo de dos vias','cruce','interseccion','dos semaforos'],
  'Dos semáforos coordinados para un cruce: cuando uno está en verde, el otro está en rojo.',
  [C('led', 'Calle A rojo', 'rojo', a='D13'), C('led', 'Calle A amarillo', 'amarillo', a='D12'), C('led', 'Calle A verde', 'verde', a='D11'),
   C('led', 'Calle B rojo', 'rojo', a='D10'), C('led', 'Calle B amarillo', 'amarillo', a='D9'), C('led', 'Calle B verde', 'verde', a='D8')],
  '''
// Semáforo de dos vías (cruce)
const int AR = 13, AA = 12, AV = 11;   // calle A
const int BR = 10, BA = 9, BV = 8;     // calle B

void poner(int ar, int aa, int av, int br, int ba, int bv, int tiempo) {
  digitalWrite(AR, ar); digitalWrite(AA, aa); digitalWrite(AV, av);
  digitalWrite(BR, br); digitalWrite(BA, ba); digitalWrite(BV, bv);
  delay(tiempo);
}

void setup() {
  for (int p = 8; p <= 13; p++) pinMode(p, OUTPUT);
}

void loop() {
  poner(0, 0, 1,  1, 0, 0, 4000);   // A verde, B rojo
  poner(0, 1, 0,  1, 0, 0, 1500);   // A amarillo
  poner(1, 0, 0,  0, 0, 1, 4000);   // A rojo, B verde
  poner(1, 0, 0,  0, 1, 0, 1500);   // B amarillo
}
''', 'Los seis LED se controlan juntos con la función poner(). Nunca hay dos verdes a la vez: así funcionan los cruces de verdad para evitar choques.',
  'Agrega 1 segundo con las dos calles en rojo entre cada cambio, como en los cruces reales.')

P('Auto fantástico', CAT, 2, ['auto fantastico','barrido de luces','kitt','luces que corren','persecucion de luces'],
  'Seis LED se encienden uno tras otro de ida y vuelta, como el famoso auto de la televisión.',
  [C('led', 'LED 1', 'rojo', a='D8'), C('led', 'LED 2', 'rojo', a='D9'), C('led', 'LED 3', 'rojo', a='D10'),
   C('led', 'LED 4', 'rojo', a='D11'), C('led', 'LED 5', 'rojo', a='D12'), C('led', 'LED 6', 'rojo', a='D13')],
  '''
// Auto fantástico: luz que va y viene
int leds[] = {8, 9, 10, 11, 12, 13};   // los seis pines en orden

void setup() {
  for (int i = 0; i < 6; i++) pinMode(leds[i], OUTPUT);
}

void loop() {
  for (int i = 0; i < 6; i++) {        // de izquierda a derecha
    digitalWrite(leds[i], HIGH);
    delay(80);
    digitalWrite(leds[i], LOW);
  }
  for (int i = 4; i > 0; i--) {        // de regreso
    digitalWrite(leds[i], HIGH);
    delay(80);
    digitalWrite(leds[i], LOW);
  }
}
''', 'Los pines se guardan en un arreglo (una lista). Así un ciclo for puede recorrerlos en orden, primero hacia adelante y luego hacia atrás.',
  'Haz que se enciendan dos LED vecinos al tiempo para que la luz se vea más grande.')

P('Contador binario de 4 bits', CAT, 2, ['binario','contador binario','numeros binarios','bits'],
  'Cuatro LED muestran los números del 0 al 15 en sistema binario.',
  [C('led', 'Bit 1', 'verde', a='D10'), C('led', 'Bit 2', 'verde', a='D11'), C('led', 'Bit 4', 'verde', a='D12'), C('led', 'Bit 8', 'verde', a='D13')],
  '''
// Contador binario de 0 a 15
int bits[] = {10, 11, 12, 13};   // valor 1, 2, 4 y 8

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 4; i++) pinMode(bits[i], OUTPUT);
}

void loop() {
  for (int n = 0; n < 16; n++) {
    Serial.print("Número: ");
    Serial.println(n);
    for (int i = 0; i < 4; i++) {
      int bit = (n >> i) & 1;       // ¿el bit i de n vale 1?
      digitalWrite(bits[i], bit);
    }
    delay(1000);
  }
}
''', 'Cada LED representa una potencia de 2 (1, 2, 4 y 8). La operación (n >> i) & 1 averigua si el bit número i del número está encendido. El monitor serie muestra el número en decimal para comparar.',
  'Cuenta hacia atrás, de 15 a 0.')

P('Luces de Navidad', CAT, 1, ['navidad','luces de navidad','arbolito','decoracion'],
  'Cuatro LED de colores se encienden en patrones que cambian solos.',
  [C('led', 'Rojo', 'rojo', a='D13'), C('led', 'Verde', 'verde', a='D12'), C('led', 'Amarillo', 'amarillo', a='D11'), C('led', 'Azul', 'azul', a='D10')],
  '''
// Luces de Navidad con tres efectos
int luces[] = {13, 12, 11, 10};

void todas(int estado) {
  for (int i = 0; i < 4; i++) digitalWrite(luces[i], estado);
}

void setup() {
  for (int i = 0; i < 4; i++) pinMode(luces[i], OUTPUT);
}

void loop() {
  // Efecto 1: todas parpadean
  for (int k = 0; k < 4; k++) { todas(HIGH); delay(300); todas(LOW); delay(300); }
  // Efecto 2: una por una
  for (int k = 0; k < 3; k++) {
    for (int i = 0; i < 4; i++) { digitalWrite(luces[i], HIGH); delay(150); digitalWrite(luces[i], LOW); }
  }
  // Efecto 3: al azar
  for (int k = 0; k < 20; k++) {
    digitalWrite(luces[random(4)], random(2));
    delay(100);
  }
  todas(LOW);
}
''', 'El loop() tiene tres efectos seguidos. La función todas() enciende o apaga todas las luces juntas, y random() escoge un LED y un estado al azar.',
  'Crea un cuarto efecto en el que se encienden de dos en dos.')

P('Luz de emergencia estroboscópica', CAT, 1, ['estroboscopica','estrobo','emergencia','luz de emergencia'],
  'Un LED blanco da destellos muy rápidos, como las luces de emergencia.',
  [C('led', 'Estrobo', 'blanco', a='D13')],
  '''
// Luz estroboscópica de emergencia
const int LUZ = 13;

void setup() {
  pinMode(LUZ, OUTPUT);
}

void loop() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(LUZ, HIGH);
    delay(30);               // destello muy corto
    digitalWrite(LUZ, LOW);
    delay(70);
  }
  delay(700);                // pausa entre ráfagas
}
''', 'Los destellos de 30 ms son tan cortos que el ojo los ve como golpes de luz. Cinco destellos seguidos y una pausa forman una ráfaga.',
  'Cambia el número de destellos por ráfaga y observa cuál llama más la atención.')

P('Latido del corazón', CAT, 1, ['latido','corazon','pulso','latido del corazon'],
  'Un LED rojo late como un corazón: dos golpes rápidos y una pausa.',
  [C('led', 'Corazón', 'rojo', a='D9')],
  '''
// Latido del corazón con brillo suave
const int CORAZON = 9;        // pin PWM (~)

void golpe(int fuerza) {
  for (int b = 0; b <= fuerza; b += 15) { analogWrite(CORAZON, b); delay(5); }
  for (int b = fuerza; b >= 0; b -= 15) { analogWrite(CORAZON, b); delay(8); }
}

void setup() {
  pinMode(CORAZON, OUTPUT);
}

void loop() {
  golpe(255);   // primer golpe fuerte
  delay(80);
  golpe(150);   // segundo golpe más suave
  delay(700);   // pausa hasta el siguiente latido
}
''', 'La función golpe() sube y baja el brillo muy rápido. Un golpe fuerte seguido de uno suave imita el "pum-pum" del corazón.',
  'Acelera el latido como si el corazón estuviera haciendo ejercicio.')

P('Ruleta de luces', CAT, 2, ['ruleta','ruleta de luces','sorteo','ruleta de la suerte'],
  'Cinco LED giran cada vez más lento hasta detenerse en uno al azar, como una ruleta.',
  [C('led', 'Casilla 1', 'rojo', a='D9'), C('led', 'Casilla 2', 'amarillo', a='D10'), C('led', 'Casilla 3', 'verde', a='D11'),
   C('led', 'Casilla 4', 'azul', a='D12'), C('led', 'Casilla 5', 'blanco', a='D13')],
  '''
// Ruleta de luces
int casillas[] = {9, 10, 11, 12, 13};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 5; i++) pinMode(casillas[i], OUTPUT);
}

void loop() {
  int vueltas = random(15, 30);      // cuántos saltos dará
  int espera = 40;
  int pos = 0;
  for (int k = 0; k < vueltas; k++) {
    digitalWrite(casillas[pos], LOW);
    pos = (pos + 1) % 5;             // pasa a la siguiente casilla
    digitalWrite(casillas[pos], HIGH);
    delay(espera);
    espera = espera + 12;            // cada vez más lento
  }
  Serial.print("Ganó la casilla ");
  Serial.println(pos + 1);
  delay(3000);
  digitalWrite(casillas[pos], LOW);
}
''', 'La variable pos guarda en qué casilla va la luz y el operador % hace que después de la 5 vuelva a la 1. Como la espera aumenta en cada salto, la ruleta se va frenando.',
  'Agrega un botón para que la ruleta solo gire cuando lo presiones.')

P('Metrónomo de luz', CAT, 1, ['metronomo','ritmo','tempo','musica'],
  'Un LED marca el ritmo de una canción: 4 tiempos, con el primero más largo.',
  [C('led', 'Primer tiempo', 'rojo', a='D13'), C('led', 'Otros tiempos', 'verde', a='D12')],
  '''
// Metrónomo de luz a 90 pulsos por minuto
const int FUERTE = 13;
const int SUAVE = 12;
const int BPM = 90;                 // pulsos por minuto

void setup() {
  pinMode(FUERTE, OUTPUT);
  pinMode(SUAVE, OUTPUT);
}

void loop() {
  int intervalo = 60000 / BPM;      // milisegundos entre pulsos
  for (int t = 1; t <= 4; t++) {
    int pin = SUAVE;
    if (t == 1) pin = FUERTE;       // el primer tiempo se marca en rojo
    digitalWrite(pin, HIGH);
    delay(100);
    digitalWrite(pin, LOW);
    delay(intervalo - 100);
  }
}
''', 'Un minuto tiene 60 000 milisegundos; dividiéndolos entre los pulsos por minuto se obtiene el tiempo entre pulsos. El primer tiempo de cada compás se marca con el LED rojo.',
  'Agrega un zumbador para escuchar el ritmo además de verlo.')

P('Escalera de luces', CAT, 1, ['escalera','barra de luces','llenar','nivel de luces'],
  'Cinco LED se encienden uno sobre otro hasta llenarse y luego se vacían.',
  [C('led', 'Nivel 1', 'verde', a='D9'), C('led', 'Nivel 2', 'verde', a='D10'), C('led', 'Nivel 3', 'amarillo', a='D11'),
   C('led', 'Nivel 4', 'amarillo', a='D12'), C('led', 'Nivel 5', 'rojo', a='D13')],
  '''
// Escalera de luces
int niveles[] = {9, 10, 11, 12, 13};

void setup() {
  for (int i = 0; i < 5; i++) pinMode(niveles[i], OUTPUT);
}

void loop() {
  for (int i = 0; i < 5; i++) {      // se llena
    digitalWrite(niveles[i], HIGH);
    delay(250);
  }
  for (int i = 4; i >= 0; i--) {     // se vacía
    digitalWrite(niveles[i], LOW);
    delay(250);
  }
}
''', 'A diferencia del auto fantástico, aquí los LED no se apagan enseguida: se quedan encendidos hasta llenar la escalera, y luego se apagan desde arriba.',
  'Haz que al llenarse los cinco parpadeen tres veces antes de vaciarse.')

P('Arcoíris con LED RGB', CAT, 2, ['arcoiris','rgb','colores','led rgb'],
  'Un LED RGB recorre los colores del arcoíris mezclando rojo, verde y azul.',
  [C('rgb', 'LED RGB', r='D9', g='D10', b='D11')],
  '''
// Arcoíris con LED RGB (cátodo común)
const int R = 9, G = 10, B = 11;    // pines PWM (~)

void color(int r, int g, int b) {
  analogWrite(R, r);
  analogWrite(G, g);
  analogWrite(B, b);
  delay(700);
}

void setup() {
  pinMode(R, OUTPUT); pinMode(G, OUTPUT); pinMode(B, OUTPUT);
}

void loop() {
  color(255, 0, 0);     // rojo
  color(255, 80, 0);    // naranja
  color(255, 200, 0);   // amarillo
  color(0, 255, 0);     // verde
  color(0, 0, 255);     // azul
  color(75, 0, 130);    // índigo
  color(160, 0, 255);   // violeta
}
''', 'Un LED RGB tiene tres LED dentro: rojo, verde y azul. Variando el brillo de cada uno con analogWrite() se mezclan para formar cualquier color.',
  'Agrega el color blanco (los tres al máximo) y el rosado.')

P('Semáforo con cuenta en el monitor', CAT, 2, ['semaforo con contador','cuenta regresiva semaforo','monitor serie'],
  'Un semáforo que además muestra en el monitor serie cuántos segundos faltan para cambiar.',
  [C('led', 'Rojo', 'rojo', a='D12'), C('led', 'Amarillo', 'amarillo', a='D11'), C('led', 'Verde', 'verde', a='D10')],
  '''
// Semáforo con cuenta regresiva en el monitor serie
const int ROJO = 12, AMARILLO = 11, VERDE = 10;

void fase(int pin, String nombre, int segundos) {
  digitalWrite(pin, HIGH);
  for (int s = segundos; s > 0; s--) {
    Serial.print(nombre);
    Serial.print(": faltan ");
    Serial.print(s);
    Serial.println(" s");
    delay(1000);
  }
  digitalWrite(pin, LOW);
}

void setup() {
  Serial.begin(9600);
  pinMode(ROJO, OUTPUT); pinMode(AMARILLO, OUTPUT); pinMode(VERDE, OUTPUT);
}

void loop() {
  fase(VERDE, "Verde", 5);
  fase(AMARILLO, "Amarillo", 2);
  fase(ROJO, "Rojo", 5);
}
''', 'La función fase() enciende una luz y cuenta los segundos hacia atrás, escribiendo cada número en el monitor serie. Así se ve cómo un programa puede mostrar información al usuario.',
  'Muestra también cuántos ciclos completos lleva el semáforo.')

P('Dos LED alternados con velocidad creciente', CAT, 1, ['alternar','velocidad','acelerar','ping pong de luces'],
  'Dos LED se alternan cada vez más rápido y vuelven a empezar.',
  [C('led', 'Izquierda', 'verde', a='D12'), C('led', 'Derecha', 'amarillo', a='D11')],
  '''
// Dos LED que se alternan cada vez más rápido
const int IZQ = 12;
const int DER = 11;

void setup() {
  pinMode(IZQ, OUTPUT);
  pinMode(DER, OUTPUT);
}

void loop() {
  for (int espera = 500; espera >= 50; espera -= 50) {
    digitalWrite(IZQ, HIGH); digitalWrite(DER, LOW);
    delay(espera);
    digitalWrite(IZQ, LOW);  digitalWrite(DER, HIGH);
    delay(espera);
  }
}
''', 'La variable espera empieza en 500 ms y baja de 50 en 50, así cada cambio es más rápido que el anterior. Cuando llega a 50 el ciclo for termina y el loop() empieza de nuevo.',
  'Haz que después de acelerar también frene poco a poco.')

P('Vela de cumpleaños RGB', CAT, 2, ['cumpleanos','vela rgb','fiesta','celebracion'],
  'Un LED RGB cambia de color al azar como una vela de fiesta.',
  [C('rgb', 'Vela de colores', r='D9', g='D10', b='D11')],
  '''
// Vela de fiesta con colores al azar
const int R = 9, G = 10, B = 11;

void setup() {
  pinMode(R, OUTPUT); pinMode(G, OUTPUT); pinMode(B, OUTPUT);
}

void loop() {
  analogWrite(R, random(256));
  analogWrite(G, random(256));
  analogWrite(B, random(256));
  delay(random(100, 400));
}
''', 'Cada vez que se repite el loop() se elige un brillo al azar para el rojo, el verde y el azul. La mezcla da un color nuevo cada vez.',
  'Haz que solo aparezcan colores cálidos (rojo y naranja).')
