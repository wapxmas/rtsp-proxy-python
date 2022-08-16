import base64
import binascii


class RtspRequest:
    request_string: str = None
    real_camera_url: str = None
    request_camera_url: str = None
    rtsp_headers: dict = {}
    rtsp_type: str = None
    rtsp_version: str = None
    camera_id: str = None

    def __init__(self, request_string):
        self.request_string = request_string

    def decode(self):
        if self.request_string is None or len(self.request_string) == 0:
            raise Exception('Request string is empty or None')

        request_lines: list[str] = self.request_string.splitlines()

        if len(request_lines) == 0:
            raise Exception('Request has no lines')

        request_header: list[str] = request_lines[0].split(' ')

        if len(request_header) != 3:
            raise Exception(f'Invalid request header: {request_lines[0]}')

        self.rtsp_type = request_header[0]
        self.request_camera_url = request_header[1]
        self.rtsp_version = request_header[2]

        rtsp_url_parts = request_header[1].split('/')

        if len(rtsp_url_parts) < 4:
            raise Exception(f'Rtsp url is not invalid for proxying: {request_header[1]}')

        self.real_camera_url = base64.urlsafe_b64decode(rtsp_url_parts[3]).decode()

        self.camera_id = rtsp_url_parts[3]

        for raw_hdr in request_lines[1:]:
            hdr_parts: list[str] = raw_hdr.split(':')
            if len(hdr_parts) != 2:
                continue
            self.rtsp_headers[hdr_parts[0]] = hdr_parts[1].strip()

    def make_camera_request(self, rtsp_camera_url: str, proxy_camera_url: str) -> str:
        new_request: str = f'{self.rtsp_type} ' \
                           f'{self.request_camera_url} ' \
                           f'{self.rtsp_version}\r\n'

        for hkey, hval in self.rtsp_headers.items():
            new_request += f'{hkey}: {hval}\r\n'

        new_request += '\r\n'

        new_request = new_request.replace(proxy_camera_url, rtsp_camera_url)

        return new_request
