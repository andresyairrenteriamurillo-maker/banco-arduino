from p_base import *
CAT = 'Seguridad y control de acceso'

FP_NOTE = 'Las huellas se guardan antes en el lector con el ejemplo «enroll» de la librería Adafruit Fingerprint (Archivo → Ejemplos). En el simulador ya están guardadas las huellas 1, 2 y 3.'
LOCK_NOTE = 'La chapa de 12 V nunca va al Arduino: el relé la conecta a su propia fuente de 12 V (COM al + de la fuente, NO al + de la chapa, − de la chapa al − de la fuente).'
RFID_NOTE = 'Para usar tu propia tarjeta, mira su código en el monitor serie y cámbialo en el programa (4A 3F 21 9C es la tarjeta blanca del simulador).'

P('Lector de huellas con luz verde y roja', CAT, 2, ['lector de huellas basico','huella dactilar','acceso con huella','biometrico'],
  'Pon tu dedo en el lector: si la huella está registrada se enciende la luz verde, si no, la roja.',
  [C('huella', 'Lector de huellas', t='D2', r='D3'), C('led', 'Permitido', 'verde', a='D12'), C('led', 'Denegado', 'rojo', a='D13')],
  FP_INC + FP_READ + '''
void setup() {
  Serial.begin(9600);
  finger.begin(57600);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
  if (finger.verifyPassword()) Serial.println("Lector de huellas listo");
  else Serial.println("No encuentro el lector");
}

void loop() {
  int id = leerHuella();
  if (id == -1) return;                // no hay dedo
  if (id > 0) {
    Serial.print("Huella reconocida: #"); Serial.println(id);
    digitalWrite(12, HIGH); delay(2000); digitalWrite(12, LOW);
  } else {
    Serial.println("Huella desconocida");
    digitalWrite(13, HIGH); delay(2000); digitalWrite(13, LOW);
  }
}
''', 'El lector toma una foto del dedo (getImage), la convierte en un patrón (image2Tz) y lo busca entre las huellas guardadas (fingerFastSearch). Si la encuentra, fingerID dice cuál es.',
  'Haz que la huella #1 sea del profesor y encienda los dos LED.', notas=[FP_NOTE])

P('Cerradura con huella y servo', CAT, 2, ['cerradura con huella','puerta con huella','huella y servo','abrir con el dedo'],
  'Con una huella registrada, un servo abre el pestillo de la puerta durante 3 segundos.',
  [C('huella', 'Lector de huellas', t='D2', r='D3'), C('servo', 'Pestillo', s='D9'), C('buzzer', 'Pitido', p='D8')],
  FP_INC + SERVO_INC + 'Servo pestillo;\n' + FP_READ + '''
void setup() {
  Serial.begin(9600);
  finger.begin(57600);
  pestillo.attach(9);
  pestillo.write(0);                   // cerrado
}

void loop() {
  int id = leerHuella();
  if (id > 0) {
    Serial.print("Bienvenido, huella #"); Serial.println(id);
    tone(8, 1500, 150);
    pestillo.write(90);                // abrir
    delay(3000);
    pestillo.write(0);                 // cerrar
  } else if (id == 0) {
    Serial.println("Acceso denegado");
    tone(8, 300, 600);
  }
}
''', 'Cuando la huella es válida el servo gira 90 grados y corre el pestillo. Si la huella no está registrada, suena un tono grave de error y la puerta sigue cerrada.',
  'Agrega una LCD que diga "Bienvenido" o "Denegado".', notas=[FP_NOTE])

P('Chapa eléctrica con huella', CAT, 3, ['chapa con huella','chapa electrica huella','cerradura electrica con huella','control de acceso biometrico'],
  'El control de acceso de una oficina: una huella válida activa el relé y la chapa eléctrica abre la puerta.',
  [C('huella', 'Lector de huellas', t='D2', r='D3'), C('relay', 'Relé de la chapa', i='D7'), C('lock12', 'Chapa eléctrica 12 V'), C('supply12', 'Fuente 12 V'),
   C('led', 'Abierto', 'verde', a='D12'), C('buzzer', 'Pitido', p='D8')],
  FP_INC + FP_READ + '''const int RELE = 7, VERDE = 12, PITO = 8;

void setup() {
  Serial.begin(9600);
  finger.begin(57600);
  pinMode(RELE, OUTPUT); pinMode(VERDE, OUTPUT);
  digitalWrite(RELE, LOW);               // chapa cerrada
}

void loop() {
  int id = leerHuella();
  if (id > 0) {
    Serial.print("Acceso permitido a la huella #"); Serial.println(id);
    digitalWrite(VERDE, HIGH);
    tone(PITO, 1800, 120);
    digitalWrite(RELE, HIGH);            // la chapa recibe 12 V y abre
    delay(3000);
    digitalWrite(RELE, LOW);             // vuelve a cerrar
    digitalWrite(VERDE, LOW);
  } else if (id == 0) {
    Serial.println("Huella no autorizada");
    for (int i = 0; i < 3; i++) { tone(PITO, 300, 150); delay(250); }
  }
}
''', 'El Arduino no puede dar los 12 V que necesita la chapa: activa un relé, que es un interruptor eléctrico. Mientras el pin está en HIGH, el relé une la fuente de 12 V con la chapa y el pestillo se recoge.',
  'Registra en el monitor la hora de cada entrada con millis().', notas=[FP_NOTE, LOCK_NOTE],
  extra=['Diodo 1N4007 en paralelo con la chapa'])

P('Saludo personalizado con huella', CAT, 3, ['saludo con huella','nombres con huella','huella y lcd','bienvenida personal'],
  'La LCD saluda por su nombre a cada persona según su huella.',
  [C('huella', 'Lector de huellas', t='D2', r='D3'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Pitido', p='D8')],
  FP_INC + LCD_INC + FP_READ + '''String nombres[] = {"Desconocido", "Profe Jair", "Ana", "Luis"};   // huellas 1, 2 y 3

void setup() {
  finger.begin(57600);
  lcd.init(); lcd.backlight();
  lcd.print("Ponga su dedo");
}

void loop() {
  int id = leerHuella();
  if (id == -1) return;
  lcd.clear();
  if (id > 0 && id <= 3) {
    lcd.print("Hola,");
    lcd.setCursor(0, 1); lcd.print(nombres[id]);
    tone(8, 1500, 150);
  } else {
    lcd.print("No te conozco");
    tone(8, 300, 500);
  }
  delay(2500);
  lcd.clear(); lcd.print("Ponga su dedo");
}
''', 'El número de la huella sirve como posición en el arreglo nombres: la huella 1 muestra nombres[1]. La posición 0 queda para "desconocido".',
  'Cambia los nombres por los de tu grupo.', notas=[FP_NOTE])

P('Registro de asistencia con huella', CAT, 3, ['asistencia con huella','lista de asistencia','control de asistencia','llamar lista'],
  'Cada estudiante pone su huella al llegar y el monitor serie va armando la lista de asistencia.',
  [C('huella', 'Lector de huellas', t='D2', r='D3'), C('led', 'Registrado', 'verde', a='D12'), C('buzzer', 'Pitido', p='D8')],
  FP_INC + FP_READ + '''bool presente[] = {false, false, false, false};
String nombres[] = {"", "Ana", "Luis", "Sofia"};

void setup() {
  Serial.begin(9600);
  finger.begin(57600);
  pinMode(12, OUTPUT);
  Serial.println("Asistencia: pongan su dedo al llegar");
}

void loop() {
  int id = leerHuella();
  if (id > 0 && id <= 3) {
    if (!presente[id]) {
      presente[id] = true;
      Serial.print(nombres[id]); Serial.print(" llegó a los ");
      Serial.print(millis() / 1000); Serial.println(" segundos");
    } else {
      Serial.print(nombres[id]); Serial.println(" ya estaba registrado");
    }
    digitalWrite(12, HIGH); tone(8, 1500, 100); delay(1500); digitalWrite(12, LOW);
  }
}
''', 'El arreglo presente recuerda quién ya llegó, para no registrar a nadie dos veces. La hora de llegada se toma con millis().',
  'Agrega un botón que imprima la lista de los que faltan.', notas=[FP_NOTE])

P('Caja fuerte con huella y alarma', CAT, 3, ['caja fuerte huella','alcancia con huella','intentos fallidos','bloqueo'],
  'Una caja fuerte que abre con huella; si alguien falla tres veces seguidas, suena la alarma.',
  [C('huella', 'Lector de huellas', t='D2', r='D3'), C('servo', 'Pestillo', s='D9'), C('buzzer', 'Alarma', p='D8'), C('led', 'Bloqueada', 'rojo', a='D13')],
  FP_INC + SERVO_INC + 'Servo pestillo;\n' + FP_READ + '''int fallos = 0;

void setup() {
  Serial.begin(9600);
  finger.begin(57600);
  pestillo.attach(9); pestillo.write(0);
  pinMode(13, OUTPUT);
}

void loop() {
  int id = leerHuella();
  if (id > 0) {
    fallos = 0;
    Serial.println("Caja abierta");
    pestillo.write(90); delay(4000); pestillo.write(0);
  } else if (id == 0) {
    fallos++;
    Serial.print("Huella incorrecta. Intentos fallidos: "); Serial.println(fallos);
    tone(8, 300, 300);
    if (fallos >= 3) {
      Serial.println("¡ALARMA! Demasiados intentos");
      for (int i = 0; i < 20; i++) { digitalWrite(13, HIGH); tone(8, 2000, 100); delay(150); digitalWrite(13, LOW); delay(100); }
      fallos = 0;
    }
    delay(800);
  }
}
''', 'La variable fallos cuenta los intentos incorrectos seguidos y vuelve a 0 con una huella válida. Al llegar a 3, la alarma suena unos 5 segundos.',
  'Bloquea la caja durante 30 segundos después de la alarma.', notas=[FP_NOTE])

P('Cerradura con clave y teclado', CAT, 2, ['cerradura con teclado','clave con teclado','contrasena','codigo de acceso'],
  'Escribe la clave de 4 dígitos en el teclado y termina con #: si es correcta, la luz verde se enciende.',
  [C('keypad', 'Teclado', **KP_PINS), C('led', 'Correcta', 'verde', a='D12'), C('led', 'Incorrecta', 'rojo', a='D13')],
  KP_INC + '''const String CLAVE = "1234";
String escrito = "";

void setup() {
  Serial.begin(9600);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
  Serial.println("Escribe la clave y presiona #");
}

void loop() {
  char tecla = teclado.getKey();
  if (!tecla) return;
  if (tecla == '#') {
    if (escrito == CLAVE) { Serial.println("Clave correcta"); digitalWrite(12, HIGH); delay(2000); digitalWrite(12, LOW); }
    else { Serial.println("Clave incorrecta"); digitalWrite(13, HIGH); delay(2000); digitalWrite(13, LOW); }
    escrito = "";
  } else if (tecla == '*') {
    escrito = "";
    Serial.println("Borrado");
  } else {
    escrito += tecla;
    Serial.print("*");                 // no mostrar la clave
  }
}
''', 'Cada tecla se agrega al texto escrito. Al presionar # se compara con la clave guardada. En el monitor solo se muestran asteriscos para que nadie vea la clave.',
  'Cambia la clave y agrega un servo que abra la puerta.')

P('Chapa eléctrica con clave', CAT, 3, ['chapa con clave','chapa electrica teclado','puerta con clave','teclado y rele'],
  'La puerta de un laboratorio: con la clave correcta el relé abre la chapa eléctrica de 12 V.',
  [C('keypad', 'Teclado', **KP_PINS), C('relay', 'Relé de la chapa', i='D10'), C('lock12', 'Chapa eléctrica 12 V'), C('supply12', 'Fuente 12 V'), C('buzzer', 'Pitido', p='D11')],
  KP_INC + '''const String CLAVE = "2580";
const int RELE = 10, PITO = 11;
String escrito = "";

void setup() {
  Serial.begin(9600);
  pinMode(RELE, OUTPUT);
  digitalWrite(RELE, LOW);
}

void loop() {
  char tecla = teclado.getKey();
  if (!tecla) return;
  tone(PITO, 2000, 40);                  // clic de cada tecla
  if (tecla == '#') {
    if (escrito == CLAVE) {
      Serial.println("Puerta abierta");
      digitalWrite(RELE, HIGH); delay(3000); digitalWrite(RELE, LOW);
    } else {
      Serial.println("Clave incorrecta");
      tone(PITO, 300, 700);
    }
    escrito = "";
  } else {
    escrito += tecla;
  }
}
''', 'Es la cerradura con teclado, pero ahora el resultado mueve un relé. El relé conecta la fuente de 12 V a la chapa solo durante 3 segundos, suficientes para empujar la puerta.',
  'Muestra en una LCD los asteriscos de la clave mientras se escribe.', notas=[LOCK_NOTE],
  extra=['Diodo 1N4007 en paralelo con la chapa'])

P('Cerradura con clave, LCD y servo', CAT, 3, ['cerradura lcd','clave en pantalla','teclado lcd servo','puerta inteligente'],
  'Un sistema completo: la LCD pide la clave, muestra asteriscos y un servo abre la puerta si es correcta.',
  [C('keypad', 'Teclado', **KP_PINS), C('lcd', 'Pantalla LCD'), C('servo', 'Puerta', s='D10')],
  KP_INC + LCD_INC + SERVO_INC + '''Servo puerta;
const String CLAVE = "1379";
String escrito = "";

void pedir() {
  lcd.clear(); lcd.print("Ingrese la clave"); lcd.setCursor(0, 1);
}

void setup() {
  lcd.init(); lcd.backlight();
  puerta.attach(10); puerta.write(0);
  pedir();
}

void loop() {
  char tecla = teclado.getKey();
  if (!tecla) return;
  if (tecla == '#') {
    lcd.clear();
    if (escrito == CLAVE) {
      lcd.print("Bienvenido!"); puerta.write(90); delay(3000); puerta.write(0);
    } else {
      lcd.print("Clave incorrecta"); delay(2000);
    }
    escrito = ""; pedir();
  } else if (tecla == '*') {
    escrito = ""; pedir();
  } else if (escrito.length() < 8) {
    escrito += tecla;
    lcd.print("*");
  }
}
''', 'Mientras escribes, la LCD muestra un asterisco por cada tecla. La función pedir() deja la pantalla lista para un nuevo intento y se reutiliza en varios lugares del programa.',
  'Después de 3 errores, bloquea el teclado 30 segundos.')

P('Control de acceso con tarjeta RFID', CAT, 2, ['rfid basico','tarjeta rfid','acceso con tarjeta','carnet'],
  'Acerca una tarjeta al lector: la autorizada enciende la luz verde y las demás la roja.',
  [C('rfid', 'Lector RFID', s='D10', r='D9'), C('led', 'Autorizada', 'verde', a='D7'), C('led', 'Rechazada', 'rojo', a='D6')],
  RFID_INC + RFID_READ + '''
void setup() {
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();
  pinMode(7, OUTPUT); pinMode(6, OUTPUT);
  Serial.println("Acerque su tarjeta");
}

void loop() {
  int r = leerTarjeta();
  if (r == 1) { Serial.println("Acceso permitido"); digitalWrite(7, HIGH); delay(2000); digitalWrite(7, LOW); }
  if (r == 0) { Serial.println("Acceso denegado"); digitalWrite(6, HIGH); delay(2000); digitalWrite(6, LOW); }
}
''', 'Cada tarjeta RFID tiene un número único (UID) de 4 bytes. El programa lo lee, lo muestra en hexadecimal y lo compara con el de la tarjeta autorizada.',
  'Autoriza también el llavero azul (93 12 AB 07).', notas=[RFID_NOTE])

P('Puerta con tarjeta RFID y servo', CAT, 2, ['puerta rfid','rfid y servo','abrir con tarjeta','torniquete'],
  'Con la tarjeta autorizada, un servo abre la puerta 3 segundos.',
  [C('rfid', 'Lector RFID', s='D10', r='D9'), C('servo', 'Puerta', s='D6'), C('buzzer', 'Pitido', p='D8')],
  RFID_INC + SERVO_INC + 'Servo puerta;\n' + RFID_READ + '''
void setup() {
  Serial.begin(9600);
  SPI.begin(); rfid.PCD_Init();
  puerta.attach(6); puerta.write(0);
}

void loop() {
  int r = leerTarjeta();
  if (r == 1) {
    tone(8, 1600, 150);
    puerta.write(90); delay(3000); puerta.write(0);
  } else if (r == 0) {
    tone(8, 300, 500);
  }
}
''', 'Se reutiliza la función leerTarjeta(): devuelve 1, 0 o −1. Así el loop() solo decide qué hacer con la respuesta.',
  'Cuenta cuántas veces se abrió la puerta.', notas=[RFID_NOTE])

P('Chapa eléctrica con tarjeta RFID', CAT, 3, ['chapa rfid','chapa electrica tarjeta','cerradura con tarjeta','acceso de oficina'],
  'Como en las oficinas: la tarjeta autorizada activa el relé y la chapa eléctrica abre la puerta.',
  [C('rfid', 'Lector RFID', s='D10', r='D9'), C('relay', 'Relé de la chapa', i='D7'), C('lock12', 'Chapa eléctrica 12 V'), C('supply12', 'Fuente 12 V'), C('led', 'Abierta', 'verde', a='D6'), C('buzzer', 'Pitido', p='D8')],
  RFID_INC + RFID_READ + '''const int RELE = 7, VERDE = 6, PITO = 8;

void setup() {
  Serial.begin(9600);
  SPI.begin(); rfid.PCD_Init();
  pinMode(RELE, OUTPUT); pinMode(VERDE, OUTPUT);
}

void loop() {
  int r = leerTarjeta();
  if (r == 1) {
    digitalWrite(VERDE, HIGH); tone(PITO, 1800, 120);
    digitalWrite(RELE, HIGH);            // abre la chapa
    delay(3000);
    digitalWrite(RELE, LOW);
    digitalWrite(VERDE, LOW);
  } else if (r == 0) {
    for (int i = 0; i < 2; i++) { tone(PITO, 300, 200); delay(300); }
  }
}
''', 'La lógica es la misma de la puerta con servo, pero la salida va a un relé. El relé maneja los 12 V de la chapa, que el Arduino no puede dar.',
  'Usa el llavero azul como "llave maestra" que deja la puerta abierta hasta pasarlo de nuevo.', notas=[RFID_NOTE, LOCK_NOTE],
  extra=['Diodo 1N4007 en paralelo con la chapa'])

P('Bienvenida con tarjeta RFID y LCD', CAT, 3, ['rfid lcd','nombre con tarjeta','tarjeta y pantalla','recepcion con tarjeta'],
  'Cada tarjeta tiene un dueño: la LCD saluda por su nombre a quien la acerca.',
  [C('rfid', 'Lector RFID', s='D10', r='D9'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Pitido', p='D8')],
  RFID_INC + LCD_INC + '''
void setup() {
  SPI.begin(); rfid.PCD_Init();
  lcd.init(); lcd.backlight();
  lcd.print("Acerque tarjeta");
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;
  byte primero = rfid.uid.uidByte[0];
  lcd.clear();
  if (primero == 0x4A) { lcd.print("Hola, Ana!"); tone(8, 1500, 150); }
  else if (primero == 0x93) { lcd.print("Hola, Profe!"); tone(8, 1800, 150); }
  else { lcd.print("Tarjeta nueva"); tone(8, 400, 400); }
  lcd.setCursor(0, 1);
  lcd.print("UID: "); lcd.print(rfid.uid.uidByte[0], HEX); lcd.print(" "); lcd.print(rfid.uid.uidByte[1], HEX);
  rfid.PICC_HaltA();
  delay(2500);
  lcd.clear(); lcd.print("Acerque tarjeta");
}
''', 'Para simplificar, aquí se distingue cada tarjeta por su primer byte. En un sistema real se comparan los 4 bytes, como en la función leerTarjeta().',
  'Agrega una tercera persona con su propia tarjeta.', notas=[RFID_NOTE])

P('Registro de entradas con RFID', CAT, 2, ['registro rfid','bitacora','cuantas entradas','historial de acceso'],
  'Cuenta cuántas veces ha entrado cada tarjeta y lo muestra en el monitor serie.',
  [C('rfid', 'Lector RFID', s='D10', r='D9'), C('buzzer', 'Pitido', p='D8')],
  RFID_INC + '''int entradasBlanca = 0, entradasAzul = 0, otras = 0;

void setup() {
  Serial.begin(9600);
  SPI.begin(); rfid.PCD_Init();
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;
  if (rfid.uid.uidByte[0] == 0x4A) entradasBlanca++;
  else if (rfid.uid.uidByte[0] == 0x93) entradasAzul++;
  else otras++;
  tone(8, 1500, 80);
  Serial.print("Blanca: "); Serial.print(entradasBlanca);
  Serial.print("  Azul: "); Serial.print(entradasAzul);
  Serial.print("  Otras: "); Serial.println(otras);
  rfid.PICC_HaltA();
}
''', 'Cada tarjeta tiene su propio contador. Después de cada lectura se imprime el resumen completo, como una bitácora de la portería.',
  'Muestra la hora (en segundos) de la última entrada de cada tarjeta.', notas=[RFID_NOTE])

P('Alarma con PIR que se desactiva con clave', CAT, 3, ['alarma con clave','desactivar alarma','pir y teclado','alarma de casa con teclado'],
  'Si el PIR detecta a alguien, hay 10 segundos para escribir la clave; si no, suena la sirena.',
  [C('pir', 'Sensor PIR', o='D10'), C('keypad', 'Teclado', **KP_PINS), C('buzzer', 'Sirena', p='D11'), C('led', 'Armada', 'rojo', a='D12')],
  KP_INC + '''const String CLAVE = "0000";
String escrito = "";
bool armada = true;

void setup() {
  Serial.begin(9600);
  pinMode(10, INPUT); pinMode(12, OUTPUT);
}

void loop() {
  digitalWrite(12, armada);
  char tecla = teclado.getKey();
  if (tecla) {
    if (tecla == '#') { if (escrito == CLAVE) { armada = !armada; Serial.println(armada ? "Alarma armada" : "Alarma desarmada"); } escrito = ""; }
    else escrito += tecla;
  }
  if (armada && digitalRead(10) == HIGH) {
    Serial.println("¡Movimiento! Tienes 10 segundos para la clave");
    unsigned long inicio = millis();
    escrito = "";
    while (millis() - inicio < 10000 && armada) {
      tone(11, 2000, 30); delay(300);
      char t = teclado.getKey();
      if (t == '#') { if (escrito == CLAVE) armada = false; escrito = ""; }
      else if (t) escrito += t;
    }
    if (armada) {
      Serial.println("¡INTRUSO!");
      for (int i = 0; i < 30; i++) { tone(11, 1500); delay(150); tone(11, 900); delay(150); }
      noTone(11);
    } else Serial.println("Alarma desarmada a tiempo");
  }
}
''', 'Las alarmas de casa dan unos segundos para desarmarlas al entrar. Mientras corre ese tiempo, el programa sigue leyendo el teclado; si la clave llega a tiempo, la sirena no suena.',
  'Agrega una LCD que muestre la cuenta regresiva.')

P('Alarma de ventana con imán', CAT, 2, ['alarma de ventana','sensor magnetico','iman','sensor de apertura'],
  'Un imán en la ventana y un sensor Hall en el marco: si la ventana se abre, el imán se aleja y suena la alarma.',
  [C('hall', 'Sensor Hall', o='D2'), C('buzzer', 'Alarma', p='D8'), C('led', 'Ventana abierta', 'rojo', a='D13')],
  '''
// Alarma de ventana con sensor Hall
const int HALL = 2;          // LOW cuando el imán está cerca (ventana cerrada)

void setup() {
  Serial.begin(9600);
  pinMode(HALL, INPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(HALL) == HIGH) {          // el imán se alejó
    Serial.println("¡Ventana abierta!");
    digitalWrite(13, HIGH);
    tone(8, 2200, 200);
    delay(400);
  } else {
    digitalWrite(13, LOW);
  }
}
''', 'El sensor Hall detecta campos magnéticos. Con la ventana cerrada el imán está pegado al sensor (LOW); al abrirla, el imán se aleja y la salida pasa a HIGH.',
  'Agrega un segundo sensor para la puerta.', notas=['En el simulador, marca «Hay un imán cerca» para simular la ventana cerrada.'])

P('Timbre que solo suena con tarjeta', CAT, 2, ['timbre con tarjeta','timbre rfid','timbre inteligente','solo familia'],
  'Un timbre inteligente: si la tarjeta es de la familia toca una melodía alegre; si no, un timbre normal.',
  [C('rfid', 'Lector RFID', s='D10', r='D9'), C('buzzer', 'Timbre', p='D8')],
  RFID_INC + RFID_READ + '''
void melodiaFamilia() {
  int notas[] = {523, 659, 784, 1047};
  for (int i = 0; i < 4; i++) { tone(8, notas[i], 150); delay(180); }
}

void setup() {
  Serial.begin(9600);
  SPI.begin(); rfid.PCD_Init();
}

void loop() {
  int r = leerTarjeta();
  if (r == 1) { Serial.println("Llegó alguien de la familia"); melodiaFamilia(); }
  if (r == 0) { Serial.println("Visitante"); tone(8, 880, 300); delay(350); tone(8, 660, 500); }
}
''', 'El mismo lector sirve para distinguir quién llega. La función melodiaFamilia() guarda las notas en un arreglo local, que solo existe dentro de ella.',
  'Agrega un LED que se encienda cuando llega un visitante.', notas=[RFID_NOTE])

P('Doble seguridad: huella y botón de salida', CAT, 3, ['boton de salida','salida libre','huella entrada boton salida','puerta de oficina'],
  'Para entrar se necesita la huella; para salir basta con presionar el botón de salida, como en las oficinas.',
  [C('huella', 'Lector de huellas', t='D2', r='D3'), C('button', 'Botón de salida', x='D4'), C('servo', 'Pestillo', s='D9'), C('led', 'Abierta', 'verde', a='D13')],
  FP_INC + SERVO_INC + 'Servo pestillo;\n' + FP_READ + '''
void abrir(String motivo) {
  Serial.println(motivo);
  digitalWrite(13, HIGH); pestillo.write(90);
  delay(3000);
  pestillo.write(0); digitalWrite(13, LOW);
}

void setup() {
  Serial.begin(9600);
  finger.begin(57600);
  pestillo.attach(9); pestillo.write(0);
  pinMode(4, INPUT_PULLUP); pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(4) == LOW) abrir("Salida con botón");
  int id = leerHuella();
  if (id > 0) abrir("Entrada con huella");
}
''', 'La función abrir() recibe un texto que explica por qué se abrió y hace todo el movimiento. Así no se repite el mismo código para la huella y para el botón.',
  'Registra en el monitor cuántas entradas y cuántas salidas hubo.', notas=[FP_NOTE])

P('Alarma de vibración para caja fuerte', CAT, 2, ['caja fuerte vibracion','alarma antirrobo vibracion','proteger caja'],
  'Si alguien golpea o intenta mover la caja fuerte, se enciende la sirena y no se apaga hasta poner la huella.',
  [C('vibracion', 'Sensor de vibración', o='D4'), C('huella', 'Lector de huellas', t='D2', r='D3'), C('buzzer', 'Sirena', p='D8'), C('led', 'Alarma', 'rojo', a='D13')],
  FP_INC + FP_READ + '''bool alarma = false;

void setup() {
  Serial.begin(9600);
  finger.begin(57600);
  pinMode(4, INPUT); pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(4) == HIGH && !alarma) { alarma = true; Serial.println("¡Golpe detectado!"); }
  if (alarma) {
    digitalWrite(13, HIGH); tone(8, 1700); delay(150);
    digitalWrite(13, LOW); tone(8, 1100); delay(150);
    if (leerHuella() > 0) { alarma = false; noTone(8); Serial.println("Alarma apagada por el dueño"); }
  }
}
''', 'Mientras la alarma está activa, en cada vuelta se intenta leer una huella. Solo una huella registrada la apaga; desconectar el sensor no sirve.',
  'Haz que la alarma también envíe un mensaje por el monitor cada 5 segundos.', notas=[FP_NOTE])

P('Botón de emergencia con sirena y luces', CAT, 2, ['emergencia en el colegio','evacuacion','alarma de evacuacion','simulacro'],
  'Un botón grande activa la alarma de evacuación con luces y sirena; un interruptor la apaga.',
  [C('button', 'Emergencia', x='D2'), C('switch', 'Restablecer', x='D3'), C('buzzer', 'Sirena', p='D8'), C('led', 'Luz roja', 'rojo', a='D12'), C('led', 'Luz blanca', 'blanco', a='D13')],
  '''
// Alarma de evacuación
bool emergencia = false;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP); pinMode(3, INPUT_PULLUP);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  if (digitalRead(2) == LOW && !emergencia) { emergencia = true; Serial.println("¡EVACUACIÓN!"); }
  if (digitalRead(3) == LOW) emergencia = false;
  if (emergencia) {
    for (int f = 700; f < 1600; f += 50) { tone(8, f); delay(10); }
    digitalWrite(12, HIGH); digitalWrite(13, LOW); delay(150);
    digitalWrite(12, LOW); digitalWrite(13, HIGH); delay(150);
  } else {
    noTone(8); digitalWrite(12, LOW); digitalWrite(13, LOW);
  }
}
''', 'La sirena sube de tono en cada ciclo y las dos luces se alternan. El interruptor de restablecer está pensado para que solo el encargado pueda apagar la alarma.',
  'Agrega un sensor de llama que active la misma alarma.')

P('Contador de intentos de acceso en LCD', CAT, 3, ['intentos de acceso','estadisticas de acceso','permitidos y denegados'],
  'La LCD lleva la cuenta de accesos permitidos y denegados con tarjeta RFID.',
  [C('rfid', 'Lector RFID', s='D10', r='D9'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Pitido', p='D8')],
  RFID_INC + LCD_INC + RFID_READ + '''int permitidos = 0, denegados = 0;

void mostrar() {
  lcd.clear();
  lcd.print("Permitidos: "); lcd.print(permitidos);
  lcd.setCursor(0, 1);
  lcd.print("Denegados:  "); lcd.print(denegados);
}

void setup() {
  Serial.begin(9600);
  SPI.begin(); rfid.PCD_Init();
  lcd.init(); lcd.backlight();
  mostrar();
}

void loop() {
  int r = leerTarjeta();
  if (r == 1) { permitidos++; tone(8, 1600, 120); mostrar(); }
  if (r == 0) { denegados++; tone(8, 300, 400); mostrar(); }
}
''', 'Las dos variables cuentan los resultados de leerTarjeta(). La pantalla solo se actualiza cuando cambia algún número.',
  'Muestra el porcentaje de accesos denegados.', notas=[RFID_NOTE])

P('Cofre del tesoro con clave', CAT, 2, ['cofre','tesoro','juego de escape','escape room'],
  'Para un juego de escape: el cofre (servo) solo se abre con la clave 7 3 9 y tocando una melodía de victoria.',
  [C('keypad', 'Teclado', **KP_PINS), C('servo', 'Tapa del cofre', s='D10'), C('buzzer', 'Música', p='D11')],
  KP_INC + SERVO_INC + '''Servo tapa;
String escrito = "";

void victoria() {
  int notas[] = {523, 659, 784, 659, 784, 1047};
  for (int i = 0; i < 6; i++) { tone(11, notas[i], 150); delay(170); }
}

void setup() {
  tapa.attach(10); tapa.write(0);
}

void loop() {
  char tecla = teclado.getKey();
  if (!tecla) return;
  tone(11, 1800, 30);
  escrito += tecla;
  if (escrito.length() == 3) {
    if (escrito == "739") { victoria(); tapa.write(100); delay(5000); tapa.write(0); }
    else tone(11, 250, 600);
    escrito = "";
  }
}
''', 'Aquí no hace falta la tecla #: al completar 3 dígitos se revisa la clave automáticamente. Los juegos de escape usan cofres así con pistas escondidas en el salón.',
  'Esconde la clave en un acertijo para tus compañeros.')

P('Lector de huellas con contador de usos', CAT, 2, ['usos por huella','estadisticas huella','quien entra mas'],
  'Lleva la cuenta de cuántas veces ha usado el lector cada huella registrada.',
  [C('huella', 'Lector de huellas', t='D2', r='D3'), C('buzzer', 'Pitido', p='D8')],
  FP_INC + FP_READ + '''int usos[] = {0, 0, 0, 0};

void setup() {
  Serial.begin(9600);
  finger.begin(57600);
}

void loop() {
  int id = leerHuella();
  if (id > 0 && id <= 3) {
    usos[id]++;
    tone(8, 1500, 100);
    Serial.print("Huella #"); Serial.print(id);
    Serial.print(" lleva "); Serial.print(usos[id]); Serial.println(" usos");
    delay(1500);
  } else if (id == 0) {
    Serial.println("Huella no registrada");
    delay(1500);
  }
}
''', 'El arreglo usos tiene una casilla por huella. El número de la huella sirve para saber qué casilla aumentar.',
  'Muestra al final del día quién usó más el lector.', notas=[FP_NOTE])
