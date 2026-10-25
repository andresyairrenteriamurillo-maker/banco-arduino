from p_base import *
CAT = 'Perillas y señales analógicas'

P('Brillo con perilla', CAT, 1, ['brillo con perilla','regular brillo','dimmer con potenciometro','perilla de luz'],
  'Al girar el potenciómetro el LED brilla más o menos.',
  [C('pot', 'Perilla', w='A0'), C('led', 'Lámpara', 'blanco', a='D9')],
  '''
// Brillo con perilla
const int PERILLA = A0;
const int LAMPARA = 9;       // pin PWM (~)

void setup() {
  Serial.begin(9600);
  pinMode(LAMPARA, OUTPUT);
}

void loop() {
  int lectura = analogRead(PERILLA);          // 0 a 1023
  int brillo = map(lectura, 0, 1023, 0, 255); // 0 a 255
  analogWrite(LAMPARA, brillo);
  Serial.print("Lectura: "); Serial.print(lectura);
  Serial.print("  Brillo: "); Serial.println(brillo);
  delay(50);
}
''', 'La entrada analógica entrega números de 0 a 1023, pero analogWrite() acepta de 0 a 255. La función map() hace esa conversión.',
  'Haz que el LED se apague por completo cuando la perilla esté casi en cero.')

P('Barra de nivel con LED', CAT, 2, ['barra de nivel','vumetro','nivel con leds','grafico de barras'],
  'Cinco LED forman una barra que crece al girar la perilla, como un medidor de volumen.',
  [C('pot', 'Perilla', w='A0'), C('led', 'Nivel 1', 'verde', a='D9'), C('led', 'Nivel 2', 'verde', a='D10'), C('led', 'Nivel 3', 'amarillo', a='D11'),
   C('led', 'Nivel 4', 'amarillo', a='D12'), C('led', 'Nivel 5', 'rojo', a='D13')],
  '''
// Barra de nivel con 5 LED
const int PERILLA = A0;
int barra[] = {9, 10, 11, 12, 13};

void setup() {
  for (int i = 0; i < 5; i++) pinMode(barra[i], OUTPUT);
}

void loop() {
  int nivel = map(analogRead(PERILLA), 0, 1023, 0, 5);   // de 0 a 5 LED
  for (int i = 0; i < 5; i++) {
    if (i < nivel) digitalWrite(barra[i], HIGH);
    else digitalWrite(barra[i], LOW);
  }
  delay(30);
}
''', 'map() convierte la lectura en un número de LED a encender (0 a 5). El ciclo for enciende los que están por debajo de ese número y apaga los demás.',
  'Haz que el LED rojo parpadee cuando la barra esté llena.')

P('Velocidad de parpadeo con perilla', CAT, 1, ['velocidad de parpadeo','parpadeo ajustable','perilla de velocidad'],
  'La perilla controla qué tan rápido parpadea el LED.',
  [C('pot', 'Velocidad', w='A0'), C('led', 'LED', 'rojo', a='D13')],
  '''
// Velocidad de parpadeo ajustable
const int PERILLA = A0;
const int LED = 13;

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  int espera = map(analogRead(PERILLA), 0, 1023, 50, 1000);
  digitalWrite(LED, HIGH);
  delay(espera);
  digitalWrite(LED, LOW);
  delay(espera);
}
''', 'La lectura del potenciómetro se convierte en un tiempo de espera entre 50 y 1000 ms. Con la perilla al mínimo el LED parpadea muy rápido.',
  'Invierte el sentido: que girar a la derecha haga el parpadeo más rápido.')

P('Voltímetro en el monitor serie', CAT, 2, ['voltimetro','medir voltaje','voltios','multimetro'],
  'Mide el voltaje en la pata central del potenciómetro (de 0 a 5 V) y lo muestra en el monitor.',
  [C('pot', 'Divisor de voltaje', w='A0')],
  '''
// Voltímetro de 0 a 5 V
const int ENTRADA = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(ENTRADA);
  float voltios = lectura * 5.0 / 1023.0;    // regla de tres
  Serial.print("Voltaje: ");
  Serial.print(voltios, 2);
  Serial.println(" V");
  delay(300);
}
''', 'El Arduino divide los 5 V en 1024 pasos. Multiplicando la lectura por 5 y dividiendo por 1023 se obtiene el voltaje real con dos decimales.',
  'Agrega LED que avisen si el voltaje es menor de 1 V o mayor de 4 V.')

P('Mezclador de colores RGB', CAT, 2, ['mezclador de colores','rgb con perillas','pintar colores','mezclar colores'],
  'Tres perillas controlan el rojo, el verde y el azul de un LED RGB para crear cualquier color.',
  [C('pot', 'Rojo', w='A0'), C('pot', 'Verde', w='A1'), C('pot', 'Azul', w='A2'), C('rgb', 'LED RGB', r='D9', g='D10', b='D11')],
  '''
// Mezclador de colores con tres perillas
const int R = 9, G = 10, B = 11;

void setup() {
  Serial.begin(9600);
  pinMode(R, OUTPUT); pinMode(G, OUTPUT); pinMode(B, OUTPUT);
}

void loop() {
  int r = analogRead(A0) / 4;     // de 0-1023 a 0-255
  int g = analogRead(A1) / 4;
  int b = analogRead(A2) / 4;
  analogWrite(R, r); analogWrite(G, g); analogWrite(B, b);
  Serial.print("R="); Serial.print(r);
  Serial.print(" G="); Serial.print(g);
  Serial.print(" B="); Serial.println(b);
  delay(100);
}
''', 'Dividir la lectura entre 4 es otra forma de pasar de 0–1023 a 0–255. Cada perilla controla un color y la mezcla aparece en el LED RGB.',
  'Busca la combinación que da el color naranja y anótala.')

P('Servo con perilla', CAT, 1, ['servo con perilla','mover servo','girar servo','control de servo'],
  'El brazo del servo sigue el giro de la perilla, de 0 a 180 grados.',
  [C('pot', 'Perilla', w='A0'), C('servo', 'Servo', s='D9')],
  SERVO_INC + '''Servo brazo;

void setup() {
  Serial.begin(9600);
  brazo.attach(9);           // señal del servo en D9
}

void loop() {
  int angulo = map(analogRead(A0), 0, 1023, 0, 180);
  brazo.write(angulo);
  Serial.print("Ángulo: ");
  Serial.println(angulo);
  delay(20);
}
''', 'La librería Servo genera los pulsos que entiende el servo. write() recibe un ángulo de 0 a 180 grados, que obtenemos con map() desde la perilla.',
  'Limita el movimiento entre 45 y 135 grados.')

P('Ventilador de velocidad variable', CAT, 2, ['ventilador variable','velocidad de motor','motor con perilla','regular motor'],
  'La perilla regula la velocidad de un motor de ventilador.',
  [C('pot', 'Velocidad', w='A0'), C('motor', 'Ventilador', p='D6')],
  '''
// Ventilador de velocidad variable
const int PERILLA = A0;
const int MOTOR = 6;          // pin PWM (~)

void setup() {
  Serial.begin(9600);
  pinMode(MOTOR, OUTPUT);
}

void loop() {
  int velocidad = map(analogRead(PERILLA), 0, 1023, 0, 255);
  analogWrite(MOTOR, velocidad);
  int porcentaje = velocidad * 100 / 255;
  Serial.print("Velocidad: ");
  Serial.print(porcentaje);
  Serial.println(" %");
  delay(100);
}
''', 'Con PWM el motor recibe pulsos de energía: con más tiempo encendido gira más rápido. Es el mismo principio del brillo del LED.',
  'Agrega un botón para apagar el ventilador de inmediato.',
  notas=['En la vida real el motor se conecta con un transistor (por ejemplo TIP120) y un diodo, porque un pin solo da 40 mA.'],
  extra=['Transistor TIP120 y diodo 1N4007'])

P('Adivina el número con perilla', CAT, 2, ['adivina el numero','juego de adivinar','numero secreto','frio caliente'],
  'El Arduino piensa un número del 0 al 10; gira la perilla y los LED te dicen si estás frío o caliente.',
  [C('pot', 'Tu número', w='A0'), C('button', 'Probar', x='D2'), C('led', 'Más alto', 'azul', a='D11'), C('led', 'Más bajo', 'amarillo', a='D12'), C('led', '¡Correcto!', 'verde', a='D13')],
  '''
// Adivina el número secreto
const int BOTON = 2;
const int SUBE = 11, BAJA = 12, BIEN = 13;
int secreto;

void setup() {
  Serial.begin(9600);
  pinMode(BOTON, INPUT_PULLUP);
  pinMode(SUBE, OUTPUT); pinMode(BAJA, OUTPUT); pinMode(BIEN, OUTPUT);
  secreto = random(0, 11);
  Serial.println("Pensé un número del 0 al 10");
}

void loop() {
  int intento = map(analogRead(A0), 0, 1023, 0, 10);
  if (digitalRead(BOTON) == LOW) {
    Serial.print("Probaste el ");
    Serial.println(intento);
    digitalWrite(SUBE, LOW); digitalWrite(BAJA, LOW);
    if (intento < secreto) digitalWrite(SUBE, HIGH);
    else if (intento > secreto) digitalWrite(BAJA, HIGH);
    else {
      Serial.println("¡Adivinaste!");
      for (int i = 0; i < 5; i++) { digitalWrite(BIEN, HIGH); delay(150); digitalWrite(BIEN, LOW); delay(150); }
      secreto = random(0, 11);
    }
    delay(400);
  }
}
''', 'El número secreto se elige con random() al iniciar. Al presionar el botón se compara tu intento: el LED azul pide subir y el amarillo pide bajar.',
  'Cuenta cuántos intentos necesitaste.')

P('Joystick que mueve una luz', CAT, 2, ['joystick con leds','palanca de luces','direccion','control de direccion'],
  'Cuatro LED muestran hacia dónde mueves el joystick: arriba, abajo, izquierda o derecha.',
  [C('joystick', 'Joystick', x='A0', y='A1', s='D2'), C('led', 'Arriba', 'verde', a='D10'), C('led', 'Abajo', 'rojo', a='D11'),
   C('led', 'Izquierda', 'amarillo', a='D12'), C('led', 'Derecha', 'azul', a='D13')],
  '''
// Joystick que enciende la luz de su dirección
const int ARRIBA = 10, ABAJO = 11, IZQ = 12, DER = 13;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);           // botón del joystick
  pinMode(ARRIBA, OUTPUT); pinMode(ABAJO, OUTPUT); pinMode(IZQ, OUTPUT); pinMode(DER, OUTPUT);
}

void loop() {
  int x = analogRead(A0);             // 0 izquierda, 512 centro, 1023 derecha
  int y = analogRead(A1);             // 0 abajo, 512 centro, 1023 arriba
  digitalWrite(DER, x > 700);
  digitalWrite(IZQ, x < 300);
  digitalWrite(ARRIBA, y > 700);
  digitalWrite(ABAJO, y < 300);
  if (digitalRead(2) == LOW) Serial.println("¡Botón del joystick!");
  delay(50);
}
''', 'El joystick tiene dos potenciómetros: uno por eje. En el centro cada uno lee cerca de 512. Si un eje pasa de 700 o baja de 300, se enciende el LED de esa dirección.',
  'Haz que el botón del joystick encienda los cuatro LED a la vez.')

P('Brazo de dos servos con joystick', CAT, 3, ['brazo robot joystick','dos servos','pan tilt','camara movil'],
  'Un joystick mueve dos servos: uno gira a los lados y el otro sube y baja, como una cámara de vigilancia.',
  [C('joystick', 'Joystick', x='A0', y='A1', s='D2'), C('servo', 'Servo base', s='D9'), C('servo', 'Servo inclinación', s='D10'), C('supply', 'Fuente 5 V para los servos')],
  SERVO_INC + '''Servo base, inclinacion;
int anguloX = 90, anguloY = 90;

void setup() {
  base.attach(9);
  inclinacion.attach(10);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  int x = analogRead(A0), y = analogRead(A1);
  if (x > 700) anguloX += 2;          // mover poco a poco
  if (x < 300) anguloX -= 2;
  if (y > 700) anguloY += 2;
  if (y < 300) anguloY -= 2;
  if (digitalRead(2) == LOW) { anguloX = 90; anguloY = 90; }   // botón: volver al centro
  anguloX = constrain(anguloX, 0, 180);
  anguloY = constrain(anguloY, 20, 160);
  base.write(anguloX);
  inclinacion.write(anguloY);
  delay(20);
}
''', 'En lugar de copiar la posición del joystick, cada servo avanza 2 grados mientras la palanca esté inclinada. Así el movimiento es suave y la posición se mantiene al soltar.',
  'Agrega un LED que se encienda cuando algún servo llegue a su límite.',
  notas=['Dos servos pueden pedir más corriente de la que da el USB: aliméntalos con una fuente externa de 5 V y une los GND.'])

P('Luxómetro casero', CAT, 2, ['luxometro','medir luz','cantidad de luz','sensor de luz'],
  'Mide la luz del lugar y la clasifica: oscuro, penumbra, normal o muy brillante.',
  [C('ldr', 'Sensor de luz', y='A0')],
  '''
// Luxómetro casero
const int LUZ = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int nivel = analogRead(LUZ);
  int porcentaje = map(nivel, 0, 1023, 0, 100);
  Serial.print("Luz: ");
  Serial.print(porcentaje);
  Serial.print(" % -> ");
  if (porcentaje < 20) Serial.println("Oscuro");
  else if (porcentaje < 45) Serial.println("Penumbra");
  else if (porcentaje < 80) Serial.println("Normal");
  else Serial.println("Muy brillante");
  delay(500);
}
''', 'Una cadena de if y else if compara la luz con varios límites, de menor a mayor, y escribe la categoría que corresponde.',
  'Mide la luz de tu salón a distintas horas del día y anótala.')

P('Termómetro de perilla para practicar', CAT, 1, ['simular temperatura','practica de condicionales','perilla como sensor'],
  'Usa la perilla como si fuera un sensor de temperatura para practicar decisiones con if.',
  [C('pot', 'Temperatura simulada', w='A0'), C('led', 'Frío', 'azul', a='D11'), C('led', 'Normal', 'verde', a='D12'), C('led', 'Calor', 'rojo', a='D13')],
  '''
// Practicar decisiones: perilla como "temperatura"
const int FRIO = 11, NORMAL = 12, CALOR = 13;

void setup() {
  Serial.begin(9600);
  pinMode(FRIO, OUTPUT); pinMode(NORMAL, OUTPUT); pinMode(CALOR, OUTPUT);
}

void loop() {
  int temperatura = map(analogRead(A0), 0, 1023, 0, 40);   // de 0 a 40 °C
  digitalWrite(FRIO, temperatura < 15);
  digitalWrite(NORMAL, temperatura >= 15 && temperatura <= 28);
  digitalWrite(CALOR, temperatura > 28);
  Serial.print(temperatura);
  Serial.println(" °C");
  delay(200);
}
''', 'Una comparación como temperatura < 15 vale 1 (verdadero) o 0 (falso), así que se puede usar directo en digitalWrite(). El operador && significa "y".',
  'Cambia los límites para un lugar de clima frío.')

CAT = 'Luz y oscuridad'

P('Interruptor crepuscular', CAT, 1, ['crepuscular','luz automatica','enciende de noche','fotocelda'],
  'Una lámpara se enciende sola cuando oscurece, como el alumbrado de un parque.',
  [C('ldr', 'Fotocelda', y='A0'), C('led', 'Lámpara', 'blanco', a='D13')],
  '''
// Interruptor crepuscular
const int FOTOCELDA = A0;
const int LAMPARA = 13;
const int UMBRAL = 350;       // por debajo de esto es "de noche"

void setup() {
  Serial.begin(9600);
  pinMode(LAMPARA, OUTPUT);
}

void loop() {
  int luz = analogRead(FOTOCELDA);
  Serial.println(luz);
  if (luz < UMBRAL) digitalWrite(LAMPARA, HIGH);
  else digitalWrite(LAMPARA, LOW);
  delay(200);
}
''', 'La fotocelda forma un divisor de voltaje con la resistencia de 10 kΩ: con poca luz el valor leído baja. Si baja del umbral, se enciende la lámpara.',
  'Agrega un margen para que la lámpara no titile cuando la luz está justo en el límite.')

P('Alarma de cajón abierto', CAT, 1, ['alarma de cajon','cajon abierto','proteger cajon','detector de apertura'],
  'Dentro de un cajón cerrado está oscuro: si alguien lo abre y entra luz, suena la alarma.',
  [C('ldr', 'Sensor de luz', y='A0'), C('buzzer', 'Alarma', p='D8')],
  '''
// Alarma de cajón abierto
const int LUZ = A0;
const int ALARMA = 8;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int luz = analogRead(LUZ);
  if (luz > 500) {                       // entró luz: alguien abrió
    Serial.println("¡Abrieron el cajón!");
    tone(ALARMA, 2000, 200);
    delay(300);
  }
  delay(100);
}
''', 'El programa aprovecha que dentro de un cajón cerrado no hay luz. Cuando la lectura sube por encima de 500, significa que lo abrieron.',
  'Cuenta cuántas veces abrieron el cajón durante el día.')

P('Lámpara de lectura automática', CAT, 2, ['lampara de lectura','brillo automatico','luz compensada','brillo segun luz'],
  'El LED da más luz cuando el lugar está más oscuro, para leer siempre con la misma iluminación.',
  [C('ldr', 'Sensor de luz', y='A0'), C('led', 'Lámpara', 'blanco', a='D9')],
  '''
// Lámpara que compensa la oscuridad
const int LUZ = A0;
const int LAMPARA = 9;        // pin PWM (~)

void setup() {
  pinMode(LAMPARA, OUTPUT);
}

void loop() {
  int ambiente = analogRead(LUZ);
  int brillo = map(ambiente, 0, 1023, 255, 0);   // al revés: menos luz, más brillo
  analogWrite(LAMPARA, brillo);
  delay(50);
}
''', 'Fíjate que en map() el rango de salida va de 255 a 0: así, cuando el ambiente tiene poca luz (número bajo), el LED recibe un brillo alto.',
  'Pon un brillo mínimo para que la lámpara nunca se apague del todo.')

P('Medidor de luz con barra de LED', CAT, 2, ['medidor de luz','barra de luz','nivel de luz con leds'],
  'Cuatro LED muestran cuánta luz hay: más luz, más LED encendidos.',
  [C('ldr', 'Sensor de luz', y='A0'), C('led', 'Poca', 'rojo', a='D10'), C('led', 'Media', 'amarillo', a='D11'),
   C('led', 'Buena', 'verde', a='D12'), C('led', 'Mucha', 'blanco', a='D13')],
  '''
// Medidor de luz con 4 LED
int barra[] = {10, 11, 12, 13};

void setup() {
  for (int i = 0; i < 4; i++) pinMode(barra[i], OUTPUT);
}

void loop() {
  int n = map(analogRead(A0), 0, 1023, 0, 4);
  for (int i = 0; i < 4; i++) digitalWrite(barra[i], i < n);
  delay(100);
}
''', 'Igual que la barra de nivel con perilla, pero ahora la entrada es la luz. El mismo programa sirve para distintos sensores: eso es lo bueno de las entradas analógicas.',
  'Agrega un zumbador que suene si hay demasiada luz.')

P('Detector de día y noche en pantalla', CAT, 2, ['dia y noche','lcd luz','pantalla dia noche','reloj solar'],
  'Una pantalla LCD dice si es de día o de noche y muestra el nivel de luz.',
  [C('ldr', 'Sensor de luz', y='A0'), C('lcd', 'Pantalla LCD')],
  LCD_INC + '''
void setup() {
  lcd.init();
  lcd.backlight();
}

void loop() {
  int luz = analogRead(A0);
  lcd.clear();
  lcd.setCursor(0, 0);
  if (luz > 400) lcd.print("Es de dia :)");
  else lcd.print("Es de noche");
  lcd.setCursor(0, 1);
  lcd.print("Luz: ");
  lcd.print(map(luz, 0, 1023, 0, 100));
  lcd.print(" %");
  delay(500);
}
''', 'La pantalla LCD con módulo I2C solo necesita 4 cables. setCursor(columna, fila) elige dónde escribir: la fila 0 es la de arriba y la fila 1 la de abajo.',
  'Agrega un LED que se encienda de noche.')

P('Barrera láser cuenta-objetos', CAT, 2, ['barrera laser','contador de objetos','banda transportadora','contar con luz'],
  'Cada vez que un objeto tapa la luz que llega al sensor, el contador suma uno.',
  [C('ldr', 'Sensor de la barrera', y='A0'), C('buzzer', 'Bip', p='D8')],
  '''
// Contador de objetos con barrera de luz
const int SENSOR = A0;
const int BIP = 8;
int cuenta = 0;
bool tapado = false;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int luz = analogRead(SENSOR);
  if (!tapado && luz < 300) {           // un objeto empezó a tapar la luz
    tapado = true;
    cuenta++;
    tone(BIP, 1500, 60);
    Serial.print("Objetos: ");
    Serial.println(cuenta);
  }
  if (tapado && luz > 450) tapado = false;   // el objeto ya pasó
  delay(10);
}
''', 'La variable tapado evita contar el mismo objeto muchas veces mientras pasa. Se usan dos límites distintos (300 y 450) para que una sombra temblorosa no cuente doble.',
  'Muestra la cuenta en una pantalla LCD.',
  notas=['En la vida real se apunta un puntero láser o una linterna hacia el sensor, al otro lado del camino.'],
  extra=['Puntero láser o linterna'])

P('Girasol de un servo', CAT, 3, ['girasol','buscar luz','seguidor de luz','orientar a la luz'],
  'Un servo con un sensor de luz busca hacia dónde hay más luz y se queda mirando hacia allá.',
  [C('ldr', 'Ojo de luz', y='A0'), C('servo', 'Cuello', s='D9')],
  SERVO_INC + '''Servo cuello;

void setup() {
  Serial.begin(9600);
  cuello.attach(9);
}

void loop() {
  int mejorAngulo = 0, mejorLuz = 0;
  for (int a = 0; a <= 180; a += 10) {    // barre de lado a lado
    cuello.write(a);
    delay(80);
    int luz = analogRead(A0);
    if (luz > mejorLuz) { mejorLuz = luz; mejorAngulo = a; }
  }
  cuello.write(mejorAngulo);             // vuelve al punto con más luz
  Serial.print("Más luz en ");
  Serial.print(mejorAngulo);
  Serial.println(" grados");
  delay(5000);
}
''', 'El servo recorre de 0 a 180 grados de 10 en 10 y en cada posición mide la luz. Guarda el ángulo con la medida más alta y al final vuelve a él.',
  'Haz que el servo se mueva más lento para medir con más cuidado.')

P('Luz nocturna con colores', CAT, 2, ['luz nocturna rgb','lampara de noche','luz de colores nocturna'],
  'De noche un LED RGB se enciende con un color suave que cambia lentamente para ayudar a dormir.',
  [C('ldr', 'Sensor de luz', y='A0'), C('rgb', 'Lámpara RGB', r='D9', g='D10', b='D11')],
  '''
// Luz nocturna de colores suaves
const int R = 9, G = 10, B = 11;
int paso = 0;

void setup() {
  pinMode(R, OUTPUT); pinMode(G, OUTPUT); pinMode(B, OUTPUT);
}

void loop() {
  if (analogRead(A0) < 300) {               // está oscuro
    paso = (paso + 1) % 360;
    float t = paso * 3.1416 / 180.0;
    analogWrite(R, 40 + 40 * sin(t));
    analogWrite(G, 20);
    analogWrite(B, 60 + 50 * sin(t + 2));
  } else {
    analogWrite(R, 0); analogWrite(G, 0); analogWrite(B, 0);
  }
  delay(40);
}
''', 'La función seno (sin) sube y baja suavemente entre −1 y 1. Usándola para el rojo y el azul con un pequeño desfase, los colores cambian despacio sin saltos.',
  'Haz que la luz se apague sola después de 30 minutos.')
