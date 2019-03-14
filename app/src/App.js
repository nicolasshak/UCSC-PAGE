import React, { Component } from 'react';
import './App.css';

import Classes from './classes.json';
import SmoothCollapse from 'react-smooth-collapse';

const GES = ['CC', 'ER', 'MF', 'SI', 'SR', 'TA', 'PE-E', 'PE-H', 'PE-T', 'PR-E', 'PR-C', 'PR-S', 'C1', 'C2', 'C'];
const TAGS = ['Math', 'Anthropology', 'Linguistics', 'Art', 'Games and Playable Media', 'Astronomy', 'Biology', 'Business', 'Chemistry', 'Language', 'College Affiliated', 'Community Studies', 'Technology', 'Critical Race and Ethnic Studies', 'Earth and Planetary Sciences', 'Economics', 'Education', 'Electrical Engineering', 'Environmental Studies', 'Environmental Science', 'Film and Digital Media', 'Feminist Studies', 'History of Art and Visual Culture', 'History', 'History of Consciousness', 'Latin American and Latino Studies', 'Legal Studies', 'Literature', 'Microbiology and Environmental Toxicology', 'Music', 'Ocean Sciences', 'Philosophy', 'Physics', 'Politics', 'Psychology', 'Sociology', 'Theater Arts', 'Writing']

class App extends Component {

	componentDidMount() {
		window.onscroll = this.collapse
	}

	constructor(props) {
		super(props);

		var ge_list = {};
		var i;
		for(i = 0; i < GES.length; i++) {
			ge_list[GES[i]] = false;
		}

		var tag_list = {};
		var j;
		for(j = 0; j < TAGS.length; j++) {
			tag_list[TAGS[j]] = false;
		}

		this.toggleTag = this.toggleTag.bind(this);
		this.collapse = this.collapse.bind(this);

		this.state = {
			ges: ge_list,
			tags: tag_list,
			collapsed: true
		}
	}

	collapse() {
		if(window.scrollY === 0) {
			this.setState((state, props) => ({collapsed: true}));
		}
		else {
			this.setState((state, props) => ({collapsed: false}));
		}
	}

	toggleTag(key, type) {

		var dict = this.state[type];
		dict[key] = !dict[key];

		this.setState({type: dict});
	}

  render() {

    return (
    	<div class="app">
    		<div class="header-wrapper">
		      <div class="header">
		        <div class="logo" onClick={() => this.setState((state, props) => ({collapsed: !this.state.collapsed}))}>PAGE</div>
		      </div>
		      <SmoothCollapse expanded={this.state.collapsed}>
			      <div class="header" id="filters">
			      	<Filter type={'ges'} quip={<div class="filter filter-ge">I need a: </div>} defaultText={"GE"} tags={GES} hash={this.state['ges']} method={this.toggleTag.bind(this)} />
			      	<Filter type={'tags'} quip={<div class="filter filter-ge">and I'm interested in: </div>} defaultText={"Everything"} tags={TAGS} hash={this.state['tags']} method={this.toggleTag.bind(this)} />
			    	</div>
		    	</SmoothCollapse>
		    </div>
	      <div class="table-wrapper">
	      	<ClassTable hashes={[this.state.tags, this.state.ges]} onScroll={() => this.setState((state, props) => ({collapsed: true}))}/>
	      </div>
	    </div>
    );
  }
}

class Filter extends Component {

	renderSentence(tags, defaultText) {

		if(tags.length === 0) {
			return(<span class="highlighted">{defaultText}</span>);
		}
		else if (tags.length === 1) {
			return(tags)
		}
		else if (tags.length === 2) {
			return([tags[0], ' and ', tags[1]])
		}
		else {
			var str = [];

			for(var i in tags) {
				if(i == tags.length - 1) {
					str.push(<div>and </div>);
				}

				str.push(tags[i]);

				if(i != tags.length - 1) {
					str.push(<div>, </div>);
				}
			}

			return str;
		}
	}

	render() {

		var inactiveTags = [];
		var activeTags = [];

		for(var i in this.props.tags) {
			if(this.props.hash[this.props.tags[i]] === false) {
				inactiveTags.push(
					<Tag
						tag={this.props.tags[i]}
						type={this.props.type} 
						method={this.props.method} 
					/>
				);
			}	
			else {
				activeTags.push(
						<ActiveTag
							tag={this.props.tags[i]}
							type={this.props.type}
							method={this.props.method}
						/>
					);
			}
		}

		return(
			<div class="filter-wrapper">
				<div class="filter">
	    		<div>{this.props.quip}</div>
	    		{this.renderSentence(activeTags, this.props.defaultText)}
	    	</div>
	    	<div class="tag-list">
	    		{inactiveTags}
	    	</div>
	    </div>
		);
	}
}

class Tag extends Component {

	render() {
		return(
			<div class="tag" onClick={() => this.props.method(this.props.tag, this.props.type)}>
				<div>{this.props.tag}</div><div> +</div>
			</div>
		);
	}
}

class ActiveTag extends Component {

	render() {
		return(
			<div><span class="highlighted" onClick={() => this.props.method(this.props.tag, this.props.type)}>{this.props.tag}</span></div>
		);
	}
}

class ClassTable extends Component {

	constructor(props) {
		super(props);

		this.state = {
			sortCol: 'title',
			sortOrder: true, // true => ascending
		}
	}

	// Unoptimized
	getClasses(sortCol, sortOrder) {

		var class_list = [];

		for(var i in Classes) {
			if(this.filter(Classes[i])) {
				class_list.push(<ClassElement class={Classes[i]}/>);
			}
		}

		class_list.sort( function(a, b) {

			var c = Classes[a.props.class.title][sortCol];
			var d = Classes[b.props.class.title][sortCol];

			if(c > d) {
				return 1;
			}
			else if(c < d) {
				return -1;
			}
			else {
				return 0;
			}
		});
		
		if(this.state.sortOrder === false) {
			class_list.reverse();
		}
		
		return class_list;
	}

	filter(classInfo) {

		var ge_hash = this.props.hashes[1];
		var allGesFalse = true;
		for(var i in ge_hash) {
			if(ge_hash[i] === true) {
				allGesFalse = false;
			}
		}

		var tag_hash = this.props.hashes[0];
		var allTagsFalse = true;
		for(var j in tag_hash) {
			if(tag_hash[j] === true) {
				allTagsFalse = false;
			}
		}

		if(allGesFalse && allTagsFalse) {
			return true;
		}

		if(allGesFalse) {
			if(tag_hash[classInfo['department']]) {
				return true;
			}
		}

		if(allTagsFalse) {
			if(ge_hash[classInfo['ge']]) {
				return true;
			}
		}

		if(ge_hash[classInfo['ge']] && tag_hash[classInfo['department']]) {
			return true;
		}

		return false;
	}

	sortBy(columnName) {
		if(this.state.sortCol === columnName) {
			this.setState((state, props) => ({sortOrder: !state.sortOrder}));
		}
		else {
			this.setState((state, props) => ({sortCol: columnName, sortOrder: true}));
		}
	}

	render() {
		return(
			<div class="table">
				<div class="row headers">
					<div class="col col1" onClick={() => this.sortBy('title')}>Course Title</div>
					<div class="col col2">Description</div>
					<div class="col col3" onClick={() => this.sortBy('instructors')}>Instructor</div>
					<div class="col col4" onClick={() => this.sortBy('ge')}>GE</div>
					<div class="col col5">Class Page</div>
				</div>
				{this.getClasses(this.state.sortCol, this.state.sortOrder)}
			</div>
		);
	}
}

class ClassElement extends Component {

	render() {
		return(
			<div class="row">
				<div class="col col1">{this.props.class.title}</div>
				<div class="col col2">{this.props.class.description}</div>
				<div class="col col3">{this.props.class.instructors}</div>
				<div class="col col4">{this.props.class.ge}</div>
				<div class="col col5"><a href={this.props.class.link}>Link</a></div>
			</div>
		);
	}
}

export default App;