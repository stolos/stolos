import React, {Component} from 'react';
import Sidebar from './Sidebar';
import Content from './Content';
import {Miss} from 'react-router';
import NotFound from './NotFound';

export default class App extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div className="container-fluid">
                <div className="row">
                    <Miss component={NotFound}/>
                    <Sidebar/>
                    <Content />
                </div>
            </div>
        );
    }
}
