import React from 'react'
import Sidebar from './Sidebar';
import Content from './Content';

export default function App({ children }) {
	return (
		<div className="row">
			<Sidebar />
			<Content>
				{ children }
			</Content>
		</div>
	)
}
