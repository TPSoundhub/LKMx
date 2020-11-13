# "sweep and plot.py"
#
# Loop eksempel med løbende plot af signal
#
# Knud - SHD - 13 nov. 2020 Version 0.1 - En første simplificering mod forløb i Skanderborg 
#
# Ved at ændre i konstanter kan man bruge den til lidt forskelligt.
#
# Når pogram er lsut skal der blot klikkes indenfor plot vinduet for at få det fjernet og ryddet op
# Pt kommer der en række fejlmeldinger hvis man klikker i 'X' i vinduet både undervejs og til slut... (
#  Brug stop stop
#
import numpy as np
import pygame
import matplotlib.pyplot as plt

#
# Globale konstanter
#
SAMPLERATE     = 44100
DURATION       = 1.0       # SKAL være >= 0.2 for at koden nedenfor fungerer mht delay/pauser. Angives i sekunder. OK med decimaltal
MAX_AMP        = 15000
MAX_FREQ       = 4000      # Max freq i Hz
TIME_TO_PLOT   = 10        # i ms
ONLY_ONE_CURVE = True
SPEED_OF_SOUND = 343       # m/s i luft ved 20 grader celsius
DELTA          = 0         # DELTA er forskel på frekvens i højre og venstre. hvis > 0 opleves stødtoner. 
STEP_IN_SWEEP  = 100       # i Hz - den forskel der er mellem freq i while loop i sweep
AMP_LEFT       = 5000
AMP_RIGHT      = 5000
#
# Globale variable - Start frekvens i de 2 kanaler.
#
freq_left  = 100
freq_right = freq_left+DELTA      # Lad evt frekvensen i højre være nogle få hertz større end i venstre for at opleve stødtoner/interferens. Sæt DELTA>0

#
# initialiseringer med hensyn til plot og figur
#
plt.ion()                          # sætter plot funktionen til at tegne på skærm direkte så hvert kald får effekt med det samme
                                   # Hvis den ikke er kaldt så laver man tegning/plot i baggrunden og den bliver først vist når man kalder plt.show()
plt.figure(figsize=[14,7])         # Laver plot vindue lidt større end default som er [6.4,4.8]
left_plot = plt.subplot(311)
plt.title("Venstre "+str(TIME_TO_PLOT)+" ms udsnit\nDet der er i plot bevæger sig ca. "+str(SPEED_OF_SOUND*TIME_TO_PLOT/1000)+" meter i luft ved 20 grader celsius")         
plt.ylabel("amp")
plt.axis([0,TIME_TO_PLOT,-MAX_AMP,MAX_AMP])    # Plot 0-TIME_TO_PLOT ms og sæt (amplitude) y-aksen til at gå fra - til + MAX_AMP

right_plot = plt.subplot(312)
plt.title("Højre "+str(TIME_TO_PLOT)+" ms udsnit")           
plt.ylabel("amp")
plt.axis([0,TIME_TO_PLOT,-MAX_AMP,MAX_AMP])    

combined_plot = plt.subplot(313)
plt.title("højre plus venstre")    
plt.ylabel("amp")
if DELTA==0:
    plt.axis([0,TIME_TO_PLOT,-MAX_AMP,MAX_AMP])       # Når DELTA er nul så bruges samme tidsvindue for sammansat signal som for H/V 
else:
    plt.axis([0,DURATION*1000,-MAX_AMP,MAX_AMP])      # MEN ved stødtoner er det mere interessant at se det over 1 sekund
                                                          

#
# initialiser pygame mixer til stereo og 16 bit (signed) så det matcher cross platform driver og lyd kort PC,MAC og PI/Beocreate
#
pygame.mixer.init(SAMPLERATE, -16, 2)

time = np.linspace(0,1000*DURATION,int(DURATION*SAMPLERATE))   # alternativ x-akse med tid i millisekunder (ms) fremfor radianer/vinkelværdier
    
while freq_left < MAX_FREQ:
    #
    # Laver en tabel for hhv højre og venstre med DURATION*freq antal perioder (omgange i enhedscirklen/bølgelængder)
    # og delt op i DURATION*SAMPLERATE antal datapunkter med sin(x)*amp som værdi og i 16 signed heltal.
    # Man kan lave sin() funktion på hele tabel på een gang. dvs alle værdier i tabel i et hug!
    # Den sidste linie kombinerer de 2 tabeller til een som kan bruges i make_sound. (copy for at få det lagt ud i række i memory)
    #
    signal_left  = (np.sin(np.linspace(0,DURATION*freq_left*2*np.pi,int(DURATION*SAMPLERATE),endpoint=False))*AMP_LEFT).astype(np.int16)
    signal_right = (np.sin(np.linspace(0,DURATION*freq_right*2*np.pi,int(DURATION*SAMPLERATE),endpoint=False))*AMP_RIGHT).astype(np.int16)
    signal = np.array((signal_left,signal_right)).T.copy()
    #
    # Bølge længden = hastighed/frekvens = (m/s divideret med 1/s) = meter (ganges med 100 så det er i cm) og med round(x,2) for at give 2 decimaler
    # Udskrives i shell til information. Både venstre og højre udskrives, hvilket er lidt overflødigt når det er samme freq i begge, men
    #  - Det kan man jo så overveje at eksperimentere med...
    #  - Tilsvarende kan set så være at man skal ekspeirmentere med længden af udsnit man plotter for det kombinerede signal..
    #
    blv = round(SPEED_OF_SOUND*100/freq_left,2)
    print("Venstre: Freq: "+str(freq_left)+"Hz. Bølgelængden: "+"%.2f" % blv+"cm.","Svingningstid: "+"%.4f" % (1000/freq_left),"ms.")
    blr = round(SPEED_OF_SOUND*100/freq_right,2)
    print("Højre: Freq:   "+str(freq_right)+"Hz. Bølgelængden: "+"%.2f" % blr+"cm.","Svingningstid: "+"%.4f" % (1000/freq_right),"ms.")
    print()
    #
    # Mixer kan håndtere at afspille 8 lyde samtidigt, men her lader vi den kun spille een ad gangen i et sweep. (Med ONLY_ONE_SOUND = True)
    # Man kan gemme reference til de enkelte lyde (lyd objekter) og starte/stoppe dem individuelt... Eksperimenter med det i senere udgave
    # Man hører kun de første 8 lyde i sweep når man sætter konstanten til True ;-) Så det er ikke så fedt.... Så bør man justere de andre
    # konstanter til sådan at man kun kommer rundt i loop 8 gange...
    #
    sound = pygame.sndarray.make_sound(signal)   
    sound.play(-1)                              
    #
    # Plot
    #
    left_curve,     = left_plot.plot(time,signal.T[0])                
    right_curve,    = right_plot.plot(time,signal.T[1])                
    combined        = signal.T[0]+signal.T[1]
    combined_curve, = combined_plot.plot(time,combined)
    #
    # For at få tegnet plot færdigt inden ny lyd bruges plt.pause 
    #
    plt.pause(DURATION-0.1)

    #
    # Med konstanterne kan man styre om der kun tegnes een kurve for den lyd der spiller eller om de tegnes oveni hinanden.
    # Nedenfor slettes gamle kurver hvis ONLY_ONE_CURVE er True. 
    #
    if ONLY_ONE_CURVE:
        left_plot.lines.remove(left_curve)          
        right_plot.lines.remove(right_curve)
        combined_plot.lines.remove(combined_curve)
        plt.draw()  # Med plt.ion() i starten så opdateres fig. løbende, men når noget fjernes skal der laves et kald til draw for at få det effektueret i vinduet

    sound.stop()                    # Stop lyden inden en ny laves så de ikke blandes

    #
    # I dette eksempel lader vi frekvenserne i både højre og venstre vokse med STEP_IN_SWEEP for hver tur i while løkken.
    #
    freq_left+=STEP_IN_SWEEP
    freq_right=freq_left+DELTA     # ved stødtoner så lad højre få en delta > 0 - Den kan evt gøres variable i loop hvis I synes

plt.waitforbuttonpress()     # vent på mus klik eller taste tryk i vinduet med figur inden program afsluttes. 
pygame.mixer.quit()          # oprydning i mixer
plt.close()                  # oprydning i plot


