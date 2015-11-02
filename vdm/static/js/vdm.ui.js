$(document).ready(function (e) {
    $('#accordion').on('hidden.bs.collapse', function() {
        //do something...
    });

    $('#accordion .accordion-toggle').click(function (e) {
        var chevState = $(e.target).siblings("i.indicator").toggleClass('glyphicon-triangle-right glyphicon-triangle-bottom');
        $("i.indicator").not(chevState).removeClass("glyphicon-triangle-bottom").addClass("glyphicon-triangle-right");
    });

    // Make Expandable Rows.
    $('tr.parent > td:first-child' || 'tr.parent > td:fourth-child')
        .css("cursor", "pointer")
        .attr("title", "Click to expand/collapse")
        .click(function () {
            var parent = $(this).parent();
            parent.siblings('.child-' + parent.attr("id")).toggle();
            parent.find(".glyphicon-triangle-right").toggleClass("glyphicon-triangle-bottom");
        });
    $('tr[class^=child-]').hide().children('td');
    

    $("#navbar li").click(function () {
        $("#navbar li").removeClass('active');
        $(this).addClass('active');
        getCurrentTabContent();
        VoltDbManagerUI.CurrentTab = getCurrentTab();
        saveSessionCookie("current-tab", VoltDbManagerUI.CurrentTab);
        $("#navbar").removeClass("in");
    });

    loadPage();
});

var saveCookie = function (name, value) {
    $.cookie(name + "_" + VoltDBConfig.GetPortId(), value, { expires: 365 });
};

var saveSessionCookie = function (name, value) {
    $.cookie(name + "_" + VoltDBConfig.GetPortId(), value);
};

var NavigationTabs = {
    DBManager: 1,
    ServerSetting: 2
};

var getCurrentTab = function () {
    var activeLinkId = "";
    var activeLink = $("#navbar  li.active a");
    if (activeLink.length > 0) {
        activeLinkId = activeLink.attr("id");
    }
    if (activeLinkId == "serverSetting")
        return NavigationTabs.ServerSetting;

    return NavigationTabs.DBManager;
};

var getCurrentTabContent = function() {
    var activeLinkId = "";
    var activeLink = $("#navbar  li.active a");
    if (activeLink.length > 0) {
        activeLinkId = activeLink.attr("id");
    }
    if (activeLinkId == "serverSetting") {
        $("#divDbManager").addClass("hidden");
        $("#divServerSetting").removeClass("hidden");
    } else {
        $("#divServerSetting").addClass("hidden");
        $("#divDbManager").removeClass("hidden");
    }
};

var saveCurrentServer = function (serverName) {
    saveCookie("currentServer", serverName);
};

var getCurrentServer = function () {
    return VoltDbManagerUI.getCookie("currentServer");
};

var loadPage = function() {
    //Retains the current tab while page refreshing.
    var retainCurrentTab = function () {
        var curTab = VoltDbManagerUI.getCookie("current-tab");
        if (curTab != undefined) {
            curTab = curTab * 1;
            if (curTab == NavigationTabs.ServerSetting) {
                $("#overlay").show();
                setTimeout(function () { $("#serverSetting").trigger("click"); }, 100);
            }
        }
    };
    retainCurrentTab();

    VoltDBService.GetServerList(function(connection){
        debugger;
        VoltDbManagerUI.displayServers(connection.Metadata['SERVER_LISTING'])
    })

    $('#btnCreateServerOk').on('click', function(){
        var serverName = $('#serverName').val()
        var serverData ={
            "name" : serverName,
            "hostname" : serverName,
            "description" : "test " + serverName
        }
        VoltDBService.CreateServer(function(connection){
            if(connection.Metadata['SERVER_CREATE'].status == 1){
                VoltDBService.GetServerList(function(connection){
                    debugger;
                    VoltDbManagerUI.displayServers(connection.Metadata['SERVER_LISTING'])
                })
            }
        },serverData);
    });

    $('#deleteServerOk').on('click',function(){
        debugger;
        var serverId = $('#deleteConfirmation').data('serverid');
        var serverData = {
           "id": serverId
        }
        VoltDBService.DeleteServer(function(connection){
            VoltDBService.GetServerList(function(connection){
                debugger;
                VoltDbManagerUI.displayServers(connection.Metadata['SERVER_LISTING'])
            })
        }, serverData);
    })

};

(function (window) {
    var iVoltDbManagerUi = (function () {
        this.CurrentTab = NavigationTabs.DBMonitor;

        this.getCookie = function(name) {
            return $.cookie(name + "_" + VoltDBConfig.GetPortId());
        };

        this.displayServers = function(serverList){
            if (serverList == undefined) {
                return;
            }
            var htmlList = '<tr>' +
                            '<th><span class="serverIcon">Servers</span></th>' +
                            '<th>' +
                            '<div class="addServer">' +
                            '<a id="btnAddServer" href="javascript:void(0);"data-toggle="modal" data-target="#addServer"> <span class="plus"></span>Add Server</a> </div>' +
                            '</th>' +
                       '</tr>';

            serverList.servers.forEach(function (info) {
                var hostName = info["hostname"];
                var hostId = info["id"];
                htmlList += '<tr>' +
                            '<td>' + hostName + '</td>' +
                            '<td data-id="' + hostId + '" ><a class="btnDeleteServer" href="javascript:void(0);"data-toggle="modal" data-target="#deleteConfirmation" >' +
                            '<div class="deleteServer"></div>' +
                            '</a> <span class="deleteServerTxt">Delete</span></td>' +
                        '</tr>';
            });

            $('#serverList').html(htmlList)

            $('.btnDeleteServer').on('click', function(){
                var serverId = $(this.parentElement).data('id');
                $('#deleteConfirmation').data('serverid',serverId);
            });

            $('#btnAddServer').on('click', function(){
                $('#serverName').val('');
            });
        };
    });
    window.VoltDbManagerUI = VoltDbManagerUI = new iVoltDbManagerUi();

})(window);



