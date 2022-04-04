---
title: "Water models"
teaching: 15
exercises: 0
questions:
- "Why do we want to use water in out simulations?"
- "What water models are commonly used?"
- "How to chose a model of water for a simulation?"
objectives:
- "Learn how water molecules are modeled in simulations"
- "Understand how choice of water model can affect a simulation"
keypoints:
- "Continuum models cannot reproduce the microscopic details of the protein–water interface"
- "Water–water interactions dominate the computational cost of simulations"
- "Good water model needs to be fast and accurate in reproduction of the bulk properties of water"
---

### Introduction
Realistic water environment is essential for accurate simulation of biological molecules.

 Two approaches to solvation: 
 1. Add explicit water molecules. 
 2. Treat water as a continuous medium instead of individual molecules. 
 
#### Continuum models
- Significantly faster than explicit solvation. 
- Cannot reproduce the microscopic details of the protein–water interface. 
- Do not produce same conformational ensembles as explicit water (salt bridges are over-stabilized, a higher-than-native alpha helix population). 
- Useful for calculation of binding free energies or for flexible protein-protein docking.  

Most molecular dynamics simulations are carried out with explicit water molecules. 

#### Explicit models
- Typically water molecules account for over 80% of the particles in the simulation.
- Water–water interactions dominate the computational cost of such simulations.
- The water model needs to be fast and accurate.


- Explicit water models are empirical models derived to reproduce some bulk properties in a particular phase. 
- None of water models accurately reproduce all of the key properties of bulk water. 
- Which water model is optimal for the simulation depends on the desired properties of interest.

|An early model of water||
|:-|:-:|
|<br>$\circ$  Rigid geometry closely matching actual water molecule.  <br>$\circ$ O-H and H-H distances are constrained with harmonic potential. <br>$\circ$  Point charges replace electron density distribution.| ![Water Models]({{ page.root }}/fig/tip3p-points.svg){: width="200"}|

#### How are water models derived?
A good water model must faithfully reproduce six bulk properties of water:
- Static dielectric constant, $$ \epsilon_{0} $$
- Self diffusion coefficient, $$ \vec{D} $$
- Heat of vaporization, $$ \Delta{H}_{vap} $$
- Isobaric heat capacity, $$ \vec{C}_{p} $$
- Thermal expansion coefficient, $$ \alpha_{p} $$
- Isothermal compressibility, $$ \kappa_{T} $$

Many water models with different level of complexity (the number of interaction points) have been developed. We will discuss only the models most widely used in simulations, and refer you to the excellent [article in Wikipedia](https://en.wikipedia.org/wiki/Water_model) for an overview of all water models.

#### 3-charge 3-point models.
- Three interaction points corresponding to the atoms of the water molecule. 
- Only oxygen atom has Lennard-Jones parameters.
- 3-site models are commonly used because computationally they are highly efficient.

|||
|:-|:-:|
|**TIP3P (transferable intermolecular potential)**  <br><br>$\circ$  Rigid geometry closely matching actual water molecule.  | ![Water Models]({{ page.root }}/fig/tip3p.svg){: width="150"}|
|**SPC/E (simple point charge)**  <br><br>$\circ$  More obtuse tetrahedral angle of 109.47°.<br>$\circ$  Adds an average polarization correction to the potential energy function.<br>$\circ$  Reproduces density and diffusion constant better than the original SPC model. | ![Water Models]({{ page.root }}/fig/spce.svg){: width="150"}|


#### 3-charge 4-point models.
- The negative charge is not centered on the oxygen atom, but shifted towards hydrogen atoms
- The position of charge is represented with the fourth dummy atom (EP)
- EP is located near the oxygen along the bisector of the HOH angle. 

|||
|:-|:-:|
|**TIP4P-Ew**<br><br>$\circ$  Improves association/dissociation balance compared to 3-point models. | ![Water Models]({{ page.root }}/fig/tip4p.svg){: width="150"}|

#### Water models have their limitations.
- Early water models were developed with cut-off of electrostatic interactions. Using these models with full electrostatic method results in stronger electrostatic interactions and consequently higher density.
- Most of the more complex new water models attempt to reproduce specific properties of a specific phase, but this comes at the expense of other properties.
- TIP3P model predicts hydration free energies of small neutral molecules more accurately than the TIP4PEw model.
- 4-charge 5-point model TIP5P predicts excellent water structure, but poor hydration energies. 

|Challenges in developing water models.||
|:-|:-:|
|<br>$\circ$ Finding an accurate yet simplified description of the charge distribution that can adequately account for the hydrogen bonding in the liquid phase.<br>$\circ$ Traditional approach is to place point charges on or near the nuclei.<br>$\circ$ Electrostatic potential of water molecule is reproduced considerably more accurately with 3 point charges when they form tight cluster.|![Charge distribution of the water molecule]({{ page.root }}/fig/water_charge_densityl.gif){: width="300"}|

|||
|:-|:-:|
|**OPC (Optimal Point Charges)**<br><br>$\circ$ Designed without geometrical restraints.<br>$\circ$ Considerably better reproduces the six bulk properties of water. | ![Water Models]({{ page.root }}/fig/opc.svg){: width="150"}|

#### Quality scores of different water models 
- The test models in which the moments were close to the QM values had low quality. 
- The models that scored better had moments very different from the QM moments. 

This indicates that three point charges, even if placed optimally, are not enough to represent the complex charge distribution of real water molecule to the needed degree of accuracy. 

![Quality scores of water models]({{ page.root }}/fig/Water_models_quality_scores.gif){: width="350"}

The distribution of quality scores for different water models in the space of dipole (μ) and quadruple (QT) moments. Figure from [2].

#### Performance Considerations
- Computation cost is proportional to the number of pairwise distances.
- 3-charge 3-point model: 9 distances 
- 3-charge 4-site model: 10 distances (3x3 Coulomb interactions plus one VDW O–O interaction).

#### Other things to consider
- Water models commonly used in bio-molecular simulation have been traditionally parameterized only for a single temperature of 298K (SPC/E, TIP3P, etc).  


### Force Field Parameters of the common Water Models

|     | TIP3P  | SPC/E   | TIP4P-Ew | OPC    |
|---  |--------|---------|----------|--------|
|OH   | 0.9572 | 1.0     | 0.9572   | 0.8724 |
|HH   | 1.5136 | 1.63    | 1.5136   | 1.3712 | 
|HOH  | 104.52 | 109.47  | 104.52   | 103.6  |
|OM   | -      |  -      | 0.125    | 0.1594 |
|A(12)| 582.0  |629.4    | 656.1    | 865.1  |
|B(6) | 595.0  |625.5    | 653.5    | 858.1  |
|qO   | −0.834 | −0.8476 | −1.04844 | −1.3582|
|qH   | +0.417 | +0.4238 | +0.52422 | +0.6791|
 
#### References
1. [Structure and Dynamics of the TIP3P, SPC, and SPC/E Water Models at 298 K](https://pubs.acs.org/doi/full/10.1021/jp003020w)
2. [Building Water Models: A Different Approach](https://pubs.acs.org/doi/abs/10.1021/jz501780a)  
3. [Effect of the Water Model in Simulations of Protein–Protein Recognition and Association](https://doi.org/10.3390/polym13020176) 