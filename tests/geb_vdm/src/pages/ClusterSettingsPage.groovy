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
        popupAddServer                  { $("#addServer > div > div") }
        popupAddServerNameField         { $("#serverName") }
        popupAddServerHostNameField     { $("#txtHostName") }
        popupAddServerDescriptionField  { $("#txtDescription") }
        popupAddServerButtonOk          { $("#btnCreateServerOk") }
        popupAddServerButtonCancel      { $("#addServer > div > div > div.modal-footer > button.btn.btn-gray") }
        
        // Delete Server
        deleteServer                    { $("#serverList > tbody > tr:nth-child(5) > td:nth-child(2) > a > div") }
        popupDeleteServer               { $("#deleteConfirmation > div > div") }
        popupDeleteServerButtonOk       { $("#deleteServerOk") }

        testingPath    (required:false) { $("#serverList > tbody > tr:nth-child(5) > td:nth-child(1)") }
    }

    static at = {
        waitFor(30) { clusterSettingsTab.isDisplayed() }
        waitFor(30) { serverSettingsTab.isDisplayed() }
    }
}
