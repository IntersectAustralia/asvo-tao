import sys, random, subprocess, shlex, math
from decimal import Decimal

class generator(object):

    def __init__(self, **kwargs):
        self.sfr_rng = kwargs.get('sfr_rng', (0.1, 1.0))
        self.metal_rng = kwargs.get('metal_rng', (0.0, 1.0))
        self.coldgas_rng = kwargs.get('coldgas_rng', (0.0, 1.0))
        self.tree_depth = kwargs.get('tree_depth', 10)
        self.tree_children = kwargs.get('tree_children', 2)

    def make_node(self, cur_depth=0):
        sfr = random.uniform(*self.sfr_rng)*1e-9
        metal = random.uniform(*self.metal_rng)
        cold_gas = metal + random.uniform(*self.coldgas_rng)
        return [
            sfr, metal, cold_gas,
            [self.make_node(cur_depth + 1) for ii in range(self.tree_children)] if cur_depth < (self.tree_depth - 1) else []
        ]

    def make_age(self, cur, max, prev, rng=(0.0, 1.0)):
        return [prev] + (self.make_age(cur + 1, max, prev + random.uniform(*rng), rng) if cur < (max - 1) else [])

    def rebin(self, node, depth, snap_ages, ssp_ages, age_mass, age_metal):
        oldest_age = snap_ages[-1]
        lo_age = oldest_age - snap_ages[-1 - depth]
        hi_age = oldest_age - snap_ages[-1 - depth - 1]
        lo_bin = self.find_bin(lo_age, ssp_ages)
        hi_bin = self.find_bin(hi_age, ssp_ages)
        # print '%d, %d'%(lo_bin, hi_bin)
        mass = (hi_age - lo_age)*node[0]*1e9
        prev_age = lo_age
        all_fracs = []
        # print 'Age range: %f - %f'%(lo_age, hi_age)
        while lo_bin <= hi_bin:
            if lo_bin == len(ssp_ages) - 1:
                upper = hi_age
            else:
                upper = min(0.5*(ssp_ages[lo_bin + 1] + ssp_ages[lo_bin]), hi_age)
            if upper <= prev_age:
                frac = 1.0
            else:
                frac = min((upper - prev_age)/(hi_age - lo_age), 1.0)
            all_fracs.append(frac)
            # print 'Overlapping bin: %d, %f, %f'%(lo_bin, upper, frac)
            # print '%d, %d, %f'%(depth, lo_bin, frac*mass)
            cur_mass = age_mass[lo_bin];
            age_mass[lo_bin] += frac*mass
            age_metal[lo_bin] = (cur_mass*age_metal[lo_bin] + frac*mass*(node[1]/node[2]))/age_mass[lo_bin];
            prev_age = upper
            lo_bin += 1
        # print sum(all_fracs)
        for child in node[3]:
            self.rebin(child, depth + 1, snap_ages, ssp_ages, age_mass, age_metal)

    def find_bin(self, val, bins):
        for ii in range(len(bins) - 1):
            if val < 0.5*(bins[ii + 1] + bins[ii]):
                return ii
        return len(bins) - 1

def generate(num_wavelengths, num_bpf_points, ll, lu, func, bp_func):
    random.seed()
    gen = generator()

    num_snap_ages = gen.tree_depth + 1
    num_ssp_ages = 6
    wavelength_range = (ll, lu)
    num_metals = 4

    root = gen.make_node()
    ssp_ages = gen.make_age(0, num_ssp_ages, 0)
    snap_ages = gen.make_age(0, num_snap_ages, 0)
    metals = gen.make_age(0, num_metals, 0)
    waves = [wavelength_range[0] + (Decimal(ii)/Decimal(num_wavelengths - 1))*(wavelength_range[1] - wavelength_range[0]) for ii in range(num_wavelengths)]

    # print ssp_ages
    # print snap_ages

    age_mass = [0.0]*num_ssp_ages
    age_metal = [0.0]*num_ssp_ages
    gen.rebin(root, 0, snap_ages, ssp_ages, age_mass, age_metal)
    # print age_mass
    # print age_metal

    ssp = [0.0]*num_wavelengths*num_metals*num_ssp_ages
    age_idx = random.randint(0, num_ssp_ages - 1)
    for ii in range(num_wavelengths):
        metal_idx = gen.find_bin(age_metal[age_idx], metals)
        while age_mass[age_idx] == 0.0:
            age_idx = (age_idx + 1)%num_ssp_ages
        pos = age_idx*num_wavelengths*num_metals + ii*num_metals + metal_idx
        ssp[pos] = Decimal(func(Decimal(waves[ii])))/Decimal(age_mass[age_idx])
        age_idx = (age_idx + 1)%num_ssp_ages

    with open('snapshots.dat', 'w') as out:
        out.write(str(len(snap_ages)) + '\n')
        for age in snap_ages:
            out.write(str(age) + '\n')

    with open('merger_tree.dat', 'w') as out:
        def _count(node):
            return 1 + sum([_count(c) for c in node[3]])
        size = _count(root)
        out.write(str(size) + '\n')
        def _write_snap(node, depth):
            out.write(str(gen.tree_depth - depth) + ' ')
            for c in node[3]:
                _write_snap(c, depth + 1)
        _write_snap(root, 0)
        out.write('\n')
        def _write_sfr(node):
            out.write(str(node[0]) + ' ')
            for c in node[3]:
                _write_sfr(c)
        _write_sfr(root)
        out.write('\n')
        def _write_bulge_sfr(node):
            out.write('0.0 ')
            for c in node[3]:
                _write_bulge_sfr(c)
        _write_bulge_sfr(root)
        out.write('\n')
        def _write_metal(node):
            out.write(str(node[1]) + ' ')
            for c in node[3]:
                _write_metal(c)
        _write_metal(root)
        out.write('\n')
        def _write_coldgas(node):
            out.write(str(node[2]) + ' ')
            for c in node[3]:
                _write_coldgas(c)
        _write_coldgas(root)
        out.write('\n')

    with open('ssp_ages.dat', 'w') as out:
        out.write(str(len(ssp_ages)) + '\n')
        for age in ssp_ages:
            out.write(str(age) + '\n')

    with open('ssp_metallicities.dat', 'w') as out:
        out.write(str(len(metals)) + '\n')
        for metal in metals:
            out.write(str(metal) + '\n')

    with open('ssp_wavelengths.dat', 'w') as out:
        for wave in waves:
            out.write(str(wave) + '\n')

    with open('ssp.dat', 'w') as out:
        for ii in range(len(ssp_ages)):
            for jj in range(len(waves)):
                pos = ii*num_wavelengths*num_metals + jj*num_metals
                for val in ssp[pos:pos + num_metals]:
                    out.write(str(val) + ' ')
                out.write('\n')

    with open('bandpass.dat', 'w') as out:
        out.write(str(num_bpf_points) + '\n')
        for ii in range(num_bpf_points):
            wave = wavelength_range[0] + (Decimal(ii)/Decimal(num_bpf_points - 1))*(wavelength_range[1] - wavelength_range[0])
            out.write(str(wave) + ' ' + str(bp_func(Decimal(wave))) + '\n')

def parse(stdout):
    f = stdout.find('=') + 1
    l = stdout.find('\n')
    denom = Decimal(stdout[f:l])
    f = stdout.find('=', f) + 1
    l = stdout.find('\n', l + 1)
    enum = Decimal(stdout[f:l])
    return (enum, denom)

def run_jobs(gen_cmd, repetitions):
    avg_enum = Decimal(0.0)
    avg_denom = Decimal(0.0)
    for ii in range(repetitions):
        subprocess.check_call(shlex.split(gen_cmd))
        stdout = subprocess.check_output('../../../build/debug/bin/analytic')
        enum, denom = parse(stdout)
        avg_enum += enum
        avg_denom += denom
    avg_enum /= Decimal(repetitions)
    avg_denom /= Decimal(repetitions)
    return avg_enum, avg_denom

def plot(results, name, xlabel):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    from matplotlib import rcParams
    rcParams['axes.labelsize'] = 9
    rcParams['xtick.labelsize'] = 9
    rcParams['ytick.labelsize'] = 9
    rcParams['legend.fontsize'] = 9
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = ['Computer Modern Roman']
    # rcParams['text.usetex'] = True

    golden_ratio = (math.sqrt(5.0) - 1.0)/2.0
    fig_width_in = 6.0
    fig_height_in = fig_width_in*golden_ratio
    fig_dims = [fig_width_in, fig_height_in]

    fig = plt.figure(figsize=fig_dims, dpi=80)
    ax = fig.add_subplot(111)
    x = [r[0] for r in results]
    y_enum = [(r[1] - r[2])/r[2] for r in results]
    y_denom = [(r[3] - r[4])/r[4] for r in results]

    ax.plot(x, y_enum, label='Enumerator')
    ax.plot(x, y_denom, label='Denominator')

    locs = ax.get_yticks()
    ax.set_yticklabels(map(lambda x: '%.1e'%x, locs))

    # ax.set_title('Percentage error vs. resolution')
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Percentage error')
    ax.legend(loc=7)
    plt.tight_layout()
    plt.savefig(name + '.pdf')

def run(analytic_enum, analytic_denom):
    resolutions = range(10, 1000, 100)
    lambda_ranges = [(1, 2), (1, 5), (1, 10), (1, 100), (1, 1000), (1, 10000), (1, 100000)]

    print 'Generating resolution results...'
    results = []
    for res in resolutions:
        ll = Decimal(1)
        lu = Decimal(100000)

        cmd = './generate.py %d %d %e %e'%(100 + res, res, ll, lu)
        enum, denom = run_jobs(cmd, 1)

        result = (res, enum, analytic_enum(ll, lu), denom, analytic_denom(ll, lu))
        results.append(result)
        # print '  %e, %e'%(result[1], result[2])
        print '  %e, %e'%((result[1] - result[2])/result[2], (result[3] - result[4])/result[4])

    plot(results, 'res_error', 'Wavelength/bandpass resolution')

    print 'Generating wavelength results...'
    results = []
    for ll, lu in lambda_ranges:
        ll = Decimal(ll)
        lu = Decimal(lu)

        cmd = './generate.py %d %d %e %e'%(1100, 1000, ll, lu)
        enum, denom = run_jobs(cmd, 1)

        result = (lu - ll, enum, analytic_enum(ll, lu), denom, analytic_denom(ll, lu))
        results.append(result)
        # print '  %e, %e'%(result[1], result[2])
        print '  %e, %e'%((result[1] - result[2])/result[2], (result[3] - result[4])/result[4])

    plot(results, 'wave_error', 'Wavelength range')
