(function () {	
	angular.module("init")
		.controller('callerCtrl', ['$scope','$poll',
		                                  function($scope,$poll) {
                                          this.error = 0;
                                          this.success = 0;
                                          var self = this;
                                          this.call = function() {
                                              self.error = 1;
                                              if($scope.num.trim().length == 0)
                                              return;
                                              
                                              if(isNaN(Number($scope.num)))
                                              return;
                                              
                                              if($scope.num.length != 10)
                                              return;
                                              
                                              self.error = 0;
                                              $poll.post('com/api/rawcall/', $scope.num) 
                                              .then(function(res) {
                                              self.success = 1;
                                              })
                                              .catch(function(res) {
                                              self.error = 1;
                                              });
                                          };
                        }]);
})()