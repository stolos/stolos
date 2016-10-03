// modules/About.js
import React from 'react'
import NavLink from './NavLink'
import { IndexLink } from 'react-router'

export default function(props) {
	return (
		<div>
			<div>Project uuid: {props.params.uuid}</div>
			<div>
				<IndexLink to="/projects" activeClassName="active">Back to projects</IndexLink>
			</div>
		</div>
	)
}
