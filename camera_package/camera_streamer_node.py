import os
import cv2
from flask import Flask, render_template, Response
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from rclpy.node import Node

app = Flask(__name__)

class ImageStreamer(Node):
    def __init__(self):
        super().__init__('image_streamer')
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',  # Replace with your image topic
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
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    rclpy.init()
    image_streamer = ImageStreamer()

    # Run Flask app in a separate thread
    import threading
    thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    thread.daemon = True
    thread.start()

    try:
        rclpy.spin(image_streamer)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()

if __name__ == '__main__':
    main()
