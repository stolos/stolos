webpackJsonp([0,3,4],{

/***/ 0:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _reactDom = __webpack_require__(34);
	
	var _reactDom2 = _interopRequireDefault(_reactDom);
	
	var _App = __webpack_require__(172);
	
	var _App2 = _interopRequireDefault(_App);
	
	var _Content = __webpack_require__(238);
	
	var _Content2 = _interopRequireDefault(_Content);
	
	var _Projects = __webpack_require__(239);
	
	var _Projects2 = _interopRequireDefault(_Projects);
	
	var _Project = __webpack_require__(240);
	
	var _Project2 = _interopRequireDefault(_Project);
	
	var _Home = __webpack_require__(241);
	
	var _Home2 = _interopRequireDefault(_Home);
	
	var _reactRouter = __webpack_require__(174);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	_reactDom2.default.render(_react2.default.createElement(
		_reactRouter.Router,
		{ history: _reactRouter.browserHistory },
		_react2.default.createElement(
			_reactRouter.Route,
			{ path: '/', component: _App2.default },
			_react2.default.createElement(_reactRouter.IndexRoute, { component: _Home2.default }),
			_react2.default.createElement(_reactRouter.Route, { path: '/projects', component: _Projects2.default }),
			_react2.default.createElement(_reactRouter.Route, { path: '/projects/:uuid/services', component: _Project2.default })
		)
	), document.getElementById('root'));

/***/ },

/***/ 172:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
		value: true
	});
	exports.default = App;
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _Sidebar = __webpack_require__(173);
	
	var _Sidebar2 = _interopRequireDefault(_Sidebar);
	
	var _Content = __webpack_require__(238);
	
	var _Content2 = _interopRequireDefault(_Content);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function App(_ref) {
		var children = _ref.children;
	
		return _react2.default.createElement(
			'div',
			{ className: 'row' },
			_react2.default.createElement(_Sidebar2.default, null),
			_react2.default.createElement(
				_Content2.default,
				null,
				children
			)
		);
	}

/***/ },

/***/ 173:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
		value: true
	});
	
	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _reactRouter = __webpack_require__(174);
	
	var _NavLink = __webpack_require__(237);
	
	var _NavLink2 = _interopRequireDefault(_NavLink);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
	
	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }
	
	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }
	
	var Sidebar = function (_Component) {
		_inherits(Sidebar, _Component);
	
		function Sidebar() {
			_classCallCheck(this, Sidebar);
	
			return _possibleConstructorReturn(this, (Sidebar.__proto__ || Object.getPrototypeOf(Sidebar)).apply(this, arguments));
		}
	
		_createClass(Sidebar, [{
			key: 'render',
			value: function render() {
				console.log('Sidebar.render()');
				return _react2.default.createElement(
					'div',
					{ className: 'col-sm-3', id: 'sidebar' },
					_react2.default.createElement(
						'ul',
						{ role: 'nav' },
						_react2.default.createElement(
							'li',
							null,
							_react2.default.createElement(
								_reactRouter.IndexLink,
								{ to: '/', activeClassName: 'active' },
								'Home'
							)
						),
						_react2.default.createElement(
							'li',
							null,
							_react2.default.createElement(
								_NavLink2.default,
								{ to: '/projects' },
								'Projects'
							)
						)
					)
				);
			}
		}]);
	
		return Sidebar;
	}(_react.Component);
	
	exports.default = Sidebar;
	;

/***/ },

/***/ 237:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
		value: true
	});
	
	var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; // modules/NavLink.js
	
	
	exports.default = NavLink;
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _reactRouter = __webpack_require__(174);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function NavLink(props) {
		return _react2.default.createElement(_reactRouter.Link, _extends({}, props, { activeClassName: 'active' }));
	}

/***/ },

/***/ 238:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
		value: true
	});
	
	exports.default = function (_ref) {
		var children = _ref.children;
	
		console.log('Content.render()');
		return _react2.default.createElement(
			'div',
			{ className: 'col-sm-9', id: 'content' },
			_react2.default.createElement(
				'div',
				{ className: 'row', id: 'header' },
				'Stolos Dashboard'
			),
			children
		);
	};
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);

	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/***/ },

/***/ 239:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
		value: true
	});
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _NavLink = __webpack_require__(237);
	
	var _NavLink2 = _interopRequireDefault(_NavLink);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	// modules/About.js
	exports.default = _react2.default.createClass({
		displayName: 'Projects',
		render: function render() {
			return _react2.default.createElement(
				'div',
				null,
				_react2.default.createElement(
					'h2',
					null,
					'Projects'
				),
				_react2.default.createElement(
					'ul',
					null,
					_react2.default.createElement(
						'li',
						null,
						_react2.default.createElement(
							_NavLink2.default,
							{ to: '/projects/hbtrbr/services', activeClassName: 'active' },
							'Project 1'
						)
					),
					_react2.default.createElement(
						'li',
						null,
						_react2.default.createElement(
							_NavLink2.default,
							{ to: '/projects/vfdvcw/services', activeClassName: 'active' },
							'Project 2'
						)
					)
				)
			);
		}
	});

/***/ },

/***/ 240:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
		value: true
	});
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _NavLink = __webpack_require__(237);
	
	var _NavLink2 = _interopRequireDefault(_NavLink);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	// modules/About.js
	exports.default = _react2.default.createClass({
		displayName: 'Project',
		render: function render() {
			return _react2.default.createElement(
				'div',
				null,
				_react2.default.createElement(
					'div',
					null,
					'Project uuid: ',
					this.props.params.uuid
				),
				_react2.default.createElement(
					'div',
					null,
					_react2.default.createElement(
						_NavLink2.default,
						{ to: '/projects', activeClassName: 'active' },
						'Back to projects'
					)
				)
			);
		}
	});

/***/ },

/***/ 241:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	exports.default = _react2.default.createClass({
	  displayName: 'Home',
	  render: function render() {
	    return _react2.default.createElement(
	      'div',
	      null,
	      'Home'
	    );
	  }
	}); // modules/About.js

/***/ }

});
//# sourceMappingURL=app.bundle.js.map