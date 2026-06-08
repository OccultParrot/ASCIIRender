from pathlib import Path
import os
import argparse
import time

from rich import print as printc
from PIL import Image
from rich.align import Align
from rich.panel import Panel

# Arg stuff
parser = argparse.ArgumentParser(
    prog="ASCII Renderer",
    description="Takes an image and renders it with text.",
)
parser.add_argument('filename')
parser.add_argument('-c', '--color', action="store_true")
args = parser.parse_args()

path = Path(args.filename)
if not path.exists():
    print(f"File at {path} does not exist.")
    exit(1)

# In the tuple, the number after the char is the start point for checking luminance
chars = [
    ('@', 0),
    ('#', 10),
    ('M', 20),
    ('W', 28),
    ('N', 35),
    ('B', 42),
    ('8', 48),
    ('Q', 54),
    ('0', 60),
    ('D', 66),
    ('E', 72),
    ('H', 78),
    ('G', 84),
    ('K', 89),
    ('R', 94),
    ('X', 100),
    ('U', 105),
    ('5', 110),
    ('S', 115),
    ('Z', 120),
    ('w', 125),
    ('p', 130),
    ('e', 134),
    ('o', 138),
    ('a', 142),
    ('d', 146),
    ('6', 150),
    ('q', 154),
    ('b', 158),
    ('k', 162),
    ('n', 166),
    ('f', 170),
    ('t', 174),
    ('c', 178),
    ('x', 182),
    ('u', 186),
    ('v', 190),
    ('z', 194),
    ('r', 198),
    ('l', 202),
    ('!', 206),
    (';', 210),
    (':', 214),
    (',', 218),
    ("'", 222),
    ('`', 226),
    ('.', 232),
    ('-', 240),
    (' ', 255),
]

# Starting timer for stats
start = time.time()

im = Image.open(path)
original_size = im.size  # Collecting for later stats

terminal_width, _ = os.get_terminal_size()
scale = terminal_width / im.size[0]  # Formula for percentage is p = w1 / w2

# Scaling
new_size = (int(im.width * scale), int(im.height * scale))
im = im.resize(new_size)

# Final string is used for counting the unique chars at the end
final_string = ""

# Looping through each pixel
for y in range(im.height):
    # The line to print at the end of the line
    line = ""
    for x in range(im.width):
        pixel = im.getpixel((x, y))
        choice = ""
        for i, c in enumerate(chars):
            l = (pixel[0] + pixel[1] + pixel[2]) / 3  # Getting the luminescence of the pixel
            if l < c[1]:
                choice = chars[i - 1][0]  # Selecting the character
                final_string += choice  # Append it to the final string
                # Print in color of the color flag is true
                if args.color:
                    choice = f"[rgb({pixel[0]},{pixel[1]},{pixel[2]})]{choice}[/]"
                break
        # Append the choice character to the final line
        line += choice

    # Print in color of the color flag is true
    if args.color:
        printc(line)
    else:
        print(line)

end = time.time()  # End time for stats

info = (
    f"Original image scale: {original_size}\n"
    f"Downscale percentage: {round(scale * 100, 4)}\n"
    f"Final image scale: {new_size}\n"
    f"Unique chars used: {len(set(final_string))}\n"
    f"Duration: {round(end - start, 4)} second(s)"
)

printc(Align(Panel(info, title="Stats", expand=False), "center"))
