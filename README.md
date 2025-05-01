# SISTEMA DE CONTEO DE DEDOS - PHYTON & ARDUINO

## Descripción

En este proyecto se utiliza la visión por computadora con (Phyton - OpenCV - MediaPipe)
detectando la cantidad de los dedos levantados en una mano y estos datos se envian a Arduino
el cual controla los LEDSs, esto permite crear una interfaz física visual y teniendo el monitoreo en la consola.

## Hardware necesario

- Webcam
- Una placa de Arduino (Uno o nano)
- 5 LEDs (uno para cada dedo)
- Resistencias
- Protoboard y los jumpers de conexión
- Una computadora con Phyton y Arduino IDE instalados

## Conexiones de Arduino

- Pin 2 - LED1
- Pin 3 - LED2
- Pin 4 - LED3
- Pin 5 - LED4
- Pin 6 - LED5
- GND - Conexión de resistencias de 220 Ohms para los LEDs

## Software Necesario

- Python 3.8 o mayor
- Bibliotecas de Python: cv2, mediapipe, serial, time

# Funcionamiento General

1. **Python - OpenCV - MediaPipe** (detectan la mano y sus dedos)
2. Se cuentan los dedos levantados (0 - 5)
3. El numero de dedos se envia por serial a Arduino
4. Arduino encendera la cantidad de LEDs

# Logica que detecta los dedos

- El script en Phython detecta los dedos usando los puntos de MediaPipe.
- Si se detecta un dedo levantado, se compara con la posicion vertical "tip" con la articulacion intermedia "pip".
- Se configura la logica para detectar si el pulgar esta levantado o no, usando como referencia el eje X. 

## Recomendaciones

1. Actualizar siempre las conexiones de hardware dependiendo como se tenga conectado
2. Actualizar el protocolo de comunicación