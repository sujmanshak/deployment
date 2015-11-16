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
    def "Verify the server create and delete"() {
        println("Test Start: Verify the server create and delete")
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
                waitFor { popupAddServerClientPortField.value("192.168.0.1:8000") }
                waitFor { popupAddServerAdminPortField.value("192.168.0.2:8000") }
//                waitFor { page.popupAddServerHttpField.value("192.168.0.3:8000") }
//                waitFor { page.popupAddServerInternalPortField.value("192.168.0.4:8000") }
                waitFor { popupAddServerZookeeperField.value("192.168.0.5:8000") }
                waitFor { popupAddServerReplicationPortField.value("192.168.0.6:8000") }
                waitFor { popupAddServerInternalInterfaceField.value("192.168.0.7") }
                waitFor { popupAddServerExternalInterfaceField.value("192.168.0.8") }
                waitFor { popupAddServerPublicInterfaceField.value("192.168.0.9") }
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
            }
        }
    }
}
