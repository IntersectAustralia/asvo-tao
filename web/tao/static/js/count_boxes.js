jQuery(document).ready(function($) {

    var lc_id = function(bare_name) {
        return '#id_light_cone-' + bare_name;
    };

    // convert from degrees to radians
    Math.radians = function(degrees) {
        return degrees * Math.PI / 180;
    };

    var mid = function(rng) {
        return rng[0] + 0.5*(rng[1] - rng[0]);
    }

    var ecs_to_cart = function(ra, dec) {
        dec = 0.5*Math.PI - dec;
        var sint = Math.sin( dec );
        var x = sint*Math.cos( ra );
        var y = sint*Math.sin( ra );
        var z = Math.cos( dec );
        return [x, y, z]; // need to use either an array or object like dict
    }

    var intersect = function(line_a, line_b, plane) {
        var denom = (line_b[0] - line_a[0])*plane[0] +
                    (line_b[1] - line_a[1])*plane[1] +
                    (line_b[2] - line_a[2])*plane[2];
        var enumr = line_a[0]*plane[0] + line_a[1]*plane[1] + line_a[2]*plane[2] - plane[3];
        var x = line_a[0] - (line_b[0] - line_a[0])*enumr/denom;
        var y = line_a[1] - (line_b[1] - line_a[1])*enumr/denom;
        var z = line_a[2] - (line_b[2] - line_a[2])*enumr/denom;
        return [x, y, z];
    }

    var points_to_plane = function(point_a, point_b, point_c) {
        var ab = [point_b[0] - point_a[0], point_b[1] - point_a[1], point_b[2] - point_a[2]];
        var ac = [point_c[0] - point_a[0], point_c[1] - point_a[1], point_c[2] - point_a[2]];
        var x = -(ab[1]*ac[2] - ab[2]*ac[1]);
        var y = -(-ab[0]*ac[2] + ab[2]*ac[0]);
        var z = -(ab[0]*ac[1] - ab[1]*ac[0]);
        var inv_mag = 1.0/math.sqrt( x*x + y*y + z*z );
        x = x*inv_mag;
        y = y*inv_mag;
        z = z*inv_mag;
        var w = x*point_a[0] + y*point_a[1] + z*point_a[2];
        return [x, y, z, w];
    }

    var inside = function(point, plane) {
        return (point[0]*plane[0] + point[1]*plane[1] + point[2]*plane[2]) >= plane[3];
    }

    var box_plane_overlap = function(box_low, box_upp, plane) {
//        FIXME cartesian product of this
//        for (perm in product([0, 1], repeat=3)) {
            var point = [];
            for (var ii = 0; ii < len(box_low); ii++) {
                if (perm[ii]) {
                    point.append(box_upp[ii]);
                }
                else {
                    point.append(box_low[ii]);
                }
            }
            if (inside(point, plane)) {
                return true;
            }
//        }
        return false;
    }

    var redshift_to_distance_func = function(z, omega_m, omega_k, omega_v) {
        var z_sq = (1.0 + z)*(1.0 + z);
        var e_z = Math.sqrt(z_sq*(1.0 + z)*omega_m + z_sq*omega_k + omega_v);
        return 1.0/e_z;
    }

    // use comoving distance instead of transeverse comoving
    var redshift_to_distance = function(z) {
        var hubble = 71.0;
        var omega_v = 0.73;
        var omega_m = 0.27;
        var omega_k = 1.0 - omega_m - omega_v;

//        TODO get integral by Simpson's rule
        var val = quad(redshift_to_distance_func, 0.0, z, (omega_m, omega_k, omega_v))[0];
        var dh = 300000.0/hubble;
        val = val*dh;
//        transverse
//        if (omega_k > 1e-8) {
//            val = Math.sinh(Math.sqrt(omega_k)*val/dh)*dh/Math.sqrt(omega_k);
//        else if (omega_k < -1e-8) {
//            val = math.sinh(math.sqrt(-omega_k)*val/dh )*dh/math.sqrt(omega_k)
        return val;
    }

    var count_boxes = function(box_size, min_ra, max_ra, min_dec, max_dec, max_z) {
        var ra_rng = (Math.radians(min_ra), Math.radians(max_ra));
        var dec_rng = (Math.radians(min_dec), Math.radians(max_dec));
        var max_dist = redshift_to_distance(max_z);

        var ecs_mid = (mid(ra_rng), mid(dec_rng));
        var xyz = ecs_to_cart(ecs_mid); // returns [x, y, z]
        var plane = (xyz[0], xyz[1], xyz[2], max_dist);

        var poly = [];
        var zero = (0, 0, 0);
        poly.append(zero);
        var line = ecs_to_cart(ra_rng[0], dec_rng[0]);
        poly.append(intersect(zero, line, plane));
        line = ecs_to_cart(ra_rng[1], dec_rng[0]);
        poly.append(intersect(zero, line, plane));
        line = ecs_to_cart(ra_rng[0], dec_rng[1]);
        poly.append(intersect(zero, line, plane));
        line = ecs_to_cart(ra_rng[1], dec_rng[1]);
        poly.append(intersect(zero, line, plane));

        var planes = [];
        planes.append(points_to_plane(poly[0], poly[1], poly[3]));
        planes.append(points_to_plane(poly[0], poly[3], poly[4]));
        planes.append(points_to_plane(poly[0], poly[4], poly[2]));
        planes.append(points_to_plane(poly[0], poly[2], poly[1]));
        planes.append(points_to_plane(poly[1], poly[2], poly[3]));

        var max = [null, null, null];
        for (pnt in poly) {
            for (var ii = 0; ii < 3; ii++) {
                if (max[ii] == null || pnt[ii] > max[ii]) {
                    max[ii] = pnt[ii];
                }
            }
        }

        var num_boxes = 0;
        var box = [0, 0, 0];
        while (box[0] < max[0]) {
            while (box[1] < max[1]) {
                while (box[2] < max[2]) {
                    if (Math.sqrt(box[0]*box[0] + box[1]*box[1] + box[2]*box[2]) <= max_dist) {
                        var box_upp = (box[0] + box_size, box[1] + box_size, box[2] + box_size);
                        var okay = true;
                        for (plane in planes) {
                            if (!box_plane_overlap(box, box_upp, plane)) {
                                okay = false;
                                break;
                            }
                        }
                        if (okay){
                            num_boxes += 1;
                        }
                    }
                    box[2] += box_size;
                }
                box[2] = 0;
                box[1] += box_size;
            }
            box[1] = 0;
            box[0] += box_size;
        }

        return num_boxes;
    }

    (function() {
        var box_size = $(lc_id('number_of_light_cones')).data("simulation-box-size"); //size of the simulation box
        var min_ra = 0.0; // minimum right-ascension in degrees
        var max_ra = $(lc_id('ra_opening_angle')).val(); // maximum right-ascension in degrees
        var min_dec = 0.0; // minimum declination in degrees
        var max_dec = $(lc_id('dec_opening_angle')).val(); // maximum declination in degrees
        var max_z = $(lc_id('redshift_max')).val(); // maximum redshift

        var num_boxes = count_boxes(box_size, min_ra, max_ra, min_dec, max_dec, max_z);

        console.log(num_boxes);
    })();
});