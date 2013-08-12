job_size = {};

job_size.box_count = function(box_size, ra_min, ra_max, dec_min, dec_max, z_min, z_max, H0) {
    if (z_min > z_max) {
        return "Error: z_min can not be larger than z_max.";
    }
    
    if (ra_max < ra_min || dec_max < dec_min) {
        return "Error: ra_max must be larger than ra_min and dec_max must be larger than dec_min.";
    }
    
    if (box_size < 0) {
        return "Error: box_size can not be smaller than 0.";
    }
    
    d_min  = job_size.redshift2distance(z_min, H0);
    d_max  = job_size.redshift2distance(z_max, H0);
    
    x_min = d_min*Math.cos(ra_min*Math.PI/180)*Math.cos(dec_min*Math.PI/180);
    x_max = d_max*Math.cos(ra_min*Math.PI/180)*Math.cos(dec_min*Math.PI/180);
    
    n = 0;
    for (x = x_min; x <= x_max; x += box_size) {
        y_max = x*Math.tan(ra_max*Math.PI/180);
        if (y_max > d_max*Math.sin(ra_max*Math.PI/180)) {
            y_max = d_max*Math.sin(ra_max*Math.PI/180);
        }
        y_min = x*Math.tan(ra_min*Math.PI/180);
        
        z_max = x*Math.tan(dec_max*Math.PI/180);
        if (z_max > d_max*Math.sin(dec_max*Math.PI/180)) {
            z_max = d_max*Math.sin(dec_max*Math.PI/180);
        }
        z_min = x*Math.tan(dec_min*Math.PI/180);
        
        n_y = Math.floor((y_max - y_min)/box_size) + 1;
        n_z = Math.floor((z_max - z_min)/box_size) + 1;
        
        n += n_y*n_z;
    }
    return n;
}

job_size.redshift2distance = function(z, H0) {
	
    c = 299792.458;
    n = 1000;
    dz = z/n;
    
    h = H0/100;
    WM = 0.25;
    WV = 1.0 - WM - 0.4165/(H0*H0);
    WR = 4.165E-5/(h*h);
    WK = 1-WM-WR-WV;
    az = 1.0/(1+1.0*z);
    DTT = 0.0;
    DCMR = 0.0;
    for (i = 0; i < n; i++) {
        a = az+(1-az)*(i+0.5)/n;
        adot = Math.sqrt(WK+(WM/a)+(WR/(a*a))+(WV*a*a));
        DTT = DTT + 1.0/adot;
        DCMR = DCMR + 1.0/(a*adot);
    }
    DTT = (1.-az)*DTT/n;
    DCMR = (1.-az)*DCMR/n;
    d = (c/H0)*DCMR;
    
    return d;
}

job_size.esttime = function(x, p1, p2, p3) {
    return (p1 * x * x) + (p2 * x) + p3;
}

job_size.from_count = function(estimated_count, max_boxes, p1, p2, p3) {
    return job_size.esttime(estimated_count, p1, p2, p3) / job_size.esttime(max_boxes, p1, p2, p3);
}

job_size.job_size = function(box_size, ra_min, ra_max, dec_min, dec_max, z_min, z_max, H0, max_boxes,
		p1, p2, p3) {
	var estimated_count = job_size.box_count(box_size, ra_min, ra_max, dec_min, dec_max, z_min, z_max, H0);

	return job_size.from_count(estimated_count, max_boxes, p1, p2, p3);
}
