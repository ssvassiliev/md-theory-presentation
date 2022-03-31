from matplotlib import pyplot as plt
import numpy as np

def LJ(v,epsilon, sigma):
    """ Lennard-Jones potential """
    return (4*epsilon*(pow(sigma/v,12) - pow(sigma/v,6)))

def BUK(v, A, B, C):
    """ Bukingham potential """
    return (A*(np.exp(-B*v))-C*pow(1/v,6))


fig = plt.figure(figsize=(7,5))
fig.tight_layout()
ax = fig.add_subplot(111)

v = np.arange(0.75,2,0.01) 
lj = LJ(v, 180.0, 0.98)
#lj2 = BUK(v, 6.2e7, 11.7, 603.5)
ax.plot(v,lj,label='Lennard-Jones',lw=2)
#ax.plot(v,lj2,label='Buckingham',lw=2)
ax.legend(loc=0,fontsize=14)
ax.set_xlabel('Distance between atoms, $r$',fontsize=16)
ax.set_ylabel('Potential energy, $V$',fontsize=16)
#ax.set_title("Krypton, 83.798 amu")
plt.axhline(y=0.3, color='grey', linestyle='--')  
ax.set_ylim(-210,500)
ax.set_xlim(0.85,2.0)

plt.savefig("lj.svg")
plt.show()
