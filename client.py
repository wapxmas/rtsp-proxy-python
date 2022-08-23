from rtsp_request import RtspRequest
from camera import Camera
import socket
import threading


class ClientThread(threading.Thread):
    camera = None
    client_socket: socket.socket = None
    client_address: str = None

    def __init__(self, client_socket: socket.socket, client_address: str):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self) -> None:
        print(f'Connected client: {self.client_address}')

        camera = None

        try:
            while True:
                request_bytes = bytearray()
                while True:
                    data = self.client_socket.recv(1024)
                    request_bytes.extend(data)
                    if request_bytes.find(b'\r\n\r\n') == -1:
                        continue
                    break
                print(f'------- client request: \r\n{request_bytes.decode()}')
                rtsp_request = RtspRequest(request_bytes.decode())
                rtsp_request.parse()
                if camera is None:
                    camera = Camera(rtsp_request.camera_id,
                                    rtsp_request.real_camera_url,
                                    rtsp_request.request_camera_url)
                    camera.connect()
                camera.send_client_request(rtsp_request)
                camera_response = camera.get_response()
                self.client_socket.sendall(str.encode(camera_response))
                print(f'------- camera response: \r\n{camera_response}')
        finally:
            self.client_socket.close()
            if camera is not None:
                camera.disconnect()
