# ExfilQR
A tool to turn text into a QR video feed for very fast data exfiltration using a camera.
## Usage

python3 file.py INPUT OUTPUT --fps FPS --chunk-size CHUNK_SIZE

markdown


**Arguments:**

- `INPUT`: The path to the input file to be converted into QR code images.
- `OUTPUT`: The path for the output video file.
- `--fps FPS`: The frames per second for the output video (Default is 30).
- `--chunk-size CHUNK_SIZE`: The size of data chunks that will be converted into individual QR code images (Default is 1024).
- `--verbose`: Increase output verbosity.

## Requirements

This script requires Python 3.6 or higher, and the following Python libraries:

- argparse
- imageio
- qrcode
- numpy
- PIL (pillow)
## Installation

### pip

To install the necessary Python libraries via pip, you can use the provided requirements.txt file:

pip install -r requirements.txt

### apt

For apt, you may need to install the Python 3 pip package, and the ffmpeg library for imageio:


sudo apt-get update
sudo apt-get install python3-pip ffmpeg
pip3 install -r requirements.txt