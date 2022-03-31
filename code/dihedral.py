from matplotlib import pyplot as plt
import numpy as np
import math

def LJ(v, A, n, phi):
    """ Dihedral period n, phase phi"""
    return (A*np.cos(n*v+phi))

r2d=180/math.pi

fig = plt.figure(figsize=(7,5))
fig.tight_layout()
ax = fig.add_subplot(111)
A=2
v = np.arange(-math.pi,math.pi,0.01) 
lj1 = LJ(v, A*0.5, 2, 0)
lj2 = LJ(v, A*1, 3, math.pi)
lj3=lj1+lj2+2.5

#lj2 = BUK(v, 6.2e7, 11.7, 603.5)
ax.plot(v*r2d,lj1,label='n=2',lw=1.5, linestyle='--')
ax.plot(v*r2d,lj2,label='n=3',lw=1.5, linestyle='--')
ax.plot(v*r2d,lj3,label='sum',lw=2)
#ax.plot(v,lj2,label='Buckingham',lw=2)
#ax.legend(loc=1,fontsize=14)
ax.set_xlabel('Dihedral angle, $\phi$',fontsize=16)
ax.set_ylabel('Potential energy, $V$',fontsize=16)
#ax.set_title("Krypton, 83.798 amu")
#plt.axhline(y=0.0, color='grey', linestyle='--')  
#ax.set_ylim(-1,1)
ax.set_xlim(-180,180)
ax.xaxis.set_ticks(np.arange(-180, 180, 60))

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.savefig("dih.svg")
plt.show()
