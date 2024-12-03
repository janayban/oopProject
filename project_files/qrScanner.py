import cv2
from pyzbar.pyzbar import decode
import time

cam = cv2.VideoCapture(0)
cam.set(5, 640)
cam.set(6, 480)

camera = True

while camera:
    success, frame = cam.read()
    if not success:
        print("Failed to capture frame. Exiting...")
        break

    for i in decode(frame):
        print(i.data.decode("utf-8"))
        time.sleep(3)

    cv2.imshow("QR_Code_Scanner", frame)

    # Check for user closing the window (pressing "X")
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # If the user presses 'q' (or any key you choose)
        break

    # Check if the window is closed by "X" button
    if cv2.getWindowProperty("QR_Code_Scanner", cv2.WND_PROP_VISIBLE) < 1:
        break

# Release resources and close window
cam.release()
cv2.destroyAllWindows()
