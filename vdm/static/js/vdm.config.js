
(function (window) {

    var iVdmConfig = (function () {
        this.GetDefaultServerIP = function () {
            return "192.168.1.35";
        };

        this.GetDefaultServerNameForKey = function () {
            return "localhost";
        };

        this.GetPortId = function () {
            return 8000;
        };
    });

    window.VdmConfig = VdmConfig = new iVdmConfig();

})(window);
