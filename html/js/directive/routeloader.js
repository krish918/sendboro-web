(function() {

	angular.module("util")
	
	.controller("loaderCtrl", ['$scope', function ($scope) {
		$scope.purple = 'purple';
		$scope.large = 'large';
		$scope.green = 'green';
		$scope.square = 'square';
		$scope.home = 'home';
	}])
	
	.directive('routeLoader', function($rootScope) {
		
		var template = '<div class="view-loader" ng-if="isRouteLoading">'
			+ '<img ng-src="static/resource/loader/'
			+ '{{size}}-{{color}}-{{type}}.gif">'
			+ '<div class="inline-middle loader-cover-small"></div>' + '</div>'
			+ '<div class="view-loader loader-error" ng-if="isLoadingFailed">'
			+ '<div class="alert-text">'
			+ 'Dayum! There was some error.' + ' Please try later.'
			+ '</div>' + '</div>';
		
		return {
			restrict : 'E',
			template : template,
			scope: {
				size: '=',
				color: '=',
				type: '='
			},
			link: function($scope) {
				$scope.isRouteLoading = true;
				$scope.isLoadingFailed = false;

				$scope.$on('$stateChangeStart', function() {
					$scope.isRouteLoading = true;
					$rootScope.uiTransit = 'ui-disappear';
				});

				$scope.$on('$stateChangeSuccess', function() {
					$scope.isRouteLoading = false;
					$rootScope.uiTransit = '';
				});

				$scope.$on('$stateChangeError', function() {
					$scope.isRouteLoading = false;
					$scope.isLoadingFailed = true;
				});

			}
		};
	});
})();