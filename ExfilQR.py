import os
import argparse
import imageio
import qrcode
import numpy as np
from PIL import Image

def data_to_qr(data, size=(512, 512)):
    """Converts data to a QR code image and returns it."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").resize(size)
    return np.array(img).astype(np.uint8) * 255  # Convert boolean array to 8-bit array


def file_to_images(file_path, chunk_size=1024, verbose=False):
    """Reads data from a file and converts it to images."""
    with open(file_path, "rb") as f:
        data = f.read()

    chunks = [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]
    images = [data_to_qr(chunk) for chunk in chunks]

    if verbose:
        print(f"Generated {len(images)} images from file {file_path}")
    return images

def images_to_mp4(images, save_path, fps=30, verbose=False):
    """Converts a list of images to a video and saves it."""
    with imageio.get_writer(save_path, fps=fps) as writer:
        for image in images:
            if verbose:
                print(f"Writing frame to video")
            writer.append_data(image)


def main():
    parser = argparse.ArgumentParser(description="Convert QR code images to a video.")
    parser.add_argument("input", help="Input folder containing QR code images.")
    parser.add_argument("output", help="Output video file.")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second.")
    parser.add_argument("--verbose", action="store_true", help="Increase output verbosity.")
    parser.add_argument("--chunk-size", type=int, default=1024, help="Size of the data chunks.")
    args = parser.parse_args()

    images = file_to_images(args.input, args.chunk_size, args.verbose)
    images_to_mp4(images, args.output, args.fps, args.verbose)

if __name__ == "__main__":
    main()




