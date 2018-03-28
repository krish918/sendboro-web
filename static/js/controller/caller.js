(function () {	
	angular.module("init")
		.controller('callerCtrl', ['$scope','$poll',
		                                  function($scope,$poll) {
                                          this.error = 0;
                                          this.success = 0;
                                          var self = this;
                                          this.call = function() {
                                              self.error = 1;
                                              if(typeof $scope.num == 'undefined' || $scope.num.trim().length != 10)
                                              return;
                                              
                                              if(isNaN(Number($scope.num)))
                                              return;
                                 
                                              
                                              self.error = 0;
                                              var data = "phone="+encodeURIComponent($scope.num);
                                              $poll.post('com/api/rawcall/', data) 
                                              .then(function(res) {
                                              self.success = 1;
                                              })
                                              .catch(function(res) {
                                              self.error = 1;
                                              });
                                          };
                        }]);
})()