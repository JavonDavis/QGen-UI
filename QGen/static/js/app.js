var app = angular.module('Variables',['ui.bootstrap']);

app.controller('MainCtrl', function($scope){
	
	$scope.newvariable = "";
	
	$scope.title = "Build a Question template!";
	$scope.alertblank = { show: false, type:"Info", msg:"Info"};
	$scope.success_alert = { show: true, type: 'success', msg:"Successfully added variable!"};
	$scope.danger_alert = { show: true, type: 'danger', msg:"Please enter a valid variable name"};
	$scope.variables = [];
	$scope.alert = $scope.alertblank;
	$scope.addvariable = function(variable){
		if (variable == ""){
			$scope.alert = $scope.danger_alert;
		}else{
			$scope.variables.push(variable);
			
			$scope.newvariable = "";
			
			$scope.alert = $scope.success_alert;

		}
		
		
	};
	
	$scope.removeItem = function (x) {
        $scope.variables.splice(x, 1);
    }
	
	
})