'use strict';

// Declare app level module which depends on views, and components
var myApp = angular.module('myApp', [
  'ngRoute',
  'appConfig',
  'ui.bootstrap'
]);
myApp.config(['$routeProvider', '$httpProvider', 'configuration', function($routeProvider, $httpProvider, configuration) {
    $routeProvider.when('/home', {templateUrl: 'front/partials/home.html', controller: 'homeCtrl'});
    $routeProvider.otherwise({redirectTo: '/home'});

    $httpProvider.interceptors.push(function ($q) {
             return {
                 'request': function (config) {
                     if (config.url.lastIndexOf("restapi:", 0) === 0)
                        config.url = configuration.serviceUrl + config.url.slice("restapi:".length);
                     return config || $q.when(config);
                 }
             }
         });
}]);
