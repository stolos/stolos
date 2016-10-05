import React, { Component } from 'react';
import { Link } from 'react-router';

export default class Sidebar extends Component{
    render() {
        console.log('Sidebar.render()');
        return (
            <div className="col-sm-3" id="sidebar">
                <nav>
                    <div><Link to="/" activeClassName="active">Projects</Link></div>
                </nav>
            </div>
        );
    }
}
