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
            $('.overlay-item').hide();
    	});
        $('#stop_job_confirm').dialog({
            resizable: false,
            modal: true,
            autoOpen: false,
            buttons: {
                Ok: {
                    text: "Stop",
                    id: "id_confirm_stop",
                    click: function() {
                        $.ajax({
                            url: TAO_JOB_CTX + 'stop_job/' + TaoJob['job-id'],
                            type: 'POST',
                            success: function(response, textStatus, jqXHR) {
                                location.reload();
                            },
                            error: function(response, textStatus, jqXHR) {
                                console.log(response.responseText);
                                console.log("Couldn't stop SUBMITTED job: " + response + textStatus);
                            }
                        });
                        $(this).dialog("close");
                    }
                },
                Cancel: {
                    text: "Cancel",
                    id: "id_cancel_stop",
                    click: function() {
                        $(this).dialog("close");
                    }
                }
            }
        });
        $('#rerun_job_confirm').dialog({
            resizable: false,
            modal: true,
            autoOpen: false,
            buttons: {
                Ok: {
                    text: "Re-run",
                    id: "id_confirm_rerun",
                    click: function() {
                        $.ajax({
                            url: TAO_JOB_CTX + 'rerun_job/' + TaoJob['job-id'],
                            type: 'POST',
                            success: function(response, textStatus, jqXHR) {
                                location.reload();
                            },
                            error: function(response, textStatus, jqXHR) {
                                console.log("Couldn't change job status from COMPLETED to SUBMITTED: " + response + textStatus);
                            }
                        });
                        $(this).dialog("close");
                    }
                },
                Cancel: {
                    text: "Cancel",
                    id: "id_cancel_rerun",
                    click: function() {
                        $(this).dialog("close");
                    }
                }
            }
        });
        $('#delete_job_output_confirm').dialog({
            resizable: false,
            height: 210,
            width: 510,
            modal: true,
            autoOpen: false,
            buttons: {
                Ok: {
                    text: "Delete",
                    id: "id_confirm_delete_output",
                    click: function() {
                        $.ajax({
                            url: TAO_JOB_CTX + 'delete_job_output/' + TaoJob['job-id'],
                            type: 'POST',
                            success: function(response, textStatus, jqXHR) {
                                location.reload();
                            },
                            error: function(response, textStatus, jqXHR) {
                                console.log("Couldn't create job_output_delete workflow command: " + response + textStatus);
                            }
                        });
                        $(this).dialog("close");
                    }
                },
                Cancel: {
                    text: "Cancel",
                    id: "id_cancel_delete_output",
                    click: function() {
                        $(this).dialog("close");
                    }
                }
            }
        });
        $('#release_job_confirm').dialog({
            resizable: false,
            modal: true,
            autoOpen: false,
            buttons: {
                Ok: {
                    text: "Release",
                    id: "id_confirm_release",
                    click: function() {
                        $.ajax({
                            url: TAO_JOB_CTX + 'release_job/' + TaoJob['job-id'],
                            type: 'POST',
                            success: function(response, textStatus, jqXHR) {
                                location.reload();
                            },
                            error: function(response, textStatus, jqXHR) {
                                console.log("Couldn't change job status from HELD to SUBMITTED: " + response + textStatus);
                            }
                        });
                        $(this).dialog("close");
                    }
                },
                Cancel: {
                    text: "Cancel",
                    id: "id_cancel_release",
                    click: function() {
                        $(this).dialog("close");
                    }
                }
            }
        });
        $("#id-job_stop").click(function(e) {
            e.preventDefault();
            $('#stop_job_confirm').dialog("open");
            return false;
        });
        $("#id-job_rerun").click(function(e) {
            e.preventDefault();
            $('#rerun_job_confirm').dialog("open");
            return false;
        });
        $("#id-job_output_delete").click(function(e) {
            e.preventDefault();
            $("#delete_job_output_confirm").dialog("open");
            return false;
        });
        $("#id-job_release").click(function(e) {
            e.preventDefault();
            $('#release_job_confirm').dialog("open");
            return false;
        });

    	// Set up the auto-height handler for the job description textarea
        $('#id-job_description').bind('keyup', function(){
            var h = $(this)[0].scrollHeight - 8;
            $(this).height( Math.min(h, 300) );
        });

        return vm;
    }

    var original_height = $('#id-job_description')[0].scrollHeight;

    this.save_description = function(evt) {
    	// KO takes care of the core model (catalogue.vm.description),
    	// but we want to save a backup in case of later cancellation
    	vm.description_bak(catalogue.vm.description());

		$.ajax({
			url: TAO_JSON_CTX + 'edit_job_description/' + TaoJob['job-id'],
			type: 'POST',
			data: {"job-description": catalogue.vm.description()},
			success: function(response, textStatus, jqXHR) {
                $('#id-job_description').height(original_height);
				$('#savecancel').hide();
                $('.overlay-item').show();
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
        $('#id-job_description').height(original_height);
    	setTimeout("$('#savecancel').hide()", 100);
        setTimeout("$('.overlay-item').show()", 100);
   	}

}
