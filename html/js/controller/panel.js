
(function () {
	angular.module("init")
		.controller('panelController', function ($scope) {
			this.panel = 0;
			
			this.showPanel = function(pan) {
				$scope.visibility = 'visible';
				this.panel = pan;
				$scope.inputClass = '';  //flushes the ng-class for both input-boxes to bring them to normal state
			}
			
			this.isClicked = function(pan) {
				return this.panel === pan;
		}
	});
})();