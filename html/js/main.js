/**
 * 
 */

(function  () {
		
	angular.module('util', ['ui.router']);
	
	angular.module('init',['ngAnimate', 'ngCookies', 'ui.router', 'util'])
	
	.config(function ($stateProvider, $urlRouterProvider, $locationProvider) {
				
				$stateProvider
				
				.state('index', {
					url: '/',
					templateUrl: '/partial/init'
				})
				
				.state('team',{
					url: '/team',
					templateUrl: '/partial/team',
					controller: function ($scope, $window) {
						$scope.back = function () {
							$window.history.back();
						}
					}
				});
				
				$locationProvider.html5Mode({
					enabled: true,
					requireBase: false
				});
	});
	
	var frameObj = {
			templateUrl: '/partial/homeframe',
			
			//controller initialization will be halted till metaboro service will be resolved
			//this service will be injected in homeFrameController
			resolve: {
				user: '$metaboro'
			},
			controller: 'homeFrameController',
			controllerAs: 'hfCtrl'
		};
	
	var widgetObj = {
		templateUrl: '/partial/quickcontact',
		controller: 'quickContactController',
		controllerAs: 'qctCtrl',
	};
	
	angular.module('borocasa', ['ngAnimate', 'ngCookies', 'ui.router','util','angularFileUpload'])
		
	.config(function ($stateProvider, $urlRouterProvider, $locationProvider) {
			
				$stateProvider
				
				.state('homeframe',{
					url: '/',
					views: {
						'frame@': frameObj,
						'widget@homeframe': widgetObj
					}
				})
				
				.state('homeframe.settings', {
					url: 'settings',
					views: {
						'widget@homeframe': {
							templateUrl: '/partial/settings',
							controller: 'settingsController',
							controllerAs: 'setCtrl'
						}
					}
				})
				
				.state('homeframe.send', {
					url: 'send',
					views: {
						'widget@homeframe' : {
							templateUrl: '/partial/send',
							controller: 'shareController',
							controllerAs: 'shCtrl'
						}
					},
				})
				
				.state('homeframe.inbox', {
					url: 'inbox',
					views: {
						'widget@homeframe' : {
							templateUrl: '/partial/inbox',
							controller: 'inboxController',
							controllerAs: 'inbxCtrl'
						}
					},
				});
				
				$locationProvider.html5Mode({
					enabled: true,
					requireBase: false
				});
					
			});
	
}());	

	
	