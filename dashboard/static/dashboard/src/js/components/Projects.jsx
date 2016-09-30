// modules/About.js
import React from 'react'
import NavLink from './NavLink'

export default React.createClass({
	render() {
		return (
			<div>
				<h2>Projects</h2>
				<ul>
					<li>
						<NavLink to="/projects/hbtrbr/services" activeClassName="active">Project 1</NavLink>
					</li>
					<li>
						<NavLink to="/projects/vfdvcw/services" activeClassName="active">Project 2</NavLink>
					</li>
				</ul>
			</div>
		);
	}
})
