---
title: "Controlling Temperature"
teaching: 30
exercises: 0
questions:
- "What is temperature on the molecular level?"
- "Why do we want to control the temperature of our MD-simulations?"
- "What temperature control algorithms are commonly used?"
- "What are the strengths and weaknesses of these common thermostats?"
objectives:
- "Remind us how Maxwell-Boltzmann distributions relate to temperature."
- "Quickly review thermodynamic ensembles."
- "Learn about different thermostats and get an idea how they work."
- "Learn where thermostats that don't produce correct thermodynamic ensembles can still be very useful."
keypoints:
- "On the molecular level, temperature manifests itself as a number of particles having a certain average kinetic energy."
- "Temperature control algorithms are needed to describe constant temperature thermodynamic ensembles."
- "Some temperature control algorithms (e.g. the Berendsen thermostat) fail to produce kinetic energy distributions that represent a correct thermodynamic ensemble."
- "Other thermostats, like Nosé-Hoover, produce correct thermodynamic ensembles but can take long to converge."
- "Even though the the Berendsen thermostat fails to produce correct thermodynamic ensembles, it can be useful for system relaxation as it is robust and converges fast."
---

## Temperature at the molecular level.

- Temperature is defined by the average kinetic energy of all the particles.
- A system in equilibrium, will have all of its energy distributed in the most probable way. 
- Particles in a system at equilibrium don't all have the same velocity. 
- Velocities follow a distribution that depends on their mass and the temperature of the system:

<center>$$f_v(v)=\left(\frac{m}{2\pi k_B T}\right)^{3/2}\cdot4\pi v^2\cdot\exp({-mv^2/2k_B T})$$</center>

#### <center>Maxwell-Boltzmann distributions</center>

|:--:|:--:|:--:|
|Krypton at different temperatures||Noble gases with different mass at 298K|

![Plot of velocity distributions]({{ page.root }}/fig/MB_ideal_gas.svg)

Velocity distributions obtained from MD simulations of water at different temperature. 

![Plot of Maxwell-Boltzmann distributions]({{ page.root }}/fig/Maxwell_Boltzmann_distributions.svg){: width="320"} 

## Thermodynamic ensembles
MD simulations usually simulate one of the following thermodynamic ensembles:

1. The *microcanonical* or constant *NVE* ensemble.
2. The *canonical* or constant *NVT* ensemble.
3. The *isothermal-isobaric* or constant *NPT* ensemble.

- Simulation of *NVE* ensemble is relatively easy to achieve, as long as the MD code manages to conserve the energy of the system.
- The *NVT* ensemble is more practically relevant, as in the real world it is much easier to manage the temperature of a system rather than it's energy. 
- Need to use a temperature control algorithm, a *thermostat*.
- In many cases constant ambient pressure and temperature are desired. In addition to using a thermostat to control the temperature, we also need to use a pressure control algorithm, a *barostat*.


## Temperature Control Algorithms
- Allow energy to enter and leave the simulated system to keep its temperature constant. 
- In practice thermostats do that by adjusting the velocities of a subset of particles. 
- The methods of maintaining temperature fall into four categories:

1. Strong coupling methods
2. Weak coupling methods
3. Stochastic methods
4. Extended system dynamics

### 1. Strong coupling methods
#### Velocity rescaling 
- Rescale the velocities at each step (or after a preset number of steps) to get the desired target temperature. 

#### Velocity reassignment
- Periodically assign new randomized velocities so that the entire system is set to the desired temperature. 

- Both methods do not generate the correct canonical ensemble. 
- Not recommended for equilibrium dynamics
- Useful for heating or cooling. 
##### Downsides:
- Rescaling will make hot spots even hotter.
- Temperature reassignment avoids this problem, but the kinetic energy of particles is no longer consistent with their potential energy, and thus needs to be redistributed. 

### 2. Weak coupling methods
#### Berendsen thermostat
- Rescale the velocities of all particles to remove a fraction of the difference from the predefined temperature.
- The rate of temperature equilibration is controlled by strength of the coupling. 
- The Berendsen thermostat a predictably converging and robust thermostat.
- Very useful when allowing the system to relax.
##### Downsides:
- Cannot be mapped onto a specific thermodynamic ensemble. 
- Produces an energy distribution with a lower variance than of a true canonical ensemble. 
- Should be avoided for production MD simulations.

Heat flows between the simulation system and the heat bath with the rate defined by a time constant $$\tau_T$$ 

### 3. Stochastic methods
Randomly assign a subset of atoms new velocities based on Maxwell-Boltzmann distributions for the target temperature. Randomization interferes with correlated motion and thus slows down the system's kinetics.

#### Andersen thermostat
- Assign a subset of atoms new velocities that are randomly selected from the Maxwell-Boltzmann distribution for the target temperature. 
- "massive Andersen" thermostat randomizes the velocities of all atoms. 

- Correctly samples the canonical ensemble
- Does not conserve momentum.  
- Can impair correlated motions and thus slow down the kinetics of the system. 
- Not recommended when studying kinetics or diffusion properties of the system. 

#### Lowe-Andersen thermostat 
- A variant of the Andersen thermostat that conserves momentum. 
- Perturbs the system dynamics to a far less than the original Andersen method. 
- Improves suppressed diffusion in the system relative to the original Andersen.

#### Bussi stochastic velocity rescaling thermostat
- Extension of the Berendsen method corrected for sampling the canonical distribution. 
- The velocities of all the particles are rescaled by a properly chosen random factor.

#### Langevin thermostat
- Mimics the viscous aspect of a solvent and interaction with the environment. 
- Adds a frictional force and a random force. 
- The frictional force and the random force combine to give the correct canonical ensemble.

The amount of friction is controlled by the damping coefficient.  If its value is high, atoms will experience too much unnatural friction, however if the coefficient is too low, your system will fluctuate too far away from the desired temperature. The default value is usually 1/ps.



### 4. Extended system thermostats
#### Nosé-Hoover thermostat
- The heat bath is integrated with the system by addition of an artificial variable associated with a fictional "heat bath mass" to the equations of motion. 
- The temperature can be controlled without involving random numbers. 
- Correlated motions are not impaired
- Better description of kinetics and diffusion properties.

##### Drawbacks:
 - Periodic temperature fluctuations with the frequency proportional to the "heat bath mass". 
 - Imparts the canonical distribution as well as ergodicity (space-filling). 

The time constant parameter in this thermostat controls the period of temperature fluctuations at equilibrium. 

#### Nosé-Hoover-chains
- A modification of the Nosé-Hoover thermostat which includes not a single thermostat variable but a chain of variables with different "masses". 
- Chaining variables with different masses helps to suppress oscillations. 

### Global and local thermostats
- Global thermostats control temperature of all atom in a system uniformly. 
- This may lead to cold solute and hot solvent due to a slow heat transfer.

- Local thermostats allow to control temperature in selected groups of atoms independently. 
- Local thermostats work well for large solutes.
- Temperature of small solutes this approach may significantly fluctuate leading to unrealistic dynamics.


### Selecting thermostats in molecular dynamics packages

| Thermostat/MD package | GROMACS                      |  NAMD                    | AMBER         |
|-----------------------|------------------------------|--------------------------|---------------|
| velocity rescaling    |                              |  reascaleFreq (steps)    |               |
| velocity reassignment |                              |  reassignFreq (steps)    |               |
| Andersen              | tcoupl = andersen            |                          |               |
| massive-Andersen      | tcoupl = andersen-massive    |                          | ntt = 2       |
| Lowe-Andersen         |                              |  loweAndersen on         |               |
| Berendsen             | tcoupl = berendsen           |  tCouple on              | ntt = 1       |
| Langevin              |                              |  langevin on             | ntt = 3       |
| Bussi                 | tcoupl = V-rescale           |  stochRescale  on        |               |
| Nose-Hoover           | tcoupl = nose-hoover         |                          |               |
| Nose-Hoover-chains    | nh-chain-length (default 10) |                          |               |


