# "numpy plt sound progression.py"
#
# Lidt kode eksempler som opfølgning på observation af brug af Lyd KIT i fysik/inofrmatik forløb på Herningsholm september 20
# Tænkt som input/inspiration til lærer
#
#  - Essensen i linie 63 til 83 for dem som vil have den korte version :-) Og bare 87 til 90 for den super utålmodige!
#
# Knud - SHD - 14 sept. 2020 - Inkluderes i notesbog..
#
# At betragte som noter/forbedringspunkter/reflektioner som kan bruges når der skal rulles på Modul 2.
# Hoved pointe er at få lavet kode som hænger bedre sammen med/kan forklares nemmere ud fra sammenhæng til matematik/fysik ifm sinus ..
# Forsøger med eksemplerne her at lave en fornuftig progression - tabel -> sin -> plt -> lyd
#
# En anden pointe er at få strammet op omkring navngivning i hele materialesættet. Det er ikke taget med her. Men i overskrifter:
#  - signal - lyd - mixer - monosignal - stereosignal - lyd kanaler i mixer - lydkanaler på lydkort etc.....
#

import numpy as np
import pygame
import matplotlib.pyplot as plt

sf = 44100       # Forbedring: - Brug mere sigende navne og store bogstaver for konstanter iht Python konvention
d = 2.0          # d for duration of signal

SAMPLERATE = 44100
DURATION   = 2

freq  = 440
freq2 = 1000     # til højre spor når vi når til stereo nedenfor (til sidst)
amp   = 10000

#-----------------------------------
# Basis array håndtering - Kør program/script og tast så variabel navn ind in shell og se array indhold direkte
# Default værdier i array/tabel er float 64 så det behøver man ikke at specificere!
#
t1 = np.arange(0,3)             # tabel med en dim med 3 værdier i en dimension [a1,b1,c1]
                                # - Her [0,1,2] start med 0 slut med værdien inden 3 (3 ikke inkluderet) med default step på 1
                                # - Kan sætte step til andet gennem optional argument til funktionen
                                # - Se: https://numpy.org/doc/stable/reference/generated/numpy.arange.html 
t2 = np.linspace(5,7,3)         # tabel med 3 værdier (bestemt med argument/parameter nummer 3) med lige meget afstand mellem værdierne (spasering)
                                # - her [5,6,7] da startværdi er sat til 5 og slut til 7 (som inkluderes default) med lige meget spasering mellem værdierne.
                                # - Se: https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
t3 = np.array((t1,t2))          # tabel med 2 dimensioner sammensat af de 2 endimensionelle tabeller [[a1,b1,c1],[a2,b2,c2]]
t4 = t3.T                       # Transpose - vender dimensionen på tabellen. så der bliver par med [[a1,a2],[b1,b2],[c1,c2]] Det som sndarray vil have!
                                #  - når der er tale om et stereo signal!
#
# ------------------------------------------------------------------------------------
#
# Som brugt i min kode pt biblioteker i version 0.4 fra april 2020:   (Som der er forbedringsforslag til efterfølgende)
#

t5 = np.arange(0,d,1/sf)   # tabel med en dim [a,b,c]    Værdier fra 0 til d med spacering 1/sf  - Savner sammenhæng med enhedscirklen!

# Fyld hele tabel med værdier fra en funktion på een gang,
# og konverter til 16 bit integer for hele tabel på en gang
# - (aht driver der genererer et signal til lydkort) 
#
t6  = np.sin(2*np.pi*freq*t5)
t7  = (t6*amp).astype(np.int16)


# ------------------------------------------------
# Forbedring aht at forklare matematik og fysik sammenhængen:
#
# Bedre forklaring af sinus til tabel - som hænger sammen med enhedscirklen og radianer - Her een peiode, een bølgelængde med 100 datapunkter.
#
t8 = np.linspace(0,2*np.pi,100)           # Een hel gang rundt i enhedscirklen fra 0 til 2pi på een gang - med diskrete værdier 100 stk (samples)
t9 = np.sin(t8)                           # Sinus på alle 100 datapunkter (vinkelværdier) på een gang
#
# for at se den - visualiser med plot funktionen
#
plt.figure(1)
plt.xlabel("x = Vinkel i radianer")
plt.ylabel("sin(x)")
plt.plot(t8,t9)                        # plot (vinkel,sin(vinkel) med de 100 datapunkter i figur 1.
plt.show(block=False)                  # Program/script afvikling stopper ikke og venter på input i plot vinduet.
                                       # Den fortsætter efter plot er lavet, når "block=False" gives som parameter/argument. Default er True og så venter den.
                                       # Vil man lave flere vinduer med plot kan man definere dem som forskellige figurer med 'figure' funktion/metode 
plt.pause(DURATION)                    # vi holder en lille pause for at se plot, inden vi lader koden fortsætte

#
#--------------------------------------------
#
# Når der så er SAMPLERATE samples pr sek og der er DURATION sekunder kan man fylde hele tabellen ud med sin(vinkel) ved nedenstående
# (NB - grænser for hvor lang man kan lave den da vædier vokser, men ok med float 64 vædier til rådighed og man typisk laver korte signaler)
#
t10 = np.linspace(0,DURATION*freq*2*np.pi,DURATION*SAMPLERATE)   # Een stor tabel med værdier fra radian/vinkel på een gang for hele perioden DURATION
                                                                 # - med DURATION*SAMPLERATE antal datapunkter for at det skal passe med perioden
t11 = np.sin(t10)                                                # Een tabel med sinus for alle datapunkter på een gang.
t12 = (t11*amp).astype(np.int16)                                 # Gange med amplituden og konvertering til heltal (signed) på hele tabel.

#
# Visualiser med et plot
#
plt.figure(2)
plt.xlabel("x = Vinkel i radianer")
plt.ylabel("amp*sin(x) i heltal 16")
plt.plot(t10,t12)                     # Kan tilføje en ekstra parameter/argument "ob" for at få punkter fremfor graf hvis det har interesse.
                                      # Kan bruges til at forklare diskret versus kontinuert.       plt.plot(t11,t13,"ob")
                                      # Bemærk at plots med høje frekvenser ikke bliver 'pæn'. Men lyden gør, så længe den er < SAMPLERATE/2!
plt.show(block=False)                 # Her plottes hele DURATION hvilket ikke er så illustrativt og med x-aksen med vinkel værdier... Forbedring nedenfor

#
# Så er der udfordringen med at konvertere til tid - ms, samt at skalere til et passende udsnit
#

t13 = np.linspace(0,1000*DURATION,DURATION*SAMPLERATE)   # alternativ x-akse med tid i millisekunder (ms) fremfor radianer/vinkelværdier
#
# Alternativ visualisering, de viser tid og amplitude og kun 10 ms - Bemærk det er for lidt til at vise en hel periode for freq<
#
plt.figure(3,figsize=[8,6])           # Laver plot vindue lidt større end default som er [6.4,4.8]
plt.title("Frekvens : "+str(freq))    # med en overskrift der viser frekvensen der er plottet
plt.xlabel("x = tid i ms\nLyd bevæger sig ca. 1 meter på 3ms. - 0.3432 m/ms ved 20 grader celsius i luft")  # \n giver linie skift
plt.ylabel("amp*sin(x) i heltal 16")
plt.axis([0,10,-20000,20000])         # Plot 0-10 ms og sæt (amplitude) y-aksen til at gå fra -20000 til +20000 fremfor en autoskalering pba værdierne
plt.plot(t13,t12)                     # Som graf
plt.plot(t13,t12, "ob")               # som diskrete punkter for at vise hvor få per periode når freq bliver > 1000, og graf begynder at blive 'takket'
plt.show(block=False)                 # - Bemærk at lyden der genereres med sndarry er ok så længe freq<SAMPLERATE/2 selvom graf er 'takket'
                                      # - Når freq < 100 skal der større antal ms til for at vise een periode - og der er rigeligt med datapunkter


#
# Lad os lave noget lyd ud af signalerne i tabellerne..
# initialiser pygame mixer til mono og 16 bit (signed) så det matcher cross platform driver og lyd kort PC,MAC og PI/Beocreate
#
pygame.mixer.init(SAMPLERATE, -16, 1)

sound = pygame.sndarray.make_sound(t12)   # Kun een dimension i t12, men lyddriver/mixer håndterer mono signal og laver det i de 2 stereo kanaler.
sound.play()                              # Uden parameter/argument spiller lyden kun DURATION - med -1 spiller den indtil stoppet i baggrund


#
# Så laver vi et skifte for at gå over i stereo. Det gør man ikke lige. Der skal pygame mixer genstartes så det vil ikke normalt være
# noget man gør indenfor et program. Der vælger man om man er i 'mono' eller 'stereo'
# Så her kun for at vise sammenhængen med tabeller og dimensionerne på tabeller
#
#pygame.time.delay(DURATION*1000)         # Vent DURATION sekunder til lyd er afviklet - Plots hænger også imens hvis blocked=False så ...
plt.pause(DURATION)                       # bedre at bruge plt.puse, da plot så laves færdig inden pause
pygame.mixer.quit()                       # Stop og frigør Mixer så den kan reinitialiseres

#
# initialiser pygame mixer til stereo og 16 bit (signed) så det matcher cross platform driver og lyd kort PC,MAC og PI/Beocreate
#
pygame.mixer.init(SAMPLERATE, -16, 2)

#
# Lav tabel med 2 dimensioner med samme signal i begge og transformer det til tal par som kan bruges i stereo signalet
# Samme oplevelse, men man kan nu gå videre med at lave forskellige signaler i de 2 som er i stereo signalet
#
t17 = (np.sin(np.linspace(0,DURATION*freq2*2*np.pi,DURATION*SAMPLERATE))*amp).astype(np.int16) # som line 80-83 i een linie til anden lyd i højre spor

t14 = np.array((t12,t17))          # tabel med 2 dimensioner sammensat af de 2 endimensionelle tabeller for hhv venstre først dernæst højre
t15 = t14.T.copy()                 # her er det lidt langhåret SKAL bruge copy for at få det udlagt i memory så det er C-contignous
t16 = np.dstack((t12,t17))[0]      # det gør dstack umiddelbart, men dstack er en funktion på vej ud så bedre med den anden!!!

sound = pygame.sndarray.make_sound(t15)   # t15 og t16 er ens og har værdier i par og continuert lagt ud i memory så sndarray kan lave et stereo lyd signal.
sound.play()                              # Uden parameter/argument spiller lyden kun DURATION - med -1 spiller den indtil stoppet i baggrund

# Og så er der det med at få fat i mixerens kanaler og så kan man justere på lydstyrken i de 2 i mixer og så lave pan etc...
# Det er som i stereo udgave af biblioteket på github version fra april, så ikke mere om det her i denne omgang
#

#
# Visualisering af stereo signalet i t15 - Kan naturligvis også bare bruge t12 direkte som tidligere, men for at vise transpose for at pille det ud..
# samt at man kan lave subplots
#
plt.figure(4,figsize=[8,6])           # Laver plot vindue lidt større end default som er [6.4,4.8]

plt.subplot(211)
plt.title("Frekvens i venstre spor: "+str(freq))    # med en overskrift der viser frekvensen der er plottet
plt.ylabel("amp*sin(x) i heltal 16")
plt.axis([0,10,-20000,20000])         # Plot 0-10 ms og sæt (amplitude) y-aksen til at gå fra -20000 til +20000 fremfor en autoskalering pba værdierne
plt.plot(t13,t15.T[0])                # Som graf

plt.subplot(212)
plt.title("Frekvens i højre spor: "+str(freq2))    # med en overskrift der viser frekvensen der er plottet
plt.xlabel("x = tid i ms\nLyd bevæger sig ca. 1 meter på 3ms. -  0.3432 m/ms ved 20 grader celsius i luft")  # \n giver linie skift
plt.ylabel("amp*sin(x) i heltal 16")
plt.axis([0,10,-20000,20000])         # Plot 0-10 ms og sæt (amplitude) y-aksen til at gå fra -20000 til +20000 fremfor en autoskalering pba værdierne
plt.plot(t13,t15.T[1])                # som diskrete punkter for at vise hvor få per periode når freq bliver > 1000, og graf begynder at blive 'takket'
plt.show(block=False)                 # - Bemærk at lyden der genereres med sndarry er ok så længe freq<SAMPLERATE/2 selvom graf er 'takket'
                                      # - Når freq < 100 skal der større antal ms til for at vise een periode - og der er rigeligt med datapunkter






