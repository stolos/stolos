import React from 'react';
import NavLink from './NavLink';

export default function() {
	return (
		<div>
			<h2>Projects</h2>
			<ul>
				<li>
					<NavLink to={`hbtrbr/services`} activeClassName="active">Project 1</NavLink>
				</li>
				<li>
					<NavLink to={`vevefv/services`} activeClassName="active">Project 2</NavLink>
				</li>
			</ul>
		</div>
	);
}
