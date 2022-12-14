from flask import Flask, render_template, url_for, Response
import cv2 as cv
import numpy as np

# # #  Import the functions you need from the SDKs you need
# # import { initializeApp } from "firebase/app";
# # import { getAnalytics } from "firebase/analytics";
# # # // TODO: Add SDKs for Firebase products that you want to use
# # # // https://firebase.google.com/docs/web/setup#available-libraries

# # # // Your web app's Firebase configuration
# # # // For Firebase JS SDK v7.20.0 and later, measurementId is optional
# # firebaseConfig = {
# #   apiKey: "AIzaSyBdKaaG7FDF7YovzMAJxeX55D-n4wRoTgM",
# #   authDomain: "sharkcamapp.firebaseapp.com",
# #   projectId: "sharkcamapp",
# #   storageBucket: "sharkcamapp.appspot.com",
# #   messagingSenderId: "416897826819",
# #   appId: "1:416897826819:web:21ee93949de0c9fcfd4e36",
# #   measurementId: "G-5Y35RKDW7F"
# # };

# # # // Initialize Firebase
# # app = initializeApp(firebaseConfig);
# # analytics = getAnalytics(app);

app = Flask(__name__)

#webpages
@app.route('/', methods = ['GET', 'POST'])
#homepage has buttons that navigate to controls page and photo viewer page
def index():
   return render_template('index.html')

@app.route('/controls', methods = ['GET', 'POST'])
def controls():
    return render_template('controls.html')


@app.route('/photoviewer')
def photoViewer():
    return render_template('photoViewer.html')

# Controls
@app.route('/start', methods=['GET', 'POST'])
def start():
    start_message = "Robot has been started"
    print("started")
    return render_template('controls.html', message=start_message)

@app.route('/stop', methods=['GET', 'POST'])
def stop():
    stop_message = "Robot has been stopped"
    print("stopped")
    return render_template('controls.html', message=stop_message)

@app.route('/photomessage', methods=['GET','POST'])
def photoMessage():
    camera_message = "Camera is streaming"
    print("recording")
    return render_template('controls.html', message=camera_message)


#I know global variables are a sin
camera = cv.VideoCapture(0) #use local camera feed

def get_frames():
    while True:
        success, frame = camera.read()
        if not success: #if nothing happens, break
            break
        else:
            ret, image = cv.imencode('.jpg', frame)
            frame = image.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/livestream', methods=['GET','POST'])
def livestream():
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def photoCapture():
    # only captures one frame on click
    ret, frame = camera.read()
    if not ret:
        print("no photo taken")
    else:
        ret, image = cv.imencode('.jpg', frame)
        frame = image.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  #decode frame

@app.route('/takephoto', methods=['GET','POST'])
def takePhoto():
    return Response(photoCapture(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Settings def and functions
@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    return render_template('settings.html')

def sendScanCommand():
    #send an MQTT command to start the robot
    # for now, will run my own MQTT server to test functionality
    try:
        print("scan command sent")
    except:
        print("Scan command not sent")


