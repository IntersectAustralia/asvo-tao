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

    var get_global_maximum_light_cones = function() {
        if (typeof get_global_maximum_light_cones._max == 'undefined') {
            var param = catalogue.util.global_parameter_or_null('maximum-random-light-cones');
            var val = param == null ? NaN : parseInt(param.fields.parameter_value);
            if (isNaN(val)) {
                var msg = "'maximum-random-light-cones' not properly configured for this installation";
                alert(msg);
                console.log(msg);
                val = 1;
            }
            get_global_maximum_light_cones._max = val;
        }
        return get_global_maximum_light_cones._max;
    }

    //    /**
    //     * Compute the maximum number of unique cones available for selected parameters
    //     */
    var get_number_of_unique_light_cones = function () {
        var vm = catalogue.modules.light_cone.vm;

        // forces KO dependencies, even if algorithm fails halfway through
        vm.ra_opening_angle();
        vm.dark_matter_simulation();
        vm.redshift_min();
        vm.redshift_max();
        vm.dec_opening_angle();

        var alpha1 = parseFloat(vm.ra_opening_angle());
        var box_side = vm.dark_matter_simulation().fields.box_size;
        var d1 = redshift_to_distance(parseFloat(vm.redshift_min()));
        var d2 = redshift_to_distance(parseFloat(vm.redshift_max()));
        var beta1;
        for (beta1 = alpha1; beta1 < 90; beta1 = beta1 + 0.01) {
            if ((d2 - box_side) * Math.sin((Math.PI / 180) * (beta1 + alpha1)) <= d2 * Math.sin((Math.PI / 180) * beta1)) {
                break;
            }
        }
        var hv = Math.floor(d2 * Math.sin((Math.PI / 180) * (alpha1 + beta1)) - d1 * Math.sin((Math.PI / 180) * (alpha1 + beta1)));

        var hh = 2 * d2 * Math.sin((Math.PI / 180) * (parseFloat(vm.dec_opening_angle())) / 2);

        var nv = Math.floor(box_side / hv);
        var nh = Math.floor(box_side / hh);
        return nv * nh;
    }


