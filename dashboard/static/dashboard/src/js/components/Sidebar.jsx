import React, { Component } from 'react';
import { Link } from 'react-router';

export default class Sidebar extends Component{
    render() {
        return (
            <div className="col-sm-3 col-xl-2" id="sidebar">
                <nav>
                    <div className="nav-link-container">
                        <Link to="/" activeClassName="active">Projects</Link>
                    </div>
                </nav>
            </div>
        );
    }
}
