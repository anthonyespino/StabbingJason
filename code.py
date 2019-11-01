import time
from adafruit_crickit import crickit
import board
import neopixel
import array
import math
from analogio import AnalogIn
from simpleio import map_range
import audioio
from adafruit_seesaw.neopixel import NeoPixel

num_pixels = 2  # Number of pixels driven from Crickit NeoPixel terminal
# Crickit NeoPixel
pixels = neopixel.NeoPixel(board.A1, num_pixels, brightness=0.3,
                           auto_write=False)
# Pixels
pixels.fill((0, 0, 0))
pixels.show()

# Light Sensor
analogin = AnalogIn(board.LIGHT)

# WAV File Play
f = open("robot1.wav", "rb")
robotsounds1 = audioio.WaveFile(f)

length = 8000 // 440
sine_wave = array.array("H", [0] * length)

for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / 18) * (2 ** 15) + 2 ** 15)

a = audioio.AudioOut(board.A0)

# Crickit NeoPixel
RED = (255, 0, 0)

while True:

    print(analogin.value)
    if analogin.value <= 2000:
        print("<=2000")
        crickit.servo_1.angle = 0
        for i in range(0, 2, 1):
            pixels[i] = (255, 0, 0)
        pixels.show()

        for angle in range(40, 179, 15):  # 0 - 180 degrees, 2 degrees at a time.
            crickit.servo_3.angle = angle
            time.sleep(0.01)

        for angle in range(179, 40, -15):  # 0 - 180 degrees, 2 degrees at a time.
            crickit.servo_3.angle = angle
            time.sleep(0.01)

    elif analogin.value > 4200:
        print(">4200")
        a.play(robotsounds1, loop = True)
        for i in range(0, 2, 1):
            pixels[i] = (50, 50, 50)
        crickit.servo_3.angle = 5

        for angle in range(0, 90, 3):  # 0 - 180 degrees, 2 degrees at a time.
            crickit.servo_1.angle = angle
            time.sleep(0.01)

        for angle in range(90, 15, -3):  # 0 - 180 degrees, 2 degrees at a time.
            crickit.servo_1.angle = angle
            time.sleep(0.01)

        pixels.show()
