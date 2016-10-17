import React from 'react';
import $ from 'jquery';

export default function Header() {

    function logout() {
        window.location = '/logout/';
    }

    return (
        <div className="col-xs-12" id="header">
            <div className="row">
                <div className="col-xs-12">
                    <span>Stolos Dashboard</span>
                    <button className="btn" id="logout" onClick={logout}>
                        <i className="fa fa-power-off" aria-hidden="true"></i>
                    </button>
                </div>
            </div>
        </div>
    );
}
