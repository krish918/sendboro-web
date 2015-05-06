(function () {
  angular.module("init")
	.directive('authPanel', function() {
		return {
			restrict: 'E',
			templateUrl: '/decorator/auth-panel',
			
			controller: function ($scope) {
				
				//these classes are for keeping the shake-on-error effect available 
				this.classArr = ['invalid-input-1','invalid-input-2'];
				
				$scope.inputClass = '';
				
				
				this.validateForm = function (obj) {
					
					//obj will inject the appropriate form(signup/signin) into the controller
					
					if (obj === undefined || !obj.$valid) {
						$scope.inputClass = ($scope.inputClass == this.classArr[0])
											? this.classArr[1] : this.classArr[0];
						return false;						
					}
					else $scope.inputClass = '';
					return true;
				};
				
				
				
			},
			
			controllerAs: 'frmCtrl'
		};
		
	});
	
})();