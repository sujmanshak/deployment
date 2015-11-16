/*
This file is part of VoltDB.

Copyright (C) 2008-2015 VoltDB Inc.

This file contains original code and/or modifications of original code.
Any modifications made by VoltDB Inc. are licensed under the following
terms and conditions:

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
*/

import geb.spock.GebReportingSpec
import org.openqa.selenium.WebElement
import geb.navigator.Navigator

class ClusterSettingsTest extends TestBase {
    def setup() { // called before each test
        count = 0

        while(count<numberOfTrials) {
            count ++
            try {
                setup: 'Open Cluster Settings page'
                to ClusterSettingsPage
                expect: 'to be on Cluster Settings page'
                at ClusterSettingsPage

                break
            } catch (org.openqa.selenium.ElementNotVisibleException e) {
                println("ElementNotVisibleException: Unable to Start the test")
                println("Retrying")
            }
        }
    }

    def "Verify the server create and delete"() {
        println("Test Start: Verify the server create and delete")
        boolean status = false
        int newValue = 1
        when:
        for(count=1; count<numberOfTrials; count++) {
            try {
                waitFor { $(id:page.getIdofDeleteButton(count)).isDisplayed() }
            } catch(geb.waiting.WaitTimeoutException e) {
                break
            }
        }
        newValue = count+1
        then:
        println("The count is " + newValue)
        
        when:
        try {
            waitFor { page.buttonAddServer.click() }
            waitFor { page.popupAddServer.isDisplayed() }
        } catch(geb.waiting.WaitTimeoutException e) {
            println("Unable to find Add Server button or popup - Retrying")
        } 
        and:   
        for(count=0; count<numberOfTrials; count++) {
            try {
               
                waitFor { popupAddServerNameField.value("new_server") }
                waitFor { popupAddServerHostNameField.value("new_host") }
                waitFor { popupAddServerDescriptionField.value("") }
                waitFor { popupAddServerClientListenerField.value("192.168.0.1:8000") }
                waitFor { popupAddServerAdminListenerField.value("192.168.0.2:8000") }
                waitFor { popupAddServerHttpListenerField.value("192.168.0.3:8000") }
                waitFor { popupAddServerInternalListenerField.value("192.168.0.4:8000") }
                waitFor { popupAddServerZookeeperListenerField.value("192.168.0.5:8000") }
                waitFor { popupAddServerReplicationListenerField.value("192.168.0.6:8000") }
                waitFor { popupAddServerInternalInterfaceField.value("192.168.0.7") }
                waitFor { popupAddServerExternalInterfaceField.value("192.168.0.8") }
                waitFor { popupAddServerPublicInterfaceField.value("192.168.0.9") }
                waitFor { popupAddServerPlacementGroupField.value("placement_value")}
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to provide value to the text fields - Retrying")
            }
        }
        count = 0
        then:
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupAddServerButtonOk.click()
                waitFor { !popupAddServerButtonOk.isDisplayed() }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to Close Popup - Retrying")   
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
                try {
                    waitFor { !popupAddServerButtonOk.isDisplayed() }
                } catch(geb.waiting.WaitTimeoutException f) {
                    println("Popup Closed")
                    break
                }
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element Exception - Retrying")
            }
        }
        
        when:
        String str = getIdOfDeleteButton(newValue)
        for(count=0; count<numberOfTrials; count++) {
            try {
                waitFor { $(id:str).isDisplayed() }
                status = true
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to find created server - Retrying")
            }
        }
        then:
        if(status == true) { 
            println("The new server was created")
        }
        else {
            println("Test False: The new server wasn't created")
            assert false
        }
        
        when:
        for(count=0; count<numberOfTrials; count++) {
            try {
                $(id:str).click()
                waitFor { popupDeleteServerButtonOk.isDisplayed() }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to find the delete popup - Retrying")
            } catch(geb.error.RequiredPageContentNotPresent e) {
                println("Unable to find the delete button - Retrying")
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element Exception - Retrying")
            }
        }
        then:
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupDeleteServerButtonOk.click()
                waitFor { !$(id.str).isDisplayed() }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Test Pass: The new server was created and deleted")
                break
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
                println("Test Pass: The new server was created and deleted")
                break
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element Exception - Retrying")
            }
        }
    }

    def "Verify the server create, edit and delete"() {
        println("Test Start: Verify the server create, edit and delete")
        boolean status = false
        int newValue = 1
        when:
        for(count=1; count<numberOfTrials; count++) {
            try {
                waitFor { $(id:page.getIdofDeleteButton(count)).isDisplayed() }
            } catch(geb.waiting.WaitTimeoutException e) {
                break
            }
        }
        newValue = count+1
        then:
        println("The count is " + newValue)
        
        when:
        try {
            waitFor { page.buttonAddServer.click() }
            waitFor { page.popupAddServer.isDisplayed() }
        } catch(geb.waiting.WaitTimeoutException e) {
            println("Unable to find Add Server button or popup - Retrying")
        } 
        and:   
        for(count=0; count<numberOfTrials; count++) {
            try {
                waitFor { popupAddServerNameField.value("new_server") }
                waitFor { popupAddServerHostNameField.value("new_host") }
                waitFor { popupAddServerDescriptionField.value("") }
                waitFor { popupAddServerClientListenerField.value("192.168.0.1:8000") }
                waitFor { popupAddServerAdminListenerField.value("192.168.0.2:8000") }
                waitFor { popupAddServerHttpListenerField.value("192.168.0.3:8000") }
                waitFor { popupAddServerInternalListenerField.value("192.168.0.4:8000") }
                waitFor { popupAddServerZookeeperListenerField.value("192.168.0.5:8000") }
                waitFor { popupAddServerReplicationListenerField.value("192.168.0.6:8000") }
                waitFor { popupAddServerInternalInterfaceField.value("192.168.0.7") }
                waitFor { popupAddServerExternalInterfaceField.value("192.168.0.8") }
                waitFor { popupAddServerPublicInterfaceField.value("192.168.0.9") }
                waitFor { popupAddServerPlacementGroupField.value("") }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to provide value to the text fields - Retrying")
            }
        }
        count = 0
        then:
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupAddServerButtonOk.click()
                waitFor { !popupAddServerButtonOk.isDisplayed() }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to Close Popup - Retrying")   
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
                try {
                    waitFor { !popupAddServerButtonOk.isDisplayed() }
                } catch(geb.waiting.WaitTimeoutException f) {
                    println("Popup Closed")
                    break
                }
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element Exception - Retrying")
            }
        }
        
        when:
        String str = getIdOfDeleteButton(newValue)
        for(count=0; count<numberOfTrials; count++) {
            try {
                waitFor { $(id:str).isDisplayed() }
                status = true
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to find created server - Retrying")
            }
        }
        then:
        if(status == true) { 
            println("The new server was created")
        }
        else {
            println("Test False: The new server wasn't created")
            assert false
        }
        
        when:
        status = false
        String str_edit = getIdOfEditButton(newValue)
        for(count=0; count<numberOfTrials; count++) {
            try {
                $(id:str_edit).click()
                waitFor { popupAddServerButtonOk.isDisplayed() }
                status = true
                break
            } catch(geb.error.RequiredPageContentNotPresent e) {
                println("Unable to find the edit button - Retrying")
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element Exception - Retrying")
            }

        }
        if(status==true) {
            println("Edit button found")
        }
        else {
            println("Edit button not found")
            assert false
        }
        and:
        for(count=0; count<numberOfTrials; count++) {
            try {
                waitFor { popupAddServerNameField.value("new_edited_server") }
                waitFor { popupAddServerHostNameField.value("new_edited_host") }
                waitFor { popupAddServerDescriptionField.value("") }
                waitFor { popupAddServerClientListenerField.value("192.168.0.10:8000") }
                waitFor { popupAddServerAdminListenerField.value("192.168.0.20:8000") }
                waitFor { popupAddServerHttpListenerField.value("192.168.0.30:8000") }
                waitFor { popupAddServerInternalListenerField.value("192.168.0.40:8000") }
                waitFor { popupAddServerZookeeperListenerField.value("192.168.0.50:8000") }
                waitFor { popupAddServerReplicationListenerField.value("192.168.0.60:8000") }
                waitFor { popupAddServerInternalInterfaceField.value("192.168.0.70") }
                waitFor { popupAddServerExternalInterfaceField.value("192.168.0.80") }
                waitFor { popupAddServerPublicInterfaceField.value("192.168.0.90") }
//                waitFor { popupAddServerPlacementGroupField.value("new_value_for_placement)") }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to provide value to text fields - Retrying")
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element Exception - Retrying")
            }
        }
        count = 0
        then:
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupAddServerButtonOk.click()
                waitFor { !popupAddServerButtonOk.isDisplayed() }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to Close Popup - Retrying")   
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
                try {
                    waitFor { !popupAddServerButtonOk.isDisplayed() }
                } catch(geb.waiting.WaitTimeoutException f) {
                    println("Popup Closed")
                    break
                }
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element Exception - Retrying")
            }
        }
        
        when:
        for(count=0; count<numberOfTrials; count++) {
            try {
                $(id:str).click()
                waitFor { popupDeleteServerButtonOk.isDisplayed() }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to find the delete popup - Retrying")
            } catch(geb.error.RequiredPageContentNotPresent e) {
                println("Unable to find the delete button - Retrying")
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element Exception - Retrying")
            }
        }
        then:
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupDeleteServerButtonOk.click()
                waitFor { !$(id.str).isDisplayed() }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Test Pass: The new server was created, edited and deleted")
                break
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
                println("Test Pass: The new server was created, edited and deleted")
                break
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element Exception - Retrying")
            }
        }
    }

    def "Ensure Server name and Host name is not empty"(){
        when:"Click Add Server button"
        try {
            page.buttonAddServer.click()
//            waitFor { page.popupAddServer.isDisplayed() }
        } catch(geb.waiting.WaitTimeoutException e) {
            println("Unable to find Add Server button or popup - Retrying")
        }

        then: "Check popup is displayed"
        waitFor{page.popupAddServer.isDisplayed()}
        when: "click the Ok button"
        popupAddServerButtonOk.click()

        then: "Check validation for server name and host name exists"
        errorServerName.isDisplayed()
        errorHostName.isDisplayed()
    }

    def "Ensure Duplicate Server name validation"(){
        boolean status = false
        int newValue = 1
        when:
        for(count=1; count<numberOfTrials; count++) {
            try {
                waitFor { $(id:page.getIdofDeleteButton(count)).isDisplayed() }
            } catch(geb.waiting.WaitTimeoutException e) {
                break
            }
        }
        newValue = count+1
        then:
        println("The count is " + newValue)

        when:
        try {
            waitFor { page.buttonAddServer.click() }
            waitFor { page.popupAddServer.isDisplayed() }
        } catch(geb.waiting.WaitTimeoutException e) {
            println("Unable to find Add Server button or popup - Retrying")
        }
        and:
        for(count=0; count<numberOfTrials; count++) {
            try {
                waitFor { popupAddServerNameField.value("new_server") }
                waitFor { popupAddServerHostNameField.value("new_host") }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to provide value to the text fields - Retrying")
            }
        }
        count = 0
        then:
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupAddServerButtonOk.click()
                waitFor { !popupAddServerButtonOk.isDisplayed() }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to Close Popup - Retrying")
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
                try {
                    waitFor { !popupAddServerButtonOk.isDisplayed() }
                } catch(geb.waiting.WaitTimeoutException f) {
                    println("Popup Closed")
                    break
                }
            }
        }

        when:"Click Add Server button"
            waitFor { page.buttonAddServer.click() }
        then:
            waitFor { page.popupAddServer.isDisplayed() }

        when: "click the Ok button"
        popupAddServerButtonOk.click()
        then: "Check validation for server name and host name exists"
        errorServerName.isDisplayed()
        errorHostName.isDisplayed()
        println(errorHostName.text())
        println(errorServerName.text())
//        errorServerName.text().equals("This server name already exists.")
//        errorHostName.text().equals("This host name already exists.")
    }

    def "Ensure client listener is valid"(){
        boolean status = false
        int newValue = 1
        when:
        for(count=1; count<numberOfTrials; count++) {
            try {
                waitFor { $(id:page.getIdofDeleteButton(count)).isDisplayed() }
            } catch(geb.waiting.WaitTimeoutException e) {
                break
            }
        }
        newValue = count+1
        then:
        println("The count is " + newValue)

        when:
        try {
            waitFor { page.buttonAddServer.click() }
            waitFor { page.popupAddServer.isDisplayed() }
        } catch(geb.waiting.WaitTimeoutException e) {
            println("Unable to find Add Server button or popup - Retrying")
        }
        and:
        for(count=0; count<numberOfTrials; count++) {
            try {
                waitFor { popupAddServerNameField.value("new_server") }
                waitFor { popupAddServerHostNameField.value("new_host") }
                waitFor { popupAddServerDescriptionField.value("") }
                waitFor { popupAddServerClientPortField.value("192.168.0.1") }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to provide value to the text fields - Retrying")
            }
        }

        count = 0
        then:
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupAddServerButtonOk.click()
                waitFor { !popupAddServerButtonOk.isDisplayed() }
                errorClientPort.isDisplayed()
                errorClientPort.text().equals("Please enter a valid value.(e.g, 127.0.0.1:8000 or 8000(1-65535))")
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to Close Popup - Retrying")
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
                try {
                    waitFor { !popupAddServerButtonOk.isDisplayed() }
                } catch(geb.waiting.WaitTimeoutException f) {
                    println("Popup Closed")
                    break
                }
            }
        }
    }

    def "Ensure internal interface is valid"(){
        boolean status = false
        int newValue = 1
        when:
        to ClusterSettingsPage
        and:
        at ClusterSettingsPage
        for(count=1; count<numberOfTrials; count++) {
            try {
                waitFor { $(id:page.getIdofDeleteButton(count)).isDisplayed() }
            } catch(geb.waiting.WaitTimeoutException e) {
                break
            }
        }
        newValue = count+1
        then:
        println("The count is " + newValue)

        when:
        try {
            waitFor { page.buttonAddServer.click() }
            waitFor { page.popupAddServer.isDisplayed() }
        } catch(geb.waiting.WaitTimeoutException e) {
            println("Unable to find Add Server button or popup - Retrying")
        }
        and:
        for(count=0; count<numberOfTrials; count++) {
            try {
                waitFor { popupAddServerNameField.value("new_server") }
                waitFor { popupAddServerHostNameField.value("new_host") }
                waitFor { popupAddServerDescriptionField.value("") }
                waitFor { popupAddServerInternalInterfaceField.value("sfdsaf12321") }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to provide value to the text fields - Retrying")
            }
        }

        count = 0
        then:
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupAddServerButtonOk.click()
                waitFor { !popupAddServerButtonOk.isDisplayed() }
                errorInternalInterface.isDisplayed()
                errorInternalInterface.text().equals("Please enter a valid IP address.")
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to Close Popup - Retrying")
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
                try {
                    waitFor { !popupAddServerButtonOk.isDisplayed() }
                } catch(geb.waiting.WaitTimeoutException f) {
                    println("Popup Closed")
                    break
                }
            }
        }

    }
}
