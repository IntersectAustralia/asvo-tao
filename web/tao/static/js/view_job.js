//
// Worker routines for the Job View page
//
// This is configured as a separate module so that we inherit module initialisation, etc.
// 

var catalogue = catalogue || {};
catalogue.modules = catalogue.modules || {};


catalogue.modules.view_job = function ($) {
    // KO ViewModel
    var vm = {}
    this.vm = vm;

	//
    // Leave out the usual validation and job submission functions.
    // This module should only be loaded when viewing a job.
    //

    this.init_model = function(init_params) {
    	// Store a copy of the description in case the user cancels
    	vm.description_bak = ko.observable(catalogue.vm.description());

    	// Manage visibility of the job description save / cancel buttons 
    	$("#inlineedit").click(function() {
    		$('#savecancel').show();
    	});
    	// Set up the auto-height handler for the job description textarea
    	new TextareaHeight({textarea: $('#id-job_description')[0]});
    }

    this.save_description = function(evt) {
    	// KO takes care of the core model (catalogue.vm.description),
    	// but we want to save a backup in case of later cancellation
    	vm.description_bak(catalogue.vm.description());

		$.ajax({
			url: TAO_JSON_CTX + 'edit_job_description/' + TaoJob['job-id'],
			type: 'POST',
			data: {"job-description": catalogue.vm.description()},
			success: function(response, textStatus, jqXHR) {
				$('#savecancel').hide();
			},
			error: function(response, textStatus, jqXHR) {
				// Save parameters for debugging purposes
				catalogue.last_submit_error = {
						response: response,
						text_status: textStatus,
						jqXHR: jqXHR
				}
				alert("Couldn't save job description");
			}
		});
   	}

    this.cancel_description = function(evt) {
    	catalogue.vm.description(vm.description_bak());
    	setTimeout("$('#savecancel').hide()", 100);
   	}

}
