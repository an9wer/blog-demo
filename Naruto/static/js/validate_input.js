function validate_input(input_name) {
	var request = new XMLHttpRequest();
	if (request) {
		request.onreadystatechange = function() {
			if (request.readyState === 4) {
				if (request.status === 200 || request.status === 304) {
					// fetch the request data 
					var data = JSON.parse(request.responseText);
					var input_error = data[input_name + '_errors'][0];

					if (input_error) {
						// The input of url should be correct or none.
						// If the input of url is none, it will not send error information.
						if ( (input_value) || (input_name != 'url') ) {
							document.getElementById(input_name + '_error').innerHTML = '* ' + input_error;
						} else {
							document.getElementById(input_name + '_error').innerHTML = '';
						} 
					} else {
						document.getElementById(input_name + '_error').innerHTML = '';
					}
				}
			}
		}
		request.open('POST', '/_validate_input_ajax');
		request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		var input_value = document.getElementById(input_name).value;
		var postVar = input_name + '=' + input_value;
		request.send(postVar);
	}
}
