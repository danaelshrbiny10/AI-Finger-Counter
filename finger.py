import cv2
import mediapipe as mp


# Declaring the MediaPipe objects and the finger and thumb coordinates
cap = cv2.VideoCapture(0)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4,2)

# Converting the input image to RGB image
while True:
    success, image = cap.read()
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks

# Drawing the landmarks present in the hand
    if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)

            # Changing the hand points coordinates into image pixels
            for idx, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handList.append((cx, cy))
            
            # Circling the hand points
            for point in handList:
                cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)

                # Checking finger is open or closed
                upCount = 0
                for coordinate in finger_Coord:
                    if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                        upCount += 1
                if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
                    upCount += 1
                    
                    # Displaying output
                cv2.putText(image, str(upCount), (150,150), cv2.FONT_HERSHEY_PLAIN, 12, (0,255,0), 12)
                
            cv2.imshow("Counting number of fingers", image)
            cv2.waitKey(1)    
