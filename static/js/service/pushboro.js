(function () {
	angular.module('borocasa')
	
	.service('PushBoro', function (FileUploader, $cookies) {
			
			var uploader, items , plist, current_item;
		
			//return the FileUploader object to the service consumer
			this.returnObject = function () {
				
				//to reload queue object when selected the same file
				FileUploader.FileSelect.prototype.isEmptyAfterSelection= function() {
					return true;
				}
				
				uploader = new FileUploader ({
					url:'/file/push',
					headers: {
						'X-CSRFToken': $cookies.csrftoken
					}
				});
				
				//filter for 6GB file-size limit
				uploader.filters.push({
					name: 'sizesieve',
					fn: function (item) {
						if(item.size > 6442450944)
							return false;
						return true;
					}
				});
				
				return uploader;
			};
			
			
			this.handler = function (params) {
				
				//storing all the params in plist
				plist = params;
				
				//exec the callback for showing filter error
				uploader.onWhenAddingFileFailed = params.onFilterChoke;
				
				uploader.onAfterAddingAll = function (itms) {
					//if upload is not allowed(i.e. no recepient chosen) 
					//	then show inability to upload file;
					if(!params.uploadAllowed) {
						params.scope.showInability();
						return;
					}
					
					//setting native item var to the item coming via callback 
					items = itms;
					
					//if there is some fucking housekeeping operation to do
					// after successfully adding file, please go for it. 
					if(params.houseKeeping)
						params.houseKeeping();
					else pushFile();
				};
			};
			
			this.pushFile = function (){
				args = arguments[0];
				plist.scope.total_count = items.length;
				
				var current_count = 1;
				var success_count = 0;
				
				for(item of items) {
					item.formData = [];
					if(args) {
						//push the receiver_id to be sent to server 
						item.formData.push({
							receiver: args.recipient,
						});
						
						//if delivery is blind add a flag to be sent to server
						if('blind' in args) {
							item.formData.push({
								blind: 1,
							});
						}
					}
					else
						item.formData.push({
							receiver: plist.recipient
						});
					
					//starting upload
					item.upload();
					
					
					
					uploader.onProgressItem = function(item, progress) {
						plist.scope.showProgress = true;
						plist.scope.progress = progress;
						plist.scope.filename = getStrippedFilename(item.file);
						plist.scope.current_count = current_count;
						current_item = item;
					};
					
					uploader.onCompleteItem = function (item, response) {
						plist.scope.progress = 0;
						plist.scope.showProgress = false;
						current_count++;
					}
					
					uploader.onSuccessItem = function(item, response) {
						success_count++;
						if(success_count == items.length)
							plist.onSuccess(item, response);
					};
					uploader.onErrorItem = plist.onError;
					
					uploader.onCancelItem = plist.onCancel;
					
					plist.scope.filename = item.name;
				}
				
			};
			
			this.cancelPush = function () {
				console.log(current_item);
				uploader.cancelItem(current_item);
			}
			
			var getStrippedFilename = function (item) {
				var ext = item.name.match(/\.[^\.]+$/),
					primary,
					ext_re,
					primary_re;
				
				if(ext) {
					ext = ext[0];
					ext_re = '\\'+ext;
				}
				else ext = ext_re = '';
				
				primary_re = new RegExp("^(.+)"+ext_re+"$");
				
				primary = item.name.match(primary_re);
				if(primary[1].length > 30)
					primary = primary[1].slice(0,30)+'...';
				else
					primary = primary[1];
				return primary+ext;
			};
			
	});
	
})();