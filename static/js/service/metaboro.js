(function () {
	angular.module('borocasa')
	
	
	.factory('$metaboro', ['$rootScope','$http','$q','mbStatus', 
	                      function($rootScope,$http, $q, mbStatus) {
		
		this.dump = {};
		
		
		var e = 'metaboro.update',
		    deferred = $q.defer(),
		    self = this;
		
		//called whenever a controller updates data of this service
		var updateState = function (data) {
			

				/*for(var key in self.dump) {
				if(self.dump.hasOwnProperty(key)) {
					for(key2 in data) {
						if(data.hasOwnProperty(key2) && key2 == key) {
							self.dump[key] = data[key2];
						}
					}
				}
				
			}*/
			//self.dump['sent'] = data.sent;
			if('immediate' in data) {
					self.dump['data'] = data['data'];
					//console.log(self.dump.data);
					broadcast();
			}
			else {
			
			for (var key in data) {
				if(typeof data[key] !== 'object')
					self.dump.data[key] = data[key];
				else {
					for(var key2 in data[key])
						if(typeof data[key][key2] !== 'object')
							self.dump.data[key][key2] = data[key][key2];
						else {
							for (var key3 in data[key][key2])
							   if(typeof data[key][key2][key3] !== 'object')
								   self.dump.data[key][key2][key3] = data[key][key2][key3];
						}
				}
			}
			}
			broadcast();
		};
		
		//internally used by updateState to broadcast changes to all child elements
		var broadcast = function () {
			$rootScope.$broadcast(e);
		}
		
		//called by a controller to keep listening to updates and update their data as well
		var onUpdate = function (scope, callback) {
			scope.$on(e, function () {
				callback();
			});
		};
		
		this.dump.update = updateState;
		this.dump.listenUpdate = onUpdate;
		
		var metaboroService = function () {
			
			if(self.dump.data) {
				return self.dump;
			}
			
			$http({
				url: '/api/metauser',
				method: 'get',
				
				//setting custom headers for a loose protections against CSRF
				headers: {
					'X-CSRF-Header': 'ahusnodjTG76gf98gHG'
				}
			})
			
			.success(function(response) {
				console.log(response);
				if('error' in response)
					deferred.reject();
				else {
					self.dump.data = response 
					mbStatus.resolved = true;
					deferred.resolve(self.dump);
				}
					
			})
			.error(function(response) {
				console.log(response);
				deferred.reject();
			});
			
			return deferred.promise;
		};
		
		return metaboroService();
		
	}])
	
	.factory('mbStatus', function () {
		return {
			resolved: false,
			appRunning: false,
		};
	});
	
})();