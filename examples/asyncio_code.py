import board
import time
import neopixel
import asyncio

import msgpack
import io

CUBEPIN = board.GP28
NUM_PIXELS = 3 * 3 * 3

pixels = neopixel.NeoPixel(CUBEPIN, NUM_PIXELS, brightness=1)
status = neopixel.NeoPixel(board.NEOPIXEL, 1)
status.fill(0)

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.helper import PixelMap
from adafruit_led_animation.color import PURPLE, AMBER, JADE

map1_1 = PixelMap(pixels, [(x,) for x in range(NUM_PIXELS//2)], individual_pixels=True)
map1_2 = PixelMap(pixels, [(x,) for x in range(NUM_PIXELS//2,NUM_PIXELS)], individual_pixels=True)
gchase = Chase(map1_1, speed=0.03, size=3, spacing=7, color=AMBER)
gsparkle = Sparkle(map1_2, speed=0.12, color=PURPLE, num_sparkles=4)
group1 = AnimationGroup(gchase, gsparkle)

rainbow = Rainbow(pixels, speed=0.1)
chase = Chase(pixels, speed=0.04, size=3, spacing=7, color=AMBER)
comet = Comet(pixels, speed=0.02, color=JADE, tail_length=10, bounce=True)
sparkle = Sparkle(pixels, speed=0.5, color=PURPLE, num_sparkles=3)
spalse = SparklePulse(pixels, speed=0.5, color=(0,0,255))
rainkle = RainbowSparkle(pixels, speed=0.5, num_sparkles=4)

animations = AnimationSequence(comet, chase)
group = AnimationGroup(comet, chase)
rainkleGroup = AnimationGroup(rainbow, sparkle)

allSequence = AnimationSequence(group1, group, sparkle, spalse, rainkle, chase, comet)
sparkleSequence = AnimationSequence(sparkle, spalse, rainkle)
sequence = sparkleSequence

async def advance():
    while True:
        await asyncio.sleep(20)
        #pixels.fill(0)
        #pixels.show()
        #sequence.next()

async def main():
    asyncio.create_task(advance())
    while True:
        sequence.animate()
        await asyncio.sleep(0.01)

async def test_msgpack():
    obj = [0b1000, 0b1000_0000, 0b1000_0000_0000_0000, 0.55]
    st = io.BytesIO()
    msgpack.pack(obj, st)
    s2 = [
        io.BytesIO(b'\x91\xcc\xc8'),
        io.BytesIO(b'\x93\x08\xcc\x80\xcd\x80\x00'),
        io.BytesIO(b'\x94\x08\xcc\x80\xcd\x80\x00\xcb?\xe1\x99\x99\x99\x99\x99\x9a')
    ]
    while True:
        print(obj)
        print("-", st.getvalue())
        for so in s2:
            try:
                so.seek(0)
                print("-", msgpack.unpack(so))
            except NotImplementedError as er:
                print("- Not Implemented:", er)
        await asyncio.sleep(5)

asyncio.run(main())
