(function () {
  angular.module("init")
	.directive('authPanel', function() {
		return {
			restrict: 'E',
			templateUrl: '/decorator/auth-panel',
		};
		
	})
	
	.directive('featurePanel', function(){
		return {
			restrict: 'E',
			templateUrl: '/decorator/feature-panel'
		};
	});
	
})();