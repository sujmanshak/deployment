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

    //multi-select
    var s = $('#my-select');
    s.multiSelect({
        selectableHeader: "<div class='custom-header'>All Database</div>",
        selectionHeader: "<div class='custom-header'>Selected Database</div>"
    });

    loadPage();
});


var editStates = {
    ShowEdit: 0,
    ShowOkCancel: 1,
    ShowLoading: 2
};


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
        },
        PortRule:{
            portRegex : /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/
        },
        PortMessage:{
            portRegex : "Please enter a valid value.(e.g, 127.0.0.1:8000 or 8000(1-65535))"
        },
        IpRule:{
            regex: /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/
        },
        IpMessage:{
            regex: 'Please enter a valid IP address.'
        },
        DatabaseNameRule:{
            required: true,
            checkDuplicateDb: [],
            regex: /^[a-zA-Z0-9_.]+$/
        },
        DatabaseNameMessage:{
            required: "This field is required.",
            checkDuplicateDb: 'This database already exists.',
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
        "checkDuplicateDb",
        function (value) {
            var arr = VdmUI.CurrentDbList;
            if (VdmUI.isDbCreate == false) {
                if ($.inArray(value, arr) != -1) {
                    if (value == VdmUI.dbToUpdate)
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
        "Database already exists."
    );

    $.validator.addMethod(
        "regex",
        function (value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Please enter only valid characters."
    );

    $.validator.addMethod(
        "portRegex",
        function(value, element, regexp){
            var result = true
            var values = value.split(':');
            var re = new RegExp(regexp);
            if(values.length == 1){
                if(!$.isNumeric(values[0]) || !(values[0] > 1 && values[0] < 65536))
                    result = false;
                else{
                    if(values[0].split('.').length > 1)
                        result = false;
                }
            } else if(values.length == 2){
                if(!$.isNumeric(values[1]) || !(values[1] > 1 && values[1] < 65536))
                    result = false;
                else{
                    if(values[1].split('.').length > 1)
                        result = false;
                }
                if(!re.test(values[0]))
                    result = false;
            } else {
                result = false;
            }

            return this.optional(element) || result;
        },
        "Please enter only valid character."
    );

    VdmService.GetServerList(function(connection){
        VdmUI.displayServers(connection.Metadata['SERVER_LISTING'])
    })

    VdmService.GetDatabaseList(function(connection){
        VdmUI.displayDatabases(connection.Metadata['DATABASE_LISTING'])
    });

    setInterval(function () {
        VdmService.GetServerList(function(connection){
            VdmUI.displayServers(connection.Metadata['SERVER_LISTING'])
        })
    }, 5000);

    $("#frmCreateServer").validate({
        rules: {
            serverName: validationRules.ServerNameRule,
            txtHostName: validationRules.HostNameRule,
            txtClientPort:validationRules.PortRule,
            txtAdminPort:validationRules.PortRule,
            txtZookeeper:validationRules.PortRule,
            txtReplicationPort:validationRules.PortRule,
            txtInternalInterface:validationRules.IpRule,
            txtExternalInterface:validationRules.IpRule,
            txtPublicInterface:validationRules.IpRule,
            txtInternalPort:validationRules.PortRule,
            txtHttpPort:validationRules.PortRule,
        },
        messages: {
            serverName: validationRules.ServerNameMessage,
            txtHostName: validationRules.HostNameMessage,
            txtClientPort:validationRules.PortMessage,
            txtAdminPort:validationRules.PortMessage,
            txtZookeeper:validationRules.PortMessage,
            txtReplicationPort:validationRules.PortMessage,
            txtInternalInterface:validationRules.IpMessage,
            txtExternalInterface:validationRules.IpMessage,
            txtPublicInterface:validationRules.IpMessage,
            txtInternalPort:validationRules.PortMessage,
            txtHttpPort:validationRules.PortMessage,
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
        var clientPort = $('#txtClientPort').val()
        var adminPort = $('#txtAdminPort').val()
        var internalPort = $('#txtInternalPort').val()
        var httpPort = $('#txtHttpPort').val()
        var zookeeperPort = $('#txtZookeeper').val()
        var replicationPort = $('#txtReplicationPort').val()
        var internalInterface = $('#txtInternalInterface').val()
        var externalInterface = $('#txtExternalInterface').val()
        var publicInterface = $('#txtPublicInterface').val()
        var placementGroup = $('#txtPlacementGroup').val()
        var serverInfo ={
            data:{
                "name" : serverName,
                "hostname" : hostName,
                "description" : description,
                "client-listener" : clientPort,
                "admin-listener" : adminPort,
                "internal-listener" : internalPort,
                "http-listener" : httpPort,
                "zookeeper-listener" : zookeeperPort,
                "replication-listener" : replicationPort,
                "internal-interface" : internalInterface,
                "external-interface" : externalInterface,
                "public-interface" : publicInterface,
                "placement-group" : placementGroup,
            },
            id:$('#addServer').data('serverid')
        }
        var hostId = $('#addServer').data('serverid')
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

            toggleServer(editStates.ShowLoading,hostId)

            VdmService.UpdateServer(function(connection){
                if(connection.Metadata['SERVER_UPDATE'].status == 1){
                    VdmService.GetServerList(function(connection){
                        VdmUI.displayServers(connection.Metadata['SERVER_LISTING'])
                    })
                } else{
                    $('#errorMsg').html('Unable to update server.')
                    $('#errorDialog').modal('show');
                    toggleServer(editStates.ShowEdit,hostId);
                }
            },serverInfo);

        }
        VdmUI.resetTextBox();
    });

    $('#frmCreateDB').validate({
        rules: {
            txtDbName: validationRules.DatabaseNameRule
        },
        messages: {
            txtDbName: validationRules.DatabaseNameMessage
        }

    });

    $('#btnAddDatabaseOk').on('click', function(e){
        if (!$("#frmCreateDB").valid()) {
            e.preventDefault();
            e.stopPropagation();
            return;
        }

        var dbName = $('#txtDbName').val();
        var deployment = $('#txtDeployment').val();
        var dbInfo = {
            data:{
                name: dbName,
                deployment: deployment
            },
            id:$('#addDatabase').data('id')
        }
        if(VdmUI.isDbCreate){
            VdmService.CreateDatabase(function(connection){
                if(connection.Metadata['DATABASE_CREATE'].status == 1){
                    VdmService.GetDatabaseList(function(connection){
                        VdmUI.displayDatabases(connection.Metadata['DATABASE_LISTING'])
                    })
                } else{
                    $('#errorMsg').html('Unable to create database.')
                    $('#errorDialog').modal('show');
                }
            }, dbInfo);
        } else {
            VdmService.UpdateDatabase(function(connection){
                if(connection.Metadata['DATABASE_UPDATE'].status == 1){
                    VdmService.GetDatabaseList(function(connection){
                        VdmUI.displayDatabases(connection.Metadata['DATABASE_LISTING'])
                    })
                } else {
                    $('#errorMsg').html('Unable to update database.')
                    $('#errorDialog').modal('show');
                }
            }, dbInfo);
        }

    });

    var toggleServer = function (state,hostId){

        if(state == editStates.ShowLoading)
        {
            $("#editServer_"+hostId).hide()
            $("#deleteServer_"+hostId).hide()
            $("#editServerTxt_"+hostId).hide()
            $("#deleteServerTxt_"+hostId).hide()
            $("#loadingServer_"+hostId).show()

        }
        else if (state == editStates.ShowOkCancel) {
            $("#editServer_"+hostId).show()
            $("#deleteServer_"+hostId).show()
            $("#editServerTxt_"+hostId).show()
            $("#deleteServerTxt_"+hostId).show()
            $("#loadingServer_"+hostId).hide()
        }
        else{
            $("#editServer_"+hostId).show()
            $("#deleteServer_"+hostId).show()
            $("#editServerTxt_"+hostId).show()
            $("#deleteServerTxt_"+hostId).show()
            $("#loadingServer_"+hostId).hide()
        }
    }

    $('#deleteServerOk').on('click',function(){
        var serverId = $('#deleteConfirmation').data('serverid');
        var serverData = {
           "id": serverId
        }
        toggleServer(editStates.ShowLoading,serverId)

        VdmService.DeleteServer(function(connection){
            VdmService.GetServerList(function(connection){
                VdmUI.displayServers(connection.Metadata['SERVER_LISTING'])
            })
        }, serverData);
    })

    $('#btnAddDatabase').on('click', function(){
        VdmUI.resetDbForm();
        VdmUI.isDbCreate = true;
        VdmUI.dbToUpdate = '';
        $('#dbTitle').html('Add Database');
    });

    $('#btnDeleteDatabaseOk').on('click', function(){
        var dbId = $('#deleteDatabase').data('id');
        var dbData = {
            id: dbId
        }
        VdmService.DeleteDatabase(function(connection){
            VdmService.GetDatabaseList(function(connection){
                VdmUI.displayDatabases(connection.Metadata['DATABASE_LISTING'])
            })
        }, dbData);
    });
};

(function (window) {
    var iVdmUi = (function () {
        this.CurrentTab = NavigationTabs.DBMonitor;
        this.CurrentServerList = [];
        this.CurrentHostList = [];
        this.CurrentDbList = [];
        this.isServerCreate = true;
        this.isDbCreate = true;
        this.serverToUpdate = '';
        this.hostToUpdate = '';
        this.dbToUpdate = '';
        this.members = [];
        this.getCookie = function(name) {
            return $.cookie(name + "_" + VdmConfig.GetPortId());
        };

        this.displayServers = function(serverList){
            if (serverList == undefined) {
                return;
            }
            var dbId = VdmUI.getCurrentDbCookie();
            VdmUI.members = []
            var dbData = {
                id: dbId
            }

            VdmService.GetMemberList(function(connection){
                VdmUI.members = connection['Metadata']['MEMBER_LISTING'].members;

                var htmlList = "";
                VdmUI.CurrentServerList = [];
                VdmUI.CurrentHostList = [];
                serverList.servers.forEach(function (info) {
                    var hostName = info["hostname"];
                    var serverName = info["name"]
                    var hostId = info["id"];
                    var infos = JSON.stringify(info)
                    if($.inArray(hostId, VdmUI.members) != -1){
                        htmlList += '<tr>' +
                                    '<td>' + hostName + '</td>' +
                                    '<td data-id="' + hostId + '" data-info=\''+ infos +'\'><a class="btnUpdateServer" href="javascript:void(0);"data-toggle="modal" data-target="#addServer" >' +
                                    '<div class="editServer" id="editServer_'+hostId+'"></div></a>' +
                                    '<div class="loading-small" id="loadingServer_'+hostId+'" style="display:none"></div>' +
                                    '<span class="editServerTxt" id="editServerTxt_'+hostId+'">Edit</span></td>' +
                                    '<td data-id="' + hostId + '" ><a class="btnDeleteServer" href="javascript:void(0);"data-toggle="modal" data-target="#deleteConfirmation" >' +
                                    '<div class="deleteServer" id="deleteServer_'+hostId+'"></div></a>' +
                                    '<span class="deleteServerTxt" id="deleteServerTxt_'+hostId+'">Delete</span></td>' +
                                '</tr>';
                    }
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
                    VdmUI.resetTextBox();
                    VdmUI.isServerCreate = false;
                    var serverInfo = $(this.parentElement).data('info');
                    VdmUI.serverToUpdate = serverInfo['name'];
                    VdmUI.hostToUpdate = serverInfo['hostname'];
                    $('#addServer').data('serverid',serverInfo['id']);
                    $('#serverName').val(serverInfo['name']);
                    $('#txtHostName').val(serverInfo['hostname']);
                    $('#txtDescription').val(serverInfo['description']);
                    $('#txtClientPort').val(serverInfo['client-listener']);
                    $('#txtAdminPort').val(serverInfo['admin-listener']);
                    $('#txtInternalPort').val(serverInfo['internal-listener']);
                    $('#txtHttpPort').val(serverInfo['http-listener']);
                    $('#txtZookeeper').val(serverInfo['zookeeper-listener']);
                    $('#txtReplicationPort').val(serverInfo['replication-listener']);
                    $('#txtInternalInterface').val(serverInfo['internal-interface'])
                    $('#txtExternalInterface').val(serverInfo['external-interface'])
                    $('#txtPublicInterface').val(serverInfo['public-interface']);
                    $('#txtPlacementGroup').val(serverInfo['placement-group']);
                    $('#addServerTitle').html('Update Server');
                });

                $('#btnAddServer').on('click', function(){
                    VdmUI.isServerCreate = true;
                    VdmUI.serverToUpdate = '';
                    VdmUI.hostToUpdate = '';
                    $('#addServerTitle').html('Add Server');
                    VdmUI.resetTextBox();
                });
            }, dbData);
        };

        this.resetTextBox = function(){
                $('#serverName').val('');
                $('#txtHostName').val('');
                $('#txtDescription').val('');
                $('#txtClientPort').val('');
                $('#errorClientPort').hide();
                $('#txtAdminPort').val('');
                $('#errorAdminPort').hide();
                $('#txtZookeeper').val('');
                $('#errorZookeeper').hide();
                $('#txtReplicationPort').val('');
                $('#errorReplicationPort').hide();
                $('#txtInternalInterface').val('');
                $('#txtExternalInterface').val('');
                $('#txtPublicInterface').val('');
                $('#txtInternalPort').val('');
                $('#txtHttpPort').val('');
                $('#txtPlacementGroup').val('');
                $('#errorServerName').hide();
                $('#errorHostName').hide();
                $('#errorDescription').hide();
                $('#errorInternalInterface').hide();
                $('#errorExternalInterface').hide();
                $('#errorPublicInterface').hide();
                $('#errorInternalPort').hide();
                $('#errorHttpPort').hide();
            }

        this.resetDbForm = function() {
                $('#txtDbName').val('');
                $('#txtDeployment').val('');
                $('#errorDbName').hide();
            };

        this.displayDatabases = function(databaseList){
            if(databaseList == undefined)
                return;
            var htmlList = '';
            var count = 0;
            VdmUI.CurrentDbList = [];
            var currentDbId = VdmUI.getCurrentDbCookie();
            databaseList.databases.forEach(function (info) {
                var dbName = info['name'];
                var dbId = info['id']
                var dbInfo = JSON.stringify(info);
                if(dbId == currentDbId){
                    htmlList += '<tr>' +
                                '<td data-id="' + dbId + '"><a class="btnDbList selected" href="javascript:void(0)">'+ dbName +'</a></td>' +
                                '<td data-id="' + dbId + '" data-info=\''+ dbInfo +'\' width="2%"><a class="btnUpdateDatabase" href="javascript:void(0);"data-toggle="modal" data-target="#addDatabase" >' +
                                '<div class="editServerDatabase"></div>' +
                                '</a> <span class="editServerDatabaseTxt">Edit</span></td>' +
                                '<td data-id="' + dbId + '" width="2%"><a class="btnDeleteDatabase" href="javascript:void(0);"data-toggle="modal" data-target="#deleteDatabase" >' +
                                '<div class="deleteDisableDS"></div>' +
                                '</a> <span class="deleteDisableDSTxt">Delete</span></td>' +
                                '</tr>';
                } else {
                    htmlList += '<tr>' +
                                '<td data-id="' + dbId + '"><a class="btnDbList" href="javascript:void(0)">'+ dbName +'</a></td>' +
                                '<td data-id="' + dbId + '" data-info=\''+ dbInfo +'\' width="2%"><a class="btnUpdateDatabase" href="javascript:void(0);"data-toggle="modal" data-target="#addDatabase" >' +
                                '<div class="editServerDatabase"></div>' +
                                '</a> <span class="editServerDatabaseTxt">Edit</span></td>' +
                                '<td data-id="' + dbId + '" width="2%"><a class="btnDeleteDatabase" href="javascript:void(0);"data-toggle="modal" data-target="#deleteDatabase" >' +
                                '<div class="deleteDatabaseServer"></div>' +
                                '</a> <span class="deleteServerDatabaseTxt">Delete</span></td>' +
                                '</tr>';
                }
                VdmUI.CurrentDbList.push(dbName);
            });

            if(htmlList == ""){
                $('#tblDatabaseList').html('<tr><td style="top:-1px !important">No servers Available.</td><td></td></tr>')
            }else{
                $('#tblDatabaseList').html(htmlList)
            }

            $('.btnUpdateDatabase').on('click', function(){
                VdmUI.resetDbForm();
                VdmUI.isDbCreate = false;
                var dbInfo = $(this.parentElement).data('info');
                VdmUI.dbToUpdate = dbInfo['name'];
                $('#addDatabase').data('id',dbInfo['id']);
                $('#txtDbName').val(dbInfo['name']);
                $('#txtDeployment').val(dbInfo['deployment']);
                $('#dbTitle').html('Update Database');
            });

            $('.btnDeleteDatabase').on('click', function(){
                var dbId = $(this.parentElement).data('id');
                $('#deleteDatabase').data('id', dbId);
            })

            $('.btnDbList').on('click', function(){
                //$('.preload').show();
                var dbId = $(this.parentElement).data('id');
                VdmUI.saveCurrentDbCookie(dbId);
                $(this).addClass('selected');
                VdmService.GetDatabaseList(function(connection){
                    VdmUI.displayDatabases(connection.Metadata['DATABASE_LISTING'])
                    //$('.preload').fadeOut(4000);
                })
            })

        };

        this.saveCurrentDbCookie = function(dbId){
             saveCookie("current-db", dbId);
        };

        this.getCurrentDbCookie = function(){
            var dbId = -1;
            var count = 0;
            try {
                dbId = $.parseJSON(VdmUI.getCookie("current-db"));
            } catch (e) {
                VdmService.GetDatabaseList(function(connection){
                    var obj =connection.Metadata['DATABASE_LISTING'].databases[0];
                    dbId = obj.id;
                    VdmUI.saveCurrentDbCookie(dbId);
                })
            }
            return dbId;
        };

        this.getNonMemberServerList = function(){

        };
    });
    window.VdmUI = VdmUI = new iVdmUi();

})(window);



