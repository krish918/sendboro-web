(function (){
	
	var ctrlFunc = function($scope, user, $poll, $timeout){

		var self = this;

		$scope.isEmpty = false;

		$scope.init = function() {
			$scope.animateWidget = 'animateWidget';
			self.user = user.data;

			if(self.user.sent.length == 0)
				isEmpty = true;

			user.listenUpdate($scope, function (newdata) {
						self.user = user.data;
					});

			
		};
		
	};	
	
	angular.module("borocasa")
	
	.controller('sentController', ctrlFunc);
	
})()