import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
from flask import Flask, render_template, Response
import socket
import threading

current_directory = os.path.dirname(__file__)
share_directory = os.path.abspath(os.path.join(current_directory, '..', '..', '..', '..', 'share/camera_package/camera_package'))
templates_folder = 'views'
static_folder = 'static'
templates_path = os.path.join(share_directory, templates_folder)
static_path = os.path.join(share_directory, static_folder)
print("Templates path:", templates_path, "Static path:", static_path)

app = Flask(__name__, template_folder=templates_path, static_folder=static_path)

class ImageStreamer(Node):
    def __init__(self):
        super().__init__('image_streamer')

        self.declare_parameter('ip', "0.0.0.0")

        self.ip = self.get_parameter('ip').value

        self.subscription = self.create_subscription(
            Image,
            '/opencv_image',  # Replace with your image topic
            self.image_callback,
            10  # Adjust the queue size based on your needs
        )
        self.subscription  # Prevent unused variable warning
        self.bridge = CvBridge()

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        _, buffer = cv2.imencode('.jpg', cv_image)
        image_data = buffer.tobytes()
        app.image_data = image_data

def generate():
    while True:
        if hasattr(app, 'image_data'):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + app.image_data + b'\r\n')

@app.route('/')
def index():
    return render_template('index_2.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    rclpy.init()
    image_streamer = ImageStreamer()

    # Run Flask app in a separate thread
    
    # Get the local IP address dynamically
    # local_ip = socket.gethostbyname(socket.gethostname())
    print('--------------------------------------------')
    print(f" access video feed on http://{image_streamer.ip}:5000")
    print('--------------------------------------------')

    thread = threading.Thread(target=app.run, kwargs={'host': image_streamer.ip, 'port': 5000})
    thread.daemon = True
    thread.start()

    

    try:
        rclpy.spin(image_streamer)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()

if __name__ == '__main__':
    main()
