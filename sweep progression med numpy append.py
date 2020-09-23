# "sweep progression med numpy append.py"
#
# Lidt kode eksempler som opfølgning på observation af brug af Lyd KIT i fysik/informatik forløb på Herningsholm september 20
# Tænkt som input/inspiration til lærer - Ender med en smooth sweep der er robust for startværdier givet i konstanter.
#
# Knud - SHD - 23 sept. 2020 - Inkluderes i notesbog..
#
# At betragte som noter/forbedringspunkter/reflektioner som kan bruges når der skal rulles på Modul 2.
# Hoved pointe er at man har et datapunkt for meget med hvis man tager en fuld periode og dermed får man ticks når man
# afspiller lyd. Ved at fjerne det sidste datapunkt inden man sætter til afspilning kan det laves helt smooth.
#
# Bruges til at lave et sweep - I 3 udgaver der gradvist bliver mere robust for ændrede værdier i konstanterne.
# - Sammenhæng med hele peridoder og en længde på de enkelte steps i sweep.
#
# Materiale der kunne tænkes anvendt i matematik (diskret matematik) og i programmering for at gå i dybden.
#
#

import numpy as np
import pygame
import matplotlib.pyplot as plt

TEST_PRINT = False
SAMPLERATE = 44100
DURATION   =     1     # Signal længde i sekunder SKAL være langt nok til at indenholde et helt antal perioder.
                       # så længe der bruges heltal i freq vil vi så ved at fjerne sidste datapunkt kunne få smooth overgang.
AMP        = 8000

freq       =  440


#-----------------------------------
# Basis array håndtering - Kør program/script og tast så variabel navn ind in shell og se array indhold direkte
# Default værdier i array/tabel er float 64 så det behøver man ikke at specificere!
#
t1 = np.arange(0,3)             # tabel med en dim med 3 værdier i en dimension [a1,b1,c1]
                                # - Her [0,1,2] start med 0 slut med værdien inden 3 (3 ikke inkluderet) med default step på 1
                                # - Kan sætte step til andet gennem optional argument til funktionen
                                # - Se: https://numpy.org/doc/stable/reference/generated/numpy.arange.html 
t2 = np.linspace(5,7,3)         # tabel med 3 værdier (bestemt med argument/parameter nummer 3) med lige meget afstand mellem værdierne (spasering)
                                # - delta (afstand mellem værdier) er her lig med 2/2=1 (Kun 2 gange spasering da 7 er inkluderet) 
                                # - her [5,6,7] da startværdi er sat til 5 og slut til 7 (som inkluderes default) med lige meget spasering mellem værdierne.
                                # - Se: https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
t3 = np.array((t1,t2))          # tabel med 2 dimensioner sammensat af de 2 endimensionelle tabeller [[a1,b1,c1],[a2,b2,c2]]
t4 = t3.T                       # Transpose - vender dimensionen på tabellen. så der bliver par med [[a1,a2],[b1,b2],[c1,c2]] Det som sndarray vil have!
                                #  - når der er tale om et stereo signal!

t5 = np.append(t1,t2)           # sammensætter en ny tabel af to andre ved at tilføje det andet til enden af det første

t6 = np.delete(t5,len(t5)-1)    # Fjerner sidste element i tabel. Parameter 2 kan udpege et hvilket som helst datapunkt der kan fjernes i tabel.

t7 = np.linspace(5,7,3,endpoint=False)  # Sammenlig denne med t2 - Her er 3 værdier med ens spasering fra 5 til sidste som IKKE er 7!!! 
                                        # - delta (afstand mellem værdier) er her lig med 3/2 (3 gange spacering - da 7 IKKE er med)
#
#
#--------------------------------------------
# Lav en tone med et fuldt antal peridoer - Lyt til det ved gentagne afspilninger og hør ticks
# De skyldes at det første og det sidste datapunkt i tabel er det samme, så der er overlap og dermed bliver kurven ikke helt smooth
# Fjern det sidte og så bliver det bedre - Sammenlign t10 og t11
# Se værdierne i tabellerne evt. med et plot for at forstå.
# skal bruge den med endpoint=False - fordi der så opretholdes det rigtige antal datapunkter!!
# MEN ikke en hel omgang og dermed 2 gange nul i overgange når man sætter sammen !!!!
#
# læring - OBS - ifm tonegenerator LKM2 så skal der kikkes på at freq som ikke er heltal skal gå op i duration for at vi kan sammensætte ordentligt
#    (eller holde os til heltals frekvenser)
#
# Den funktion der er i LKM2 pt (forår 20) er OK i den forbindelse -
# DET var linspace der var et step tilbage i den sammenhæng.... uden endpoint=False!
#

# 
# t10 indeholder x = DURATION*SAMPLERATE datapunkter, hvor sidste værdi er samme som første - ved freq der går op.
# D.v.s. at det er et helt antal perioder og 0 såvel som x*2pi er repræsenteret som første og sidste værdi
#
# t11 fjerner sidste datpunkt så man kan sammensætte flere til en jævn kurve (unden dobbelt værdier pga første og sidste er ens.
# Samtidigt bliver antal datapunkter i tabel een mindre
# 
t10 = ((np.sin(np.linspace(0,DURATION*freq*2*np.pi,DURATION*SAMPLERATE)))*AMP).astype(np.int16)
t11 = np.delete(t10,len(t10)-1)                                                                     

#
# Som brugt på Herningsholm - svarer til det som er i biblioteket men opbygget step for step. Og som ikke har 2 gange samme værdi (0 og 2*pi)!
#
t12 = np.zeros(SAMPLERATE,dtype=np.int16)
for s in range(SAMPLERATE):
    t      = float(s)/SAMPLERATE
    t12[s] = int(AMP*np.sin(2*np.pi*freq*t))   
#
# Ved at bruge endpoint=False i linspace funktionen så bliver sidste punkt IKKE lig med det første ved helt antal perioder
# så svarer til t11. Dog med den lille forskel at der her er et fuldt antal datapunkter
#
t13 = ((np.sin(np.linspace(0,DURATION*freq*2*np.pi,DURATION*SAMPLERATE,endpoint=False)))*AMP).astype(np.int16)  
#
# Lad os lave noget lyd ud af signalerne i tabellerne..
# initialiser pygame mixer til mono og 16 bit (signed) så det matcher cross platform driver og lyd kort PC,MAC og PI/Beocreate
#
pygame.mixer.init(SAMPLERATE, -16, 1)

print("Hør t10 hvor både nul og 2*pi er med og dermed dobbelt værdi i overgang - Giver klik ved repetition")
sound = pygame.sndarray.make_sound(t10)   # Hør først t10 med fuld periode til slut og dermed et datapunkt for meget 
sound.play(-1)                            # 

pygame.time.delay(int(DURATION*5000))
sound.stop()

# Så det samme - næsten, men med t11 uden det sidste datapunkt
print("Hør t11 hvor 2*pi er fjernet og der er eet datapunkt mindre - ingen dublering af værdier - ingen klik")
sound = pygame.sndarray.make_sound(t11)   # Hør t11 uden sidste datapunkt til en sammenligning Samme kurve men helt anden lyd.
sound.play(-1)                            # 

pygame.time.delay(int(DURATION*5000))
sound.stop()

# Så det samme - næsten, men med t11 uden det sidste datapunkt men fuld tabel (een værdi mere)
print("Hør t13 hvor 2*pi slutpunkt ikke er med men der er alle datapunkter - ingen klik - kan ikke høre forskel til t11")
sound = pygame.sndarray.make_sound(t13)   # Hør t13 uden sidste datapunkt til en sammenligning Samme kurve men helt anden lyd.
sound.play(-1)                            # 

pygame.time.delay(int(DURATION*5000))
sound.stop()

print("Pause på 5 sek")
pygame.time.delay(5000)
print("")

#
# -----------
# En loop der sammensætter en sweep med issues ift hvad man giver af værdier, da det kan resultere i at der IKKE er et halt antal peridoder pr
# step - og det medfører hørbare effekter sm man ikke er interesseret i ved en jævn sweep - Prøv af og hør
# Kan bruge plt.plot(t20) efterfulgt af plt.show() i shell for at få syn for sagen - man kan så finde overgangene som ikke er 'pæne'
#
print("Sweep som tager udgangspunkt i ens længde på alle steps")
print("Stor risiko for at der IKKE er et helt antal perioder i hvert step og dermed ikke glidende overgange i lyd - Prøv med andre konstanter")

START_FREQ         = 100                               # heltals værdi for at det skal gå op med helt antal perioder ift ..
SWEEP_DURATION     = 1                                 # i helt antal sekunder så der er helt antal perioder med START_FREQ
NOF_STEPS          = 100                               #  10 ms pr step
FREQ_STEP          = 100                               # 100 hz tager 10 ms for hel periode så det vil gå op

nof_datapoints     = SWEEP_DURATION*SAMPLERATE
datapoints_pr_step = nof_datapoints/NOF_STEPS
duration_pr_step   = SWEEP_DURATION*1000/NOF_STEPS     # i ms - SKAL kunne have et helt antal perioder af START_FREQ for ikke at give ticks

if TEST_PRINT: print("nof datapoints ",nof_datapoints,"datapoints pr step ",datapoints_pr_step,"duration pr step ",duration_pr_step)

t20 = np.zeros(0,dtype=np.int16)  # initielt een tabel med 0 datapunkter men defineret med dtype, som der efterfølgende tilføjes til (append)

for i in range(NOF_STEPS):
    freq = START_FREQ+(i*FREQ_STEP)
    if TEST_PRINT: print("iteration no: ",i," freq stump: ",freq)
    t21 = ((np.sin(np.linspace(0,duration_pr_step/1000*freq*2*np.pi,datapoints_pr_step,endpoint=False)))*AMP).astype(np.int16)
    t20 = np.append(t20,t21)

sound = pygame.sndarray.make_sound(t20)   # Hør t11 uden sidste datapunkt til en sammenligning Samme kurve men helt anden lyd.
sound.play(-1)                            # 

pygame.time.delay(int(SWEEP_DURATION*3000))  # 3 gange rundt i sweep
sound.stop()

print("Pause på 10 sek")
pygame.time.delay(10000)
print("")

#
# Lad os vende det om og regne ud hvor længe/hvor mange data punkter vi skal have pr. freq for at får et helt antal perioder
# og ikke lade os begrænse af den samlede længde af sweep.
# Det resulterer i noget der er langt mere robust ift at ændre i konstanter og blive ved med at få et smooth forløb
#
print("Sweep som tager udgangspunkt i et helt antal perioder ud fra frekvens så der altid er bløde overgange")
print("- Prøv med andre konstanter, og se den er langt mere robust")
print("- Tilgengæld er der stor forskel på hvor lang tid de enkelte steps tager") 

START_FREQ         = 100                               
NOF_STEPS          = 1000                              
FREQ_STEP          = 10                               

freq = START_FREQ

t22 = np.zeros(0,dtype=np.int16)     # initielt een tabel med 0 datapunkter men defineret med dtype, som der efterfølgende tilføjes til (append)

for i in range(NOF_STEPS):
    duration_in_step = 5000/freq     # ms som kan rumme mindst 5 hele perioder ud fra freq. Når freq er >=100
    datapoints_in_step = duration_in_step*SAMPLERATE/1000  # hvor mange ift SAMPLERATE
    if TEST_PRINT: print("freq",freq,"datapoints in step ",datapoints_in_step,"duration in step ",duration_in_step)
    t23 = ((np.sin(np.linspace(0,duration_in_step/1000*freq*2*np.pi,datapoints_in_step,endpoint=False)))*AMP).astype(np.int16)
    t22 = np.append(t22,t23)
    freq = freq+FREQ_STEP
    
sound = pygame.sndarray.make_sound(t22)   
sound.play(-1)                            

pygame.time.delay(int(2000*len(t22)/SAMPLERATE))
sound.stop()

print("Pause på 10 sek")
pygame.time.delay(10000)
print("")

#
# Kan så rafinere det yderligere til at man ved lave frekvenser tager færre perioder end 5 med - da det ellers er for langt til at opfattes som smooth
# - under 900 hz se om man kan komme tættere på en varighed omkring de 5-10 ms (stadig helt antal perioder!! 
# og tilsvarende ved højere frekvenser tager flere peridoer med så man når op på min 5 ms varighed med hver frekvens så man kan nå at opleve den.
# - over 1200 tag flere perioder med så det ca rammer 5-10 ms (igen skal det være hele perioder!!)
# 
# Hvad sker for oplevelsen når vi optimerer mod at ramme nogenlunde samme længde men med hele perioder? den første loop tog udgangpunkt i at alle
# steps tog lige lang tid (som gav problemstillingen med at vi så ikke altid fik et helt antal perioder og dermed problemer i overgangen mellem steps.
#
print("Nu til udgave der raffinerer yderligere og laver steps nogenlunde lige lange")
print("- MEN fortsat med alle steps indeholdende et helt antal peridoer for at få et smooth forløb")

START_FREQ         = 50                             
NOF_STEPS          = 1000                            
FREQ_STEP          = 10


#
# Funktion der runder op til nærmeste 100
#
def roundup(x):
    if x % 100 == 0:
        if x == 0: x = 100
        return x
    else:
        return(x + 100 - x % 100)

#
# Globale variabler
#
freq         = START_FREQ
faktor       = 10*roundup(START_FREQ)    # Mindst een fuld periode og tættest på 10 ms i varighed - divideret med freq giver det varighed i ms
delta        = 0
delta_faktor = roundup(FREQ_STEP)
#
# initialisering
#
pygame.mixer.init(SAMPLERATE, -16, 1)

t24 = np.zeros(0,dtype=np.int16)     # initielt een tabel med 0 datapunkter men defineret med dtype, som der efterfølgende tilføjes til (append)
print("start freq: ",freq," start faktor: ",faktor, " delta faktor: ",delta_faktor)

if (START_FREQ+(NOF_STEPS*FREQ_STEP)>(SAMPLERATE/2)):
    print("Vil ende i for høj frekvens - der vil opstå artifakter - Prøv det bare og lyt")

#
# Løkke der laver sweep iht værdierne i de globale konstanter og variabler
#
for i in range(NOF_STEPS):
    duration_in_step = faktor/freq     # ms som kan rumme mindst een hel periode og varer mindst 5 ms.
    datapoints_in_step = duration_in_step*SAMPLERATE/1000  # hvor mange ift SAMPLERATE
    if TEST_PRINT: print("freq",freq,"datapoints in step ",datapoints_in_step,"duration in step ",duration_in_step, " faktor: ",faktor)
    t25 = ((np.sin(np.linspace(0,duration_in_step/1000*freq*2*np.pi,datapoints_in_step,endpoint=False)))*AMP).astype(np.int16)
    t24 = np.append(t24,t25)
 
    freq = freq+FREQ_STEP
    delta = delta+FREQ_STEP
    if delta >= delta_faktor:             
        faktor = faktor + 10*delta_faktor
        delta = 0

print("slut freq: ",freq," sweeps varighed: ",int(len(t24)/SAMPLERATE)," sek")

#
# Afspil lyden - repetitivt
#
sound = pygame.sndarray.make_sound(t24)   
sound.play(-1)                            

pygame.time.delay(int(3000*int(len(t24)/SAMPLERATE)))
sound.stop()

