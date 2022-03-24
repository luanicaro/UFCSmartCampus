import os
from attr import Attribute
import cv2
import numpy as np
from flask import Flask, render_template, Response, url_for

app = Flask(__name__)
#http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg
#rtsp://ipcam.stream:8554/bars
cap = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4')

path = './frames'

def creath_path(path):
    try:
        os.makedirs(path)
    except OSError:
        pass

creath_path(path)


def returnAndSaveFrames(cap):
    
    idx = 0
    print(cap.get(cv2.CAP_PROP_FPS))
    framesPerSecond = cap.get(cv2.CAP_PROP_FPS)
    print(framesPerSecond)
    retFrame = True
    while(retFrame):    
        retFrame, frame = cap.read()
        try:
            if(idx%(5*round(framesPerSecond)) == 0):
                cv2.imwrite(f"{path}/{idx}.jpg", frame)
            idx+=1
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            print('No retrived frames!')

@app.route('/')
def index():
    return render_template('index.html')    


@app.route('/video_feed1')
def video_feed1():
    return Response(returnAndSaveFrames(cap), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run()