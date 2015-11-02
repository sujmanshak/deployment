(function (window) {
    var procedures = {};
    var tips = $(".validateTips");
    var server = VoltDBConfig.GetDefaultServerIP();
    var port = VoltDBConfig.GetPortId();
    var user = "";
    var password = "";
    var admin = true;
    var isHashedPassword = true;
    this.connection = null;
    var iVoltDbService = (function () {
        var _connection = connection;

        this.SetUserCredentials = function (lUsername, lPassword, lAdmin) {
            user = lUsername;
            password = lPassword;
            admin = lAdmin;
        };

        // build Authorization header based on scheme you could flip to diff header. Server understands both.
        this.BuildAuthorization = function(user, isHashedPassword, password) {
            var authz = null;
            if (user != null && isHashedPassword != null) {
                authz = "Hashed " + user + ":" + isHashedPassword;
            } else if (user != null && password != null) {
                var up = user + ":" + password;
                authz = "Basic " + CryptoJS.SHA256({ method: "b64enc", source: up });
            }
            return authz;
        };

        this.ChangeServerConfiguration = function (serverName, portId, userName, pw, isHashPw, isAdmin) {
            server = serverName != null ? serverName : server;
            port = portId != null ? portId : port;
            user = userName != undefined ? userName : "";
            password = pw != undefined ? pw : "";
            isHashedPassword = isHashPw;
            admin = isAdmin != undefined ? isAdmin : true;

        };

        this.GetServerList = function (onConnectionAdded) {
           debugger;
            try {
                var processName = "SERVER_LISTING";
                var requestMethod = "get"
                _connection = VoltDBCore.HasConnection(server, port, admin, user, processName);
                if (_connection == null){
                    VoltDBCore.AddConnection(server, port, admin, user, password, isHashedPassword, processName, function (connection, status) {
                        onConnectionAdded(connection, status);
                    }, requestMethod);

                } else {
                    VoltDBCore.updateConnection(server, port, admin, user, password, isHashedPassword, processName, _connection, function (connection, status) {
                        onConnectionAdded(connection, status);
                    }, requestMethod);
                }
            } catch (e) {
                console.log(e.message);
            }
        };

        this.CreateServer = function (onConnectionAdded, serverData) {
            try {
                var processName = "SERVER_CREATE";
                var requestMethod = "POST"
                var serverDetails = {
                    "serverData" :serverData
                }
                _connection = VoltDBCore.HasConnection(server, port, admin, user, processName);
                if (_connection == null){
                    VoltDBCore.AddConnection(server, port, admin, user, password, isHashedPassword, processName, function (connection, status) {
                        onConnectionAdded(connection, status);
                    }, requestMethod,serverDetails);
                } else {
                    VoltDBCore.updateConnection(server, port, admin, user, password, isHashedPassword, processName, _connection, function (connection, status) {
                        onConnectionAdded(connection, status);
                    }, requestMethod,serverDetails);
                }
            } catch (e) {
                console.log(e.message);
            }
        };

        this.DeleteServer = function (onConnectionAdded,serverData){
            try {
                var processName = "SERVER_DELETE";
                var requestMethod = "DELETE"
                var serverDetails = {
                    serverData:serverData
                };
                _connection = VoltDBCore.HasConnection(server, port, admin, user, processName);
                if (_connection == null){
                    VoltDBCore.AddConnection(server, port, admin, user, password, isHashedPassword, processName, function (connection, status) {
                        onConnectionAdded(connection, status);
                    }, requestMethod,serverDetails);
                } else {
                    VoltDBCore.updateConnection(server, port, admin, user, password, isHashedPassword, processName, _connection, function (connection, status) {
                        onConnectionAdded(connection, status);
                    }, requestMethod,serverDetails);
                }
            } catch (e) {
                console.log(e.message);
            }
        }
    });
    window.VoltDBService = VoltDBService = new iVoltDbService();
})(window);

