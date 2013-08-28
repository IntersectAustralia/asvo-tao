//
// Module: textarea_height
// Class: TextareaHeight
//
// Auto size the textarea height as the user types.
//
// Parameters:
// - textarea: The textarea DOM to be managed
// - max_height: The maximum number of rows to grow the textarea
//				The count excludes wrapped lines (so a window with one very long
//				line will fail to grow).
//				Default = 20
//

function TextareaHeight(params) {
	if (params.textarea == undefined)
		throw "TextareaHeight requires the textarea";
	this.textarea = params.textarea;
    // Attach ourself to the widget for easy debugging
	this.textarea.textarea_height_mgr = this;
	this.textarea.onkeyup = this.update.bind(this);
	// The page may not be ready yet.
	// Update the height in 100ms and 1s
	setTimeout(this.update.bind(this), 100);
	setTimeout(this.update.bind(this), 1000);
	return this;
}

TextareaHeight.prototype = {
	update: function textarea_height_dom() {
        setTimeout( function() {
            console.log($(params.textarea));
            var h = $(this.textarea)[0].scrollHeight;
            $(this.textarea).height( h );
        }, 1);
	}
}