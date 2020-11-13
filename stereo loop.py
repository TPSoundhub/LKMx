# "stereo loop.py"
#
# Loop eksempel med løbende plot af signal  - 
#
# Knud - SHD - 13 nov. 2020 - Som ex opsamling efter observation i HH.
#
# Ex til inspiration når der skal rulles på Modul 2.
# Der er ticks mellem lydene og sweep er ikke så 'smooth' - det kræver noget andet,hvis det skal ske - så kun som illustration.
# For at lave en smooth sweep vil man lave een lyd der øges i freq i een tabel og konvertere til en lyd der afspilles.
#
# andre forbedringsmuligheder: Tabel med freq den løber igennem for at kunne lave flere 'sjove' kombinationer ??
# Hvordan får jeg overtoner med i denne? Eller skal det bare være et program for sig selv. Skal evt. fjerne ONLY_ONE_SOUNd
# - dvs muligheden for at blande flere i denne... Giver nok ikke rigtig noget andet end at det forvirrer.
#
import numpy as np
import pygame
import matplotlib.pyplot as plt
from scipy.fftpack import fft,fftfreq      # scipy pakken skal med i pakken aht FFT. Fjernes den del kan den udelades. (Tools - manage packages)
#
# Globale konstanter
#
SAMPLERATE     = 44100
DURATION       = 1.0       # SKAL være >= 0.2 for at koden nedenfor fungerer mht delay/pauser. Angives i sekunder. Eksperimenteres med stødtoner så sæt evt til 1.0
MAX_AMP        = 15000
MAX_FREQ       = 3000      # Max freq til plot i FFT og i loop (while løkken)
TIME_TO_PLOT   = 10        # i ms
PLOT           = True
ONLY_ONE_CURVE = True
ONLY_ONE_FFT   = False
ONLY_ONE_SOUND = True
SPEED_OF_SOUND = 343       # m/s i luft ved 20 grader celsius
DELTA          = 0         # DELTA er forskel på frekvens i højre og venstre. hvis > 0 opleves stødtoner. 
STEP_IN_SWEEP  = 100       # i Hz - den forskel der er mellem freq i while loop i sweep
#
# Globale variable
#
freq_left  = 50
freq_right = freq_left+DELTA      # Lad evt frekvensen i højre være nogle få hertz større end i venstre for at opleve stødtoner/interferens. Sæt DELTA>0
amp        = 5000
#
# initialiseringer med hensyn til plot og figur
#
if PLOT:
    plt.ion()                          # sætter plot funktionen til at tegne på skærm direkte så hvert kald får effekt med det samme
                                       # Hvis den ikke er kaldt så laver man tegning/plot i baggrunden og den bliver først vist når man kalder plt.show()
    plt.figure(figsize=[14,7])         # Laver plot vindue lidt større end default som er [6.4,4.8]
    left_plot = plt.subplot(411)
    plt.title("Venstre "+str(TIME_TO_PLOT)+" ms udsnit\nDet der er i plot bevæger sig ca. "+str(SPEED_OF_SOUND*TIME_TO_PLOT/1000)+" meter i luft ved 20 grader celsius")         
    plt.ylabel("amp")
    plt.axis([0,TIME_TO_PLOT,-MAX_AMP,MAX_AMP])    # Plot 0-TIME_TO_PLOT ms og sæt (amplitude) y-aksen til at gå fra - til + MAX_AMP

    right_plot = plt.subplot(412)
    plt.title("Højre "+str(TIME_TO_PLOT)+" ms udsnit")           
    plt.ylabel("amp")
    plt.axis([0,TIME_TO_PLOT,-MAX_AMP,MAX_AMP])    

    combined_plot = plt.subplot(413)
    plt.title("højre plus venstre")    
    plt.ylabel("amp")
    if DELTA==0:
        plt.axis([0,TIME_TO_PLOT,-MAX_AMP,MAX_AMP])       # Når DELTA er nul så bruges samme tidsvindue for sammansat signal som for H/V 
    else:
        plt.axis([0,DURATION*1000,-MAX_AMP,MAX_AMP])      # MEN ved stødtoner er det mere interessant at se det på længere tid
                                                          # - helst med DURATION sat til 1 sek. Hvorfor?
    
    fft_plot = plt.subplot(414)
    plt.title("FFT af højre+venstre")    
    plt.xlabel("Frekvens i Hz")  
    plt.axis([0,MAX_FREQ,5,10])                           # plot frekvenser under MAX_FREQ og amp over 5 i log10

#
# initialiser pygame mixer til stereo og 16 bit (signed) så det matcher cross platform driver og lyd kort PC,MAC og PI/Beocreate
#
pygame.mixer.init(SAMPLERATE, -16, 2)

time = np.linspace(0,1000*DURATION,DURATION*SAMPLERATE)   # alternativ x-akse med tid i millisekunder (ms) fremfor radianer/vinkelværdier
    
while freq_left < MAX_FREQ:
    #
    # Laver en tabel for hhv højre og venstre med DURATION*freq antal perioder (omgange i enhedscirklen/bølgelængder)
    # og delt op i DURATION*SAMPLERATE antal datapunkter med sin(x)*amp som værdi og i 16 signed heltal.
    # Man kan lave sin() funktion på hele tabel på een gang. dvs alle værdier i tabel i et hug!
    # Den sidste linie kombinerer de 2 tabeller til een som kan bruges i make_sound. (copy for at få det lagt ud i række i memory)
    #
    signal_left  = (np.sin(np.linspace(0,DURATION*freq_left*2*np.pi,DURATION*SAMPLERATE,endpoint=False))*amp).astype(np.int16)
    signal_right = (np.sin(np.linspace(0,DURATION*freq_right*2*np.pi,DURATION*SAMPLERATE,endpoint=False))*amp).astype(np.int16)
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
    # Hvis konstanten PLOT er True så fylder vi figuren med plot af den lyd som spiller
    #
    if PLOT: 
        left_curve,     = left_plot.plot(time,signal.T[0])                
        right_curve,    = right_plot.plot(time,signal.T[1])                
        combined        = signal.T[0]+signal.T[1]
        combined_curve, = combined_plot.plot(time,combined)
        FFT             = abs(fft(combined))
        freqs           = fftfreq(combined.size, 1/SAMPLERATE)
        fft_curve,      = fft_plot.plot(freqs,np.log10(FFT))
 
    #
    # Aht at få tegnet plot færdigt inden en pause bruges plt.pause hvis vi laver plot ellers pygame delay
    #
    if PLOT: plt.pause(DURATION-0.1)
    else: pygame.time.delay(500)
    #
    # Med konstanterne kan man styre om der kun tegnes een kurve for den lyd der spiller eller om de tegnes oveni hinanden.
    # Nedenfor slettes gamle kurver hvis ONLY_ONE_CURVE er True. FFT får særstatus og kan styres individuelt.
    #
    if PLOT and ONLY_ONE_CURVE:
        left_plot.lines.remove(left_curve)          
        right_plot.lines.remove(right_curve)
        combined_plot.lines.remove(combined_curve)
        if ONLY_ONE_FFT: fft_plot.lines.remove(fft_curve) 
        plt.draw()  # Med plt.ion() i starten så opdateres fig. løbende, men når noget fjernes skal der laves et kald til draw for at få det effektueret i vinduet

    if ONLY_ONE_SOUND: sound.stop()                    # Stop lyden hvis de ikke skal blandes

    #
    # I dette eksempel lader vi frekvenserne i både højre og venstre vokse med STEP_IN_SWEEP for hver tur i while løkken.
    #
    freq_left+=STEP_IN_SWEEP
    freq_right=freq_left+DELTA     # ved stødtoner så lad højre få en delta > 0 - Den kan evt gøres variable i loop hvis I synes

if PLOT: plt.waitforbuttonpress()  # vent på mus klik eller taste tryk i vinduet med figur inden program afsluttes. 
pygame.mixer.quit()                # oprydning i mixer
plt.close()                        # oprydning i plot


