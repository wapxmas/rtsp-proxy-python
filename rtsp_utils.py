def is_response_full(response_bytes: bytearray) -> bool:
    if response_bytes.find(b'\r\n\r\n') == -1:
        return False
    r_str = response_bytes.decode()
    r_parts = r_str.splitlines()
    for r_hdr in r_parts[1:]:
        hdr_parts = r_hdr.split(':')
        if len(hdr_parts) != 2:
            continue
        if hdr_parts[0].lower() == 'content-length':
            return int(hdr_parts[1].strip()) == \
                   len(response_bytes) - response_bytes.find(b'\r\n\r\n') - 4
    return True


def update_content_length(response: str) -> str:
    end_hdr_idx = response.find('\r\n\r\n')
    if response == -1:
        raise Exception(f'No end headers marker '
                        f'in request/response: {response}')
    if end_hdr_idx + 4 == len(response):
        return response
    h_parts = response[:end_hdr_idx].splitlines()
    for hdr in h_parts[1:]:
        hdr_parts = hdr.split(':')
        if len(hdr_parts) != 2:
            continue
        if hdr_parts[0].lower() == 'content-length':
            content_length = len(response) - end_hdr_idx - 4
            return response.replace(hdr, f'Content-Length: {content_length}')
    raise Exception('No content length found, but content is present.')
