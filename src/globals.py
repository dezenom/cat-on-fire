
from mytoolkit_pygame.radio import Radio
from pygame import mixer as mx
# globals
change_level = True
Current_level = 1

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

radio = Radio(songs,effects)
