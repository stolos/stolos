// modules/About.js
import React, { Component } from 'react';
import ProjectsList from './ProjectsList';

export default class Projects extends Component {
    constructor(props) {
        super(props);
        this.state = {projects : []};
    }

    componentDidMount() {
        $.ajax({
            url : this.props.apiUrl,
        })
        .done(function( data ) {
            this.setState({
                projects : data
            });
        }.bind(this));
    }

    deleteProject(uuid) {
        $.ajax({
            url : `/api/a0.1/projects/${uuid}`,
            type : 'DELETE',
        })
        .done(function() {
            this.setState({
                projects : this.state.projects.filter(function(project) {
                    return project.uuid !== uuid;
                })
            });
        }.bind(this));
    }

    render() {
        console.log('Projects state : ',this.state.projects);
        console.log('Projects props : ',this.props);
        console.log('Projects.render()');
        return (
            <ProjectsList { ...this.state } deleteProject={this.deleteProject.bind(this)}/>
        );
    }

}
