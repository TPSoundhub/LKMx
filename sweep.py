# Knud SHD 24-september 20 - "sweep.py"  - tilføjes til sweep progression som en aha til sidst ...
# Smooth sweep med power of x i sinus funktionen.
#
import numpy as np
import pygame
import matplotlib.pyplot as plt

#
# Globale konstanter
#
SAMPLERATE    = 44100
AMP           = 8000
FREQ_START    = 10          # Denne gang som start freq der i alle datapunkter bliver opløftet til POWER så den skal være LILLE. 10 opløftet til 2 er 100    
DURATION      = 10          # Samlet længde af sweep. Gør den evt mindre hvis POWER sættes højere end 2. Men OK at prøve.. 'Sjove effekter'
POWER         = 2           # Det som alle datapunkter opløftes til inden sinus funktionen anvendes på dem Prøv bare med 3 og 4 - OG 1 for den sags skyld

pygame.mixer.init(SAMPLERATE, -16, 1)

x1  = np.linspace(0,DURATION*FREQ_START*2*np.pi,DURATION*SAMPLERATE,endpoint=False)
x2  = np.arange(0,DURATION*SAMPLERATE)
x2.fill(POWER)

x3 = np.power(x1,x2)  # Alle datapunkter i x1 bliver opløftet til værdi i x2 på samme position (alle værdier i x2 indeholder POWER som værdi)

t1 = (np.sin(x3)*AMP).astype(np.int16)

#
# Afspil lyden 
#
sound = pygame.sndarray.make_sound(t1)   
sound.play()                            