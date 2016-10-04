import React from 'react';
import Sidebar from './Sidebar';
import Content from './Content';
import { Miss } from 'react-router';
import NotFound from './NotFound';

export default function App({ projects }) {
    return (
        <div className="row">
            <Miss component={NotFound} />
            <Sidebar />
            <Content projects = {projects} />
        </div>
    );
}
