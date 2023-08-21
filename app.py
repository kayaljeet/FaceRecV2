from flask import Flask, Response, render_template
import socket
import pickle
import struct
import logging

app = Flask(__name__)


def receive_frames():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))  # Use the same port number as in Computer A
    server_socket.listen(5)

    client_socket, addr = server_socket.accept()

    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K buffer size
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        yield frame


@app.route("/")
def index():
    return render_template("index.html")


logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG


@app.route("/video_feed")
def video_feed():
    logging.debug("Entering video_feed route")  # Debug log message
    return Response(receive_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    host = "127.0.0.1"  # Use localhost for local testing
    port = 8080  # Use a port that is available for local testing

    app.run(host=host, port=port)
