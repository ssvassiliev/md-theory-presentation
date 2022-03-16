---
title: "Advancing Simulation in Time"
teaching: 20
exercises: 0
questions:
- "How is simulation time advanced in a molecular dynamics simulation?"
- "What factors are limiting a simulation time step?"
- "How to accelerate a simulation?"
objectives:
- "Understand how simulation is advanced in time."
- "Learn how to choose time parameters and constraints for an efficient and accurate simulation."
- "Learn how to specify time parameters and constraints in GROMACS and NAMD."
keypoints:
- "A good integration algorithm for MD should be time-reversible and energy conserving."
- "The most widely used integration method is the velocity Verlet."
- "Simulation time step must be short enough to describe the fastest motion."
- "Time step can be increased if bonds involving hydrogens are constrained."
- "Additional time step increase can be achieved by constraining all bonds and angles involving hydrogens."
---
## Integration Algorithms
- To simulate evolution of the system in time we need to solve Newtonian equations of motions. 
- The exact analytical solution is not feasible, the problem is solved numerically. 
- The approach used to find a numerical approximation to the exact solution is called integration. 
- The integration algorithm advances positions of all atoms by  small time steps $$\delta{t}$$. 
- If the time step is small enough the trajectory will be reasonably accurate. 
- A good integration algorithm for MD should be time-reversible and energy conserving.

### The Euler Algorithm
- The simplest integration method

1. Use $\overrightarrow{r}, \overrightarrow{v},\overrightarrow{a}$ at time $t$ to compute   $\overrightarrow{r}(t+\delta{t})$ and $\overrightarrow{v}(t+\delta{t})$:

<span style="color:gray">
$\qquad\overrightarrow{r}(t+\delta{t})=\overrightarrow{r}(t)+\overrightarrow{v}(t)\delta{t}+\frac{1}{2}\overrightarrow{a}(t)\delta{t}^2,\qquad\overrightarrow{v}(t+\delta{t})=\overrightarrow{v}(t)+\frac{1}{2}\overrightarrow{a}(t)\delta{t}$
</span>

- Assumes that acceleration does not change during time step. 
- In reality acceleration is a function of coordinates, it changes when atoms move.

Drawbacks:
1. Not energy conserving
2. Not reversible in time

#### Applications
- Not recommended for classical MD
- Can be used to integrate some other equations of motion. For example, GROMACS offers a Euler integrator for Brownian (position Langevin) dynamics.


### The Verlet Algorithm
Using the current positions and forces and the previous positions calculate the positions at the next time step:

$\overrightarrow{r}(t+\delta{t})=2\overrightarrow{r}(t)-\overrightarrow{r}(t-\delta{t})+a(t)\delta{t}^2$

The Verlet algorithm  [(Verlet, 1967)]({{ page.root }}/reference.html#Verlet-1967) requires positions at two time steps. It is inconvenient when starting a simulation. While velocities are not needed to compute trajectories, they are useful for calculating observables e.g. the kinetic energy. The velocities can only be computed once the next positions are calculated:

$\overrightarrow{v}(t+\delta{t})=\frac{r{(t+\delta{t})-r(t-\delta{t})}}{2\delta{t}}$

### The Velocity Verlet Algorithm
Euler integrator can be improved by introducing evaluation of the acceleration at the next time step. Recollect that acceleration is a function of atomic coordinates and is fully defined by interaction potential.

- The velocities, positions and forces are calculated at the same time using the following algorithm:

1. Use $\overrightarrow{r}, \overrightarrow{v},\overrightarrow{a}$ at time $t$ to compute   $\overrightarrow{r}(t+\delta{t})$:<span style="color:gray"> $\qquad\overrightarrow{r}(t+\delta{t})=\overrightarrow{r}(t)+\overrightarrow{v}(t)\delta{t}+\frac{1}{2}\overrightarrow{a}(t)\delta{t}^2$ </span>
2. Derive $ \overrightarrow{a}(t+\delta{t})$ from the interaction potential using new positions $\overrightarrow{r}(t+\delta{t})$ 
3.  Use both $\overrightarrow{a}(t)$ and $\overrightarrow{a}(t+\delta{t})$ to compute $\overrightarrow{v}(t+\delta{t})$:  <span style="color:gray"> $\quad\overrightarrow{v}(t+\delta{t})=\overrightarrow{v}(t)+\frac{1}{2}(\overrightarrow{a}(t)+\overrightarrow{a}(t+\delta{t}))\delta{t} $</span>

- The Verlet algorithm is time-reversible and energy conserving.

The Velocity Verlet algorithm is mathematically equivalent to the original Verlet algorithm. It explicitly incorporates velocity, solving the problem of the first time step in the basic Verlet algorithm.
- *Due to its simplicity and stability the Velocity Verlet has become the most widely used algorithm in the MD simulations.*


#### Leap Frog Variant of Velocity Verlet

- The leap frog algorithm is a modified version of the Verlet algorithm.
- The only difference is that the velocities are not calculated at the same time as positions.
- Positions and velocities are computed at interleaved time points, staggered in such a way that they "leapfrog" over each other.

1. Derive $ \overrightarrow{a}(t)$ from the interaction potential using positions $\overrightarrow{r}(t)$ 
2. Use $\overrightarrow{v}(t-\frac{\delta{t}}{2})$ and $\overrightarrow{a}(t)$ to compute $\overrightarrow{v}(t+\frac{\delta{t}}{2})$:<span style="color:gray"> $\qquad\overrightarrow{v}(t+\frac{\delta{t}}{2})=\overrightarrow{v}(t-\frac{\delta{t}}{2}) + \overrightarrow{a}(t)\delta{t}$
3. Use current $\overrightarrow{r}(t)$ and $\overrightarrow{v}(t+\frac{\delta{t}}{2})$ to compute $\overrightarrow{r}(t+\delta{t})$ : <span style="color:gray"> $\qquad\overrightarrow{r}(t+\delta{t})=\overrightarrow{r}(t)+\overrightarrow{v}(t+\frac{\delta{t}}{2})\delta{t}$ </span>
 
- The Leap Frog and the Velocity Verlet integrators give equivalent trajectories.
- Restart files are different 


## How to Choose Simulation Time Step?
Larger time step allows to run simulation faster, but accuracy decreases.

- Verlet family integrators are stable for time steps
$$\delta{t}\leq\frac{2}{w}$$ where $$\omega$$ is angular frequency.

- Vibrations of bonds with hydrogens have period of 10 fs
- Bond vibrations involving heavy atoms and angles involving hydrogen atoms have period of 20 fs

- Stretching of bonds with the lightest atom H is the fastest motion. 
- As period of oscillation of a C-H bond is about 10 fs, Verlet integration is stable for time steps < 3.2 fs. 
- In practice, the time step of 1 fs is recommended to describe this motion reliably.
- Simulation step can be doubled by constraining bonds with hydrogens.
- Further increase of the simulation step requires constraining bonds between all atoms and angles involving hydrogen atoms. 

#### Other ways to increase simulation speed
- Compute long range electrostatic interactions less often than the short range interactions. 
- Employ an intermediate timestep for the short-range non-bonded interactions, performing only bonded interactions at each timestep.
- Hydrogen mass repartitioning allows increasing time step to 4 fs.

### Constraint Algorithms
- To constrain bond length in a simulation the equations of motion must be modified.
- The goal is to constrain some bonds without affecting dynamics and energetics of a system.
- One way to constrain bonds is to apply constraint force acting along a bond in opposite direction. 

In constrained simulation first the unconstrained step is done, then corrections are applied to satisfy constraints.

- As bonds in molecules are coupled satisfying all constraints in a molecule becomes increasingly complex for larger molecules. 
- Several algorithms have been developed for use specifically with small or large molecules.

#### SETTLE 
- Very fast analytical solution for small molecules. 
- Widely used to constrain bonds in water molecules.

#### SHAKE 
- Iterative algorithm that resets all bonds to the constrained values sequentially until the desired tolerance is achieved.
- Simple and stable, it can be applied for large molecules.
- Works with both bond and angle constraints. 
- Slower than SETTLE and hard to parallelize.
- SHAKE may fail to find the constrained positions when displacements are large. 

Extensions of the original SHAKE algorithm:  RATTLE, QSHAKE, WIGGLE, MSHAKE, P-SHAKE.

#### LINCS  
- Linear constraint solver 
- 3-4 times faster than SHAKE and easy to parallelize. 
- The parallel LINCS (P-LINKS) allows to constrain all bonds in large molecules. 
- Not suitable for constraining both bonds and angles.

> ## Specifying Constraints
> **GROMACS**
>
>SHAKE, LINKS and SETTLE constraint algorithms are implemented. They are selected via keywords in mdp input files
> ~~~
>constraints = h-bonds
>; Constrain bonds with hydrogen atoms
>
>constraints = all-bonds
>; Constrain all bonds
>
>constraints = h-angles
>; Constrain all bonds and additionally the angles that involve hydrogen atoms
>
>constraints = all-angles
>; Constrain all bonds and angles
>
>constraint-algorithm = LINKS
>; Use LINKS
>
>constraint-algorithm = SHAKE
>; Use SHAKE
>
>shake-tol = 0.0001
>;  Relative tolerance for SHAKE, default value is 0.0001.
> ~~~
> {: .file-content}
>SETTLE can be selected in the topology file:
>~~~
>[ settles ]
>; OW    funct   doh     dhh
>1       1       0.1     0.16333
>~~~
> {: .file-content}
> **NAMD**
>
>SHAKE and SETTLE constraint algorithms are implemented. They are selected via keywords in simulation input file.
> ~~~
>rigidBonds water
># Use SHAKE to constrain bonds with hydrogens in water molecules.
>
> rigidBonds all
># Use SHAKE to constrain bonds with hydrogens in all molecules.
>
>rigidBonds none
># Do not constrain bonds. This is the default.
>
>rigidTolerance 1.0e-8
># Stop iterations when all constrained bonds differ from the nominal bond length by less than this amount. Default value is 1.0e-8.
>
>rigidIterations 100
># The maximum number of iterations. If the bond lengths do not converge, a warning message is emitted. Default value is 100.
>
>rigidDieOnError on
># Exit and report an error if rigidTolerance is not achieved after rigidIterations. The deault value is on.
>
>useSettle on
># If rigidBonds are enabled then use the SETTLE algorithm to constrain waters. The default value is on.
> ~~~
> {: .file-content}
{: .callout}
