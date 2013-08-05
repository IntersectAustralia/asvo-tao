
var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};


catalogue.modules.light_cone = function ($) {

    this.lc_output_props_widget = new TwoSidedSelectWidget(lc_id('output_properties'), true);

    function get_widget() {
        return catalogue.modules.light_cone.lc_output_props_widget;
    }

    // KO ViewModel
    var vm = {
        catalogue_geometry : ko.observable(),
        ra_opening_angle : ko.observable(),
        dec_opening_angle : ko.observable()
    }


    this.util = function() {


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


    }


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

    var check_number_of_boxes = function(num_boxes) {
        var dataset_id = $(lc_id('galaxy_model')).val();
        var job_size_p1 = parseFloat( $(lc_id('galaxy_model option:selected')).attr('data-job_size_p1') );
        var job_size_p2 = parseFloat( $(lc_id('galaxy_model option:selected')).attr('data-job_size_p2') );
        var job_size_p3 = parseFloat( $(lc_id('galaxy_model option:selected')).attr('data-job_size_p3') );
        var max_job_box_count = parseInt( $(lc_id('galaxy_model option:selected')).attr('data-max_job_box_count') );
        var job_size_percentage = job_size(num_boxes, max_job_box_count, job_size_p1, job_size_p2, job_size_p3)*100;
        if (job_size_percentage > 100) { //num_boxes > max_job_box_count) {
             $('#max_job_size').addClass('job_too_large_error');
             $('#max_job_size').text('Estimated job size: ' + job_size_percentage.toFixed(0) + '%. Note this exceeds the maximum allowed size, please reduce the light-cone size (RA, Dec, Redshift range).');
        } else {
             $('#max_job_size').removeClass('job_too_large_error');
             $('#max_job_size').text('Estimated job size: ' + job_size_percentage.toFixed(0) + '%'); //num_boxes + ' / ' + max_job_box_count);
        }
    }



    // count boxes code end

    var display_maximum_number_light_cones = function ($field, msg) {
        var $enclosing = $field.closest('label.control-label');
        $enclosing.find('span.lc_number-inline').remove();
        if (msg == null) return;
        $field.after('<span class="lc_number-inline"></span>');
        $enclosing.find('span.lc_number-inline').text(msg);
        show_tab($enclosing, 0);
    }


    var cache_initial_data = function() {
        var $to = $(lc_id('output_properties'));
        $to.find('option[selected="selected"]').each(function () {
            // console.log($(this).attr('value'));
            var current = [];
            var pseudo_json = [];
            var $this = $(this);
            var item = {
                pk: $this.attr('value'),
                fields: {
                    label: $this.text()
                }
            };
            pseudo_json.push(item);
            if ($this.attr('selected')) {
                current.push(item.pk);
            }
            // console.log(pseudo_json);
            get_widget().cache_store(pseudo_json);
        });
    }


    var update_output_options = function () {
        // cache_initial_data();
        var data_set_id = $(lc_id('galaxy_model')).find(':selected').attr('value');
        var $to = $(lc_id('output_properties'));
        var $from = $(lc_id('output_properties_from'));
        var current = $to.val(); // in string format
        $to.empty();
        $from.empty();
        $.ajax({
            url: TAO_JSON_CTX + 'output_choices/' + data_set_id,
            dataType: "json",
            error: function () {
                alert("Couldn't get output choices");
            },
            success: function (data, status, xhr) {
                get_widget().cache_store(data);
                catalogue.modules.record_filter.update_filter_options.output_props = true;
                // catalogue.modules.record_filter.update_filter_options.output_props = $('#RF_BOUND').val() == false;
                get_widget().display_selected(current, true);
            }
        });
    }


    var format_redshift = function (redshift_string) {
        var redshift = parseFloat(redshift_string);
        var whole_digit = parseInt(redshift).toString().length;
        return redshift.toFixed(Math.max(5 - whole_digit, 0));
    };


    var update_snapshot_options = function () {
        var simulation_id = $(lc_id('dark_matter_simulation')).val();
        var galaxy_model_id = $(lc_id('galaxy_model')).find(':selected').attr('data-galaxy_model_id');
        var $snapshot = $(lc_id('snapshot'));
        var current = $snapshot.val();
        $snapshot.empty();

        $.ajax({
            url: TAO_JSON_CTX + 'snapshots/' + simulation_id + ',' + galaxy_model_id,
            dataType: "json",
            error: function () {
                alert("Couldn't get snapshots");
            },
            success: function (data, status, xhr) {
                for (i = 0; i < data.length; i++) {
                    var item = data[i];
                    $option = $('<option/>');
                    $option.attr('value', item.pk);
                    // Redshift Formatting:
                    // The age of the universe as a function of redshift is 1 / (1 + z) where z is the redshift.
                    // So z=0 is the present, and z=Infinity is the Big Bang.
                    // This is a non-linear relationship with more variation at smaller z values.
                    // To present figures that are easy to read and have sensible precision, redshift will be displayed with up to 5 decimals.
                    $option.html(format_redshift(item.fields.redshift));
                    if (item.pk == current) {
                        $option.attr('selected', 'selected');
                    }
                    $snapshot.append($option);
                }
                // initial_snapshot = 0;

                //test
                $(lc_id('snapshot')).change();
            }
        });
    };


    var show_galaxy_model_info = function (galaxy_model_id) {
        var $galaxy_model_info = $('div.galaxy-model-info');
        if (galaxy_model_id === 0) {
            $galaxy_model_info.hide();
            return;
        }
        $.ajax({
            url: TAO_JSON_CTX + 'galaxy_model/' + galaxy_model_id,
            dataType: "json",
            error: function () {
                $galaxy_model_info.hide();
                alert("Couldn't get data for requested galaxy model");
            },
            success: function (data, status, xhr) {
                $('div.galaxy-model-info .name').html(data.fields.name);
                $('div.galaxy-model-info .details').html(data.fields.details);
                $galaxy_model_info.show();
                catalogue.util.fill_in_summary('light_cone', 'galaxy_model', data.fields.name);
                catalogue.util.fill_in_summary('light_cone', 'galaxy_model_description', '<br><b>' + data.fields.name + ':</b><br>' + data.fields.details);
            }
        });
    };


    var update_galaxy_model_options = function (simulation_id) {
        var $galaxy_model = $(lc_id('galaxy_model'));
        if (simulation_id === 0) {
            $galaxy_model.empty();
            $galaxy_model.change();
            return;
        }
        $.ajax({
            url: TAO_JSON_CTX + 'galaxy_models/' + simulation_id,
            dataType: "json",
            error: function () {
                $galaxy_model.empty();
                $galaxy_model.change();
                alert("Couldn't get data for requested simulation");
            },
            success: function (data, status, xhr) {
                var initial_data_set_id = $galaxy_model.val();
                $galaxy_model.empty();
                for (i = 0; i < data.length; i++) {
                    item = data[i];
                    $option = $('<option/>');
                    $option.attr('value', item.id);
                    $option.attr('data-galaxy_model_id', item.galaxy_model_id);
                    $option.attr('data-job_size_p1', item.job_size_p1);
                    $option.attr('data-job_size_p2', item.job_size_p2);
                    $option.attr('data-job_size_p3', item.job_size_p3);
                    $option.attr('data-max_job_box_count', item.max_job_box_count);
                    if (item.id == initial_data_set_id) {
                        $option.attr('selected', 'selected');
                    }
                    $option.html(item.name);
                    $galaxy_model.append($option);
                }
                $galaxy_model.change();
            }
        });
    };


    var show_simulation_info = function (simulation_id) {
        $.ajax({
            url: TAO_JSON_CTX + 'simulation/' + simulation_id,
            dataType: "json",
            error: function () {
                $('div.simulation-info').hide();
                alert("Couldn't get data for requested simulation");
            },
            success: function (data, status, xhr) {
                $('div.simulation-info .name').html(data.fields.name);
                $('div.simulation-info .details').html(data.fields.details);
                $('div.simulation-info').show();
                catalogue.util.fill_in_summary('light_cone', 'simulation', data.fields.name);
                catalogue.util.fill_in_summary('light_cone', 'simulation_description', '<br><b>' + data.fields.name + ':</b><br>' + data.fields.details);
                $(lc_id('number_of_light_cones')).data("simulation-box-size", data.fields.box_size);
            }
        });
    };


    var fill_in_ra_dec_in_summary = function () {
        var ra_opening_angle_value = vm.ra_opening_angle();
        var dec_opening_angle_value = vm.dec_opening_angle();
        if (!ra_opening_angle_value && !dec_opening_angle_value) {
            catalogue.util.fill_in_summary('light_cone', 'ra_opening_angle', '');
            catalogue.util.fill_in_summary('light_cone', 'dec_opening_angle', '');
        } else if (!ra_opening_angle_value) {
            catalogue.util.fill_in_summary('light_cone', 'ra_opening_angle', '');
            catalogue.util.fill_in_summary('light_cone', 'dec_opening_angle', 'Dec: ' + dec_opening_angle_value + '&deg;<br>');
        } else if (!dec_opening_angle_value) {
            catalogue.util.fill_in_summary('light_cone', 'ra_opening_angle', 'RA: ' + ra_opening_angle_value + '&deg; <br>');
            catalogue.util.fill_in_summary('light_cone', 'dec_opening_angle', '');
        } else {
            catalogue.util.fill_in_summary('light_cone', 'ra_opening_angle', 'RA: ' + ra_opening_angle_value + '&deg;, ');
            catalogue.util.fill_in_summary('light_cone', 'dec_opening_angle', 'Dec: ' + dec_opening_angle_value + '&deg;<br>');
        }
    }


    var fill_in_redshift_in_summary = function () {
        var redshift_max_value = $(lc_id('redshift_max')).val();
        var redshift_min_value = $(lc_id('redshift_min')).val();
        if (!redshift_min_value && !redshift_max_value) {
            catalogue.util.fill_in_summary('light_cone', 'redshift_min', '')
            catalogue.util.fill_in_summary('light_cone', 'redshift_max', '')
        } else if (!redshift_min_value) {
            catalogue.util.fill_in_summary('light_cone', 'redshift_min', '')
            catalogue.util.fill_in_summary('light_cone', 'redshift_max', 'Redshift: z &le; ' + redshift_max_value);
        } else if (!redshift_max_value) {
            catalogue.util.fill_in_summary('light_cone', 'redshift_min', 'Redshift: ' + redshift_min_value + ' &le; z');
            catalogue.util.fill_in_summary('light_cone', 'redshift_max', '')
        } else {
            catalogue.util.fill_in_summary('light_cone', 'redshift_min', 'Redshift: ' + redshift_min_value + ' &le; z &le; ');
            catalogue.util.fill_in_summary('light_cone', 'redshift_max', redshift_max_value);
        }
    }


    // Max's algorithm for calculating the maximum allowed number of unique light-cones
    //    /**
    //     * Convert redshift to distance
    //     * @param z redshift
    //     * @return comoving distance
    //     */
    var redshift_to_distance = function (z) {
        var n = 1000;

        var c = 299792.458;
        var H0 = 100.0;
        var h = H0 / 100;
        var WM = 0.25;
        var WV = 1.0 - WM - 0.4165 / (H0 * H0);
        var WR = 4.165E-5 / (h * h);
        var WK = 1 - WM - WR - WV;
        var az = 1.0 / (1 + 1.0 * z);
        var DTT = 0.0;
        var DCMR = 0.0;
        for (var i = 0; i < n; i++) {
            var a = az + (1 - az) * (i + 0.5) / n;
            var adot = Math.sqrt(WK + (WM / a) + (WR / (a * a)) + (WV * a * a));
            DTT = DTT + 1.0 / adot;
            DCMR = DCMR + 1.0 / (a * adot);
        }
        DTT = (1. - az) * DTT / n;
        DCMR = (1. - az) * DCMR / n;
        var d = (c / H0) * DCMR;

        return d;
    }


    //    /**
    //     * Compute the maximum number of unique cones available for selected parameters
    //     */
    var get_number_of_unique_light_cones = function () {
        var ra = vm.ra_opening_angle();
        var dec = vm.dec_opening_angle();
        var redshift_min = $(lc_id('redshift_min')).val();
        var redshift_max = $(lc_id('redshift_max')).val();

        var alfa1 = parseFloat(ra);
        var box_side = $(lc_id('number_of_light_cones')).data("simulation-box-size");
        var d1 = redshift_to_distance(parseFloat(redshift_min));
        var d2 = redshift_to_distance(parseFloat(redshift_max));
        var beta1;
        for (beta1 = alfa1; beta1 < 90; beta1 = beta1 + 0.01) {
            if ((d2 - box_side) * Math.sin((Math.PI / 180) * (beta1 + alfa1)) <= d2 * Math.sin((Math.PI / 180) * beta1)) {
                break;
            }
        }
        var hv = Math.floor(d2 * Math.sin((Math.PI / 180) * (alfa1 + beta1)) - d1 * Math.sin((Math.PI / 180) * (alfa1 + beta1)));

        var hh = 2 * d2 * Math.sin((Math.PI / 180) * (parseFloat(dec)) / 2);

        var nv = Math.floor(box_side / hv);
        var nh = Math.floor(box_side / hh);
        var n = nv * nh;

        return n;
    }


    var spinner_check_value = function (new_value) {
        var ra = vm.ra_opening_angle();
        var dec = vm.dec_opening_angle();
        var redshift_min = $(lc_id('redshift_min')).val();
        var redshift_max = $(lc_id('redshift_max')).val();
        var $spinner = $(lc_id('number_of_light_cones')).closest('span');
        var maximum = $(lc_id('number_of_light_cones')).data('spin-max');
        if (new_value <= 1) {
            if (new_value <= 0) {
                catalogue.util.show_error($spinner, "Please provide a positive number of light-cones");
                catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'Negative number of light-cones is invalid');
                return false;
            }
        }

        if (maximum > 0) {
            $(lc_id('number_of_light_cones')).spinner("option", "max", maximum);
            if (new_value >= maximum) {
                if (new_value > maximum) {
                    catalogue.util.show_error($spinner, "The maximum is " + maximum);
                    catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'Number of light cones selected exceeds the maximum');
                    return false;
                }
            }

        } else if (ra != "" && dec != "" && redshift_min != "" && redshift_max != "") {
            catalogue.util.show_error($spinner, "Selection parameters can't be used to generate unique light-cones");
            catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'An invalid number of light cones is selected');
            return false;
        }

        catalogue.util.show_error($spinner, null);
        catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', new_value + " " + $("input[name='light_cone-light_cone_type']:checked").val() + " light cones");
        return true;
    }


    var calculate_max_number_of_cones = function () {
        function spinner_set_max(maximum) {
            $spinner_label = $('label[for=id_light_cone-number_of_light_cones]');
            if (isNaN(maximum) || maximum <= 0 || !isFinite(maximum)) {
                $(lc_id('number_of_light_cones')).spinner("disable");
                $(lc_id('number_of_light_cones')).data("spin-max", 0);
                $spinner_label.html("Select the number of light-cones:*");
                catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', 'Invalid light-cone parameters selected');
                return false;
            } else {
                $(lc_id('number_of_light_cones')).spinner("enable");
                $(lc_id('number_of_light_cones')).data("spin-max", maximum);
            }
            spinner_check_value(parseInt($(lc_id('number_of_light_cones')).val()));
            return true;
        }

        var selection = $("input[name='light_cone-light_cone_type']:checked").val();

        if ("unique" == selection) {
            // TODO: remove lines below once observers point-of-view for multiple unique light cones has been fixed in science modules
            $(lc_id('number_of_light_cones')).val('1');
            $(lc_id('number_of_light_cones')).closest('div.control-group').hide();
            //////
            var maximum = get_number_of_unique_light_cones();
            if (spinner_set_max(maximum)) {
                $spinner_label.html("Select the number of light-cones: (maximum for the selected parameters is " + maximum + ")*");
            }
        } else {
            // TODO: remove line below once observers point-of-view for multiple unique light cones has been fixed in science modules
            $(lc_id('number_of_light_cones')).closest('div.control-group').show();
            //////
            $.ajax({
                url: TAO_JSON_CTX + 'global_parameter/' + 'maximum-random-light-cones',
                dataType: "json",
                error: function () {
                    alert("Couldn't get data for maximum-random-light-cones");
                },
                success: function (data, status, xhr) {
                    var maximum = parseInt(data.fields.parameter_value);
                    if (spinner_set_max(maximum)) {
                        $spinner_label.html("Select the number of light-cones: (maximum " + maximum + " random light-cones)*");
                    }
                }
            });
        }
    }


    var validate_number_of_light_cones = function () {
        var geometry = vm.catalogue_geometry(); // $(lc_id('catalogue_geometry')).val();
        if (geometry == "light-cone") {
            var number_of_light_cones = parseInt($(lc_id('number_of_light_cones')).val());
            return spinner_check_value(number_of_light_cones);
        }
        return true;
    }

    var validate_number_of_boxes = function() {
        if ($('#max_job_size').hasClass('job_too_large_error')) {
            console.log($('#max_job_size').text());
            catalogue.util.show_tab($('#max_job_size'), 0);
            return false;
        } else {
            return true;
        }
    }

    var cleanup_fields = function ($form) {
        // cleanup geometry
        var geometry = vm.catalogue_geometry(); // $(lc_id('catalogue_geometry')).val();
        if (geometry == "box") {
            $('.light_cone_field').val('');
        } else {
            $('.light_box_field').val('');
        }
    }

    // - event handlers for fields -
    //
    var catalogue_geometry_change = function (newValue) {

        console.log('catalogue_geometry change: ' + newValue);

        var light_cone_fields = $('.light_cone_field').closest('div.control-group');
        var light_box_fields = $('.light_box_field').closest('div.control-group');

        if (vm.catalogue_geometry() == "box") {
            light_box_fields.show();
            light_cone_fields.hide();
            catalogue.util.fill_in_summary('light_cone', 'geometry_type', 'Box');
            $('div.summary_light_cone .box_fields').show();
            $('div.summary_light_cone .light_cone_fields').hide();
            $(lc_id('snapshot')).change();
        } else {
            light_box_fields.hide();
            light_cone_fields.show();
            catalogue.util.fill_in_summary('light_cone', 'geometry_type', 'Light-Cone');
            $('div.summary_light_cone .box_fields').hide();
            $('div.summary_light_cone .light_cone_fields').show();
            calculate_max_number_of_cones();
        }
    };

    function put_handler_ra_and_dec(field_name) {
        var event_handler = function(newValue) {
            var $elem = $(lc_id(field_name));
            if (vm.catalogue_geometry() == "box") {
                clear_error($elem);
                return;
            }
            if (parseFloat(newValue) <= 0. || parseFloat(newValue) > 90.0) {
                set_error($elem, 'Value must be 0 < x <= 90');
            } else {
                clear_error($elem);
            }
            fill_in_ra_dec_in_summary();
            calculate_max_number_of_cones();
        }
        clean_inline($(lc_id(field_name)));
        vm[field_name].subscribe(event_handler);
    }

    function init_event_handlers() {

        $('#expand_dataset').click(function (e) {
            e.preventDefault();
            $this = $(this);
            if ($this.html() === "&gt;&gt;") {
                $('div.summary_light_cone .simulation_description, div.summary_light_cone .galaxy_model_description').show();
                $this.html("<<");
            } else {
                $('div.summary_light_cone .simulation_description, div.summary_light_cone .galaxy_model_description').hide();
                $this.html(">>");
            }
            return false;
        });


        get_widget().change_event(function (evt) {
            catalogue.modules.record_filter.update_filter_options();

            var output_properties_count = catalogue.util.list_multiple_selections_in_summary('light_cone', 'output_properties');

            if (output_properties_count == 1)
                catalogue.util.fill_in_summary('light_cone', 'output_properties', output_properties_count + " property selected");
            else
                catalogue.util.fill_in_summary('light_cone', 'output_properties', output_properties_count + " properties selected");
        });


        $('#expand_output_properties').click(function (e) {
            e.preventDefault();
            $this = $(this);
            if ($this.html() === "&gt;&gt;") {
                $('div.summary_light_cone .output_properties_list').show();
                $this.html("<<");
            } else {
                $('div.summary_light_cone .output_properties_list').hide();
                $this.html(">>");
            }
            return false;
        });


        get_widget().option_clicked_event(function (cache_item) {
            catalogue.util.show_output_property_info(cache_item);
        });


        $(lc_id('dark_matter_simulation')).change(function (evt) {
            var $this = $(this);
            var sim_id = $this.val();
            show_simulation_info(sim_id);
            update_galaxy_model_options(sim_id); // triggers galaxy_model.change
        });


        $(lc_id('galaxy_model')).change(function (evt) {
            var $this = $(this);
            var galaxy_model_id = $this.find(':selected').attr('data-galaxy_model_id');
            show_galaxy_model_info(galaxy_model_id);
            // var use_default = $('#RF_BOUND').val() == 'False'; // TODO: Investigate this
            var use_default = !bound;
            // console.log('bound: ' + bound + ', !bound' + !bound)
            if (use_default) {
                if (vm.catalogue_geometry() == "box") {
                    var simulation_box_size = $(lc_id('number_of_light_cones')).data("simulation-box-size");
                    $(lc_id('box_size')).val(simulation_box_size);
                    $(lc_id('box_size')).change();
                }
            }
            update_output_options();
            update_snapshot_options();
        });

        $(lc_id('redshift_min') + ', ' + lc_id('redshift_max')).change(function (evt) {
            fill_in_redshift_in_summary();
            calculate_max_number_of_cones();
        });


        $(lc_id('light_cone_type_0') + ', ' + lc_id('light_cone_type_1')).click(function (evt) {
            var $this = $(this);
            catalogue.util.fill_in_summary('light_cone', 'light_cone_type', $this.attr('value'));
            calculate_max_number_of_cones();
        });


        $(lc_id('number_of_light_cones')).spinner({
            spin: function (evt, ui) {
                return spinner_check_value(ui.value);
            },
            min: 1
        });


        $(lc_id('number_of_light_cones')).change(function () {
            var new_value = parseInt($(this).val());
            return spinner_check_value(new_value);
        });


        $(lc_id('box_size')).change(function (evt) {
            var $this = $(this);
            var box_size_value = parseFloat($this.val());
            var max_box_size = parseFloat($(lc_id('number_of_light_cones')).data("simulation-box-size"));
            if ($this.val() != "" && isNaN(box_size_value)) {
                catalogue.util.show_error($(lc_id('box_size')), 'Box size must be a number');
                return false;
            }
            if (!isNaN(max_box_size) && parseFloat(box_size_value) > parseFloat(max_box_size)) {
                catalogue.util.show_error($(lc_id('box_size')), 'Box size greater than simulation\'s box size');
                return false;
            }
            catalogue.util.show_error($(lc_id('box_size')), null);
            catalogue.util.fill_in_summary('light_cone', 'box_size', box_size_value);
        });


        $(lc_id('snapshot')).change(function (evt) {
            var $this = $(this);
            var snapshot_value = $this.find('option:selected').html();
            catalogue.util.fill_in_summary('light_cone', 'snapshot', snapshot_value);
        });


        $('#id_output_format-supported_formats').change(function (evt) {
            var $this = $(this);
            var output_format_value = $this.find('option:selected').text();
            catalogue.util.fill_in_summary('output', 'output_format', output_format_value);
        });


        $(lc_id('ra_opening_angle') + ', ' + lc_id('dec_opening_angle') + ', ' + lc_id('redshift_max')).change(function(evt) {
            var box_size = parseFloat($(lc_id('number_of_light_cones')).data("simulation-box-size")); //window.simulation_box_size;   // size of the simulation box
            var min_ra = 0.0;                                                               // minimum right-ascension in degrees
            var max_ra = vm.ra_opening_angle();                                // maximum right-ascension in degrees
            var min_dec = 0.0;                                                              // minimum declination in degrees
            var max_dec = $(lc_id('dec_opening_angle')).val();                              // maximum declination in degrees
            var max_z = $(lc_id('redshift_max')).val();                                     // maximum redshift

            if (max_ra != '' && max_dec != '' && max_z != '') {
                try {
                    var num_boxes = count_boxes(box_size, min_ra, max_ra, min_dec, max_dec, max_z);
                    check_number_of_boxes(num_boxes);
                } catch (err) {
                    console.log(err);
                    $('#max_job_size').addClass('job_too_large_error');
                    $('#max_job_size').text('Estimated job size: invalid parameters, please adjust RA, Dec, redshift min or max');
                }
            }
        });

    }


    var empty_light_cone_variables = function () {
        $(lc_id('ra_opening_angle')).attr('value', '');
        $(lc_id('dec_opening_angle')).attr('value', '');
        $(lc_id('redshift_min')).attr('value', '');
        $(lc_id('redshift_max')).attr('value', '');
    }


    var empty_box_variables = function () {
        $(lc_id('box_size')).attr('value', '');
    }


    this.cleanup_fields = function ($form) {
        var geometry = vm.catalogue_geometry(); // $(lc_id('catalogue_geometry')).val();
        if (geometry == 'box') {
            empty_light_cone_variables();
        } else {
            empty_box_variables();
        }
    }


    this.validate = function ($form) {
        return validate_number_of_light_cones() && validate_number_of_boxes();
    }


    this.pre_submit = function ($form) {
        $(lc_id('output_properties') + ' option').each(function (i) {
            $(this).attr("selected", "selected");
        });
    }

    var init_state = function() {
        var init_light_cone_type_value = $('input[name="light_cone-light_cone_type"][checked="checked"]').attr('value');
        catalogue.util.fill_in_summary('light_cone', 'number_of_light_cones', $(lc_id('number_of_light_cones')).val() + " " + init_light_cone_type_value + " light cones");
        $(lc_id('number_of_light_cones')).attr('class', 'light_cone_field'); // needed to associate the spinner with light-cone only, not when selecting box
        $(lc_id('dark_matter_simulation')).change();
        // update_output_options(); // this is where the record filter update is triggere
        //                          and where the selection gets wiped
        // show_simulation_info($(lc_id('dark_matter_simulation')).val());


        $(lc_id('galaxy_model')).change();

        $('#id_output_format-supported_formats').change();

        $('div.summary_light_cone .output_properties_list').hide();
        $('div.summary_light_cone .simulation_description, div.summary_light_cone .galaxy_model_description').hide();

        $(lc_id('catalogue_geometry')).change();
    }


    this.init = function () {

        vm.catalogue_geometry.subscribe(catalogue_geometry_change);
        put_handler_ra_and_dec('ra_opening_angle');
        put_handler_ra_and_dec('dec_opening_angle');
        catalogue.modules.light_cone.util = new catalogue.modules.light_cone.util();

        get_widget().init();
        catalogue.modules.light_cone.util = new catalogue.modules.light_cone.util();
        // get_widget().init();
        init_event_handlers();
        init_state();
        // this.vm.catalogue_geometry($(lc_id('catalogue_geometry')).val());
        ko.applyBindings(vm);

        vm.catalogue_geometry( $(lc_id('catalogue_geometry')).val() );
        vm.ra_opening_angle( $(lc_id('ra_opening_angle')).val() );
        vm.dec_opening_angle( $(lc_id('dec_opening_angle')).val() );

    }

}
