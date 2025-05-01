import cv2 #Librerias para su funcinamiento
import mediapipe as mp
import serial
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) #Confianza 0.7
mp_draw = mp.solutions.drawing_utils

arduino = serial.Serial('COM4', 9600, timeout=1) #Conexion con arduino
time.sleep(2)  # Espera para establecer conexión
print("** Sistema de conteo de dedos iniciado **") #print para ver el inicio

cap = cv2.VideoCapture(0) #iniciar la camara web
prev_fingers = 0
last_update_time = time.time()

while True:
    success, img = cap.read()  #Entramos al ciclo
    if not success:  #Esperamos a que no falle la camara
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    finger_count = 0  # Sino hay mano su valor es 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            fingers_up = 0

            # Detectar indice-medio-anular-meñique
            for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                if landmarks[tip].y < landmarks[pip].y - 0.08:  # comparar los ejes
                    fingers_up += 1

            # Detección del pulgar con tolerancia
            thumb_tip = landmarks[4]
            thumb_ip = landmarks[3]
            wrist = landmarks[0] #Eje X
            
            if (thumb_tip.x < thumb_ip.x and thumb_tip.x < wrist.x - 0.08) or \
               (thumb_tip.x > thumb_ip.x and thumb_tip.x > wrist.x + 0.08):
                fingers_up += 1

            finger_count = min(fingers_up, 5)  # Solo 5 dedos
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Parte de depurar
    print(f"Dedos detectados - Antes de enviar: {finger_count}")
    
    # Envio de datos a arduino
    current_time = time.time()
    if finger_count != prev_fingers and (current_time - last_update_time) > 0.5:
        if 0 <= finger_count <= 5:  # Validacion
            arduino.write(f"{finger_count}\n".encode())  # Enviar los saltos de cada linea
            print(f"Enviando a Arduino: {finger_count}")
            prev_fingers = finger_count
            last_update_time = current_time

    # Visualizar en consola
    cv2.putText(img, f"Dedos: {finger_count}", (10, 50), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Contador de Dedos", img) #Contar los dedos

    if cv2.waitKey(1) & 0xFF == ord('q'): #Salir de la ventana
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
print("Programa terminado") #Se cierra el programa