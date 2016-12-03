function submit_comment() {
	var request = new XMLHttpRequest();
	if (request) {
		request.onreadystatechange = function() {
			if (request.readyState === 4) {
				if (request.status === 200 || request.status == 304) {
					var data = JSON.parse(request.responseText);
					var error = data.error
					var id = data.id;
					var name = data.name;
					var timestamp = new Date(data.timestamp);
					var body = data.body;
					var tag = (getCount(document.getElementById('comment-list'), false) - 1) / 2 + 1;
					if (error) {
						alert(error);
					} else {
						// create a new block to store comment
						var div_id = document.createElement('div');
						var div_header = document.createElement('div');
						var div_body = document.createElement('div');
						div_id.setAttribute('id', 'comment-'+id);
						div_header.setAttribute('class', 'comment-header');
						div_body.setAttribute('class', 'comment-body');
						var header_text = document.createTextNode(name+' · '+'#'+tag+' · '+timestamp.toLocaleString());
						var body_text = document.createTextNode(body);
						div_header.appendChild(header_text);
						div_body.appendChild(body_text);
						div_id.appendChild(div_header);
						div_id.appendChild(div_body);
						document.getElementById('comment-list').appendChild(div_id);
						
						// set testarea's content to null
						document.getElementById('body').value = ''
						// scroll to the new comment
						document.getElementById('comment-'+id).scrollIntoView(true);
					}
				}
			}
		}
		request.open('POST', '/_submit_comment_ajax');
		request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		var name = document.getElementById('name').value;
		var email = document.getElementById('email').value;
		var url = document.getElementById('url').value;
		var body = document.getElementById('body').value;
		var post_id = window.location.pathname.split('/')[2];
		var postVars = 'name=' + name + '&email=' + email + '&url=' + url + '&body=' + body + '&post_id=' + post_id;
		request.send(postVars);
	}
}

// this function counts the childern of one element.
// if getChildrensChildren set true, it will count the children of the children.
function getCount(parent, getChildrensChildren) {
	var relevantChildren = 0;
	var children = parent.childNodes.length;
	for(var i=0; i < children; i++) {
		if(parent.childNodes[i].nodeType != 3) {
			if(getChildrensChildren)
				relevantChildren += getCount(parent.childNodes[i], true);
			relevantChildren++;
		}
	}
	return relevantChildren;
}
