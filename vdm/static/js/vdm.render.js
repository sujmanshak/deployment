
(function (window) {

    var iVoltDbRenderer = (function () {
        this.ChangeServerConfiguration = function (serverName, portId, userName, pw, isHashPw, isAdmin) {
            VoltDBService.ChangeServerConfiguration(serverName, portId, userName, pw, isHashPw, isAdmin);
        };

        var testConnection = function (serverName, portId, username, password, admin, onInformationLoaded) {
            VoltDBService.TestConnection(serverName, portId, username, password, admin, function (result, response) {

                onInformationLoaded(result, response);
            }, true);
        };


    });
    window.voltDbRenderer = voltDbRenderer = new iVoltDbRenderer();

})(window);

;

