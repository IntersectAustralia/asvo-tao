
var catalogue = catalogue || {}
catalogue.modules = catalogue.modules || {}


catalogue.modules.sed = function ($) {

    // KO ViewModel
    var vm = {}
    this.vm = vm;


    this.cleanup_fields = function ($form) {}

    this.validate = function ($form) {
        return true;
    }

    this.pre_submit = function ($form) {
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
            'group': bpf.fields.group
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

    this.init_model = function () {

        var vm = {};
        this.vm = vm;

        vm.apply_sed = ko.observable(false);
    	vm.stellar_models = ko.observableArray(TaoMetadata.StellarModel);
    	vm.stellar_model = ko.observable(vm.stellar_models()[0]);

        vm.bandpass_filters = TwoSidedSelectWidget(
        		sed_id('band_pass_filters'),
        		{
        			selected: [],
        			not_selected: catalogue.util.bandpass_filters()
        		},
        		band_pass_filter_to_option);
        //this.sed_band_pass_filters_widget.init();
        vm.current_bandpass_filter = ko.observable(undefined);
        vm.bandpass_filters.clicked_option.subscribe(function(v) {
        	var bpf = bandpass_filter_from_id(v);
        	vm.current_bandpass_filter(bpf);
        });

        vm.apply_dust = ko.observable(false);
    	vm.dust_models = ko.observableArray(TaoMetadata.DustModel);
    	vm.dust_model = ko.observable(vm.dust_models()[0]);

        return vm;

    }

}