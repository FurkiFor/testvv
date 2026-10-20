"""Fluid library: physics (sim) + label + SFX for every substance.
mu   kinematic viscosity (m^2/s, explicit MPM solver)
fric wall friction (0 slip .. 4 sticky)
v0   drop speed of the fluid ball (ball mode)
rho  density relative to water (object mode buoyancy; steel = 7.8)
lin  linear drag on the steel ball (object mode, 1/s)
"""
FLUIDS = {
    "water":     dict(mu=0.0,    fric=0.0, v0=-2.0, rho=1.0,  lin=0.6,  label="Water",            sfx=["water1", "water2"]),
    "blood":     dict(mu=0.002,  fric=0.3, v0=-2.0, rho=1.06, lin=1.0,  label="Blood",            sfx=["blood1", "blood2"]),
    "honey":     dict(mu=0.05,   fric=4.0, v0=-1.7, rho=1.42, lin=22.0, label="Honey",            sfx=["honey1", "honey2"]),
    "copper":    dict(mu=0.01,   fric=0.8, v0=-1.9, rho=8.0,  lin=9.0,  label="Liquid Copper",    sfx=["copper2", "copper1"]),
    "oil":       dict(mu=0.004,  fric=0.3, v0=-2.0, rho=0.92, lin=7.0,  label="Oil",              sfx=["oil1", "water2"]),
    "mercury":   dict(mu=0.0,    fric=0.0, v0=-2.0, rho=13.5, lin=8.0,  label="Mercury",          sfx=["mercury1", "copper1"]),
    "milk":      dict(mu=0.0008, fric=0.1, v0=-2.0, rho=1.03, lin=0.8,  label="Milk",             sfx=["milk1", "water1"]),
    "slime":     dict(mu=0.03,   fric=3.0, v0=-1.8, rho=1.1,  lin=12.0, label="Slime",            sfx=["slime1", "honey2"]),
    "chocolate": dict(mu=0.035,  fric=3.0, v0=-1.8, rho=1.3,  lin=15.0, label="Melted Chocolate", sfx=["chocolate1", "honey1"]),
    "lava":      dict(mu=0.06,   fric=4.0, v0=-1.7, rho=2.6,  lin=25.0, label="Lava",             sfx=["lava1", "copper2"]),
}
K_BULK = 160.0          # weakly-compressible stiffness (c = sqrt(K) m/s)
STEEL_RHO = 7.8
