// modules/About.js
import React from 'react'
import NavLink from './NavLink'

export default React.createClass({
  render() {
	  return (
		  <div>
			  <div>Project uuid: {this.props.params.uuid}</div>
			  <div>
				  <NavLink to="/projects" activeClassName="active">Back to projects</NavLink>
			  </div>
		  </div>
	  )
  }
})
