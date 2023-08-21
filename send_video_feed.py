import cv2
import socket
import pickle
import struct

class Camera:
    host = "127.0.0.1"  # Use localhost for local testing
    port = 8080  # Use the same port number as in the Flask app

    def __init__(self, host, port):
        self.camera = cv2.VideoCapture(0)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def send_frame(self):
        while True:
            success, frame = self.camera.read()
            if not success:
                break
            data = pickle.dumps(frame)
            message_size = struct.pack("Q", len(data))
            self.client_socket.sendall(message_size + data)

    def release(self):
        self.client_socket.close()
        self.camera.release()

if __name__ == "__main__":
    camera = Camera(Camera.host, Camera.port)
    camera.send_frame()
    camera.release()
