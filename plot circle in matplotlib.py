#
# tegn cirkel og een periode af sin/cos med matplotlib
#
import numpy as np
import matplotlib.pyplot as plt

R = 1  # radius, som jo så altid er 1 i enhedscirklen
N = 30 # antal datapunkter
t = np.linspace(0,2*np.pi,N,endpoint=False)
# x,y værdier
x = R*np.cos(t)
y = R*np.sin(t)
#
# plot cirklen
#
plt.subplot(211)
plt.axis("equal")
plt.grid()
plt.plot(x,y)
plt.plot(x,y,"+b")

sinus   = np.sin(t)   # Sin på alle datapunkter på een gang
cosinus = np.cos(t)   # Cos på alle datapunkter på een gang
#
# Plot sin og cos - Bemærk første/sidste værdi
#
plt.subplot(212)
plt.xlabel("x = Vinkel i radianer")
plt.ylabel("sin(x),cos(x)")
plt.grid()
plt.plot(t,sinus,"+")
plt.plot(t,cosinus,"+")
plt.show()                   
                                       
                     

