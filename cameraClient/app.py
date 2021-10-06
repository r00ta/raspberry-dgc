from picamera.array import PiRGBArray
from picamera import PiCamera
from RPi import GPIO
import time
import sys
import cv2
import zbarlight
import requests
from PIL import Image

import threading
import tkinter as tk 
import time 

def update_thread(window):
    # Initialise Raspberry Pi camera
    RESOLUTION = (480, 272)
    camera = PiCamera()
    camera.resolution = RESOLUTION

    # set up stream buffer
    rawCapture = PiRGBArray(camera, size = RESOLUTION)

    # allow camera to warm up
    time.sleep(0.1)
    print("cameraClient ready")

    # Initialise OpenCV window
    cv2.namedWindow("raspberry-dgc")
    print("OpenCV window ready")

    # Capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
    
        # as raw NumPy array
        output = frame.array.copy()

        # raw detection code
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY, dstCn=0)
        pil = Image.fromarray(gray)
        width, height = pil.size
        raw = pil.tobytes()

        # create a reader
        codes = zbarlight.scan_codes(['qrcode'], pil)
    
        # if a qrcode was found, call validatorServer
        if codes is not None:

            payload = {'dgc': codes[0]}
            r = requests.get('http://localhost:3000/', params=payload)
            print('Return code: ', r.status_code, ', Text: ', r.text)
            if r.status_code == 200:
                window.green()
                time.sleep(10)
            else:
                window.red()
                time.sleep(3)

        window.new()

        # show the frame
        cv2.imshow("raspberry-dgc", output)

        # clear stream for next frame
        rawCapture.truncate(0)
    
        # Wait for Q to quit
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord('q'):
            break

# When everything is done, release the capture
camera.close()
cv2.destroyAllWindows()

    i = 0
    while True:
        if i % 3 == 0:
            window.green()
        if i % 3 == 1:
            window.red()
        if i % 3 == 2: 
            window.new()
        time.sleep(1)
        i += 1

class GreenPassWindow:
    def __init__(self):
        # set main window
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.label = tk.Label(self.root, text="scansiona Green Pass", 
            height=500, width=500, relief='sunken', bg='green', font='Helvetica 16 bold')
        self.label.pack()
    
    def start(self):
        self.root.mainloop()

    def green(self):
        self.label.config(text = "Certificato Valido")
        self.label.config(bg = "green")

    def red(self):
        self.label.config(text = "Certificato non valido")
        self.label.config(bg = "red")

    def new(self):
        self.label.config(text = "Scansiona green pass")
        self.label.config(bg = "white")


if __name__ == "__main__":
    window = GreenPassWindow()
    thread1 = threading.Thread(target=update_thread, args=(window,))
    thread1.start()  # launch thread
    
    window.start()
