(function () {
	angular.module("init")
		.directive('authProblemPanel', function ($log) {
			return {
				restrict: 'E',
				templateUrl: '/decorator/auth-problem-panel',
				
				controller: function ($scope) {
					this.problem = 0;
					this.problist = [
					                 'I lost my authphrase partial.',
					                 'I didn\'t get authphrase partial on my phone.',
					                 'I lost my phone.',
					                 'I can\'t figure out my authphrase climax.',
					                 'I can\'t remember the authphrase separator.',
					                 'Everything\'s alright, but still I can\'t sign in.'
					                ];
					
					this.isChecked = function(choice) {
						return choice === this.problem
					};
					
					this.selectChoice = function(choice) {
						this.problem = choice;
						$scope.checkedClass = [];
						$scope.checkedClass[choice-1] = 'selected';
					}
				},
				
				controllerAs: 'authProb'
			};
		});
	
})();