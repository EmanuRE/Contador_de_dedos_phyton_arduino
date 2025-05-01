int leds[] = {2, 3, 4, 5, 6};  // Pines para los LEDs
int fingerCount = 0;            // Valor inicial
int prevCount = -1;             // Antes de iniciar -1

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // Inicia el puerto serial
  }
  
  // Configuración de LEDs
  for (int i = 0; i < 5; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);  // Se mantienen apagados al iniciar
  }
  
  Serial.println("Sistema Detector de dedos - Esperando datos de py...");
}

void loop() {
  if (Serial.available() > 0) {
    // Lee los datos de los saltos de linea
    String input = Serial.readStringUntil('\n');
    input.trim();  // Evita los espacios en blanco
    
    // Se convierte entero con la validación
    int newCount = input.toInt();
    
    // Validar el rango de los dedos
    if (newCount >= 0 && newCount <= 5) {
      fingerCount = newCount;
      
      if (fingerCount != prevCount) {
        Serial.print("Dedos recibidos: ");
        Serial.println(fingerCount);
        
        // Se actualizan los leds encendidos
        for (int i = 0; i < 5; i++) {
          digitalWrite(leds[i], (i < fingerCount) ? HIGH : LOW);
        }
        
        prevCount = fingerCount;
      }
    } else {
      Serial.print("No se recibio un valor correcto: ");
      Serial.println(input);
    }
  }
  
  // Delay para el buen funcionamiento
  delay(10);
}