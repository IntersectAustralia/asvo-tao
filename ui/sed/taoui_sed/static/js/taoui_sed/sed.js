
var catalogue = catalogue || {}
catalogue.modules = catalogue.modules || {}


catalogue.modules.sed = function ($) {

    // KO ViewModel
    var vm = {}
    this.vm = vm;

    this.cleanup_fields = function () {}

    this.validate = function () {
        return true;
    }

    this.pre_submit = function () {
    }

    this.job_parameters = function() {
    	// Dummy values until Value Model has been completed
    	var apply_sed = vm.apply_sed();
    	var selected_bpfs;
    	var bpf_ids;
    	var params = {
    		'sed-apply_sed': [apply_sed]
    	};
    	if (apply_sed) {
    		selected_bpfs = catalogue.modules.sed.vm.bandpass_filters.to_side.options_raw();
    		bpf_ids = []
    		for (var i=0; i<selected_bpfs.length; i++) {
    			bpf_ids.push(selected_bpfs[i].value);
    		}
    		jQuery.extend(params, {
    			'sed-single_stellar_population_model': [vm.stellar_model().pk],
    			'sed-apply_dust': [vm.apply_dust()],
    			'sed-select_dust_model': [vm.dust_model().pk],
    			'sed-band_pass_filters': bpf_ids
    		});
    	}
    	return params;
    }

    function band_pass_filter_to_option(bpf) {
        return {
            'value': bpf.pk,
            'text' : bpf.fields.label,
            'group': bpf.fields.group,
            'order': bpf.fields.order
        }
    }

    function bandpass_filter_from_id(bpfid) {
    	// Answer the selected bpf record from the supplied encoded id
    	// bpfid = <bpf primary key>_(apparent|absolute)
    	idx = bpfid.indexOf("_");
    	if (idx < 0) {
    		console.log("bandpass_filter_from_id: couldn't find _");
    		return undefined;
    	}
    	id = bpfid.slice(0,idx);
        return $.grep(TaoMetadata.BandPassFilter, function(elem, idx) { 
            return elem.pk == id
        })[0] || null;

    }

    this.init_model = function (init_params) {
    	// job is either an object containing the job parameters or null
    	var job = init_params.job;
    	var param; // Temporary variable for observable initialisation

    	param = job['sed-apply_sed'];
        vm.apply_sed = ko.observable(param ? param : false);
    	vm.stellar_models = ko.observableArray(TaoMetadata.StellarModel);
    	param = job['sed-single_stellar_population_model'];
    	if (param) {
    		param = catalogue.util.stellar_model(param);
    	}
    	vm.stellar_model = ko.observable(param ? param : vm.stellar_models()[0]);

    	param = job['sed-band_pass_filters'];
        if (param) {
        	// If bandpass filters have been provided, assume that we are only displaying
        	// the job, so we don't need to set up the TwoSidedSelectWidget
        	var bpfilters = [];
        	for (var i=0; i<param.length; i++) {
        		bpfilters.push(catalogue.util.bandpass_filter(param[i]));
        	}
        	param = bpfilters;
        }
        vm.bandpass_filters_options = ko.computed(function(){
            return catalogue.util.bandpass_filters();
        });
        vm.bandpass_filters = ko.observableArray(param ? param : []);
        vm.bandpass_filters_widget = TwoSidedSelectWidget({
            elem_id: sed_id('band_pass_filters'),
            options: vm.bandpass_filters_options,
            selectedOptions: vm.bandpass_filters,
            to_option: band_pass_filter_to_option
        });
        vm.current_bandpass_filter = ko.observable(undefined);
    	// if param is null assume that we are in the Catalogue wizard
    	// so set up the dependencies to update the display
        // otherwise leave it unlinked
        if (!param) {
	        vm.bandpass_filters_widget.clicked_option.subscribe(function(v) {
	        	var bpf = bandpass_filter_from_id(v);
	        	vm.current_bandpass_filter(bpf);
	        });
        }

        param = job['sed-apply_dust'];
        vm.apply_dust = ko.observable(param ? param : false);
    	vm.dust_models = ko.observableArray(TaoMetadata.DustModel);
    	param = job['sed-select_dust_model'];
    	if (param) {
    		param = catalogue.util.dust_model(param);
    	}
    	vm.dust_model = ko.observable(vm.dust_models()[0]);

        return vm;

    }

}