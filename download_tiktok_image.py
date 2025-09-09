# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import requests

def main():
    # The image URL extracted from the TikTok page
    image_url = "https://p16-sign-sg.tiktokcdn.com/tos-alisg-i-photomode-sg/6624ae04538d4c25839dfaefedaa51af~tplv-photomode-image.jpeg?dr=14555&x-expires=1756623600&x-signature=qCSKvqFy8%2Fm0dpBkn74sXy6y5v4%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=9b759fb9&idc=my2&ftpl=1"
    
    response = requests.get(image_url)
    response.raise_for_status()
    
    with open('img/tiktok_image.jpeg', 'wb') as f:
        f.write(response.content)
    
    print("Image downloaded successfully to img/tiktok_image.jpeg")

if __name__ == "__main__":
    main()
