# Tonegen sine w overtones KB.py
#
# Programme that generates tones from sine waves for frequencies corresponding to musical scale from A0 to G7.
# Tones generated with 4 harmonics (overtones).
# Tones are then mapped to Keyboard so it can be used as a 'piano' Other sensors to be used as input later on.
#
# Revision 0.4 - 20Jan2020 - Knud Funch, Soundhub danmark - LYDKit til undevisningbrug - Region MidtJylland
# To be used as input for Workshop 19/2-2020 with teachers as preparation for debate on coupling to Physics/Math class
#
# To be run from within Thonny IDE on both PC and PI.
# As precondition the following libraries needs to be included in IDE - That is to be installed via TOOLS/MANAGE PACKAGES
# from within Thonny.
#
#         - numpy
#         - matplotliob
#         - scipy
#         - pygame - which already should be in place due to project 2019
#
# The part mapping tones to keyboard and plot's a sample tone is identical to the twin program "Tonegen w sample KB.py"
# both located on GITHUB
#
# To generate sound (sine waves) and map them to Keyboard keys and play them pygame and numpy libraries are imported
#
# When running the program first a plot is made, and you must quit that by pressing the X in upper right corner before
# you get to the piano part - able to play tones by pressing keys on the keyboard.
#
# You must have focus in the small 'black' window to get keys into this program.
#  
# To shut down program and get window cleared you must either press ESC or the X in upper right corner.


import pygame
import numpy as np

# To make a plot of tone and spectrum the below is imported.
# if you remove test plot code then you do not need to improt these hence do not need them in environment
# that is to include package via Tools in Thonny
#
import matplotlib.pyplot as plt
from scipy.fftpack import fft,fftfreq

# Frequencies for 7 octaves wo sharps - from A0 to G7 included - in all 49 notes
#
frequency = [     # node and index/position in table/array
27.50,            # A0 - pos 0
30.87,            # B0 - pos 1
32.70,            # C1 - pos 2
36.71,            # D1 - pos 3
41.20,            # E1 - pos 4
43.65,            # F1 - pos 5
49.00,            # G1 - pos 6
55.00,            # A1 - pos 7
61.74,            # B1 - pos 8
65.41,            # C2 - pos 9
73.42,            # D2 - pos 10
82.41,            # E2 - pos 11
87.31,            # F2 - pos 12
98.00,            # G2 - pos 13
110.00,           # A2 - pos 14
123.47,           # B2 - pos 15
130.81,           # C3 - pos 16
146.83,           # D3 - pos 17
164.81,           # E3 - pos 18
174.61,           # F3 - pos 19
196.00,           # G3 - pos 20
220.00,           # A3 - pos 21
246.94,           # B3 - pos 22
261.63,           # C4 - pos 23
293.66,           # D4 - pos 24
329.63,           # E4 - pos 25
349.23,           # F4 - pos 26
392.00,           # G4 - pos 27
440.00,           # A4 - pos 28
493.88,           # B4 - pos 29
523.25,           # C5 - pos 30
587.33,           # D5 - pos 31
659.25,           # E5 - pos 32
698.46,           # F5 - pos 33
783.99,           # G5 - pos 34
880.00,           # A5 - pos 35
987.77,           # B5 - pos 36
1046.50,          # C6 - pos 37
1174.66,          # D6 - pos 38
1318.51,          # E6 - pos 39
1396.91,          # F6 - pos 40
1567.98,          # G6 - pos 41
1760.00,          # A6 - pos 42
1975.53,          # B6 - pos 43
2093.00,          # C7 - pos 44
2349.32,          # D7 - pos 45
2637.02,          # E7 - pos 46
2793.83,          # F7 - pos 47
3135.96           # G7 - pos 48
]

sf = 44100 # Sampling frequence! samples pr second. twice the highest frq you want to reproduce as minimum (nyquist)
d = 0.5      # duration - time in second, arbitrary length of tone Use integer value. Ought to be calculated for each so endng in zera as start so loops can be made wo ticks


# A rough test of plotting. Not needed for generating sound!
# Needs more work for better readability - get axis correct etc.
def plot_tone_and_spectrum(x):  # more work to make it more readable - axis time in ms etc...! dB scale for intensity ....
    plt.subplot(121)
    plt.axis([0,int(sf/50),-20000,20000])   # one 50th of a sec (20ms) samples in time and +/- 20000 in amp
    plt.plot(x)
    FFT = abs(fft(x))
    freqs = fftfreq(x.size, 1/sf)
    plt.subplot(122)
    plt.axis([0,2000,5,10])            # only positive below 2000 Hz and amp above 5 in log10
    plt.plot(freqs,np.log10(FFT))
    plt.show()

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
# Here 2 - means mono
#
pygame.mixer.init(sf, -16, 2)

range_of_tones = range(0, len(frequency))
sound_table = [generate_tone_with_overtones(frequency[i],6000,3000,1500,750) for i in range_of_tones]
generated_sounds = map(pygame.sndarray.make_sound, sound_table)

# Window needed for getting keyboard input to the program. (ESC stops and close window)
screen = pygame.display.set_mode((150, 150))

keys=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', 'q', 'w', 'e', 'r',
      't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j',
      'k', 'l', ';', "'",'<', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'right shift',
      'right ctrl', 'left', 'down', 'up', 'right']

sounds = map(pygame.sndarray.make_sound, generated_sounds)

# Map keys and sounds together in dictionaty for easy and fast look up
key_sound = dict(zip(keys, sounds))
# is playing table for checking sound playing pr key - and initialise all to False (not playing)
is_playing = {k: False for k in keys}


# to illustrate a plot lets plot one of the generated tones (kammertonen) and the spectrum - need more work
# only takes one channel of the stereo sound 2 channels.
# YOU must quit the plot by X'ing the plot window before getting to the playback mode!!!
sound_to_plot = sound_table[28][:,0]
plot_tone_and_spectrum(sound_to_plot)

# Take KB input events and play coresponising tone - you have a 'keyboard piano now so play along ;-)
run = True
while run:
    event = pygame.event.wait()

    if event.type == pygame.QUIT: run = False  # X'ed in window
    else:
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)
            print(key)
            if event.key == pygame.K_ESCAPE: run = False
            if (event.type == pygame.KEYDOWN) and (key in key_sound.keys()) and (not is_playing[key]):
                key_sound[key].play(-1)  # -1 means plays until stopped. ticks because not aligned start/stop values! Need trimming!!
                is_playing[key] = True
            elif event.type == pygame.KEYUP and key in key_sound.keys():
                key_sound[key].stop()
                is_playing[key] = False

# When running is stopped
pygame.quit()  # clean up - removes the window for focus/KB input
            