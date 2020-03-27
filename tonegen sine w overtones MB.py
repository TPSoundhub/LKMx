# Tonegen sine w overtones MB.py
#
# Programme that generates tones from sine waves for frequencies corresponding to musical scale from A0 to G7.
# Tones generated with 4 harmonics (overtones).
# Tones are then mapped to Micobit inputs. 7 key input from up till 7 Microbits so it can be used as a 'piano'.
# The microBits can convert any sensor input to 7 keys that are sent to this program.
#
# Revision 0.2 - 23Jan2020 - Knud Funch, Soundhub danmark - LYDKit til undevisningbrug - Region MidtJylland
# To be used as input for Workshop 19/2-2020 with teachers as preparation for debate on coupling to Physics/Math class
#
# To be run from within Thonny IDE on both PC and PI.
# As precondition the following libraries needs to be included in IDE - That is to be installed via TOOLS/MANAGE PACKAGES
# from within Thonny.
#
#         - numpy
#         - matplotlib
#         - scipy
#         - pygame - which already should be in place due to project 2019
#
# The part mapping tones to MicroBit input is identical to the twin program "Tonegen w sample MB.py"
#
# To generate sound (sine waves) and map them to Keyboard keys and play them pygame and numpy libraries are imported
#
#

import pygame
import numpy as np
import serial

# Frequencies for 7 octaves wo sharps - from A0 to G7 included - in all 49 notes
# a equal tempered scale with 440 as 'kammer tonen' se https://pages.mtu.edu/~suits/scales.html
# only the 'white' on keyboard/piano - that is the common western 7-note (heptatonic) scale see
# https://pages.mtu.edu/~suits/west_scales.html
#
frequency = [     # node and index/position in table/array
27.50,            # A0 - pos 0 --- 1  Start as deep as on grand piano
30.87,            # B0 - pos 1
32.70,            # C1 - pos 2
36.71,            # D1 - pos 3
41.20,            # E1 - pos 4
43.65,            # F1 - pos 5
49.00,            # G1 - pos 6
55.00,            # A1 - pos 7 --- 2
61.74,            # B1 - pos 8
65.41,            # C2 - pos 9
73.42,            # D2 - pos 10
82.41,            # E2 - pos 11
87.31,            # F2 - pos 12
98.00,            # G2 - pos 13
110.00,           # A2 - pos 14 --- 3
123.47,           # B2 - pos 15
130.81,           # C3 - pos 16
146.83,           # D3 - pos 17
164.81,           # E3 - pos 18
174.61,           # F3 - pos 19
196.00,           # G3 - pos 20
220.00,           # A3 - pos 21 --- 4
246.94,           # B3 - pos 22
261.63,           # C4 - pos 23
293.66,           # D4 - pos 24
329.63,           # E4 - pos 25
349.23,           # F4 - pos 26
392.00,           # G4 - pos 27
440.00,           # A4 - pos 28 --- 5 kammertonen - concert pitch - 
493.88,           # B4 - pos 29
523.25,           # C5 - pos 30
587.33,           # D5 - pos 31
659.25,           # E5 - pos 32
698.46,           # F5 - pos 33
783.99,           # G5 - pos 34
880.00,           # A5 - pos 35 --- 6
987.77,           # B5 - pos 36
1046.50,          # C6 - pos 37
1174.66,          # D6 - pos 38
1318.51,          # E6 - pos 39
1396.91,          # F6 - pos 40
1567.98,          # G6 - pos 41
1760.00,          # A6 - pos 42 --- 7
1975.53,          # B6 - pos 43
2093.00,          # C7 - pos 44
2349.32,          # D7 - pos 45
2637.02,          # E7 - pos 46
2793.83,          # F7 - pos 47
3135.96           # G7 - pos 48   # on grand piano 3 more/higher ones are included plus the sharps
]

#
# inputs (called keys even though we use it in a broader sence when taking inputs from different MB's
# They are identified as strings.
#
# Can also be used with keys from the keyboard when using pygame keyboard input.
# So in table below you map 49 inputs to specific tones that later are connected to the frequencies above 
# Key as first digit and second is the group number from 1 to 7
#
#
keys = [
'11',             # pos 0  - related to A0 in frequency --- 1
'21',             # pos 1  - related to B0 in frequency
'31',             # pos 2  - related to C1 in frequency
'41',             # pos 3  - related to D1 in frequency
'51',             # pos 4  - related to E1 in frequency
'61',             # pos 5  - related to F1 in frequency
'71',             # pos 6  - related to G1 in frequency
'12',             # pos 7  - related to A1 in frequency --- 2
'22',             # pos 8  - related to B1 in frequency
'32',             # pos 9  - related to C2 in frequency
'42',             # pos 10 - related to D2 in frequency
'52',             # pos 11 - related to E2 in frequency
'62',             # pos 12 - related to F2 in frequency
'72',             # pos 12 - related to G2 in frequency
'13',             # pos 14 - related to A2 in frequency --- 3
'23',             # pos 15 - related to B2 in frequency
'33',             # pos 16 - related to C3 in frequency
'43',             # pos 17 - related to D3 in frequency
'53',             # pos 18 - related to E3 in frequency
'63',             # pos 19 - related to F3 in frequency
'73',             # pos 20 - related to G3 in frequency
'14',             # pos 21 - related to A3 in frequency --- 4
'24',             # pos 22 - related to B3 in frequency
'34',             # pos 23 - related to C4 in frequency
'44',             # pos 24 - related to D4 in frequency
'54',             # pos 25 - related to E4 in frequency
'64',             # pos 26 - related to F4 in frequency
'74',             # pos 27 - related to G4 in frequency
'15',             # pos 28 - related to A4 in frequency --- 5
'25',             # pos 29 - related to B4 in frequency
'35',             # pos 30 - related to C5 in frequency
'45',             # pos 31 - related to D5 in frequency
'55',             # pos 32 - related to E5 in frequency
'65',             # pos 33 - related to F5 in frequency
'75',             # pos 34 - related to G5 in frequency
'16',             # pos 35 - related to A5 in frequency --- 6
'26',             # pos 36 - related to B5 in frequency
'36',             # pos 37 - related to C6 in frequency
'46',             # pos 38 - related to D6 in frequency
'56',             # pos 39 - related to E6 in frequency
'66',             # pos 40 - related to F6 in frequency
'76',             # pos 41 - related to G6 in frequency
'17',             # pos 42 - related to A6 in frequency --- 7
'27',             # pos 43 - related to B6 in frequency
'37',             # pos 44 - related to C7 in frequency
'47',             # pos 45 - related to D7 in frequency
'57',             # pos 46 - related to E7 in frequency
'67',             # pos 47 - related to F7 in frequency
'77'              # pos 48 - related to G7 in frequency
]

#
# Names of up till 7 micro bits each giving 7 inputs that are mapped to the 7 octaves each with 7 notes
# Names are 10 chars long
#

mb_grp_names = [
#0123456789
"          ",  # group 1
"MB 7Key2  ",  # group 2
"MBLightk 1",  # group 3
"MB Magkey1",  # group 4
"MB 7Key1  ",  # group 5
"MB Magkey2",  # group 6
"          "   # group 7
]

 
#
# Tone generation part
#

sf = 44100 # Sampling frequence! samples pr second. twice the highest frq you want to reproduce as minimum (nyquist)
d = 0.5      # duration - time in second, arbitrary length of tone Use integer value. Ought to be calculated for each so endng in zera as start so loops can be made wo ticks


# Generate a numpy array with a sine according to frequency and max amplity given as arguments 
def generate_pure_tone(freq,amp_max):  # for now phase is zero could be added to test phase issues....
    # make table t with sf samples pr. sec for duration d with 1/sf as spacing - sf and d is given as global constants for keeping it aligned
    t = np.arange(0,d,1/sf)
    # put sine wave with the frequency freq into table t
    x = np.sin(2*np.pi*freq*t)
    # Scale input from -/+1 to +/-amp_scale and within 16 bit integers.
    x = (x*amp_max).astype(np.int16)
    x = np.dstack((x,x))[0]  # Same in both left and right channel - to be used on PI where mono can not be played in mixer
    return x

def generate_tone_with_overtones(fundamental_freq,amp_max,amp_max_1,amp_max_2,amp_max_3):  #overtones is here harmonic - Skal vi have 4 for at indeholde 2 oktaver ??
    amp_combined = amp_max+amp_max_1+amp_max_2+amp_max_3
    if amp_combined>=65536:  # make sure to keep inside int 16 limit - should be done in smarter way!!
        print("can not keep inside int16")
        raise KeyboardInterrupt
    if fundamental_freq>sf/2: fundamental_freq=sf/2 # make sure we keep it within limits
    f  = generate_pure_tone(fundamental_freq,amp_max)
    # if's below a crude way to secure we do not get tones with freq more than twice the sampling rate
    if fundamental_freq*2<sf/2:
        o1 = generate_pure_tone(fundamental_freq*2,amp_max_1)
        if fundamental_freq*3<sf/2:
            o2 = generate_pure_tone(fundamental_freq*3,amp_max_2)
            if fundamental_freq*4<sf/2:
                o3 = generate_pure_tone(fundamental_freq*4,amp_max_3)
                x=f+o1+o2+o3
            else: x=f+o1+o2
        else: x=f+o1
    else: x=f
   
    return x

#
#
# Generate sound array for all nodes that are to be mapped to keys on keyboard
# sound array does this with the arguments the mixer is initialised with
# Here 2 - means stereo
#
pygame.mixer.init(sf, -16, 2)

range_of_tones = range(0, len(frequency))
sound_table = [generate_tone_with_overtones(frequency[i],6000,3000,1500,750) for i in range_of_tones]
generated_sounds = map(pygame.sndarray.make_sound, sound_table)

sounds = map(pygame.sndarray.make_sound, generated_sounds)

# Map keys and sounds together in dictionaty for easy and fast look up
key_sound = dict(zip(keys, sounds))

# is playing table for checking sound playing pr key - and initialise all to not playing here : "0"
gr_is_playing = ["0","0","0","0","0","0","0"]


# ON PI:
# ser = serial.Serial(baudrate = 115200, port = "/dev/ttyACM0")
# ON PC
ser = serial.Serial(baudrate = 115200, port = "COM8")

def receive_char():
    microbitdata = str(ser.readline())
    key=microbitdata[2]
    sender=microbitdata[3:13]
    print(sender)
    gr = "0" 
    if   sender == mb_grp_names[0]: gr = "1"  # could be done smarter by fixed table lookup dict..
    elif sender == mb_grp_names[1]: gr = "2"
    elif sender == mb_grp_names[2]: gr = "3"
    elif sender == mb_grp_names[3]: gr = "4"
    elif sender == mb_grp_names[4]: gr = "5"
    elif sender == mb_grp_names[5]: gr = "6"
    elif sender == mb_grp_names[6]: gr = "7"
    key = key+gr
    return key, gr


def play_note(key,is_playing):
    print("play note: ",key,is_playing)
    if key != is_playing:
        if is_playing in keys: key_sound[is_playing].stop()
        is_playing = "0"

    if key in keys:
        key_sound[key].set_volume(1.0)
        key_sound[key].play(-1) 
        is_playing = key
        
    return is_playing


while True:
   
    mb_key,mb = receive_char()
    print(mb_key, " From: ",mb)
    
    if   mb == "1": gr_is_playing[0] = play_note(mb_key,gr_is_playing[0])
    elif mb == "2": gr_is_playing[1] = play_note(mb_key,gr_is_playing[1])
    elif mb == "3": gr_is_playing[2] = play_note(mb_key,gr_is_playing[2])
    elif mb == "4": gr_is_playing[3] = play_note(mb_key,gr_is_playing[3])
    elif mb == "5": gr_is_playing[4] = play_note(mb_key,gr_is_playing[4])
    elif mb == "6": gr_is_playing[5] = play_note(mb_key,gr_is_playing[5])
    elif mb == "7": gr_is_playing[6] = play_note(mb_key,gr_is_playing[6])
            