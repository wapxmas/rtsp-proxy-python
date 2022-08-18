import socket
from rtsp_request import RtspRequest
import rtsp_utils


class Camera:
    camera_url: str = None
    proxy_camera_url: str = None
    camera_host: str = None
    camera_login: str = None
    camera_password: str = None
    camera_socket: socket = None
    camera_id: str = None

    def __init__(self, camera_id, camera_url, proxy_camera_url):
        if camera_url is None or len(camera_url) == 0:
            raise Exception('camera_url is None or empty')

        url_parts: list[str] = camera_url.split('/')

        if len(url_parts) < 3 or url_parts[0].lower() != 'rtsp:':
            raise Exception(f'Invalid camera url: {camera_url}')

        auth_parts = url_parts[2].split('@')

        if len(auth_parts) > 1:
            self.camera_host = auth_parts[1]
            auth_tokens = auth_parts[1].split(':')
            if len(auth_tokens) == 2:
                self.camera_login = auth_tokens[0]
                self.camera_password = auth_tokens[1]
        else:
            self.camera_host = auth_parts[0]

        self.camera_url = f'rtsp://{self.camera_host}/' \
                          + '/'.join(url_parts[3:])
        self.proxy_camera_url = proxy_camera_url
        self.camera_id = camera_id

    def send_client_request(self, request: RtspRequest):
        request_string = request.make_camera_request(
            self.camera_url, self.proxy_camera_url)
        self.camera_socket.sendall(str.encode(request_string))
        print(request_string)

    def get_response(self) -> str:
        response_bytes = bytearray()
        while True:
            data = self.camera_socket.recv(1024)
            response_bytes.extend(data)
            if not rtsp_utils.is_response_full(response_bytes):
                continue
            break
        response_str = response_bytes.decode()
        response_str = response_str.replace(self.camera_url,
                                            self.proxy_camera_url)
        return rtsp_utils.update_content_length(response_str)

    def connect(self):
        host_parts = self.camera_host.split(':')
        self.camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        camera_port = int(host_parts[1]) if len(host_parts) == 2 else 554
        self.camera_socket.connect((host_parts[0], camera_port))
        print(f'Connected to camera {self.camera_host}')

    def disconnect(self):
        self.camera_socket.close()
        print(f'Disconnected from camera {self.camera_host}')
