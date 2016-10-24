import React, {Component} from 'react';
import Content from './Content';
import {Miss, Match} from 'react-router';
import NotFound from './NotFound';
import Header from './Header';

export default class App extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div className="container-fluid">
                <main className="row">
                    <Miss component={NotFound}/>
                    <Header />
                    <Content />
                </main>
            </div>
        );
    }
}
