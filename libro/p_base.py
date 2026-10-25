
# Base para escribir los proyectos del libro
PROJ = []

def C(tipo, nombre, color=None, **pines):
    d = {'tipo': tipo, 'nombre': nombre}
    if color:
        d['color'] = color
    if pines:
        d['pines'] = dict(pines)
    return d

def P(titulo, cat, nivel, keys, idea, comps, code, explica, reto, notas=(), extra=()):
    PROJ.append(dict(titulo=titulo, cat=cat, nivel=nivel, keys=list(keys), idea=idea, componentes=comps,
                     codigo=code.strip('\n') + '\n', explica=explica, reto=reto, notas=list(notas), materiales_extra=list(extra)))

LCD_INC = '#include <Wire.h>\n#include <LiquidCrystal_I2C.h>\nLiquidCrystal_I2C lcd(0x27, 16, 2);   // pantalla en A4 (SDA) y A5 (SCL)\n'
SERVO_INC = '#include <Servo.h>\n'
KP_INC = '''#include <Keypad.h>
const byte FILAS = 4;
const byte COLUMNAS = 4;
char teclas[FILAS][COLUMNAS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
byte pinesFilas[FILAS] = {9, 8, 7, 6};
byte pinesColumnas[COLUMNAS] = {5, 4, 3, 2};
Keypad teclado = Keypad(makeKeymap(teclas), pinesFilas, pinesColumnas, FILAS, COLUMNAS);
'''
KP_PINS = dict(r1='D9', r2='D8', r3='D7', r4='D6', c1='D5', c2='D4', c3='D3', c4='D2')
RFID_INC = '#include <SPI.h>\n#include <MFRC522.h>\nMFRC522 rfid(10, 9);   // SDA en D10 y RST en D9\n'
FP_INC = '#include <Adafruit_Fingerprint.h>\n#include <SoftwareSerial.h>\nSoftwareSerial mySerial(2, 3);   // TX del lector en D2, RX en D3\nAdafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);\n'
DHT_INC = '#include <DHT.h>\nDHT dht(2, DHT11);   // DATA del sensor en D2\n'
FP_READ = '''// Devuelve el número de la huella reconocida, 0 si no la conoce o -1 si no hay dedo
int leerHuella() {
  if (finger.getImage() != FINGERPRINT_OK) return -1;
  if (finger.image2Tz() != FINGERPRINT_OK) return -1;
  if (finger.fingerFastSearch() != FINGERPRINT_OK) return 0;
  return finger.fingerID;
}
'''
RFID_READ = '''// Devuelve 1 si la tarjeta leída es la autorizada (blanca: 4A 3F 21 9C), 0 si es otra y -1 si no hay tarjeta
int leerTarjeta() {
  if (!rfid.PICC_IsNewCardPresent()) return -1;
  if (!rfid.PICC_ReadCardSerial()) return -1;
  Serial.print("Tarjeta:");
  for (byte i = 0; i < rfid.uid.size; i++) {
    Serial.print(" ");
    Serial.print(rfid.uid.uidByte[i], HEX);
  }
  Serial.println();
  bool ok = rfid.uid.uidByte[0] == 0x4A && rfid.uid.uidByte[1] == 0x3F && rfid.uid.uidByte[2] == 0x21 && rfid.uid.uidByte[3] == 0x9C;
  rfid.PICC_HaltA();
  if (ok) return 1;
  return 0;
}
'''
