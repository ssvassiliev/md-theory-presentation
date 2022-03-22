---
title: "Electrostatic Interactions"
teaching: 10
exercises: 0
questions:
- "How electrostatic interactions are calculated in periodic systems?"
objectives:
- "Learn what parameters control the accuracy of electrostatic calculations"
keypoints:
- "Calculation of electrostatic potentials is the most time consuming part of any MD simulation"
- "Long-range part of electrostatic interactions is calculated by approximating Coulomb potentials on a grid" 
- "Denser grid increases accuracy, but significantly slows down simulation"
---
## Coulomb interactions

- Long range: $V_{Elec}=\frac{q_{i}q_{j}}{4\pi\epsilon_{0}\epsilon_{r}r_{ij}}$

![graph: electrostatic potential]({{ page.root }}/fig/Coulomb_interaction.png){: width="260" }

- Computing Coulomb potentials is often the most time consuming part of any MD simulation. 
- Fast and efficient algorithms are required for these calculations.

### Particle Mesh Ewald (PME) 
- The most widely used method using the Ewald decomposition.
- The potential is decomposed into two parts: fast decaying and slow decaying.

![Graph: PME Decomposition]({{ page.root }}/fig/PME_decomp.svg){:width="480"}

#### Fast decaying short-ranged potential (Particle part).
- Sum of all pairwise Coulomb interactions within a cutoff radius 
- Implements same truncation scheme as the LJ potentials.

#### Slow decaying long-ranged potential (Mesh part).
- Slowly varying, smooth and periodic function.
- All periodic functions can be represented with a sum of sine or cosine components.
- Slowly varying functions can be accurately described by only a limited number of low frequency components (k vectors).

#### PME algorithm
- Long-range electrostatic interactions are evaluated using 3-D grids in reciprocal Fourier space.
 
![Image: PME]({{ page.root }}/fig/PME.png)

1. Assign charges to grid cells. Charges in grid cells are obtained by interpolation. 
2. Compute Fourier transform. 
3. Compute potential. Coulomb interaction decays rapidly in Fourier space, and summation converges fast.     
4. Compute inverse Fourier transform. 
5. Interpolate gridded potentials back to atomic centers.  

#### Simulation parameters controlling speed and accuracy of PME calculations.
- **Grid spacing**. Lower values lead to higher accuracy but considerably slow down the calculation. Default 1.0 Å. 
- **Grid dimension**. Higher values lead to higher accuracy but considerably slow down the calculation.
- **Direct space tolerance**. Controls the splitting into direct and reciprocal part. Higher tolerance shifts more charges into Fourier space.
- **Interpolation order** is the order of the B-spline interpolation. The higher the order, the better the accuracy. Default 4 (cubic spline).   


| Variable \ MD package | GROMACS                  | NAMD                      | AMBER                  |
|-----------------------|--------------------------|---------------------------|------------------------|
| Fourier grid spacing  | fourierspacing (1.2)     | PMEGridSpacing  (1.5)     |                        |
| Grid Dimension [X,Y,Z]| fourier-[nx,ny,nz]       | PMEGridSize[X,Y,Z]        |  nfft[1,2,3]           |
| Direct space tolerance| ewald-rtol ($$10^{-5}$$) | PMETolerance ($$10^{-5}$$)| dsum_tol ($$10^{-6}$$) |
| Interpolaton order    | pme-order (4)            | PMEInterpOrder (4)        | order (4)              |


Have a user who needs firewall rules for abaqus to reach their license server 27610@131.202.255.214


From this ticket:
https://support.computecanada.ca/otrs/index.pl?Action=AgentTicketZoom;TicketID=154364
I have the user who would like to access an ABAQUS license server from Graham:
- Address is : 131.202.255.214
- Ports : 27610 and 57610
Can someone add appropriate firewall rules? Thank you.