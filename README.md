# ExfilQR
A tool to turn text into a QR video feed for very fast data exfiltration using a camera.
Adjustable FPS, Data chunking and multithreading are fully functional. 
For example, this is what the ExfilQR.py file would look like. 

![](https://github.com/zaneprall/ExfilQR/blob/main/qrsource.gif?raw=true)
## Usage

python3 ExfilQR.py INPUT OUTPUT --fps FPS --chunk-size CHUNK_SIZE


```sh
$ python3 ExfilQR.py /textfiles/file.txt /QRVIDEOS/video.mp4 --fps 30 --chunk-size 1024 -p 4 -v
```
Please note that this tool can take a very long time to run depending on the size of the file.
**Arguments:**

- `INPUT`: The path to the input file to be converted into QR code images.
- `OUTPUT`: The path for the output video file.
- `--fps FPS`: The frames per second for the output video (Default is 30).
- `--chunk-size CHUNK_SIZE`: The size of data chunks that will be converted into individual QR code images (Default is 1024).
- `--verbose`: Increase output verbosity.
- `-b`: reverse the process and turn .mp4 streams into .txt files
- `-p` NUM_PROCESSES : Specify core count for multithreading on larger applications.  
## Requirements

This tool requires Python 3.6 or higher, and the following Python libraries:

- imageio
- opencv-python
- pyzbar
- qrcode
- numpy
- Pillow
- pathos

## Installation

### pip

To install the necessary Python libraries via pip, you can use the provided requirements.txt file:

pip install -r requirements.txt

### apt

For apt, you may need to install the Python 3 pip package, and the ffmpeg library for imageio:


sudo apt-get update
sudo apt-get install python3-pip ffmpeg
pip3 install -r requirements.txt
