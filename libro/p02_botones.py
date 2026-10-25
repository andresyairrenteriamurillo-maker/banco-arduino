from p_base import *
CAT = 'Botones e interruptores'

P('LED con botón', CAT, 1, ['led con boton','pulsador','encender con boton','boton y led'],
  'El LED se enciende solo mientras mantienes presionado el botón.',
  [C('button', 'Botón', x='D2'), C('led', 'LED verde', 'verde', a='D13')],
  '''
// LED con botón
const int BOTON = 2;
const int LED = 13;

void setup() {
  pinMode(BOTON, INPUT_PULLUP);   // resistencia interna: suelto = HIGH
  pinMode(LED, OUTPUT);
}

void loop() {
  if (digitalRead(BOTON) == LOW) {  // presionado = LOW
    digitalWrite(LED, HIGH);
  } else {
    digitalWrite(LED, LOW);
  }
}
''', 'Con INPUT_PULLUP el pin lee HIGH cuando el botón está suelto; al presionarlo, el botón une el pin con GND y lee LOW. El if decide si el LED se enciende.',
  'Invierte el funcionamiento: que el LED esté encendido y se apague al presionar.')

P('Interruptor de luz con un toque', CAT, 1, ['interruptor de luz','toggle','encender y apagar','lampara con boton'],
  'Cada vez que presionas el botón la lámpara cambia: si estaba apagada se enciende, y al revés.',
  [C('button', 'Botón de la lámpara', x='D2'), C('led', 'Lámpara', 'amarillo', a='D13')],
  '''
// Interruptor de un toque (encender / apagar)
const int BOTON = 2;
const int LAMPARA = 13;
bool encendida = false;
int anterior = HIGH;

void setup() {
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(LAMPARA, OUTPUT);
}

void loop() {
  int ahora = digitalRead(BOTON);
  if (anterior == HIGH && ahora == LOW) {   // el botón se acaba de presionar
    encendida = !encendida;                 // cambia el estado
    digitalWrite(LAMPARA, encendida);
    delay(50);                              // evita rebotes
  }
  anterior = ahora;
}
''', 'El programa recuerda cómo estaba el botón la vez anterior. Solo cuando pasa de suelto (HIGH) a presionado (LOW) cambia el estado de la lámpara; así un toque largo no la hace parpadear.',
  'Agrega un segundo LED que se encienda cuando la lámpara esté apagada.')

P('Contador de pulsaciones', CAT, 1, ['contador','contar pulsaciones','cuantas veces','clics'],
  'Cuenta cuántas veces presionas el botón y lo muestra en el monitor serie.',
  [C('button', 'Botón', x='D2')],
  '''
// Contador de pulsaciones
const int BOTON = 2;
int cuenta = 0;
int anterior = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(BOTON, INPUT_PULLUP);
  Serial.println("Presiona el botón");
}

void loop() {
  int ahora = digitalRead(BOTON);
  if (anterior == HIGH && ahora == LOW) {
    cuenta++;
    Serial.print("Pulsaciones: ");
    Serial.println(cuenta);
    delay(50);
  }
  anterior = ahora;
}
''', 'La variable cuenta aumenta en 1 cada vez que el botón pasa de suelto a presionado. Serial.println() envía el número al computador por el cable USB.',
  'Haz que al llegar a 10 pulsaciones se encienda un LED de premio.')

P('Timbre sencillo', CAT, 1, ['timbre sencillo','timbre','ding dong','campana'],
  'Al presionar el botón suena un "ding-dong" en el zumbador.',
  [C('button', 'Botón del timbre', x='D2'), C('buzzer', 'Zumbador', p='D8')],
  '''
// Timbre ding-dong
const int BOTON = 2;
const int ZUMBADOR = 8;

void setup() {
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(ZUMBADOR, OUTPUT);
}

void loop() {
  if (digitalRead(BOTON) == LOW) {
    tone(ZUMBADOR, 880, 300);   // "ding": nota alta
    delay(350);
    tone(ZUMBADOR, 660, 500);   // "dong": nota más baja
    delay(800);
  }
}
''', 'tone(pin, frecuencia, duración) hace sonar el zumbador. 880 Hz es una nota alta y 660 Hz una más baja; seguidas forman el sonido clásico del timbre.',
  'Cambia las notas para inventar el sonido de tu propio timbre.')

P('Dimmer con dos botones', CAT, 2, ['dimmer','subir brillo','bajar brillo','regular luz con botones'],
  'Un botón sube el brillo del LED y el otro lo baja.',
  [C('button', 'Subir', x='D2'), C('button', 'Bajar', x='D3'), C('led', 'Lámpara', 'blanco', a='D9')],
  '''
// Dimmer con dos botones
const int SUBIR = 2;
const int BAJAR = 3;
const int LAMPARA = 9;      // pin PWM (~)
int brillo = 100;

void setup() {
  Serial.begin(9600);
  pinMode(SUBIR, INPUT_PULLUP);
  pinMode(BAJAR, INPUT_PULLUP);
  pinMode(LAMPARA, OUTPUT);
}

void loop() {
  if (digitalRead(SUBIR) == LOW) brillo = brillo + 5;
  if (digitalRead(BAJAR) == LOW) brillo = brillo - 5;
  brillo = constrain(brillo, 0, 255);   // no salirse de 0 a 255
  analogWrite(LAMPARA, brillo);
  Serial.print("Brillo: ");
  Serial.println(brillo);
  delay(60);
}
''', 'Mientras un botón está presionado el brillo cambia de 5 en 5. constrain() evita que el valor se salga del rango que acepta analogWrite().',
  'Muestra el brillo en porcentaje (0 % a 100 %) en el monitor serie.')

P('¿Quién presiona primero?', CAT, 2, ['quien presiona primero','concurso','dos jugadores','boton de concurso','juego de velocidad'],
  'Dos jugadores esperan la luz amarilla: el primero en presionar su botón gana.',
  [C('button', 'Jugador 1', x='D2'), C('button', 'Jugador 2', x='D3'), C('led', 'Señal', 'amarillo', a='D11'),
   C('led', 'Gana 1', 'rojo', a='D12'), C('led', 'Gana 2', 'azul', a='D13')],
  '''
// ¿Quién presiona primero?
const int J1 = 2, J2 = 3;
const int SENAL = 11, GANA1 = 12, GANA2 = 13;

void setup() {
  Serial.begin(9600);
  pinMode(J1, INPUT_PULLUP); pinMode(J2, INPUT_PULLUP);
  pinMode(SENAL, OUTPUT); pinMode(GANA1, OUTPUT); pinMode(GANA2, OUTPUT);
}

void loop() {
  digitalWrite(GANA1, LOW); digitalWrite(GANA2, LOW);
  Serial.println("Prepárense...");
  delay(random(2000, 5000));          // espera al azar
  digitalWrite(SENAL, HIGH);           // ¡ya!
  while (true) {
    if (digitalRead(J1) == LOW) { digitalWrite(GANA1, HIGH); Serial.println("¡Gana el jugador 1!"); break; }
    if (digitalRead(J2) == LOW) { digitalWrite(GANA2, HIGH); Serial.println("¡Gana el jugador 2!"); break; }
  }
  digitalWrite(SENAL, LOW);
  delay(3000);
}
''', 'Después de una espera al azar se enciende la señal. El ciclo while(true) revisa los dos botones una y otra vez; el primero que detecte presionado gana y break termina la espera.',
  'Castiga al que presione antes de que se encienda la señal.')

P('Dado electrónico de LED', CAT, 2, ['dado de leds','dado','numero al azar','juego de mesa'],
  'Al presionar el botón, seis LED muestran un número al azar del 1 al 6.',
  [C('button', 'Lanzar', x='D2'), C('led', 'Punto 1', 'rojo', a='D8'), C('led', 'Punto 2', 'rojo', a='D9'), C('led', 'Punto 3', 'rojo', a='D10'),
   C('led', 'Punto 4', 'rojo', a='D11'), C('led', 'Punto 5', 'rojo', a='D12'), C('led', 'Punto 6', 'rojo', a='D13')],
  '''
// Dado electrónico: enciende tantos LED como el número
const int BOTON = 2;
int puntos[] = {8, 9, 10, 11, 12, 13};

void mostrar(int n) {
  for (int i = 0; i < 6; i++) {
    if (i < n) digitalWrite(puntos[i], HIGH);
    else digitalWrite(puntos[i], LOW);
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(BOTON, INPUT_PULLUP);
  for (int i = 0; i < 6; i++) pinMode(puntos[i], OUTPUT);
}

void loop() {
  if (digitalRead(BOTON) == LOW) {
    for (int k = 0; k < 10; k++) { mostrar(random(1, 7)); delay(60); }   // animación
    int dado = random(1, 7);
    mostrar(dado);
    Serial.print("Salió: ");
    Serial.println(dado);
    delay(500);
  }
}
''', 'random(1, 7) da un número entre 1 y 6. Antes de mostrar el resultado se hace una animación rápida de números al azar, como si el dado rodara.',
  'Usa dos botones para lanzar dos dados y sumar los resultados.')

P('Botón de pánico', CAT, 1, ['boton de panico','emergencia','sos con boton','alerta'],
  'Al presionar el botón se activa una alarma de luz y sonido que solo se apaga con el interruptor.',
  [C('button', 'Botón de pánico', x='D2'), C('switch', 'Apagar alarma', x='D3'), C('buzzer', 'Sirena', p='D8'), C('led', 'Luz de alerta', 'rojo', a='D13')],
  '''
// Botón de pánico
const int PANICO = 2;
const int APAGAR = 3;
const int SIRENA = 8;
const int LUZ = 13;
bool alarma = false;

void setup() {
  pinMode(PANICO, INPUT_PULLUP);
  pinMode(APAGAR, INPUT_PULLUP);
  pinMode(SIRENA, OUTPUT);
  pinMode(LUZ, OUTPUT);
}

void loop() {
  if (digitalRead(PANICO) == LOW) alarma = true;    // se activa
  if (digitalRead(APAGAR) == LOW) alarma = false;   // interruptor activado: se apaga
  if (alarma) {
    digitalWrite(LUZ, HIGH); tone(SIRENA, 1200); delay(200);
    digitalWrite(LUZ, LOW);  tone(SIRENA, 800);  delay(200);
  } else {
    digitalWrite(LUZ, LOW);
    noTone(SIRENA);
  }
}
''', 'La variable alarma recuerda que el botón se presionó aunque ya lo hayas soltado. Solo el interruptor la vuelve a false. Mientras está activa, la sirena alterna dos tonos.',
  'Haz que la alarma también se apague sola después de 30 segundos.')

P('Selector de modos de luz', CAT, 2, ['selector de modos','modos','cambiar modo','boton de modos'],
  'Cada toque del botón cambia el modo del LED: apagado, encendido, parpadeo lento y parpadeo rápido.',
  [C('button', 'Modo', x='D2'), C('led', 'Luz', 'verde', a='D13')],
  '''
// Selector de modos con un botón
const int BOTON = 2;
const int LUZ = 13;
int modo = 0;          // 0 apagado, 1 encendido, 2 lento, 3 rápido
int anterior = HIGH;
unsigned long ultimo = 0;
bool estado = false;

void setup() {
  Serial.begin(9600);
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(LUZ, OUTPUT);
}

void loop() {
  int ahora = digitalRead(BOTON);
  if (anterior == HIGH && ahora == LOW) {
    modo = (modo + 1) % 4;
    Serial.print("Modo ");
    Serial.println(modo);
    delay(50);
  }
  anterior = ahora;
  int periodo = 0;
  if (modo == 2) periodo = 600;
  if (modo == 3) periodo = 150;
  if (modo == 0) digitalWrite(LUZ, LOW);
  if (modo == 1) digitalWrite(LUZ, HIGH);
  if (periodo > 0 && millis() - ultimo > periodo) {   // parpadeo sin delay
    estado = !estado;
    digitalWrite(LUZ, estado);
    ultimo = millis();
  }
}
''', 'millis() cuenta los milisegundos desde que arrancó el Arduino. Comparándolo con la última vez que cambió el LED se puede parpadear sin delay(), y así el botón responde siempre al instante.',
  'Agrega un quinto modo: latido del corazón.')

P('Juego de reflejos con dos LED', CAT, 2, ['reflejos','tiempo de reaccion','reaccion','velocidad de reaccion'],
  'Mide en milisegundos qué tan rápido presionas el botón cuando se enciende el LED.',
  [C('button', 'Botón', x='D2'), C('led', 'Prepárate', 'amarillo', a='D12'), C('led', '¡Ya!', 'verde', a='D13')],
  '''
// Tiempo de reacción
const int BOTON = 2;
const int LISTO = 12;
const int YA = 13;

void setup() {
  Serial.begin(9600);
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(LISTO, OUTPUT);
  pinMode(YA, OUTPUT);
}

void loop() {
  digitalWrite(LISTO, HIGH);
  delay(random(1500, 4000));
  digitalWrite(LISTO, LOW);
  digitalWrite(YA, HIGH);
  unsigned long inicio = millis();
  while (digitalRead(BOTON) == HIGH) { }        // espera a que lo presionen
  unsigned long tiempo = millis() - inicio;
  digitalWrite(YA, LOW);
  Serial.print("Tu tiempo de reacción: ");
  Serial.print(tiempo);
  Serial.println(" ms");
  delay(2500);
}
''', 'Al encender el LED verde se guarda la hora con millis(). Cuando se presiona el botón se resta esa hora y se obtiene cuántos milisegundos tardaste.',
  'Guarda tu mejor tiempo y muéstralo cada vez que lo superes.')

P('Cerradura de secuencia de botones', CAT, 2, ['secuencia','cerradura de botones','combinacion','codigo secreto con botones'],
  'Tres botones forman una combinación secreta: solo la secuencia correcta enciende la luz verde.',
  [C('button', 'Botón A', x='D2'), C('button', 'Botón B', x='D3'), C('button', 'Botón C', x='D4'),
   C('led', 'Abierto', 'verde', a='D12'), C('led', 'Error', 'rojo', a='D13')],
  '''
// Cerradura de secuencia: la clave es A, C, B
const int A = 2, B = 3, CC = 4;
const int VERDE = 12, ROJO = 13;
int clave[] = {2, 4, 3};       // A, C, B
int paso = 0;

int leerBoton() {              // devuelve el pin presionado o 0
  if (digitalRead(A) == LOW) return A;
  if (digitalRead(B) == LOW) return B;
  if (digitalRead(CC) == LOW) return CC;
  return 0;
}

void setup() {
  Serial.begin(9600);
  pinMode(A, INPUT_PULLUP); pinMode(B, INPUT_PULLUP); pinMode(CC, INPUT_PULLUP);
  pinMode(VERDE, OUTPUT); pinMode(ROJO, OUTPUT);
}

void loop() {
  int b = leerBoton();
  if (b == 0) return;
  while (leerBoton() != 0) { }     // espera a que lo suelten
  if (b == clave[paso]) {
    paso++;
    Serial.print("Paso correcto ");
    Serial.println(paso);
    if (paso == 3) {
      Serial.println("¡Abierto!");
      digitalWrite(VERDE, HIGH); delay(3000); digitalWrite(VERDE, LOW);
      paso = 0;
    }
  } else {
    Serial.println("Clave incorrecta");
    digitalWrite(ROJO, HIGH); delay(1000); digitalWrite(ROJO, LOW);
    paso = 0;
  }
}
''', 'El arreglo clave guarda el orden correcto. La variable paso dice cuántos botones correctos llevas. Un error devuelve paso a 0 y hay que empezar de nuevo.',
  'Cambia la clave por una de cuatro botones.')

P('Lámpara con temporizador', CAT, 1, ['temporizador de luz','luz de escalera','apagado automatico','lampara con tiempo'],
  'Como la luz de una escalera: al presionar el botón se enciende y se apaga sola a los 10 segundos.',
  [C('button', 'Botón', x='D2'), C('led', 'Luz de la escalera', 'blanco', a='D13')],
  '''
// Luz de escalera con temporizador
const int BOTON = 2;
const int LUZ = 13;
const unsigned long DURACION = 10000;   // 10 segundos
unsigned long encendidaDesde = 0;
bool encendida = false;

void setup() {
  Serial.begin(9600);
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(LUZ, OUTPUT);
}

void loop() {
  if (digitalRead(BOTON) == LOW) {
    encendida = true;
    encendidaDesde = millis();           // vuelve a contar desde ahora
    digitalWrite(LUZ, HIGH);
  }
  if (encendida && millis() - encendidaDesde > DURACION) {
    encendida = false;
    digitalWrite(LUZ, LOW);
    Serial.println("Luz apagada por tiempo");
  }
}
''', 'Cada vez que se presiona el botón se guarda el momento con millis(). Cuando pasan 10 segundos desde ese momento, el LED se apaga solo.',
  'Haz que el LED parpadee los últimos 3 segundos para avisar que se va a apagar.')

P('Piano de cuatro teclas', CAT, 2, ['piano','piano de botones','teclas musicales','instrumento'],
  'Cuatro botones tocan las notas do, re, mi y fa en el zumbador.',
  [C('button', 'Do', x='D2'), C('button', 'Re', x='D3'), C('button', 'Mi', x='D4'), C('button', 'Fa', x='D5'), C('buzzer', 'Parlante', p='D8')],
  '''
// Piano de cuatro teclas
int teclas[] = {2, 3, 4, 5};
int notas[] = {262, 294, 330, 349};   // do, re, mi, fa (en hercios)
const int PARLANTE = 8;

void setup() {
  for (int i = 0; i < 4; i++) pinMode(teclas[i], INPUT_PULLUP);
}

void loop() {
  int sonando = 0;
  for (int i = 0; i < 4; i++) {
    if (digitalRead(teclas[i]) == LOW) sonando = notas[i];
  }
  if (sonando > 0) tone(PARLANTE, sonando);
  else noTone(PARLANTE);
}
''', 'Cada botón tiene asignada una frecuencia en el arreglo notas. Mientras un botón esté presionado suena su nota; si no hay ninguno, noTone() silencia el parlante.',
  'Agrega una quinta tecla con la nota sol (392 Hz).')

P('Cuenta regresiva con botón', CAT, 1, ['cuenta regresiva','despegue','cohete','10 9 8'],
  'Al presionar el botón empieza una cuenta de 10 a 0 en el monitor y al final se enciende el LED: ¡despegue!',
  [C('button', 'Iniciar', x='D2'), C('led', 'Despegue', 'rojo', a='D13'), C('buzzer', 'Motor', p='D8')],
  '''
// Cuenta regresiva para un cohete
const int BOTON = 2;
const int LUZ = 13;
const int ZUMBADOR = 8;

void setup() {
  Serial.begin(9600);
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(LUZ, OUTPUT);
  Serial.println("Presiona el botón para lanzar el cohete");
}

void loop() {
  if (digitalRead(BOTON) == LOW) {
    for (int n = 10; n > 0; n--) {
      Serial.println(n);
      tone(ZUMBADOR, 1000, 80);
      delay(1000);
    }
    Serial.println("¡DESPEGUE!");
    digitalWrite(LUZ, HIGH);
    tone(ZUMBADOR, 300, 2000);
    delay(3000);
    digitalWrite(LUZ, LOW);
  }
}
''', 'Un ciclo for cuenta desde 10 hasta 1 restando 1 cada segundo, con un pitido en cada número. Al terminar se enciende el LED y suena un tono grave largo.',
  'Agrega un segundo botón para abortar el lanzamiento.')

P('Pulsación larga y corta', CAT, 2, ['pulsacion larga','toque largo','toque corto','mantener presionado'],
  'Un toque corto enciende el LED verde y un toque largo (más de 1 segundo) enciende el rojo.',
  [C('button', 'Botón', x='D2'), C('led', 'Corto', 'verde', a='D12'), C('led', 'Largo', 'rojo', a='D13')],
  '''
// Detectar pulsación corta o larga
const int BOTON = 2;
const int CORTO = 12, LARGO = 13;

void setup() {
  Serial.begin(9600);
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(CORTO, OUTPUT); pinMode(LARGO, OUTPUT);
}

void loop() {
  if (digitalRead(BOTON) == LOW) {
    unsigned long inicio = millis();
    while (digitalRead(BOTON) == LOW) { }   // espera a que lo suelten
    unsigned long duracion = millis() - inicio;
    Serial.print("Duró ");
    Serial.print(duracion);
    Serial.println(" ms");
    int pin = CORTO;
    if (duracion > 1000) pin = LARGO;
    digitalWrite(pin, HIGH); delay(800); digitalWrite(pin, LOW);
  }
}
''', 'Se mide cuánto tiempo pasa entre que el botón se presiona y se suelta. Si fue más de 1000 ms es un toque largo. Muchos aparatos usan esto para tener dos funciones en un solo botón.',
  'Agrega una tercera opción: doble toque rápido.')

P('Alarma de puerta con interruptor', CAT, 1, ['alarma de puerta','sensor de puerta','puerta abierta','interruptor de puerta'],
  'Un interruptor imita el sensor de una puerta: si la puerta se abre suena la alarma.',
  [C('switch', 'Puerta (activado = cerrada)', x='D2'), C('buzzer', 'Alarma', p='D8'), C('led', 'Puerta abierta', 'rojo', a='D13')],
  '''
// Alarma de puerta abierta
const int PUERTA = 2;        // activado (LOW) = puerta cerrada
const int ALARMA = 8;
const int LUZ = 13;

void setup() {
  Serial.begin(9600);
  pinMode(PUERTA, INPUT_PULLUP);
  pinMode(ALARMA, OUTPUT);
  pinMode(LUZ, OUTPUT);
}

void loop() {
  if (digitalRead(PUERTA) == HIGH) {     // interruptor abierto: puerta abierta
    digitalWrite(LUZ, HIGH);
    tone(ALARMA, 1500, 150);
    Serial.println("¡La puerta está abierta!");
    delay(400);
  } else {
    digitalWrite(LUZ, LOW);
  }
}
''', 'Los sensores de puerta reales son interruptores que se cierran cuando la puerta está cerrada. Por eso la alarma suena cuando el pin lee HIGH (interruptor abierto).',
  'Haz que la alarma espere 5 segundos antes de sonar, para dar tiempo a cerrar la puerta.')

P('Marcador de dos equipos', CAT, 2, ['marcador','puntos','partido','goles','marcador deportivo'],
  'Dos botones suman goles a cada equipo y el monitor serie muestra el marcador.',
  [C('button', 'Gol equipo A', x='D2'), C('button', 'Gol equipo B', x='D3'), C('button', 'Reiniciar', x='D4'), C('buzzer', 'Pito', p='D8')],
  '''
// Marcador de dos equipos
const int GOL_A = 2, GOL_B = 3, REINICIAR = 4;
const int PITO = 8;
int a = 0, b = 0;

void mostrar() {
  Serial.print("Equipo A ");
  Serial.print(a);
  Serial.print(" - ");
  Serial.print(b);
  Serial.println(" Equipo B");
}

void esperarSoltar(int pin) {
  delay(30);
  while (digitalRead(pin) == LOW) { }
}

void setup() {
  Serial.begin(9600);
  pinMode(GOL_A, INPUT_PULLUP); pinMode(GOL_B, INPUT_PULLUP); pinMode(REINICIAR, INPUT_PULLUP);
  mostrar();
}

void loop() {
  if (digitalRead(GOL_A) == LOW) { a++; tone(PITO, 1500, 200); mostrar(); esperarSoltar(GOL_A); }
  if (digitalRead(GOL_B) == LOW) { b++; tone(PITO, 1500, 200); mostrar(); esperarSoltar(GOL_B); }
  if (digitalRead(REINICIAR) == LOW) { a = 0; b = 0; tone(PITO, 600, 600); mostrar(); esperarSoltar(REINICIAR); }
}
''', 'Cada botón suma a su propia variable. La función esperarSoltar() evita que un solo toque cuente muchos goles mientras el dedo sigue sobre el botón.',
  'Muestra el marcador en una pantalla LCD en lugar del monitor serie.')

P('Semáforo peatonal con interruptor nocturno', CAT, 2, ['modo nocturno semaforo','amarillo intermitente','semaforo nocturno'],
  'Un semáforo normal que, con el interruptor activado, pasa a modo nocturno con amarillo intermitente.',
  [C('switch', 'Modo noche', x='D2'), C('led', 'Rojo', 'rojo', a='D12'), C('led', 'Amarillo', 'amarillo', a='D11'), C('led', 'Verde', 'verde', a='D10')],
  '''
// Semáforo con modo nocturno
const int NOCHE = 2;
const int ROJO = 12, AMARILLO = 11, VERDE = 10;

void apagarTodo() {
  digitalWrite(ROJO, LOW); digitalWrite(AMARILLO, LOW); digitalWrite(VERDE, LOW);
}

void setup() {
  pinMode(NOCHE, INPUT_PULLUP);
  pinMode(ROJO, OUTPUT); pinMode(AMARILLO, OUTPUT); pinMode(VERDE, OUTPUT);
}

void loop() {
  if (digitalRead(NOCHE) == LOW) {          // modo nocturno
    apagarTodo();
    digitalWrite(AMARILLO, HIGH); delay(500);
    digitalWrite(AMARILLO, LOW);  delay(500);
  } else {                                   // modo normal
    apagarTodo(); digitalWrite(VERDE, HIGH);    delay(3000);
    apagarTodo(); digitalWrite(AMARILLO, HIGH); delay(1000);
    apagarTodo(); digitalWrite(ROJO, HIGH);     delay(3000);
  }
}
''', 'En cada vuelta del loop() se revisa el interruptor. Si está activado, el semáforo solo hace parpadear el amarillo, que en la noche significa "cruce con precaución".',
  'Haz que el cambio a modo nocturno sea automático con un sensor de luz.')
