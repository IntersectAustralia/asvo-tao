//
// Module: job_size
//
// Provide functions to estimate the job size based on various input parameters
//


/*
    JavaScript Example -  Lucio Tavernini

    Adaptive Simpson's Quadrature

    integral(f, a, b, errorBound) attempts to integrate f from
    a to b while keeping the asymptotic error estimate below
    errorBound using an adaptive implementation of Simpson's rule.

    The integrand can be unbounded and the limits can be infinite.
*/

        var integralError = false;
        var integralBound = 0;
        var ru = roundingUnit();

        //  Compute the rounding unit.
        function roundingUnit() {
          var ru = 1
          do {
            ru = 0.5*ru
            var value = 1 + ru
          }
          while (value != 1)
          return 2*ru
        }

        this.integral = function(f, a, b, errorBound) {
          var msg;
          //  Test parameters.
          msg = '';
          if (isNaN(a))
            msg = ' The lower limit is undefined.';
          if (isNaN(b))
            msg = msg + ' The upper limit is undefined.';
          if (isNaN(errorBound))
            msg = msg + ' The error bound is undefined.';
          else if (errorBound <= 0)
            msg = msg + ' The error bound must be positive.';
          else if (errorBound == Number.POSITIVE_INFINITY)
            msg = msg + ' The error bound cannot be +infinity.';
          if (msg != '') {
            if (document.all) document.cookie = msg;  //  Explorer
            else document.cookie += msg;              //  Netscape
        //    window.open("integralerror.html","","width=600," +
        //      "height=80,screenX=50,screenY=50,resizable=0," +
        //      "toolbar=0,directories=0," +
        //      "status=0,menubar=0,scrollbars=1");
            return NaN;
          }
          //  Return 0?
          if (a == b) return 0;
          //  Set globals.
          integralBound = errorBound;
          integralError = false;
          //  Compute.
          return _integral(f, a, b, errorBound);
        }

        function _integral(f, a, b, errorBound) {
          var left, right, max, mstart, j;
          var jend, step, m, m1, fa, fb, v1, v2;
          var error, bound, h, h6, value, result;
          if (integralError) return Math.NaN;

          //  Swap integration limits?
          if (a > b)  return -_integral(f, b, a, errorBound);

          //  Integrate over ]-infinity,+infinity[?
          if (a == Number.NEGATIVE_INFINITY &&
            b == Number.POSITIVE_INFINITY)
            return _integral(f, 0, b, 0.5*errorBound)
                     + _integral(f, a, 0, 0.5*errorBound);

          //  Integrate over [a,+infinity[?
          if (b == Number.POSITIVE_INFINITY) {
            h = 5;
            left = a;
            right = a + h;
            result = 0;
            do {
              value = _integral(f, left, right, errorBound/h);
              result += value;
              h = 2*h;
              left = right;
              right = left + h;
            }
            while (!isNaN(value) &&
              Math.abs(value) >= 0.5*errorBound/h && left < right)
            if (integralError) result = Number.NaN;
            return result;
          }

          //  Integrate over ]-infinity,b]?
          if (a == Number.NEGATIVE_INFINITY) {
            h = 5;
            left = b - h;
            right = b;
            result = 0;
            do {
              value = _integral(f, left, right, errorBound/h);
              result += value;
              h = 2*h;
              right = left;
              left = right - h;
            }
            while (!isNaN(value) &&
              Math.abs(value) >= 0.5*errorBound/h && left < right)
            if (integralError) result = Number.NaN;
            return result;
          }

          //  Integrate over [a,b].  Initialize.
          if (integralError) return Number.NaN;
          max = 1024;
          var x = new Array(max);
          var f1 = new Array(max);
          var f2 = new Array(max);
          var f3 = new Array(max);
          var v = new Array(max);
          step = 1;
          m = 1;
          bound = errorBound;
          value = 0;
          h = b - a;
          x[0] = a;
          f1[0] = f(a);
          f2[0] = f(0.5*(a + b));
          f3[0] = f(b);
          v[0] = h*(f1[0] + 4*f2[0] + f3[0])/6;
          do {
            //  Are we going to go forward or backward?
            if (step == -1) {
              //  Forward: j = m,...,max
              step = 1;
              j = m + 1;
              jend = max;
              m = 0;
              mstart = 0;
            }
            else {
              //  Backward: j = m,...,1
              step = -1;
              j = m - 1;
              jend = -1;
              m = max - 1;
              mstart = max - 1;
            }
            h = 0.5*h;
            h6 = h/6;
            bound = 0.5*bound;
            do {
              left = x[j];
              right = x[j] + 0.5*h;
              //  Complete loss of significance?
              if (left >= right) {
                alert('integral: Error 1');
                return value;
              }
              fa = f(x[j] + 0.5*h);
              fb = f(x[j] + 1.5*h);
              v1 = h6*(f1[j] + 4*fa + f2[j]);
              v2 = h6*(f2[j] + 4*fb + f3[j]);
              error = (v[j] - v1 - v2)/15;
              if (Math.abs(error) <= bound ||
                Math.abs(v1 + v2) < Math.abs(value)*ru) {
                value = ((v1 + v2) + value) - error;
              }
              else {
                if (integralError) return Number.NaN;
                //  Are we out of memory?
                if (m == j) {
                  left = x[j];
                  right = x[j] + 0.5*h;
                  //  Complete loss of significance?
                  if (left >= right) {
                    alert('integral: Error 2');
                    return value;
                  }
                  value += _integral(f, left, x[j] + 2*h, bound);
                }
                else {
                  //  No, we are not.
                  left = x[j];
                  right = x[j] + 0.125*h;
                  if (left >= right) {
                    msg = ' The error bound specified (' +
                          integralBound + ') is too small.';
                    if (document.all) document.cookie = msg;  //  Explorer
                    else document.cookie += msg;              //  Netscape
        //            window.open("integralerror.html","",
        //              "width=600,height=40," +
        //              "screenX=50,screenY=50," +
        //              "resizable=0,toolbar=0,directories=0," +
        //              "status=0,menubar=0,scrollbars=1");
                    integralError = true;
                    return Math.NaN;
                  }
                  m1 = m + step;
                  x[m] = x[j];
                  x[m1] = x[j] + h;
                  v[m] = v1;
                  v[m1] = v2;
                  f1[m] = f1[j];
                  f2[m] = fa;
                  f3[m] = f2[j];
                  f1[m1] = f2[j];
                  f2[m1] = fb;
                  f3[m1] = f3[j];
                  m += 2*step;
                }
              }
              j += step;
            }
            while (j != jend)
          }
          while (m != mstart)
          result = value;
          if (integralError) result = NaN;
          return result;
        }


    } // End: this.util


    // TODO: refactor helper methods into count_boxes local scope
    // count boxes code start


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
        return [x, y, z];
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
        if ((x*x + y*y + z*z) == 0) {
            throw new Error('Division by zero');
        }
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
        var perms = product([0, 1], 3);
        for (var i = 0; i < perms.length; i++) {
            var point = [];
            for (var ii = 0; ii < box_low.length; ii++) {
                if (perms[i][ii]) {
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

    // use Comoving Distance rather than Transeverse Comoving Distance
    var box_redshift_to_distance = function(z) {
        var hubble = 71.0;

//      get integral by Adaptive Simpson's rule
        var val = catalogue.modules.light_cone.util.integral(redshift_to_distance_func, 0.0, z, 0.5);
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
        var ra_rng = [Math.radians(min_ra), Math.radians(max_ra)];
        var dec_rng = [Math.radians(min_dec), Math.radians(max_dec)];
        var max_dist = box_redshift_to_distance(max_z);

        var ecs_mid = [mid(ra_rng), mid(dec_rng)];
        var xyz = ecs_to_cart(ecs_mid[0], ecs_mid[1]);
        var plane = [xyz[0], xyz[1], xyz[2], max_dist];

        var poly = [];
        var zero = [0, 0, 0];
        poly.push(zero);
        var line = ecs_to_cart(ra_rng[0], dec_rng[0]);
        poly.push(intersect(zero, line, plane));
        line = ecs_to_cart(ra_rng[1], dec_rng[0]);
        poly.push(intersect(zero, line, plane));
        line = ecs_to_cart(ra_rng[0], dec_rng[1]);
        poly.push(intersect(zero, line, plane));
        line = ecs_to_cart(ra_rng[1], dec_rng[1]);
        poly.push(intersect(zero, line, plane));

        var planes = [];
        planes.push(points_to_plane(poly[0], poly[1], poly[3]));
        planes.push(points_to_plane(poly[0], poly[3], poly[4]));
        planes.push(points_to_plane(poly[0], poly[4], poly[2]));
        planes.push(points_to_plane(poly[0], poly[2], poly[1]));
        planes.push(points_to_plane(poly[1], poly[2], poly[3]));

        var max = [null, null, null];
        for (var i = 0; i < poly.length; i++) {
            for (var ii = 0; ii < 3; ii++) {
                if (max[ii] == null || poly[i][ii] > max[ii]) {
                    max[ii] = poly[i][ii];
                }
            }
        }

        var num_boxes = 0;
        var box = [0, 0, 0];
        while (box[0] < max[0]) {
            while (box[1] < max[1]) {
                while (box[2] < max[2]) {
                    if (Math.sqrt(box[0]*box[0] + box[1]*box[1] + box[2]*box[2]) <= max_dist) {
                        var box_upp = [box[0] + box_size, box[1] + box_size, box[2] + box_size];
                        var okay = true;
                        for (var i = 0; i < planes.length; i++) {
                            var plane = planes[i];
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

    var esttime = function(x, p1, p2, p3) {
        return (p1 * x * x) + (p2 * x) + p3;
    }
    var job_size = function(estimated_count, max_boxes, p1, p2, p3) {
        return esttime(estimated_count, p1, p2, p3) / esttime(max_boxes, p1, p2, p3);
    }
