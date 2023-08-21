import cv2
import socket
import struct
import pickle

# Set up socket
host = '127.0.0.1'  # IP of the receiving server
port = 12345       # Same port number as in the receiving script
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Serialize the frame using pickle
    frame_data = pickle.dumps(frame)

    # Send the size of the serialized frame data
    s.send(struct.pack(">L", len(frame_data)))

    # Send the serialized frame data
    s.send(frame_data)

cap.release()
s.close()
