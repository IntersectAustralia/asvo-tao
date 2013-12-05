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
        
		var ra  = parseFloat(vm.ra_opening_angle());
		var dec = parseFloat(vm.dec_opening_angle());
		var b   = vm.dark_matter_simulation().fields.box_size;
		var d   = redshift_to_distance(parseFloat(vm.redshift_max())) + 1;
        
        if (isNaN(ra) || isNaN(dec) || isNaN(d) || isNaN(b)) {
        	return NaN;
        }
        if (d < b) {
            width  = d*Math.sin(dec*Math.PI/180);
            height = d*Math.sin(ra*Math.PI/180);
            n_vert = Math.floor(b/height);
            n_horz = Math.floor(b/width);
            return n_vert*n_horz;
        }
        if (d >= b && d*Math.sin(dec*Math.PI/180) > b) {
            return NaN;
        }
        for (ra_min = 0; ra_min < 90; ra_min += 0.01) {
            if ((d - b/Math.cos((ra_min + ra)*Math.PI/180))*Math.sin((ra_min + ra)*Math.PI/180)
                <= d*Math.sin(ra_min*Math.PI/180)) {
                width  = d*Math.sin(dec*Math.PI/180);
                height = d*Math.sin((ra_min + ra)*Math.PI/180);
                n_vert = Math.floor(b/height);
                n_horz = Math.floor(b/width);
                return n_vert*n_horz;
            }
        }
        return NaN;
    }


