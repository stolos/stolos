import React, { Component } from 'react';
import { Link } from 'react-router';

export default function Sidebar({ pathname }) {
    return (
        <div className="col-sm-3 col-xl-2" id="sidebar">
            <nav>
                <div className="nav-link-container">
                    <Link to={`/projects/`} activeClassName="active">Projects</Link>
                </div>
            </nav>
        </div>
    );
}
