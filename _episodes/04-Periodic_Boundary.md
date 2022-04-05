---
title: "Periodic Boundary Conditions"
teaching: 15
exercises: 0
questions:
- "How to simulate a bulk (gas, liquid or solid) system by using only a small part?"
objectives:
- "Understand why and when periodic boundary conditions are used."
- "Understand how shape and size of a periodic box can affect simulation."
- "Learn how to set periodic box parameters in GROMACS and NAMD."
keypoints:
- "Periodic boundary conditions are used to approximate an infinitely large system."
- "Periodic box should not restrict molecular motions in any way."
- "The macromolecule shape, rotation and conformational changes should be taken into account in choosing the periodic box parameters."
---
What is PBC and why is it important?
- In most cases we want to simulate a system in realistic environment, such as solution.
- Try simulating a droplet of water, it will simply evaporate.
- We need a boundary to contain water and control temperature, pressure, and density. 
- Periodic boundary conditions allow to approximate an infinite system by using a small part (unit cell). 

![Figure: Periodic Boundary Conditions]({{ page.root }}/fig/periodic_boundary.png){: width="240" }

- Unit cell is surrounded by an infinite number of translated copies in all directions (images). 
- When a particle in unit cell moves across the boundary it reappears on the opposite side. 
- Each molecule always interacts with its neighbors even though they may be on opposite sides of the simulation box. 
- Artifacts caused by the interaction of the isolated system with a vacuum are replaced with the PBC artifacts which are in general much less severe.


### Choosing periodic box size and shape.
#### Cubic periodic box
- A cubic box is the most intuitive and common choice
- Cubic box is inefficient due to irrelevant water molecules in the corners. 

![]({{ page.root }}/fig/cubic_box.svg){: width="200" }

- Ideal simulation system is a sphere of water surrounding the macromolecule, but spheres can't be packed to fill space.

#### Octahedral and dodecahedral periodic boxes
- The dodecahedron (12 faces) or the truncated octahedron (14 faces) are closer to sphere.

|  | Space filling with truncated octahedrons |
|:---:|:---|
| ![]({{ page.root }}/fig/trunc-octa.svg){: width="64" } | ![]({{ page.root }}/fig/truncated_octahedron_group.svg){: width="140" } |

- These shapes work reasonably well for globular macromolecules.

#### Triclinic periodic boxes
- Any repeating shape that fills all of space has an equivalent triclinic unit cell.
- A periodic box of any shape can be represented by a triclinic box with specific box vectors and angles.

![]({{ page.root }}/fig/triclinic_cell.gif){: width="200" }

- The optimal triclinic cell has about 71% the volume of the optimal rectangular cell.

####  Box size
- The minimum box size should extend at least 10 nm from the solute.

![10 nm margin]({{ page.root }}/fig/box_size-2.svg){: width="200" }

- The shortest periodic box vector should be at least twice bigger than the cuf-off radius.  

![Figure: Periodic Boundary Conditions]({{ page.root }}/fig/periodic_boundary-4.svg){: width="240" }

- In simulations with macromolecules solvent molecules should not "feel" both sides of a solute.

![]({{ page.root }}/fig/box_size.svg){: width="400" }

#### Pitfalls
 - A simulation system with elongated solute in cubic or dodecahedral box  will have a large amount of water located far away from the solute.
 - Consider using a narrow rectangular box. 
 - Rotation of elongated macromolecules and/or conformational changes must be taken in consideration.
 
![Figure: Periodic Boundary Conditions]({{ page.root }}/fig/PBC.svg){: width="300" }

- Constrain the rotational motion. 
- The box shape itself may influence conformational dynamics by restricting motions in certain directions.

References:  
1. [Molecular dynamics simulations with constrained roto-translational motions: Theoretical basis and statistical mechanical consistency](https://aip.scitation.org/doi/10.1063/1.480557) 
2. [The effect of box shape on the dynamic properties of proteins simulated under periodic boundary conditions](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.20341)
3. [Periodic box types in Gromacs manual](https://manual.gromacs.org/current/reference-manual/algorithms/periodic-boundary-conditions.html?highlight=periodic%20boundary%20conditions)

