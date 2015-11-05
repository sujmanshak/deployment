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
        VdmUI.CurrentTab = getCurrentTab();
        saveSessionCookie("current-tab", VdmUI.CurrentTab);
        $("#navbar").removeClass("in");
    });

    //checkbox
    $("input[type=checkbox]").on('ifChanged', function () {
     var onOffText = $(this).is(":checked") ? "On" : "Off";
     $(this).parent().parent().next().text(onOffText);
    });

    loadPage();
});

var saveCookie = function (name, value) {
    $.cookie(name + "_" + VdmConfig.GetPortId(), value, { expires: 365 });
};

var saveSessionCookie = function (name, value) {
    $.cookie(name + "_" + VdmConfig.GetPortId(), value);
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
    return VdmUI.getCookie("currentServer");
};

var loadPage = function() {
    //Retains the current tab while page refreshing.
    var retainCurrentTab = function () {
        var curTab = VdmUI.getCookie("current-tab");
        if (curTab != undefined) {
            curTab = curTab * 1;
            if (curTab == NavigationTabs.ServerSetting) {
                $("#overlay").show();
                setTimeout(function () { $("#serverSetting").trigger("click"); }, 100);
            }
        }
    };
    retainCurrentTab();

    var validationRules = {
        ServerNameRule: {
            required: true,
            checkDuplicateServer: [],
            regex: /^[a-zA-Z0-9_.]+$/
        },
        ServerNameMessage: {
            required: "This field is required",
            checkDuplicateServer: 'This server name already exists.',
            regex: 'Only alphabets, numbers, _ and . are allowed.'
        },
        HostNameRule:{
            required: true,
            checkDuplicateHost: [],
            regex: /^[a-zA-Z0-9_.]+$/
        },
        HostNameMessage: {
            required: "This field is required",
            checkDuplicateHost:'This host name already exists.',
            regex: 'Only alphabets, numbers, _ and . are allowed.'
        }
    }

    $.validator.addMethod(
        "checkDuplicateServer",
        function (value) {
            var arr = VdmUI.CurrentServerList;
            if (VdmUI.isServerCreate == false) {
                if ($.inArray(value, arr) != -1) {
                    if (value == VdmUI.serverToUpdate)
                        return true;
                    return false;
                } else {
                    return true;
                }
            } else {
                if ($.inArray(value, arr) != -1) {
                    return false;
                } else {
                    return true;
                }
            }
        },
        "Server name already exists."
    );

    $.validator.addMethod(
        "checkDuplicateHost",
        function (value) {
            var arr = VdmUI.CurrentHostList;
            if (VdmUI.isServerCreate == false) {
                if ($.inArray(value, arr) != -1) {
                    if (value == VdmUI.hostToUpdate)
                        return true;
                    return false;
                } else {
                    return true;
                }
            } else {
                if ($.inArray(value, arr) != -1) {
                    return false;
                } else {
                    return true;
                }
            }
        },
        "Host name already exists."
    );

    $.validator.addMethod(
        "regex",
        function (value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Please enter only valid characters."
    );

    VdmService.GetServerList(function(connection){
        VdmUI.displayServers(connection.Metadata['SERVER_LISTING'])
    })

    $("#frmCreateServer").validate({
        rules: {
            serverName: validationRules.ServerNameRule,
            txtHostName: validationRules.HostNameRule
        },
        messages: {
            serverName: validationRules.ServerNameMessage,
            txtHostName: validationRules.HostNameMessage
        }
    });

    $('#btnCreateServerOk').on('click', function(e){
        if (!$("#frmCreateServer").valid()) {
                    e.preventDefault();
                    e.stopPropagation();
                    return;
                }
        var serverName = $('#serverName').val()
        var hostName = $('#txtHostName').val()
        var description = $('#txtDescription').val()
        var serverInfo ={
            serverData:{
                "name" : serverName,
                "hostname" : hostName,
                "description" : description
            },
            id:$('#addServer').data('serverid')
        }
        if(VdmUI.isServerCreate){
            VdmService.CreateServer(function(connection){
                if(connection.Metadata['SERVER_CREATE'].status == 1){
                    VdmService.GetServerList(function(connection){
                        VdmUI.displayServers(connection.Metadata['SERVER_LISTING'])
                    })
                } else{
                    $('#errorMsg').html('Unable to create server.')
                    $('#errorDialog').modal('show');
                }
            },serverInfo);
        } else {
            VdmService.UpdateServer(function(connection){
                if(connection.Metadata['SERVER_UPDATE'].status == 1){
                    VdmService.GetServerList(function(connection){
                        VdmUI.displayServers(connection.Metadata['SERVER_LISTING'])
                    })
                } else{
                    $('#errorMsg').html('Unable to update server.')
                    $('#errorDialog').modal('show');
                }
            },serverInfo);
        }
    });

    $('#deleteServerOk').on('click',function(){
        var serverId = $('#deleteConfirmation').data('serverid');
        var serverData = {
           "id": serverId
        }
        VdmService.DeleteServer(function(connection){
            VdmService.GetServerList(function(connection){
                VdmUI.displayServers(connection.Metadata['SERVER_LISTING'])
            })
        }, serverData);
    })
};

(function (window) {
    var iVdmUi = (function () {
        this.CurrentTab = NavigationTabs.DBMonitor;
        this.CurrentServerList = [];
        this.CurrentHostList = [];
        this.isServerCreate = true;
        this.serverToUpdate = '';
        this.hostToUpdate = '';
        this.getCookie = function(name) {
            return $.cookie(name + "_" + VdmConfig.GetPortId());
        };

        this.displayServers = function(serverList){
            if (serverList == undefined) {
                return;
            }
            var htmlList = "";
            VdmUI.CurrentServerList = [];
            VdmUI.CurrentHostList = [];
            serverList.servers.forEach(function (info) {
                var hostName = info["hostname"];
                var serverName = info["name"]
                var hostId = info["id"];
                var infos = JSON.stringify(info)
                htmlList += '<tr>' +
                            '<td>' + hostName + '</td>' +
                            '<td data-id="' + hostId + '" data-info=\''+ infos +'\'><a class="btnUpdateServer" href="javascript:void(0);"data-toggle="modal" data-target="#addServer" >' +
                            '<div class="editServer"></div>' +
                            '</a> <span class="editServerTxt">Edit</span></td>' +
                            '<td data-id="' + hostId + '" ><a class="btnDeleteServer" href="javascript:void(0);"data-toggle="modal" data-target="#deleteConfirmation" >' +
                            '<div class="deleteServer"></div>' +
                            '</a> <span class="deleteServerTxt">Delete</span></td>' +
                        '</tr>';
                VdmUI.CurrentServerList.push(serverName);
                VdmUI.CurrentHostList.push(hostName)
            });
            if(htmlList == ""){
                $('#serverList').html('<tr><td style="top:-1px !important">No servers Available.</td><td></td></tr>')
            }else{
                $('#serverList').html(htmlList)
            }

            $('.btnDeleteServer').on('click', function(){
                var serverId = $(this.parentElement).data('id');
                $('#deleteConfirmation').data('serverid',serverId);
            });

            $('.btnUpdateServer').on('click', function(){
                VdmUI.isServerCreate = false;
                var serverInfo = $(this.parentElement).data('info');
                VdmUI.serverToUpdate = serverInfo['name'];
                VdmUI.hostToUpdate = serverInfo['hostname'];
                $('#addServer').data('serverid',serverInfo['id']);
                $('#serverName').val(serverInfo['name']);
                $('#txtHostName').val(serverInfo['hostname']);
                $('#txtDescription').val(serverInfo['description']);
                $('#addServerTitle').html('Update Server');
                $('#errorServerName').hide();
                $('#errorHostName').hide();
                $('#errorDescription').hide();
            });

            $('#btnAddServer').on('click', function(){
                VdmUI.isServerCreate = true;
                VdmUI.serverToUpdate = '';
                VdmUI.hostToUpdate = '';
                $('#addServerTitle').html('Add Server');
                $('#serverName').val('');
                $('#txtHostName').val('');
                $('#txtDescription').val('');
                $('#errorServerName').hide();
                $('#errorHostName').hide();
                $('#errorDescription').hide();
            });
        };
    });
    window.VdmUI = VdmUI = new iVdmUi();

})(window);



