#!/usr/bin/env python

import math
from itertools import product
import argparse
from scipy.integrate import quad

def mid(rng):
    return rng[0] + 0.5*(rng[1] - rng[0])

def ecs_to_cart(ra, dec):
    dec = 0.5*math.pi - dec;
    sint = math.sin( dec )
    x = sint*math.cos( ra )
    y = sint*math.sin( ra )
    z = math.cos( dec )
    return x, y, z

def intersect(line_a, line_b, plane):
    denom = (line_b[0] - line_a[0])*plane[0] + \
        (line_b[1] - line_a[1])*plane[1] + \
        (line_b[2] - line_a[2])*plane[2]
    enumr = line_a[0]*plane[0] + line_a[1]*plane[1] + line_a[2]*plane[2] - plane[3]
    x = line_a[0] - (line_b[0] - line_a[0])*enumr/denom
    y = line_a[1] - (line_b[1] - line_a[1])*enumr/denom
    z = line_a[2] - (line_b[2] - line_a[2])*enumr/denom
    return x, y, z

def points_to_plane(point_a, point_b, point_c):
    ab = point_b[0] - point_a[0], point_b[1] - point_a[1], point_b[2] - point_a[2]
    ac = point_c[0] - point_a[0], point_c[1] - point_a[1], point_c[2] - point_a[2]
    x = -(ab[1]*ac[2] - ab[2]*ac[1])
    y = -(-ab[0]*ac[2] + ab[2]*ac[0])
    z = -(ab[0]*ac[1] - ab[1]*ac[0])
    inv_mag = 1.0/math.sqrt( x*x + y*y + z*z )
    x *= inv_mag
    y *= inv_mag
    z *= inv_mag
    w = x*point_a[0] + y*point_a[1] + z*point_a[2]
    return x, y, z, w

def inside(point, plane):
    return (point[0]*plane[0] + point[1]*plane[1] + point[2]*plane[2]) >= plane[3]

def box_plane_overlap(box_low, box_upp, plane):
    for perm in product([0, 1], repeat=3):
        point = []
        for ii in range(len(box_low)):
            if perm[ii]:
                point.append(box_upp[ii])
            else:
                point.append(box_low[ii])
        if inside(point, plane):
            return True
    return False

def redshift_to_distance_func(z, omega_m, omega_k, omega_v):
    z_sq = (1.0 + z)*(1.0 + z)
    e_z = math.sqrt(z_sq*(1.0 + z)*omega_m + z_sq*omega_k + omega_v)
    return 1.0/e_z

def redshift_to_distance(z):
    hubble = 71.0
    omega_v = 0.73
    omega_m = 0.27
    omega_k = 1.0 - omega_m - omega_v
    val = quad(redshift_to_distance_func, 0.0, z, (omega_m, omega_k, omega_v))[0]
    dh = 300000.0/hubble
    val *= dh
    if omega_k > 1e-8:
        val = math.sinh(math.sqrt(omega_k)*val/dh)*dh/math.sqrt(omega_k)
    elif omega_k < -1e-8:
        val = math.sinh(math.sqrt(-omega_k)*val/dh )*dh/math.sqrt(omega_k)
    return val

def count_boxes(box_size, min_ra, max_ra, min_dec, max_dec, max_z):
    ra_rng = (math.radians(min_ra), math.radians(max_ra))
    dec_rng = (math.radians(min_dec), math.radians(max_dec))
    max_dist = redshift_to_distance(max_z)

    ecs_mid = (mid(ra_rng), mid(dec_rng))
    x, y, z = ecs_to_cart(*ecs_mid)
    plane = (x, y, z, max_dist)

    poly = []
    zero = (0, 0, 0)
    poly.append(zero)
    line = ecs_to_cart(ra_rng[0], dec_rng[0])
    poly.append(intersect(zero, line, plane))
    line = ecs_to_cart(ra_rng[1], dec_rng[0])
    poly.append(intersect(zero, line, plane))
    line = ecs_to_cart(ra_rng[0], dec_rng[1])
    poly.append(intersect(zero, line, plane))
    line = ecs_to_cart(ra_rng[1], dec_rng[1])
    poly.append(intersect(zero, line, plane))

    planes = []
    planes.append(points_to_plane(poly[0], poly[1], poly[3]))
    planes.append(points_to_plane(poly[0], poly[3], poly[4]))
    planes.append(points_to_plane(poly[0], poly[4], poly[2]))
    planes.append(points_to_plane(poly[0], poly[2], poly[1]))
    planes.append(points_to_plane(poly[1], poly[2], poly[3]))

    max = [None, None, None]
    for pnt in poly:
        for ii in range(3):
            if max[ii] is None or pnt[ii] > max[ii]:
                max[ii] = pnt[ii]

    num_boxes = 0
    box = [0, 0, 0]
    while box[0] < max[0]:
        while box[1] < max[1]:
            while box[2] < max[2]:
                if math.sqrt(box[0]*box[0] + box[1]*box[1] + box[2]*box[2]) <= max_dist:
                    box_upp = (box[0] + box_size, box[1] + box_size, box[2] + box_size)
                    okay = True
                    for plane in planes:
                        if not box_plane_overlap(box, box_upp, plane):
                            okay = False
                            break
                    if okay:
                        num_boxes += 1
                box[2] += box_size
            box[2] = 0
            box[1] += box_size
        box[1] = 0
        box[0] += box_size

    return num_boxes

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute number of boxes in lightcone.')
    parser.add_argument('box_size', type=float, help='size of the simulation box')
    parser.add_argument('min_ra', type=float, help='minimum right-ascension in degrees')
    parser.add_argument('max_ra', type=float, help='maximum right-ascension in degrees')
    parser.add_argument('min_dec', type=float, help='minimum declination in degrees')
    parser.add_argument('max_dec', type=float, help='maximum declination in degrees')
    parser.add_argument('max_z', type=float, help='maximum redshift')
    args = parser.parse_args()

    num_boxes = count_boxes(args.box_size, args.min_ra, args.max_ra, args.min_dec, args.max_dec, args.max_z)

    print num_boxes
