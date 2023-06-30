import cv2
import numpy as np

frame_width = 640
frame_height = 480

cap = cv2.VideoCapture(0)

cap.set(3, frame_width)
cap.set(4, frame_height)
cap.set(10, 150)

my_color = [[5, 107, 0, 19, 255, 255],
            [133, 56, 0, 159, 156, 255],
            [57, 76, 0, 100, 255, 255],
            [90, 48, 0, 118, 255, 255]]

color_value = [[51, 153, 255],          ## BGR
              [255, 0, 255],
              [0, 255, 0],
              [255, 0, 0]]

my_points = []

# Convert my_color to lower and upper HSV values
lower_values = [np.array(color[:3]) for color in my_color]
upper_values = [np.array(color[3:]) for color in my_color]

def color_track(img, lower_values, upper_values, color_value):
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    new_points = []
    
    for lower, upper, color in zip(lower_values, upper_values, color_value):
        mask = cv2.inRange(img_HSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(img, (x, y), 10, color, cv2.FILLED)
        
        if x != 0 and y != 0:
            new_points.append([x, y, color])
    
    return new_points

def getContours(frame):
    contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    
    return x + w // 2, y

def drawOnCanvas(my_points, color_value):
    for point in my_points:
        cv2.circle(img_result, (point[0], point[1]), 10, point[2], cv2.FILLED)

while cap.isOpened():
    success, frame = cap.read()
    
    if not success:
        break
    
    img_result = frame.copy()
    new_points = color_track(frame, lower_values, upper_values, color_value)
    
    if len(new_points) != 0:
        for new in new_points:
            my_points.append(new)
    
    if len(my_points) != 0:
        drawOnCanvas(my_points, color_value)
    
    cv2.imshow("Video Camera", img_result)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
