import cv2
import numpy as np
import time

def nothing(x):
    pass

cv2.namedWindow("HSV Controls")
cv2.createTrackbar("Lower-H", "HSV Controls", 22, 180, nothing)
cv2.createTrackbar("Lower-S", "HSV Controls", 100, 255, nothing)
cv2.createTrackbar("Lower-V", "HSV Controls", 70, 255, nothing)
cv2.createTrackbar("Upper-H", "HSV Controls", 130, 180, nothing)
cv2.createTrackbar("Upper-S", "HSV Controls", 255, 255, nothing)
cv2.createTrackbar("Upper-V", "HSV Controls", 255, 255, nothing)

cap = cv2.VideoCapture(0)
time.sleep(2)

print("⏳ wait")
for i in range(30):
    ret, background = cap.read()
background = np.flip(background, axis=1)

print("✅ ready")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = np.flip(frame, axis=1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("Lower-H", "HSV Controls")
    l_s = cv2.getTrackbarPos("Lower-S", "HSV Controls")
    l_v = cv2.getTrackbarPos("Lower-V", "HSV Controls")
    u_h = cv2.getTrackbarPos("Upper-H", "HSV Controls")
    u_s = cv2.getTrackbarPos("Upper-S", "HSV Controls")
    u_v = cv2.getTrackbarPos("Upper-V", "HSV Controls")

    lower_bound = np.array([l_h, l_s, l_v])
    upper_bound = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    mask = cv2.medianBlur(mask, 5)
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)
    mask_inv = cv2.bitwise_not(mask)

    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final_output = cv2.add(res1, res2)

    cv2.imshow("Harry's Cloak", final_output)
    cv2.imshow("Mask", mask)
    cv2.imshow("Original", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
