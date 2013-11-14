#!/usr/bin/env python

import random

def func(x):
    return 1.0

class generator(object):

    def __init__(self, **kwargs):
        self.sfr_rng = kwargs.get('sfr_rng', (0.1, 1.0))
        self.metal_rng = kwargs.get('metal_rng', (0.0, 1.0))
        self.coldgas_rng = kwargs.get('coldgas_rng', (0.0, 1.0))
        self.tree_depth = kwargs.get('tree_depth', 10)
        self.tree_children = kwargs.get('tree_children', 2)

    def make_node(self, cur_depth=0):
        sfr = random.uniform(*self.sfr_rng)
        metal = random.uniform(*self.metal_rng)
        cold_gas = metal + random.uniform(*self.coldgas_rng)
        return [
            sfr, metal, cold_gas,
            [self.make_node(cur_depth + 1) for ii in range(self.tree_children)] if cur_depth < (self.tree_depth - 1) else []
        ]

    def make_age(self, cur, max, prev, rng=(0.0, 1.0)):
        return [prev] + (self.make_age(cur + 1, max, prev + random.uniform(*rng), rng) if cur < max else [])

    def rebin(self, node, depth, snap_ages, ssp_ages, age_mass, age_metal):
        oldest_age = snap_ages[-1]
        lo_age = snap_ages[-1 - depth] - oldest_age
        hi_age = snap_ages[-1 - depth - 1] - oldest_age
        lo_bin = self.find_bin(lo_age, ssp_ages)
        hi_bin = self.find_bin(hi_age, ssp_ages)
        mass = (hi_age - lo_age)*node[0]
        prev_age = lo_age
        all_fracs = []
        # print 'Age range: %f - %f'%(lo_age, hi_age)
        while lo_bin <= hi_bin:
            upper = min(0.5*(ssp_ages[lo_bin + 1] + ssp_ages[lo_bin]), hi_age)
            if upper <= prev_age:
                frac = 1.0
            else:
                frac = min((upper - prev_age)/(hi_age - lo_age), 1.0)
            all_fracs.append(frac)
            # print 'Overlapping bin: %d, %f, %f'%(lo_bin, upper, frac)
            age_mass[lo_bin] += frac*mass
            age_metal[lo_bin] = 1.0
            prev_age = 0.5*(ssp_ages[lo_bin + 1] + ssp_ages[lo_bin])
            lo_bin += 1
        # print sum(all_fracs)
        for child in node[3]:
            self.rebin(child, depth + 1, snap_ages, ssp_ages, age_mass, age_metal)

    def find_bin(self, val, bins):
        for ii in range(len(bins) - 1):
            if val < 0.5*(bins[ii + 1] + bins[ii]):
                break
        return ii

if __name__ == '__main__':

    random.seed()

    gen = generator()

    num_snap_ages = gen.tree_depth + 1
    num_ssp_ages = 10
    num_wavelengths = num_ssp_ages
    wavelength_range = (1.0, 2.0)
    num_metals = 3

    root = gen.make_node()
    ssp_ages = gen.make_age(0, num_ssp_ages, 0)
    snap_ages = gen.make_age(0, num_snap_ages, 0)
    snap_ages.reverse()
    metals = gen.make_age(0, num_metals, 0)
    waves = [wavelength_range[0] + (float(ii)/float(num_wavelengths - 1))*(wavelength_range[1] - wavelength_range[0]) for ii in range(num_wavelengths)]

    age_mass = [0.0]*num_ssp_ages
    age_metal = [0.0]*num_ssp_ages
    gen.rebin(root, 0, snap_ages, ssp_ages, age_mass, age_metal)

    ssp = [1e10]*num_wavelengths*num_metals*num_ssp_ages
    age_idx = 0 #random.randint(0, num_ssp_ages - 1)
    for ii in range(num_wavelengths):
        metal_idx = gen.find_bin(age_metal[age_idx], metals)
        while age_mass[age_idx] == 0.0:
            age_idx = (age_idx + 1)%num_ssp_ages
        pos = age_idx*num_wavelengths*num_metals + ii*num_metals + metal_idx
        ssp[pos] = func(waves[ii])/age_mass[age_idx]
        age_idx = (age_idx + 1)%num_ssp_ages

    with open('snapshots.dat', 'w') as out:
        out.write(str(len(snap_ages)) + '\n')
        for age in snap_ages:
            out.write(str(age) + '\n')

    with open('ssp_ages.dat', 'w') as out:
        out.write(str(len(ssp_ages)) + '\n')
        for age in ssp_ages:
            out.write(str(age) + '\n')

    with open('metallicities.dat', 'w') as out:
        out.write(str(len(metals)) + '\n')
        for metal in metals:
            out.write(str(metal) + '\n')

    with open('ssp.dat', 'w') as out:
        for ii in range(len(ssp_ages)):
            for jj in range(len(waves)):
                pos = ii*num_wavelengths*num_metals + jj*num_metals
                for val in ssp[pos:pos + num_metals]:
                    out.write(str(val) + ' ')
                out.write('\n')
