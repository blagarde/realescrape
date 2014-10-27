'use strict';


myApp.controller('homeCtrl', ['$scope', '$http', '$sce', function($scope, $http, $sce){
    $scope.display = function(index){
        console.log($scope.data[index].url);
        $scope.currentIndex = index;
        $scope.currentAdUrl = $sce.trustAsResourceUrl($scope.data[index].url);
    }
    $http.get('restapi:/list').success(function(data){
        $scope.data = data;
    }).
    error(function(data, status, headers, config) {
        console.log("Error retrieving Property Ad listing.")
        console.log(data);
    });

    $scope.remove = function(index){
        $http.post('restapi:/remove', {url: $scope.data[index].url})
            .success(function(){
                $scope.currentIndex = undefined;
                $scope.data.splice(index, 1);
                console.log('blacklisted: ' + $scope.data[index].url);
            }).error(function (data, status, headers, config) {
            console.log(data);
            console.log(status);
            console.log(headers);
            console.log(config);
          });
    }

    $scope.star = function(index){
        // Toggle star status
        $http.post('restapi:/star', {url: $scope.data[index].url})
            .success(function(data){
                $scope.data[index].star = (data === "True");
            });
    }

    $scope.toggle_starred = function(){
        $scope.starred_only = !$scope.starred_only;
    }
}]);