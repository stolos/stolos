import React from 'react';

export default function({ children }) {
	console.log('Content.render()');
	return (
		<div className="col-sm-9" id="content">
			<div className="row" id="header">Stolos Dashboard</div>
			{ children }
		</div>
	)
}
