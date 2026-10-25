from p_base import *
CAT = 'Temperatura y clima'

P('Termómetro en el monitor serie', CAT, 1, ['termometro serial','medir temperatura','lm35 basico','grados centigrados'],
  'El sensor LM35 mide la temperatura y el Arduino la muestra en grados Celsius.',
  [C('lm35', 'Sensor LM35', o='A0')],
  '''
// Termómetro con LM35
const int SENSOR = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(SENSOR);
  float temperatura = lectura * 500.0 / 1023.0;   // 10 mV por cada grado
  Serial.print("Temperatura: ");
  Serial.print(temperatura, 1);
  Serial.println(" °C");
  delay(1000);
}
''', 'El LM35 entrega 10 milivoltios por cada grado. Como 5 V corresponden a 1023 en la lectura, multiplicar por 500 y dividir por 1023 da los grados directamente.',
  'Muestra también la temperatura en grados Fahrenheit (F = C × 1,8 + 32).')

P('Termómetro con pantalla LCD', CAT, 2, ['termometro lcd','temperatura en pantalla','termometro digital'],
  'Un termómetro digital que muestra la temperatura en una pantalla LCD.',
  [C('lm35', 'Sensor LM35', o='A0'), C('lcd', 'Pantalla LCD')],
  LCD_INC + '''
void setup() {
  lcd.init();
  lcd.backlight();
  lcd.print("Termometro");
}

void loop() {
  float t = analogRead(A0) * 500.0 / 1023.0;
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(t, 1);
  lcd.print(" C   ");          // espacios para borrar números viejos
  delay(1000);
}
''', 'La primera línea de la pantalla se escribe una sola vez en setup(). En loop() solo se actualiza la segunda línea; los espacios al final borran los dígitos que sobran.',
  'Agrega la temperatura máxima registrada en la primera línea.')

P('Alarma de calor', CAT, 1, ['alarma de calor','temperatura alta','sobrecalentamiento','alerta de temperatura'],
  'Si la temperatura pasa de 35 °C suena una alarma y se enciende un LED rojo.',
  [C('lm35', 'Sensor LM35', o='A0'), C('buzzer', 'Alarma', p='D8'), C('led', 'Peligro', 'rojo', a='D13')],
  '''
// Alarma de calor
const float LIMITE = 35.0;
const int ALARMA = 8, LUZ = 13;

void setup() {
  Serial.begin(9600);
  pinMode(LUZ, OUTPUT);
}

void loop() {
  float t = analogRead(A0) * 500.0 / 1023.0;
  Serial.println(t, 1);
  if (t > LIMITE) {
    digitalWrite(LUZ, HIGH);
    tone(ALARMA, 2500, 300);
  } else {
    digitalWrite(LUZ, LOW);
  }
  delay(500);
}
''', 'El valor límite está guardado en una constante al comienzo del programa, para que sea fácil cambiarlo sin buscarlo por todo el código.',
  'Agrega un segundo nivel de alerta (LED amarillo) a partir de 30 °C.')

P('Estación del clima con DHT11', CAT, 2, ['estacion del clima','estacion meteorologica','dht11 lcd','temperatura y humedad'],
  'Muestra en la LCD la temperatura y la humedad del aire medidas por el DHT11.',
  [C('dht11', 'Sensor DHT11', d='D2'), C('lcd', 'Pantalla LCD')],
  DHT_INC + LCD_INC + '''
void setup() {
  dht.begin();
  lcd.init();
  lcd.backlight();
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  lcd.clear();
  if (isnan(t) || isnan(h)) {          // el sensor no respondió
    lcd.print("Error del sensor");
  } else {
    lcd.print("Temp: "); lcd.print(t, 0); lcd.print(" C");
    lcd.setCursor(0, 1);
    lcd.print("Humedad: "); lcd.print(h, 0); lcd.print(" %");
  }
  delay(2000);                          // el DHT11 mide cada 2 segundos
}
''', 'El DHT11 mide temperatura y humedad y las envía por un solo cable con un código especial; la librería DHT lo traduce. isnan() detecta si la lectura falló.',
  'Agrega un LED que avise cuando la humedad pase del 80 %.')

P('Alerta de humedad alta', CAT, 2, ['humedad alta','moho','humedad del cuarto','deshumidificador'],
  'Avisa con un LED y un pitido cuando el aire está demasiado húmedo, para evitar el moho.',
  [C('dht11', 'Sensor DHT11', d='D2'), C('led', 'Humedad alta', 'azul', a='D13'), C('buzzer', 'Aviso', p='D8')],
  DHT_INC + '''const int LUZ = 13, AVISO = 8;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(LUZ, OUTPUT);
}

void loop() {
  float h = dht.readHumidity();
  Serial.print("Humedad: "); Serial.print(h, 0); Serial.println(" %");
  if (h > 75) {
    digitalWrite(LUZ, HIGH);
    tone(AVISO, 900, 150);
  } else {
    digitalWrite(LUZ, LOW);
  }
  delay(2000);
}
''', 'La humedad relativa dice cuánta agua hay en el aire, en porcentaje. Por encima del 75 % durante mucho tiempo aparecen hongos en paredes y ropa.',
  'Muestra en el monitor si el ambiente está seco, agradable o húmedo.')

P('Semáforo de confort', CAT, 2, ['confort','comodidad termica','semaforo del clima','ambiente agradable'],
  'Un LED RGB se pone verde si el salón está cómodo, azul si hace frío y rojo si hace calor.',
  [C('dht11', 'Sensor DHT11', d='D2'), C('rgb', 'Indicador', r='D9', g='D10', b='D11')],
  DHT_INC + '''const int R = 9, G = 10, B = 11;

void color(int r, int g, int b) { analogWrite(R, r); analogWrite(G, g); analogWrite(B, b); }

void setup() {
  dht.begin();
  pinMode(R, OUTPUT); pinMode(G, OUTPUT); pinMode(B, OUTPUT);
}

void loop() {
  float t = dht.readTemperature();
  if (t < 18) color(0, 0, 255);          // frío
  else if (t > 27) color(255, 0, 0);     // calor
  else color(0, 255, 0);                 // cómodo
  delay(2000);
}
''', 'Se usa una cadena if / else if / else para escoger un solo color. La función color() hace el código más corto y fácil de leer.',
  'Usa también la humedad: si pasa de 70 %, que el color sea morado.')

P('Termostato con perilla', CAT, 3, ['termostato','temperatura deseada','calefaccion','control de temperatura'],
  'Eliges la temperatura deseada con la perilla; si hace más frío, se enciende la calefacción (LED rojo).',
  [C('lm35', 'Sensor LM35', o='A0'), C('pot', 'Temperatura deseada', w='A1'), C('led', 'Calefacción', 'rojo', a='D13'), C('lcd', 'Pantalla LCD')],
  LCD_INC + '''const int CALEFACCION = 13;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(CALEFACCION, OUTPUT);
}

void loop() {
  float actual = analogRead(A0) * 500.0 / 1023.0;
  int deseada = map(analogRead(A1), 0, 1023, 15, 30);
  bool encender = actual < deseada - 0.5;       // margen de medio grado
  digitalWrite(CALEFACCION, encender);
  lcd.setCursor(0, 0);
  lcd.print("Actual: "); lcd.print(actual, 1); lcd.print(" C  ");
  lcd.setCursor(0, 1);
  lcd.print("Quiero: "); lcd.print(deseada); lcd.print(" C  ");
  delay(500);
}
''', 'Un termostato compara la temperatura medida con la deseada. El margen de medio grado evita que la calefacción se prenda y apague sin parar cuando están muy cerca.',
  'Agrega un ventilador que se encienda si hace 2 grados más de lo deseado.')

P('Registro de temperatura máxima y mínima', CAT, 2, ['maxima y minima','record de temperatura','registro','estadisticas'],
  'Guarda la temperatura más alta y la más baja medidas y las muestra en el monitor.',
  [C('lm35', 'Sensor LM35', o='A0'), C('button', 'Borrar registro', x='D2')],
  '''
// Temperatura máxima y mínima
float maxima = -100, minima = 200;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  float t = analogRead(A0) * 500.0 / 1023.0;
  if (t > maxima) maxima = t;
  if (t < minima) minima = t;
  if (digitalRead(2) == LOW) { maxima = t; minima = t; Serial.println("Registro borrado"); }
  Serial.print("Ahora: "); Serial.print(t, 1);
  Serial.print("  Máx: "); Serial.print(maxima, 1);
  Serial.print("  Mín: "); Serial.println(minima, 1);
  delay(1000);
}
''', 'La máxima empieza en un valor muy bajo y la mínima en uno muy alto, para que la primera medición reemplace a las dos. Después solo cambian si aparece un récord.',
  'Calcula también el promedio de todas las mediciones.')

P('Alarma de nevera abierta', CAT, 2, ['nevera','refrigerador','cadena de frio','vacunas'],
  'Vigila la temperatura de una nevera: si pasa de 8 °C por mucho tiempo, avisa con sonido.',
  [C('lm35', 'Sensor en la nevera', o='A0'), C('buzzer', 'Alarma', p='D8'), C('led', 'Todo bien', 'verde', a='D12'), C('led', 'Muy caliente', 'rojo', a='D13')],
  '''
// Alarma de nevera
const float LIMITE = 8.0;
int minutosCaliente = 0;

void setup() {
  Serial.begin(9600);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  float t = analogRead(A0) * 500.0 / 1023.0;
  if (t > LIMITE) minutosCaliente++;
  else minutosCaliente = 0;
  digitalWrite(12, minutosCaliente == 0);
  digitalWrite(13, minutosCaliente > 0);
  if (minutosCaliente >= 3) tone(8, 2000, 400);   // 3 lecturas seguidas
  Serial.print(t, 1); Serial.print(" °C  lecturas calientes: "); Serial.println(minutosCaliente);
  delay(1000);    // en una nevera real se mediría cada minuto
}
''', 'No basta una lectura caliente (puede ser que abrieron la puerta un momento): la alarma suena solo si se repite varias veces seguidas. Así funcionan las neveras de vacunas.',
  'Cambia el tiempo entre lecturas a 60 segundos para usarlo de verdad.')

P('Indicador de sensación de bochorno', CAT, 2, ['bochorno','calor humedo','indice de calor','sensacion termica'],
  'Combina temperatura y humedad para saber si el ambiente se siente sofocante.',
  [C('dht11', 'Sensor DHT11', d='D2'), C('led', 'Agradable', 'verde', a='D11'), C('led', 'Pesado', 'amarillo', a='D12'), C('led', 'Sofocante', 'rojo', a='D13')],
  DHT_INC + '''
void setup() {
  Serial.begin(9600);
  dht.begin();
  for (int p = 11; p <= 13; p++) pinMode(p, OUTPUT);
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  float sensacion = t + (h - 40) * 0.1;      // fórmula sencilla para practicar
  Serial.print("Se siente como "); Serial.print(sensacion, 1); Serial.println(" °C");
  digitalWrite(11, sensacion < 27);
  digitalWrite(12, sensacion >= 27 && sensacion < 32);
  digitalWrite(13, sensacion >= 32);
  delay(2000);
}
''', 'Con mucha humedad el sudor se evapora menos y sentimos más calor. La fórmula suma un poco a la temperatura según cuánto pase la humedad del 40 %.',
  'Investiga la fórmula oficial del índice de calor y compárala.')

P('Ventilador por temperatura con DHT11', CAT, 2, ['ventilador dht','ventilador automatico','enfriar cuarto','clima automatico'],
  'El ventilador gira más rápido cuanto más calor haga, según el DHT11.',
  [C('dht11', 'Sensor DHT11', d='D2'), C('motor', 'Ventilador', p='D6')],
  DHT_INC + '''const int VENTILADOR = 6;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(VENTILADOR, OUTPUT);
}

void loop() {
  float t = dht.readTemperature();
  int velocidad = 0;
  if (t > 24) velocidad = map(t, 24, 34, 100, 255);
  velocidad = constrain(velocidad, 0, 255);
  analogWrite(VENTILADOR, velocidad);
  Serial.print(t, 0); Serial.print(" °C -> velocidad "); Serial.println(velocidad);
  delay(2000);
}
''', 'Por debajo de 24 °C el ventilador está apagado. Por encima, map() reparte la velocidad entre 100 y 255 según qué tan caliente esté.',
  'Agrega una pantalla LCD que muestre la temperatura y la velocidad.',
  notas=['En la vida real usa un transistor o un relé para el motor del ventilador.'])

P('Termómetro de barra con LED', CAT, 1, ['termometro de leds','barra de temperatura','columna de mercurio'],
  'Cinco LED suben como la columna de un termómetro de mercurio.',
  [C('lm35', 'Sensor LM35', o='A0'), C('led', '20 °C', 'azul', a='D9'), C('led', '24 °C', 'verde', a='D10'), C('led', '28 °C', 'amarillo', a='D11'),
   C('led', '32 °C', 'rojo', a='D12'), C('led', '36 °C', 'rojo', a='D13')],
  '''
// Termómetro de barra
int barra[] = {9, 10, 11, 12, 13};

void setup() {
  for (int i = 0; i < 5; i++) pinMode(barra[i], OUTPUT);
}

void loop() {
  float t = analogRead(A0) * 500.0 / 1023.0;
  for (int i = 0; i < 5; i++) {
    float marca = 20 + i * 4;          // 20, 24, 28, 32 y 36 grados
    digitalWrite(barra[i], t >= marca);
  }
  delay(500);
}
''', 'Cada LED tiene una marca de temperatura. Si la temperatura medida alcanza la marca, el LED se enciende; así la barra crece con el calor.',
  'Cambia las marcas para medir la temperatura del cuerpo (35 a 39 °C).')

P('Incubadora de huevos sencilla', CAT, 3, ['incubadora','huevos','pollitos','temperatura constante'],
  'Mantiene la temperatura cerca de 37,5 °C encendiendo un bombillo con un relé.',
  [C('lm35', 'Sensor LM35', o='A0'), C('relay', 'Relé del bombillo', i='D7'), C('led', 'Calentando', 'rojo', a='D13'), C('lcd', 'Pantalla LCD')],
  LCD_INC + '''const int RELE = 7, LUZ = 13;
const float META = 37.5;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(RELE, OUTPUT); pinMode(LUZ, OUTPUT);
}

void loop() {
  float t = analogRead(A0) * 500.0 / 1023.0;
  bool calentar = t < META - 0.3;
  if (t > META + 0.3) calentar = false;
  digitalWrite(RELE, calentar);
  digitalWrite(LUZ, calentar);
  lcd.setCursor(0, 0); lcd.print("Temp: "); lcd.print(t, 1); lcd.print(" C  ");
  lcd.setCursor(0, 1);
  if (calentar) lcd.print("Calentando...  ");
  else lcd.print("Temperatura OK ");
  delay(1000);
}
''', 'El relé es un interruptor que el Arduino activa con un pin. Así una salida de 5 V puede encender un bombillo de 110 V sin que el Arduino toque esa corriente.',
  'Agrega un zumbador que avise si la temperatura pasa de 39 °C.',
  notas=['El bombillo de 110 V solo lo conecta un adulto, con el relé bien aislado y en una caja cerrada.'],
  extra=['Bombillo incandescente de 40 W con su roseta', 'Caja de icopor'])

P('Detector de fiebre para practicar', CAT, 2, ['fiebre','temperatura corporal','salud','termometro medico'],
  'Simula un termómetro médico: indica si la temperatura del cuerpo es normal o hay fiebre.',
  [C('lm35', 'Sensor LM35', o='A0'), C('led', 'Normal', 'verde', a='D12'), C('led', 'Fiebre', 'rojo', a='D13'), C('buzzer', 'Aviso', p='D8')],
  '''
// Detector de fiebre (para practicar)
void setup() {
  Serial.begin(9600);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
}

void loop() {
  float t = analogRead(A0) * 500.0 / 1023.0;
  Serial.print(t, 1); Serial.print(" °C: ");
  if (t >= 37.8) {
    Serial.println("fiebre");
    digitalWrite(13, HIGH); digitalWrite(12, LOW);
    tone(8, 1500, 100);
  } else {
    Serial.println("normal");
    digitalWrite(12, HIGH); digitalWrite(13, LOW);
  }
  delay(1000);
}
''', 'La temperatura normal del cuerpo está alrededor de 36,5 °C; desde 37,8 °C se considera fiebre. El programa toma esa decisión y avisa con luz y sonido.',
  'Toma tres medidas y usa el promedio antes de decidir.',
  notas=['Es un proyecto para aprender: no reemplaza un termómetro médico.'])

CAT = 'Distancia y movimiento'

P('Medidor de distancia en el monitor', CAT, 1, ['medir distancia','ultrasonico basico','hc-sr04','regla electronica'],
  'El sensor ultrasónico mide a qué distancia está un objeto y la muestra en centímetros.',
  [C('sonar', 'Sensor ultrasónico', t='D7', e='D6')],
  '''
// Medidor de distancia con HC-SR04
const int TRIG = 7, ECHO = 6;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
}

void loop() {
  digitalWrite(TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);   // pulso de 10 microsegundos
  digitalWrite(TRIG, LOW);
  long tiempo = pulseIn(ECHO, HIGH);     // cuánto tardó el eco
  long cm = tiempo / 58;                 // convertir a centímetros
  Serial.print("Distancia: ");
  Serial.print(cm);
  Serial.println(" cm");
  delay(300);
}
''', 'El sensor lanza un sonido que no podemos oír y espera su eco, como un murciélago. pulseIn() mide el tiempo del eco y dividirlo entre 58 da la distancia en centímetros.',
  'Muestra la distancia también en metros.')

P('Medidor de distancia con pantalla', CAT, 2, ['distancia en lcd','cinta metrica digital','metro electronico'],
  'Una cinta métrica digital: la LCD muestra la distancia al objeto.',
  [C('sonar', 'Sensor ultrasónico', t='D7', e='D6'), C('lcd', 'Pantalla LCD')],
  LCD_INC + '''const int TRIG = 7, ECHO = 6;

long medir() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long cm = pulseIn(ECHO, HIGH) / 58;   // en Arduino la división entera no deja decimales
  return cm;
}

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
  lcd.print("Cinta metrica");
}

void loop() {
  long cm = medir();
  lcd.setCursor(0, 1);
  lcd.print(cm); lcd.print(" cm          ");
  delay(300);
}
''', 'La función medir() encierra los pasos del sensor y devuelve los centímetros. Así el loop() queda corto y claro.',
  'Agrega un botón que congele la medida en la pantalla.')

P('Alarma de proximidad', CAT, 1, ['alarma de proximidad','alguien se acerca','distancia minima','zona prohibida'],
  'Si alguien se acerca a menos de 30 cm suena una alarma.',
  [C('sonar', 'Sensor ultrasónico', t='D7', e='D6'), C('buzzer', 'Alarma', p='D8'), C('led', 'Alerta', 'rojo', a='D13')],
  '''
// Alarma de proximidad
const int TRIG = 7, ECHO = 6, ALARMA = 8, LUZ = 13;

void setup() {
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT); pinMode(LUZ, OUTPUT);
}

void loop() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10); digitalWrite(TRIG, LOW);
  long cm = pulseIn(ECHO, HIGH) / 58;
  if (cm > 0 && cm < 30) {
    digitalWrite(LUZ, HIGH);
    tone(ALARMA, 1800, 150);
  } else {
    digitalWrite(LUZ, LOW);
  }
  delay(200);
}
''', 'Se comprueba que la distancia sea mayor que 0 porque el sensor devuelve 0 cuando no recibe eco. Si está entre 1 y 29 cm, se activa la alarma.',
  'Haz que la alarma suene más rápido cuanto más cerca esté la persona.')

P('Sensor de distancia con semáforo', CAT, 2, ['semaforo de distancia','distancia segura','garaje','estacionar'],
  'Tres LED indican la distancia: verde lejos, amarillo cuidado y rojo ¡pare!',
  [C('sonar', 'Sensor ultrasónico', t='D7', e='D6'), C('led', 'Lejos', 'verde', a='D11'), C('led', 'Cuidado', 'amarillo', a='D12'), C('led', 'Pare', 'rojo', a='D13')],
  '''
// Semáforo de distancia para estacionar
const int TRIG = 7, ECHO = 6;

void setup() {
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
  for (int p = 11; p <= 13; p++) pinMode(p, OUTPUT);
}

void loop() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10); digitalWrite(TRIG, LOW);
  long cm = pulseIn(ECHO, HIGH) / 58;
  digitalWrite(11, cm >= 60);
  digitalWrite(12, cm >= 25 && cm < 60);
  digitalWrite(13, cm < 25);
  delay(150);
}
''', 'Cada LED se enciende solo en su rango de distancia. Los garajes de los centros comerciales usan sistemas parecidos para ayudar a estacionar.',
  'Haz que el rojo parpadee cuando el carro esté a menos de 10 cm.')

P('Theremin ultrasónico', CAT, 2, ['theremin ultrasonico','musica con la mano','instrumento de distancia'],
  'Mueve la mano sobre el sensor: cuanto más cerca, más aguda la nota.',
  [C('sonar', 'Sensor ultrasónico', t='D7', e='D6'), C('buzzer', 'Parlante', p='D8')],
  '''
// Theremin ultrasónico
const int TRIG = 7, ECHO = 6, PARLANTE = 8;

void setup() {
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
}

void loop() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10); digitalWrite(TRIG, LOW);
  long cm = pulseIn(ECHO, HIGH) / 58;
  if (cm > 3 && cm < 50) tone(PARLANTE, map(cm, 3, 50, 1500, 200));
  else noTone(PARLANTE);
  delay(40);
}
''', 'map() convierte la distancia (de 3 a 50 cm) en una frecuencia (de 1500 a 200 Hz). Fuera de ese rango el instrumento queda en silencio.',
  'Haz que solo suenen notas de la escala musical.')

P('Contador de visitantes con ultrasonido', CAT, 2, ['contador de visitantes','cuantas personas entran','entrada de la tienda'],
  'Cuenta cuántas personas pasan frente al sensor de la puerta y lo muestra en la LCD.',
  [C('sonar', 'Sensor de la puerta', t='D7', e='D6'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Bip', p='D8')],
  LCD_INC + '''const int TRIG = 7, ECHO = 6;
int visitantes = 0;
bool alguien = false;

long medir() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10); digitalWrite(TRIG, LOW);
  long cm = pulseIn(ECHO, HIGH) / 58;   // en Arduino la división entera no deja decimales
  return cm;
}

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
  lcd.print("Visitantes: 0");
}

void loop() {
  long cm = medir();
  if (!alguien && cm < 60) {        // llegó una persona
    alguien = true;
    visitantes++;
    tone(8, 1200, 80);
    lcd.setCursor(12, 0); lcd.print(visitantes);
  }
  if (alguien && cm > 80) alguien = false;   // la persona ya pasó
  delay(100);
}
''', 'La variable alguien recuerda que hay una persona frente al sensor, para no contarla muchas veces mientras pasa. Solo cuando se aleja se puede contar a la siguiente.',
  'Agrega un botón para reiniciar la cuenta al empezar el día.')

P('Detector de intrusos con PIR', CAT, 1, ['detector de intrusos','pir basico','movimiento','vigilancia'],
  'Un sensor PIR detecta el movimiento de una persona y enciende una luz roja.',
  [C('pir', 'Sensor PIR', o='D2'), C('led', 'Intruso', 'rojo', a='D13')],
  '''
// Detector de intrusos con PIR
const int PIR = 2, LUZ = 13;

void setup() {
  Serial.begin(9600);
  pinMode(PIR, INPUT);
  pinMode(LUZ, OUTPUT);
}

void loop() {
  if (digitalRead(PIR) == HIGH) {
    digitalWrite(LUZ, HIGH);
    Serial.println("¡Movimiento detectado!");
    delay(1000);
  } else {
    digitalWrite(LUZ, LOW);
  }
}
''', 'El PIR detecta los cambios de calor que produce el cuerpo de una persona al moverse. Cuando eso pasa, su salida se pone en HIGH durante unos segundos.',
  'Cuenta cuántas veces se detectó movimiento.')

P('Luz automática de pasillo', CAT, 1, ['luz de pasillo','luz con movimiento','ahorro de energia','luz automatica pir'],
  'La luz del pasillo se enciende al detectar movimiento y se apaga 15 segundos después de la última persona.',
  [C('pir', 'Sensor PIR', o='D2'), C('led', 'Luz del pasillo', 'blanco', a='D13')],
  '''
// Luz de pasillo con PIR
const int PIR = 2, LUZ = 13;
const unsigned long TIEMPO = 15000;
unsigned long ultimoMovimiento = 0;

void setup() {
  pinMode(PIR, INPUT);
  pinMode(LUZ, OUTPUT);
}

void loop() {
  if (digitalRead(PIR) == HIGH) ultimoMovimiento = millis();
  if (millis() - ultimoMovimiento < TIEMPO && ultimoMovimiento > 0) digitalWrite(LUZ, HIGH);
  else digitalWrite(LUZ, LOW);
}
''', 'Cada movimiento actualiza la hora del último movimiento. La luz queda encendida mientras no hayan pasado 15 segundos desde entonces; así se ahorra energía.',
  'Combínalo con un sensor de luz para que solo funcione de noche.')

P('Saludo automático en la entrada', CAT, 2, ['saludo automatico','bienvenida','recepcion','mensaje de bienvenida'],
  'Cuando alguien llega a la entrada, la LCD muestra "¡Bienvenido!" y suena una melodía corta.',
  [C('pir', 'Sensor PIR', o='D2'), C('lcd', 'Pantalla LCD'), C('buzzer', 'Melodía', p='D8')],
  LCD_INC + '''const int PIR = 2, PARLANTE = 8;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(PIR, INPUT);
  lcd.print("Te esperamos...");
}

void loop() {
  if (digitalRead(PIR) == HIGH) {
    lcd.clear();
    lcd.print("  Bienvenido!");
    lcd.setCursor(0, 1);
    lcd.print(" Pasa adelante");
    tone(PARLANTE, 523, 150); delay(180);
    tone(PARLANTE, 659, 150); delay(180);
    tone(PARLANTE, 784, 300); delay(3000);
    lcd.clear();
    lcd.print("Te esperamos...");
  }
}
''', 'Al detectar a alguien, el programa borra la pantalla, escribe el saludo y toca tres notas que suben (do, mi, sol). Luego vuelve al mensaje de espera.',
  'Cuenta cuántas personas han llegado y muéstralo en la segunda línea.')

P('Radar con servo y ultrasonido', CAT, 3, ['radar','barrido','sonar con servo','mapa de distancias'],
  'Un servo gira el sensor ultrasónico de lado a lado y el monitor muestra la distancia en cada ángulo, como un radar.',
  [C('sonar', 'Sensor ultrasónico', t='D7', e='D6'), C('servo', 'Giro del radar', s='D9'), C('led', 'Objeto cerca', 'rojo', a='D13')],
  SERVO_INC + '''Servo giro;
const int TRIG = 7, ECHO = 6, LUZ = 13;

long medir() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10); digitalWrite(TRIG, LOW);
  long cm = pulseIn(ECHO, HIGH) / 58;   // en Arduino la división entera no deja decimales
  return cm;
}

void barrer(int desde, int hasta, int paso) {
  for (int a = desde; a != hasta + paso; a += paso) {
    giro.write(a);
    delay(60);
    long cm = medir();
    digitalWrite(LUZ, cm < 40);
    Serial.print(a); Serial.print("°: "); Serial.print(cm); Serial.println(" cm");
  }
}

void setup() {
  Serial.begin(9600);
  giro.attach(9);
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT); pinMode(LUZ, OUTPUT);
}

void loop() {
  barrer(0, 180, 15);
  barrer(180, 0, -15);
}
''', 'La función barrer() mueve el servo paso a paso y mide en cada posición. Llamándola de ida y de vuelta, el radar vigila todo el semicírculo.',
  'Guarda el ángulo donde está el objeto más cercano y apunta allí al terminar.')

P('Barrera automática de parqueadero', CAT, 2, ['barrera automatica','talanquera','parqueadero','pluma'],
  'Cuando un carro se acerca, la barrera (servo) se levanta y baja de nuevo cuando ya pasó.',
  [C('sonar', 'Sensor del carro', t='D7', e='D6'), C('servo', 'Barrera', s='D9'), C('led', 'Pase', 'verde', a='D12'), C('led', 'Pare', 'rojo', a='D13')],
  SERVO_INC + '''Servo barrera;
const int TRIG = 7, ECHO = 6;

long medir() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10); digitalWrite(TRIG, LOW);
  long cm = pulseIn(ECHO, HIGH) / 58;   // en Arduino la división entera no deja decimales
  return cm;
}

void setup() {
  barrera.attach(9);
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
  pinMode(12, OUTPUT); pinMode(13, OUTPUT);
  barrera.write(0);
}

void loop() {
  if (medir() < 20) {
    digitalWrite(13, LOW); digitalWrite(12, HIGH);
    barrera.write(90);                  // subir
    while (medir() < 20) delay(100);    // esperar a que pase
    delay(2000);
    barrera.write(0);                   // bajar
    digitalWrite(12, LOW);
  }
  digitalWrite(13, HIGH);
  delay(100);
}
''', 'Mientras el carro sigue frente al sensor, el ciclo while espera. Cuando se va, se esperan 2 segundos más por seguridad y la barrera baja.',
  'Agrega un contador de cupos libres en una LCD.')

P('Medidor de nivel con ultrasonido', CAT, 2, ['nivel con ultrasonido','tanque de agua','medir nivel','deposito'],
  'El sensor, puesto en la tapa de un tanque, calcula qué porcentaje de agua tiene.',
  [C('sonar', 'Sensor en la tapa', t='D7', e='D6'), C('lcd', 'Pantalla LCD'), C('led', 'Tanque bajo', 'rojo', a='D13')],
  LCD_INC + '''const int TRIG = 7, ECHO = 6;
const int ALTURA = 100;        // cm desde el sensor hasta el fondo

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT); pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10); digitalWrite(TRIG, LOW);
  long aire = pulseIn(ECHO, HIGH) / 58;           // distancia hasta el agua
  int nivel = constrain(map(aire, ALTURA, 5, 0, 100), 0, 100);
  lcd.setCursor(0, 0); lcd.print("Nivel: "); lcd.print(nivel); lcd.print(" %   ");
  lcd.setCursor(0, 1);
  if (nivel < 20) lcd.print("Llenar tanque!  ");
  else lcd.print("                ");
  digitalWrite(13, nivel < 20);
  delay(500);
}
''', 'El sensor mide la distancia hasta la superficie del agua. Si el agua está lejos (100 cm), el tanque está vacío; si está cerca (5 cm), lleno. map() lo convierte a porcentaje.',
  'Calcula los litros si sabes el ancho y el largo del tanque.')

P('Regla digital con botón de guardar', CAT, 2, ['regla digital','medir objetos','guardar medida','cinta metrica con memoria'],
  'Mide distancias y al presionar el botón guarda la medida en la memoria para compararla.',
  [C('sonar', 'Sensor ultrasónico', t='D7', e='D6'), C('button', 'Guardar', x='D2'), C('lcd', 'Pantalla LCD')],
  LCD_INC + '''const int TRIG = 7, ECHO = 6, BOTON = 2;
long guardada = 0;

void setup() {
  lcd.init(); lcd.backlight();
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT); pinMode(BOTON, INPUT_PULLUP);
}

void loop() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10); digitalWrite(TRIG, LOW);
  long cm = pulseIn(ECHO, HIGH) / 58;
  if (digitalRead(BOTON) == LOW) guardada = cm;
  lcd.setCursor(0, 0); lcd.print("Ahora:   "); lcd.print(cm); lcd.print(" cm   ");
  lcd.setCursor(0, 1); lcd.print("Guardada:"); lcd.print(guardada); lcd.print(" cm   ");
  delay(250);
}
''', 'La variable guardada solo cambia cuando se presiona el botón; mientras tanto la primera línea sigue midiendo. Así se pueden comparar dos medidas.',
  'Muestra la diferencia entre la medida actual y la guardada.')

P('Detector de movimiento con sirena y luces', CAT, 2, ['alarma pir','sirena con pir','alarma de casa','sistema de alarma'],
  'Una alarma de casa: si el PIR detecta movimiento, suenan la sirena y las luces durante 10 segundos.',
  [C('pir', 'Sensor PIR', o='D2'), C('buzzer', 'Sirena', p='D8'), C('led', 'Luz roja', 'rojo', a='D12'), C('led', 'Luz azul', 'azul', a='D13')],
  '''
// Alarma de casa con PIR
const int PIR = 2, SIRENA = 8, ROJA = 12, AZUL = 13;

void setup() {
  Serial.begin(9600);
  pinMode(PIR, INPUT); pinMode(ROJA, OUTPUT); pinMode(AZUL, OUTPUT);
}

void loop() {
  if (digitalRead(PIR) == HIGH) {
    Serial.println("¡ALARMA!");
    unsigned long inicio = millis();
    while (millis() - inicio < 10000) {         // 10 segundos de alarma
      digitalWrite(ROJA, HIGH); digitalWrite(AZUL, LOW); tone(SIRENA, 1500); delay(200);
      digitalWrite(ROJA, LOW); digitalWrite(AZUL, HIGH); tone(SIRENA, 1000); delay(200);
    }
    noTone(SIRENA); digitalWrite(AZUL, LOW);
  }
}
''', 'El ciclo while repite el efecto de luces y sirena hasta que pasan 10 segundos, contados con millis().',
  'Agrega un interruptor para armar y desarmar la alarma.')
