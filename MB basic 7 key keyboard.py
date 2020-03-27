# Basic keyboard for LYDKit project P1 spring 2020. SSG, SHD, Herningsholm, Skanderborg - sponsered by Region MidtJylland
#
# Version 17 jan  2020, Knud Funch SHD
#
# Keybord - read pin 0-2 and combine into 7 key active/inactive that are sent on the seriel port so it eg can be used as
# 7 keys together with Tonegenertor for a demo
#
#
from microbit import *
import radio

# 10 char id "0123456789"
name =       "MB 7Key2  "


last_key_sent = "0"
key_read_1    = "0"
key_read_2    = "0"

local_connected = True

def display_current_mode(lc):
    if lc:
        display.show(Image.SQUARE_SMALL)
    else:
        display.show(Image.SQUARE)


def check_mode_shift():
    global local_connected
    both_pressed = button_a.is_pressed() and button_b.is_pressed()
    if both_pressed:
        display_current_mode(local_connected)
        sleep(3000)
        display.clear()
        both_pressed = button_a.is_pressed() and button_b.is_pressed()
        if both_pressed:  # still after 3 sec
            if local_connected: local_connected = False
            else: local_connected = True
            display_current_mode(local_connected)
            sleep(3000)
            display.clear()

def read_key():
    p0 = pin0.is_touched()
    p1 = pin1.is_touched()
    p2 = pin2.is_touched()
    if p0 and p1 and p2:             key="7"
    if not p0 and p1 and p2:         key="6" 
    if p0 and not p1 and p2:         key="5" 
    if not p0 and not p1 and p2:     key="4"
    if p0 and p1 and not p2:         key="3"
    if not p0 and p1 and not p2:     key="2" 
    if p0 and not p1 and not p2:     key="1" 
    if not p0 and not p1 and not p2: key="0"   # no pins touched -> no key pressed  
    return(key)

def send_streng(k):
    if local_connected:
        print(k+name)
    else:
        radio.send(k+name)


print("Hello World - Klar på den serielle ",name)

display.show(Image.HAPPY)
sleep(2000)
display.clear()

radio.on()




while True:                  # Forever - at least until power off/reset - generate events on USB or radio
    
    key_read_1 = read_key()
    sleep(50)                # 2 readings with same to detect for removing worst jitter
    key_read_2 = read_key()
    
    if (key_read_1 == key_read_2) and (key_read_1 != last_key_sent):
        send_streng(key_read_1)
        if key_read_1 == "0": display.clear()
        else:display.show(key_read_1) 
        last_key_sent = key_read_1
        
    check_mode_shift()
    
    if local_connected:
        r = radio.receive()
        if r: print(r)
        if button_a.was_pressed(): print("A")
        if button_b.was_pressed(): print("B")
        

 

   
        
     
        
