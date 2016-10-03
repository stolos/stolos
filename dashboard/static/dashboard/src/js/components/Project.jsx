// modules/About.js
import React from 'react'
import { Link } from 'react-router'

export default function Project({ params }) {
	return (
		<div>
			<div>Project uuid: { params.uuid } </div>
			<div>
				<Link to="/" activeOnlyWhenExact activeClassName="active">Back to projects</Link>
			</div>
		</div>
	)
}
