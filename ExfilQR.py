import os
import time
import argparse
import imageio
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
import numpy as np
from multiprocessing import Pool

def data_to_qr(data, size=(512, 512)):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").resize(size)
    img = np.array(img).astype(np.uint8) * 255
    return img

def file_to_images(file_path, chunk_size=1024, verbose=False, num_processes=4):
    with open(file_path, "rb") as f:
        data = f.read()

    chunks = [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Create a process pool
    with Pool(num_processes) as p:
        images = p.map(data_to_qr, chunks)

    if verbose:
        print(f"Generated {len(images)} images from file {file_path}")
    return images

def video_to_data(video_path, verbose=False):
    data = b""
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        decoded_objects = decode(Image.fromarray(gray))

        for obj in decoded_objects:
            data += bytes(obj.data)

        if verbose:
            print(f"Processed frame of video {video_path}")

    cap.release()
    return data

def images_to_mp4(images, save_path, fps=30, verbose=False):
    with imageio.get_writer(save_path, fps=fps) as writer:
        for image in images:
            if verbose:
                print(f"Writing frame to video")
            writer.append_data(image)

def main():
    start_time = time.time()  # record the start time

    parser = argparse.ArgumentParser(description="Converts files to QR code videos and back.")
    parser.add_argument("input", help="Input file or video.")
    parser.add_argument("output", help="Output video or file.")
    parser.add_argument("-f", "--fps", type=int, default=30, help="Frames per second (only applicable when creating a video).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity.")
    parser.add_argument("--chunk-size", type=int, default=1024, help="Size of the data chunks (only applicable when creating a video).")
    parser.add_argument("-b", "--backward", action="store_true", help="Enable backward operation (video to file).")
    parser.add_argument("-p", "--num-processes", type=int, default=4, help="Number of processes to use.")
    args = parser.parse_args()

    input_size = os.path.getsize(args.input)  # get the size of the input file

    if args.backward:
        data = video_to_data(args.input, args.verbose)
        with open(args.output, "wb") as f:
            f.write(data)
        output_size = len(data)
    else:
        images = file_to_images(args.input, args.chunk_size, args.verbose, args.num_processes)
        images_to_mp4(images, args.output, args.fps, args.verbose)
        output_size = os.path.getsize(args.output)  # get the size of the output file

    end_time = time.time()  # record the end time

    elapsed_time = end_time - start_time  # calculate elapsed time

    print(f"Input size: {input_size / (1024 * 1024):.2f} MB")
    print(f"Output size: {output_size / (1024 * 1024):.2f} MB")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Speed: {input_size / elapsed_time / (1024 * 1024):.2f} MB/s")

    if not args.backward:
        duration = len(images) / args.fps
        print(f"Video duration: {duration:.2f} seconds")
        print(f"Bitrate: {output_size * 8 / duration / 1000:.2f} kbps")

if __name__ == "__main__":
    main()
