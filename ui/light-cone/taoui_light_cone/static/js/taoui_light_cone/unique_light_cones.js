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


