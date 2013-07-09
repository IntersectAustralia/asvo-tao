$(function() {

    var lc_id = function(bare_name) {
        return '#id_light_cone-' + bare_name;
    };

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
        var inv_mag = 1.0/Math.sqrt( x*x + y*y + z*z );
        x = x*inv_mag;
        y = y*inv_mag;
        z = z*inv_mag;
        var w = x*point_a[0] + y*point_a[1] + z*point_a[2];
        return [x, y, z, w];
    }

    var inside = function(point, plane) {
        return (point[0]*plane[0] + point[1]*plane[1] + point[2]*plane[2]) >= plane[3];
    }

//    from https://gist.github.com/ramn/3103615
    var cartesian_product = function(param_array) {
        if (!param_array || param_array.length < 1) {
            return [];
        }
        else {
            var head = param_array[0];
            var tail = param_array.slice(1);
            var result = [];
            for (var i = 0; i < head.length; i++) {
                var product_of_tail = cartesian_product(tail);
                if (product_of_tail && product_of_tail.length > 0) {
                    for (var j = 0; j < product_of_tail.length; j++) {
                        result.push([head[i]].concat(product_of_tail[j]));
                    }
                }
                else
                    result.push([head[i]]);
            }
            return result;
        }
    }

    var product = function(elem, repeats) {
        arr = [];
        for (var i = 0; i < repeats; i++) {
            arr.push(elem);
        }
        return cartesian_product(arr);
    }

    var box_plane_overlap = function(box_low, box_upp, plane) {
        for (perm in product([0, 1], 3)) {
            var point = [];
            for (var ii = 0; ii < box_low.length; ii++) {
                if (perm[ii]) {
                    point.push(box_upp[ii]);
                }
                else {
                    point.push(box_low[ii]);
                }
            }
            if (inside(point, plane)) {
                return true;
            }
        }
        return false;
    }

    var redshift_to_distance_func = function(z) {
        var omega_v = 0.73;
        var omega_m = 0.27;
        var omega_k = 1.0 - omega_m - omega_v;
        var z_sq = (1.0 + z)*(1.0 + z);
        var e_z = Math.sqrt(z_sq*(1.0 + z)*omega_m + z_sq*omega_k + omega_v);
        return 1.0/e_z;
    }

    // use comoving distance instead of transeverse comoving
    var redshift_to_distance = function(z) {
        alert('redshift_to_distance(' + z + ') starts');
        var hubble = 71.0;

//        TODO get integral by (Adaptive) Simpson's rule
        var val = integral(redshift_to_distance_func, 0.0, z, 0.5); //quad(redshift_to_distance_func, 0.0, z, (omega_m, omega_k, omega_v))[0];
        alert('integral =' + val);
        var dh = 300000.0/hubble;
        val = val*dh;
//        transverse
//        if (omega_k > 1e-8) {
//            val = Math.sinh(Math.sqrt(omega_k)*val/dh)*dh/Math.sqrt(omega_k);
//        else if (omega_k < -1e-8) {
//            val = math.sinh(math.sqrt(-omega_k)*val/dh )*dh/math.sqrt(omega_k)
        alert('redshift_to_distance(' + z + ') =' + val);
        return val;
    }

    var count_boxes = function(box_size, min_ra, max_ra, min_dec, max_dec, max_z) {
        var ra_rng = [Math.radians(min_ra), Math.radians(max_ra)];
        var dec_rng = [Math.radians(min_dec), Math.radians(max_dec)];
        var max_dist = redshift_to_distance(max_z);

        var ecs_mid = [mid(ra_rng), mid(dec_rng)];
        console.log('ecs_mid = ' + ecs_mid);
        var xyz = ecs_to_cart(ecs_mid[0], ecs_mid[1]); // returns [x, y, z]
        console.log('xyz = ' + xyz);
        var plane = [xyz[0], xyz[1], xyz[2], max_dist];
        console.log('plane = ' + plane);

        var poly = [];
        var zero = [0, 0, 0];
        poly.push(zero);
        var line = ecs_to_cart(ra_rng[0], dec_rng[0]);
        console.log('line 00: ' + line);
        poly.push(intersect(zero, line, plane));
        line = ecs_to_cart(ra_rng[1], dec_rng[0]);
        console.log('line 10: ' + line);
        poly.push(intersect(zero, line, plane));
        line = ecs_to_cart(ra_rng[0], dec_rng[1]);
        console.log('line 01: ' + line);
        poly.push(intersect(zero, line, plane));
        line = ecs_to_cart(ra_rng[1], dec_rng[1]);
        console.log('line 11: ' + line);
        poly.push(intersect(zero, line, plane));
        console.log('poly = ' + poly);

        var planes = [];
        planes.push(points_to_plane(poly[0], poly[1], poly[3]));
        planes.push(points_to_plane(poly[0], poly[3], poly[4]));
        planes.push(points_to_plane(poly[0], poly[4], poly[2]));
        planes.push(points_to_plane(poly[0], poly[2], poly[1]));
        planes.push(points_to_plane(poly[1], poly[2], poly[3]));
        console.log('planes = ' + planes);

        var max = [null, null, null];
        for (var i = 0; i < poly.length; i++) { //pnt in poly) {
            console.log('max: ' + max + ', pnt: poly[' + i + '] = ' + poly[i]);
            for (var ii = 0; ii < 3; ii++) {
                if (max[ii] == null || poly[i][ii] > max[ii]) {
                    max[ii] = poly[i][ii];
                }
            }
        }
        console.log('max: ' + max);

        var num_boxes = 0;
        var box = [0, 0, 0];
        while (box[0] < max[0]) {
            while (box[1] < max[1]) {
                while (box[2] < max[2]) {
                    if (Math.sqrt(box[0]*box[0] + box[1]*box[1] + box[2]*box[2]) <= max_dist) {
                        var box_upp = [box[0] + box_size, box[1] + box_size, box[2] + box_size];
                        console.log('box_upp = [' + box[0] + '+' + box_size + ', ' + box[1] + '+' + box_size + ', ' + box[2] + '+' + box_size + '] = ' + box_upp);
                        var okay = true;
                        for (var i = 0; i < planes.length; i++) { //plane in planes) {
                            var plane = planes[i];
                            if (!box_plane_overlap(box, box_upp, plane)) {
                                console.log('!box_plane_overlap(' + box + ', ' + box_upp + ', ' + plane + ')');
                                okay = false;
                                break;
                            }
                        }
                        if (okay){
                            num_boxes += 1;
                            console.log(num_boxes);
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
        console.log('count_boxes: ' + num_boxes);
        return num_boxes;
    }

    $(lc_id('ra_opening_angle') + ', ' + lc_id('dec_opening_angle') + ', ' + lc_id('redshift_max')).change(function(evt) {
        var box_size = window.simulation_box_size;   // size of the simulation box
        var min_ra = 0.0;                                                               // minimum right-ascension in degrees
        var max_ra = $(lc_id('ra_opening_angle')).val();                                // maximum right-ascension in degrees
        var min_dec = 0.0;                                                              // minimum declination in degrees
        var max_dec = $(lc_id('dec_opening_angle')).val();                              // maximum declination in degrees
        var max_z = $(lc_id('redshift_max')).val();                                     // maximum redshift

        if (max_ra != 0 && max_dec != 0 && max_z != 0) {
            var num_boxes = count_boxes(box_size, min_ra, max_ra, min_dec, max_dec, max_z);
            alert('Compute number of boxes in lightcone: ' + num_boxes);
            $(lc_id('max_job_size')).val(num_boxes);
        }
    });
});