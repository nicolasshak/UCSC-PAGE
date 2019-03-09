import React, { Component } from 'react';
import './App.css';

import Classes from './classes.json';

class App extends Component {

  render() {
    return (
    	<div class="app">
    		<div class="header-wrapper">
		      <div class="header">
		        <div class="logo">PAGE</div>
		      </div>
		      <Filters />
		    </div>
	      <div class="table-wrapper">
	      	<ClassTable />
	      </div>
	    </div>
    );
  }
}

class Filters extends Component {

	constructor(props) {
		super(props);

		this.state = {
			activefilters: {
				ges: [],
				tags: []
			},
			inactivefilters: {
				ges: ['CC', 'ER', 'MF', 'SI', 'SR', 'TA', 'PE', 'PE-E', 'PE-H', 'PE-T', 'PR', 'PR-E', 'PR-C', 'PR-S', 'C1', 'C2', 'C'],
				tags: []
			}
		}
	}

	activate() {

	}

	deactivate() {

	}

	makeEnglish(array, type) {

		if(array.length === 0) {
			var str = '';
			if(type === 'ge')
				str = 'Any GE';
			if(type === 'tag')
				str = 'Everything';
			return(<span class="highlighted">{str}</span>);
		}

		var english = [<div>a </div>];
		for(var i in array) {
			if(i >= array.length - 1) {
				english.push(<div>and </div>);
			}

			english.push(<span class="highlighted">{array[i]}</span>);

			if(i < array.length - 1) {
				english.push(<div>, </div>);
			}
		}

		return(english);
	}

	render() {
		return(
			<div class="header" id="filters">
      	<div class="filter filter-ge">
      		<div>I need: </div>
      		{this.makeEnglish(this.state.activefilters.ges, 'ge')}
      	</div>
      	<div class="tag-list">
      		<Tag />
      	</div>
      	<div class="filter filter-tag">
      		<div>and I'm interested in: </div>
      		{this.makeEnglish(this.state.activefilters.tags, 'tag')}
      	</div>
      	<div class="tag-list">
      		<Tag />
      	</div>
      </div>
		);
	}
}

class Tag extends Component {

	render() {
		return(
			<div class="tag">
				<div>Tag +</div>
			</div>
		);
	}
}

class ClassTable extends Component {

	constructor(props) {
		super(props);

		this.state = {
			sort_col: 1,
			sort_order: true, // true => ascending
			class_list: this.getClasses()
		}
	}

	getClasses() {

		var class_list = [];

		for(var class_element in Classes) {
			class_list.push(<ClassElement class={Classes[class_element]}/>);
		}

		return class_list;
	}

	// 1: Class title, 3: Instructor, 4: GE
	sort(col_num) {

		var copy = this.state.class_list.slice();

		if(this.state.sort_col === col_num) {
			this.setState((state, props) => ({sort_order: !state.sort_order}));
			copy.reverse();
		}
		else {
			this.setState((state, props) => ({sort_col: col_num, sort_order: true}));
			copy.sort( function(a, b) {

				var c, d;

				switch(col_num) {
					case 1:
						c = a.props.class.title;
						d = b.props.class.title;
						break;
					case 3:
						c = a.props.class.instructors;
						d = b.props.class.instructors;
						break;
					case 4:
						c = a.props.class.ge;
						d = b.props.class.ge;
						break;
					default:
						return 0;
				}

				if(c > d) {
					return 1;
				}
				if(c == d) {
					return 0;
				}
				else {
					return -1;
				}
			});
		}

		this.setState((state, props) => ({class_list: copy}));
	}

	render() {
		return(
			<div class="table">
				<div class="row headers">
					<div class="col col1" onClick={() => this.sort(1)}>Course Title</div>
					<div class="col col2">Description</div>
					<div class="col col3" onClick={() => this.sort(3)}>Instructor</div>
					<div class="col col4" onClick={() => this.sort(4)}>GE</div>
					<div class="col col5">Class Page</div>
				</div>
				{this.state.class_list}
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
