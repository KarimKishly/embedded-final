from PIL import Image
import requests
from object_logic.Color import Color
from camera import Rp_Cam

def send_image_basic(loc: str):
    url = "http://10.31.201.192:8080/process_image"

    payload = {}
    files=[
    ('image',('pic.jpg',
              open(loc,'rb'),
              'image/jpg'))
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    

