// modules/About.js
import React, { Component } from 'react';
import ProjectsList from './ProjectsList';
import $ from 'jquery';

export default class Projects extends Component {
    constructor(props) {
        super(props);
        this.state = {
            projects : [],
            fetched : false
        };
    }

    componentDidMount() {
        $.ajax({
            url : this.props.apiUrl,
        })
        .done(function( data ) {
            this.setState({
                projects : data,
                fetched : true
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
        if (process.env.NODE_ENV !== 'production') {
            console.log('Projects state : ',this.state.projects);
            console.log('props: ', this.props);
        }
        if (this.state.fetched) {
            return (
                <ProjectsList { ...this.state } deleteProject={this.deleteProject.bind(this)}/>
            );
        } else {
            return null;
        }
    }

}
