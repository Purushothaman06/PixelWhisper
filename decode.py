# This script is used to decode and decrypt the message from the encoded video

"""
Install dependencies:
pip install -r requirements.txt

Usage: 
python decode.py <path_to_encoded_video>

Example:
python decode.py video.mov
"""

from stegano import lsb
import cv2
import os
import sys
import shutil
from termcolor import cprint
from pyfiglet import figlet_format
import rsautil1

os.system("cls" if os.name == "nt" else "clear")
cprint(figlet_format("Pixel Whisper", font="slant"), "cyan", attrs=["bold"])
cprint(
    figlet_format("Secure Message & Media Concealment", font="digital"),
    "green",
    attrs=["bold"],
)
ENCODED_VIDEO = sys.argv[1]
temp_folder = "tmp2"
frame_choice = int(
    input(
        "1) Extract and enter frame numbers from image /n 2) Enter frame numbers manually : "
    )
)
decoded = {}

if frame_choice == 1:
    ENCODED_IMAGE = input("/n Enter image name with extension : ")
    res = lsb.reveal(ENCODED_IMAGE)
    print(f"Encrypted frame numbers : {res}")
    cprint("RSA Encrypted {Assysmetric Encryption}", "blue")
    cprint("Reading private key from keys folder and trying to decrypt", "red")
    msg1 = rsautil1.decrypt(message=res)
    msg1 = msg1.decode("utf-8")
    cprint(f"Decoded image: \n {msg1}", "green")
    FRAMES = list(
        map(int, input("Enter Above FRAME NUMBERS seperated by space: ").split())
    )
else:
    FRAMES = list(map(int, input("Enter FRAME NUMBERS seperated by space: ").split()))
    # print(FRAMES)


def createTmp():

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)


def countFrames():

    cap = cv2.VideoCapture(ENCODED_VIDEO)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length


def decodeVideo(number_of_frames):

    # First get the frame
    cap = cv2.VideoCapture(ENCODED_VIDEO)
    frame_number = -1
    while frame_number <= number_of_frames:
        frame_number += 1
        frame_file_name = os.path.join(temp_folder, f"{frame_number}.png")
        encoded_frame_file_name = os.path.join(temp_folder, f"{frame_number}-enc.png")
        # print(f"Frame number {frame_number}")
        ret, frame = cap.read()

        if frame_number in FRAMES:
            cv2.imwrite(encoded_frame_file_name, frame)
            clear_message = lsb.reveal(encoded_frame_file_name)
            decoded[frame_number] = clear_message
            cprint(f"Frame {frame_number} DECODED: {clear_message}", "blue")


def clean_tmp(path="./tmp2"):

    if os.path.exists(path):
        shutil.rmtree(path)
        cprint("[INFO] tmp files are cleaned up", "green")


def arrangeAndDecrypt():

    res = ""
    for fn in FRAMES:
        res = res + decoded[fn]
    cprint(f"Final string: {res}", "green")
    cprint("Reading private key from keys folder and trying to decrypt", "red")
    msg1 = rsautil1.decrypt(message=res)
    msg1 = msg1.decode("utf-8")
    cprint(f"Decoded text: \n {msg1}", "yellow")
    clean_tmp()


createTmp()
frames = countFrames()
decodeVideo(frames)
arrangeAndDecrypt()