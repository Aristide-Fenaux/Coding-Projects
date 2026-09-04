# 2D Incompressible Navier–Stokes Solver

A 2D incompressible Navier–Stokes solver written from scratch in Python (no CFD libraries), simulating viscous flow around an immersed airfoil or cylinder using a discretised projection method.

## Overview

The incompressible Navier–Stokes equations don't have a closed-form solution for flow around a body, so this solver marches the velocity and pressure fields forward in time on a structured grid, using a predictor-corrector scheme to enforce incompressibility at every step. Neglecting body forces:

$$\begin{cases} \text{div}(\vec{u}) = 0 \\[6pt] \dfrac{\partial \vec{u}}{\partial t} + \text{grad}(\vec{u})\,\vec{u} = -\dfrac{1}{\rho}\text{grad}(p) + \nu\,\text{Lap}(\vec{u}) \end{cases}$$

where $\vec{u} = (u(x,y,t),\, v(x,y,t))$, $p$ = pressure, $\rho$ = fluid density, $\nu$ = fluid kinematic viscosity.

The solid body (an airfoil, or optionally a cylinder) is handled as an immersed boundary (a boolean mask over the grid)

## Features

- Fractional-step (projection) method: predict velocity, solve a pressure Poisson equation, then correct velocity to be divergence-free
- Immersed boundary via cell masking (cylinder and a NACA-style airfoil)
- Upwind differencing for advection (stability at higher Reynolds numbers), central differencing for viscous diffusion
- SOR-accelerated Gauss–Seidel pressure solver with a convergence tolerance and iteration cap
- Automatic CFL and viscous-stability checks before the simulation runs
- Numba-JIT-compiled inner loops so a fine grid runs faster
- Lift and drag computed from both pressure and skin friction contributions integrated over the immersed surface, non-dimensionalized into $C_L$ / $C_D$
- Dual-panel animation of the pressure field and velocity magnitude + streamlines, exported to video

## How it works

1. **Setup** : build the structured grid, define the immersed body as a boolean mask, initialize the velocity/pressure fields, and check the CFL and viscous-diffusion stability limits before running.
2. **Predictor step** : compute an intermediate velocity field $(u^*, v^*)$ from advection and viscous diffusion via explicit Euler, ignoring pressure.
3. **Pressure correction** : solve $\nabla^2 p = \frac{\nabla\cdot\mathbf{u}^*}{\Delta t}$ with SOR-accelerated Gauss–Seidel (Neumann on walls and the immersed surface, Dirichlet $p=0$ at the outlet).
4. **Velocity correction** : project $(u^*, v^*)$ onto a divergence-free field using the pressure gradient.
5. **Boundary conditions** : re-applied every step: Dirichlet inflow, Neumann outflow/free-stream, no-slip on the immersed body.
6. **Repeat** : saving periodic snapshots of pressure and velocity.
7. **Post-process** : integrate surface pressure and viscous stress to get lift/drag, plot $C_L$/$C_D$ time histories, and render the flow-field animation.

## Setup used for the featured results

| Parameter | Wing | Cylinder |
|---|---|---|
| Domain | 2 × 1, grid spacing 0.01 (201 × 101 points) | same |
| Body | NACA-style airfoil, chord 0.8, 10° angle of attack | diameter 0.4 |
| Reynolds number | 100 | 100 |
| Time step | 0.001 s, simulated to t = 5 s | 0.001 s, simulated to t = 3 s |

## Results

Flow field (pressure and velocity magnitude + streamlines) developing around the wing:

![Flow field animation around the wing](assets/simulation_wing_preview.gif)

*(downsampled preview — [full-resolution video](assets/simulation_wing_final.mp4))*

And around a cylinder, for comparison:

![Flow field animation around the cylinder](assets/simulation_cylinder_preview.gif)

*(downsampled preview — [full-resolution video](assets/simulation_cylinder_final.mp4))*

In both cases, a high-pressure stagnation region forms at the leading edge, and the wake visibly grows behind the body before settling, which is the expected qualitative behaviour for this kind of flow.

Lift and drag coefficients over time for the wing:

![Lift and drag coefficient full history](assets/lift_and_drag_coefficients_final.png)

![Lift and drag coefficient croped history](assets/lift_and_drag_coefficients.png)

| Metric | Value |
|---|---|
| Steady-state $C_D$ | 0.548 |
| Steady-state $C_L$ | 0.525 |
| Lift-to-drag ratio | 0.957 |

There exists a large transient spike in the first ~0.05s as the flow is started impulsively from rest, so both coefficients briefly swing to unphysical extremes before the wake develops and they settle onto the trend shown here. During these initial instants, the flow is in fact not divergence free. 

Lift gradually decreases over the simulation as the wake behind the wing grows and causes local flow reversal, while drag stays roughly constant, which consistent with viscous drag dominating over pressure-driven lift at this low speed and Reynolds number. An L/D close to 1 reflects the fact that real aircraft operate at Reynolds numbers orders of magnitude higher, where pressure effects dominate and L/D is much greater, explaining the poor performance of this wing. 

## Getting started

```bash
pip install -r requirements.txt
jupyter notebook NS-Sovler.ipynb
```

## Limitations & possible improvements

- Explicit Euler time-stepping is only conditionally stable, which caps the usable time step via the CFL and viscous-diffusion limits enforced at startup, but computationally less expensive. 
- The immersed boundary is a simple cell mask, so curved surfaces are only resolved to the grid spacing (a staircase approximation) rather than a sharper interface method
- Uniform grid with no local refinement near the body or in the boundary layer
- Results shown here are for a single Reynolds number — the solver could be swept across Reynolds number and angle of attack to build up a proper $C_L$/$C_D$ polar

## Author

Aristide Fenaux & Adrien Lassau