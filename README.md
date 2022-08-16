# RTSP Proxy

## Requirements

- Python >= 3.10.5

## Usage

```shell
python -m venv ./venv

source ./venv/bin/activate

pip install -r requirements.txt

python main.py --encode rtsp://A.B.C.D:554/onvif/profile2/media.smp

cnRzcDovL0EuQi5DLkQ6NTU0L29udmlmL3Byb2ZpbGUyL21lZGlhLnNtcA==

vlc rtsp://localhost:2002/cnRzcDovL0EuQi5DLkQ6NTU0L29udmlmL3Byb2ZpbGUyL21lZGlhLnNtcA==
```
