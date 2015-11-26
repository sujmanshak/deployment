import geb.Page

class ClusterSettingsPage extends Page {
    static content = {
        // Tabs
        clusterSettingsTab              { $("#dbManager") }
        serverSettingsTab               { $("#serverSetting") }
        // DB
        startCluster                    { $("#divDbManager > div.clusterContent > div.clusterStartStop > div > a") }

        // Servers
        buttonAddServer                 { $("#btnAddServer") }

        // Add Server Popup
        popupAddServer                          { $("#addServer > div > div") }
        popupAddServerNameField                 { $("#serverName") }
        popupAddServerHostNameField             { $("#txtHostName") }
        popupAddServerDescriptionField          { $("#txtDescription") }
        popupAddServerClientListenerField       { $("#txtClientPort") }
        popupAddServerAdminListenerField        { $("#txtAdminPort") }
        popupAddServerHttpListenerField         { $("#txtHttpPort") }
        popupAddServerInternalListenerField     { $("#txtInternalPort") }
        popupAddServerZookeeperListenerField    { $("#txtZookeeper") }
        popupAddServerReplicationListenerField { $("#txtReplicationPort") }
        popupAddServerInternalInterfaceField    { $("#txtInternalInterface") }
        popupAddServerExternalInterfaceField    { $("#txtExternalInterface") }
        popupAddServerPublicInterfaceField      { $("#txtPublicInterface") }
        popupAddServerPlacementGroupField       { $("#txtPlacementGroup") }

        popupAddServerButtonOk          { $("#btnCreateServerOk") }
        popupAddServerButtonCancel      { $("#addServer > div > div > div.modal-footer > button.btn.btn-gray") }
        
        // Delete Server
        deleteServer                    { $("#serverList > tbody > tr:nth-child(5) > td:nth-child(2) > a > div") }
        popupDeleteServer               { $("#deleteConfirmation > div > div") }
        popupDeleteServerButtonOk       { $("#deleteServerOk") }

        testingPath    (required:false) { $("#serverList > tbody > tr:nth-child(5) > td:nth-child(1)") }

        errorServerName {$("#errorServerName")}

        errorHostName {$("#errorHostName")}

        errorClientPort {$("#errorClientPort")}

        errorInternalInterface {$("#errorInternalInterface")}

        // Database
        buttonAddDatabase                   { $("#btnAddDatabase") }

        popupAddDatabase                    { $("#txtDbName") }
        popupAddDatabaseNameField           { $("#txtDbName") }
        popupAddDatabaseDeploymentField     { $("#txtDeployment") }
        popupAddDatabaseButtonOk            (required:false) { $("#btnAddDatabaseOk") }
        popupAddDatabaseButtonCancel        { $("#addDatabase > div > div > div.modal-footer > button.btn.btn-gray") }

        popupDeleteDatabaseButtonOk         { $("#btnDeleteDatabaseOk") }
    }

    static at = {
//        waitFor(30) { clusterSettingsTab.isDisplayed() }
  //      waitFor(30) { serverSettingsTab.isDisplayed() }
    }

    /*
     *  Return the id of delete button with index as input
     */
    String getIdOfDeleteButton(int index) {
        return ("deleteServer_" + String.valueOf(index))
    }

    /*
     *  Return the id of edit button with index as input
     */
    String getIdOfEditButton(int index) {
        return ("editServer_" + String.valueOf(index))
    }

    String getIdOfDatabaseDeleteButton(int index) {
        return ("deleteDatabase_" + String.valueOf(index))
    }

    String getIdOfDatabaseEditButton(int index) {
        return ("editDatabase_" + String.valueOf(index))
    }
}
