var serviceUrl = 'http://localhost:8000';

angular.module("appConfig", []).
    constant('configuration', {
    	serviceUrl: serviceUrl
    });