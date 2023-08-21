import cv2
import socket
import struct
import pickle

# Set up socket
host = '0.0.0.0'   # Listen on all available interfaces
port = 12345       # Same port number as in the sender script
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

conn, addr = s.accept()

while True:
    # Receive frame size
    size_data = conn.recv(4)
    if not size_data:
        break
    size = struct.unpack(">L", size_data)[0]

    # Receive frame data
    frame_data = b""
    while len(frame_data) < size:
        data = conn.recv(size - len(frame_data))
        if not data:
            break
        frame_data += data

    # Deserialize frame using pickle
    frame = pickle.loads(frame_data)

    # Display frame
    cv2.imshow('Received Video', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
conn.close()
s.close()
