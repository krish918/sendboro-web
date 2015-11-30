(function() {

	angular.module("util")
	
	.directive('routeLoader', ['$rootScope','$timeout',function($rootScope, $timeout) {
		
		var template = '<div class="loader-template" ng-if="isRouteLoading">'
			+'<div class="app-logo">'
			+'  <img ng-src="/static/resource/picture/boro-logo-s-1.png">'
			+'</div>'
			+'<div class="progress-bar-container" ng-hide="isLoadingFailed"></div>'
			+'<div class="loading-failed alert-text" ng-show="isLoadingFailed">'
			+'Hiccch! <br /> An error ocurred. Please try later!</div>'
			+'</div>';
		
		return {
			restrict : 'E',
			template: template,
			scope: {
				size: '=',
				color: '=',
				type: '='
			},
			link: function($scope) {				
				$scope.isRouteLoading = true;
				$scope.isLoadingFailed = false;

				$scope.$on('$stateChangeStart', function() {
					NProgress.configure({parent : '.progress-bar-container'});
	    			NProgress.start();
					$scope.isRouteLoading = true;
					$rootScope.uiTransit = 'ui-disappear';
				});

				$scope.$on('$stateChangeSuccess', function() {
					$rootScope.uiTransit = '';
					NProgress.done();
					$timeout(function(){
						$scope.isRouteLoading = false;
					},1000);
				});

				$scope.$on('$stateChangeError', function() {					
					$scope.isLoadingFailed = true;
				});

			}
		};
	}]);
})();