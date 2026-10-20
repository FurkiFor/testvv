"""Container library — each container is an SDF (solid walls, floor excluded) + fill region.
The same SDF drives the physics collision AND the rendered mesh (marching cubes)."""
import numpy as np


def _len(*a):
    return np.sqrt(sum(x * x for x in a))


def sd_box(X, Y, Z, c, h, r=0.0):
    qx = np.abs(X - c[0]) - h[0] + r
    qy = np.abs(Y - c[1]) - h[1] + r
    qz = np.abs(Z - c[2]) - h[2] + r
    out = _len(np.maximum(qx, 0), np.maximum(qy, 0), np.maximum(qz, 0))
    inn = np.minimum(np.maximum(qx, np.maximum(qy, qz)), 0)
    return out + inn - r


def sd_cyl(X, Y, Z, cx, cy, z0, z1, rad, rr=0.0):
    dr = _len(X - cx, Y - cy) - rad + rr
    dz = np.abs(Z - (z0 + z1) / 2) - (z1 - z0) / 2 + rr
    out = _len(np.maximum(dr, 0), np.maximum(dz, 0))
    inn = np.minimum(np.maximum(dr, dz), 0)
    return out + inn - rr


def sd_frustum(X, Y, Z, z0, z1, r0, r1):
    """vertical truncated cone, approx SDF (exact enough near walls)"""
    t = np.clip((Z - z0) / (z1 - z0), 0, 1)
    rz = r0 + (r1 - r0) * t
    k = 1.0 / np.sqrt(1 + ((r1 - r0) / (z1 - z0)) ** 2)
    dr = (_len(X, Y) - rz) * k
    dz = np.abs(Z - (z0 + z1) / 2) - (z1 - z0) / 2
    out = _len(np.maximum(dr, 0), np.maximum(dz, 0))
    inn = np.minimum(np.maximum(dr, dz), 0)
    return out + inn


def sd_torus_x(X, Y, Z, c, R, r):
    """torus whose ring lies in the XZ plane (for side handles)"""
    q = _len(X - c[0], Z - c[2]) - R
    return _len(q, Y - c[1]) - r


# ---------------------------------------------------------------- definitions
def bathtub():
    def sdf(X, Y, Z):
        o = sd_box(X, Y, Z, (0, 0, 0.29), (0.85, 0.41, 0.29), 0.06)
        i = sd_box(X, Y, Z, (0, 0, 0.07 + 0.6), (0.77, 0.33, 0.6), 0.08)
        return np.maximum(o, -i)

    def fill(X, Y, Z):
        return (sd_box(X, Y, Z, (0, 0, 0.67), (0.77, 0.33, 0.6), 0.08) < -0.012) & (Z < 0.53)
    return dict(sdf=sdf, fill=fill, lo=(-0.86, -0.42, 0), hi=(0.86, 0.42, 0.59), rim=0.58,
                ball=(0.12, 0.0, 1.20, 0.21), material="ceramic")


def bowl():
    R, t, cz = 0.62, 0.055, 0.62

    def sdf(X, Y, Z):
        d = _len(X, Y, Z - cz)
        shell = np.maximum(np.abs(d - (R - t / 2)) - t / 2, Z - cz)
        foot = sd_cyl(X, Y, Z, 0, 0, 0.0, 0.075, 0.27, 0.015)
        return np.minimum(shell, foot)

    def fill(X, Y, Z):
        return (_len(X, Y, Z - cz) < R - t - 0.012) & (Z < cz - 0.045)
    return dict(sdf=sdf, fill=fill, lo=(-R, -R, 0), hi=(R, R, cz + 0.01), rim=cz,
                ball=(0.07, 0.0, 1.30, 0.22), material="ceramic")


def tumbler():
    def sdf(X, Y, Z):
        o = sd_cyl(X, Y, Z, 0, 0, 0.0, 1.0, 0.42, 0.02)
        i = sd_cyl(X, Y, Z, 0, 0, 0.09, 1.4, 0.345, 0.03)
        return np.maximum(o, -i)

    def fill(X, Y, Z):
        return (_len(X, Y) < 0.33) & (Z > 0.10) & (Z < 0.92)
    return dict(sdf=sdf, fill=fill, lo=(-0.42, -0.42, 0), hi=(0.42, 0.42, 1.0), rim=1.0,
                ball=(0.04, 0.0, 1.62, 0.19), material="glass")


def bucket():
    def sdf(X, Y, Z):
        o = sd_frustum(X, Y, Z, 0.0, 0.82, 0.36, 0.48)
        i = sd_frustum(X, Y, Z, 0.06, 1.3, 0.315, 0.315 + (0.48 - 0.36) * (1.24 / 0.82))
        return np.maximum(o, -i)

    def fill(X, Y, Z):
        rz = 0.315 + (0.12 / 0.82) * (Z - 0.06)
        return (_len(X, Y) < rz - 0.015) & (Z > 0.075) & (Z < 0.77)
    return dict(sdf=sdf, fill=fill, lo=(-0.48, -0.48, 0), hi=(0.48, 0.48, 0.83), rim=0.82,
                ball=(0.05, 0.0, 1.42, 0.2), material="plastic")


def pot():
    def sdf(X, Y, Z):
        o = sd_cyl(X, Y, Z, 0, 0, 0.0, 0.52, 0.56, 0.02)
        i = sd_cyl(X, Y, Z, 0, 0, 0.06, 1.0, 0.515, 0.02)
        body = np.maximum(o, -i)
        h1 = sd_torus_x(X, Y, Z, (0.62, 0, 0.44), 0.07, 0.022)
        h2 = sd_torus_x(X, Y, Z, (-0.62, 0, 0.44), 0.07, 0.022)
        return np.minimum(body, np.minimum(h1, h2))

    def fill(X, Y, Z):
        return (_len(X, Y) < 0.5) & (Z > 0.075) & (Z < 0.47)
    return dict(sdf=sdf, fill=fill, lo=(-0.72, -0.56, 0), hi=(0.72, 0.56, 0.53), rim=0.52,
                ball=(0.06, 0.0, 1.15, 0.22), material="steel")


def aquarium():
    def sdf(X, Y, Z):
        o = sd_box(X, Y, Z, (0, 0, 0.375), (0.7, 0.38, 0.375), 0.012)
        i = sd_box(X, Y, Z, (0, 0, 0.05 + 0.6), (0.648, 0.328, 0.6), 0.006)
        return np.maximum(o, -i)

    def fill(X, Y, Z):
        return (sd_box(X, Y, Z, (0, 0, 0.65), (0.648, 0.328, 0.6)) < -0.012) & (Z < 0.70)
    return dict(sdf=sdf, fill=fill, lo=(-0.7, -0.38, 0), hi=(0.7, 0.38, 0.75), rim=0.75,
                ball=(0.1, 0.0, 1.35, 0.21), material="glass")


CONTAINERS = dict(bathtub=bathtub, bowl=bowl, tumbler=tumbler, bucket=bucket, pot=pot, aquarium=aquarium)


def get(name):
    return CONTAINERS[name]()
