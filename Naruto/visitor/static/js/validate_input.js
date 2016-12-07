function validate_input(this_input) {
	if (this_input.checkValidity() == false) {
		if (this_input.id === 'name') {
			document.getElementById('name_error').innerHTML = 'Please enter your name.'
		}
		if (this_input.id === 'email') {
			document.getElementById('email_error').innerHTML = 'Please enter the correct email address.(e.g. john@example.com)'
		}
		if (this_input.id === 'url') {
			document.getElementById('url_error').innerHTML = 'Please enter the correct Web address.(e.g. http://www.example.com)'
		}
	} else {
		document.getElementById(this_input.id+'_error').innerHTML = ''
	}
}

