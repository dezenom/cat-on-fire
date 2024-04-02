
from mytoolkit_pygame.radio import Radio
from pygame import mixer as mx
from time import time
# globals
change_level = True
Current_level = 3

# player globals
cool_on = True

# radio
sndd = mx.Sound
songs=[
    sndd("resources/sounds/firecat.mp3")
]

effects = {
    "hit":sndd("resources/sounds/hitHurt.wav"),
    "jump":sndd("resources/sounds/jump.wav")
}

effects["jump"].set_volume(0.3)

radio = Radio(songs,effects)

start_time = time()

# ^^^^^^^^^^^^^^^^^^^^^^ this should not be here just leave it tho
