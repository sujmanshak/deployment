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

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

class DatabaseTest extends TestBase {

    String create_DatabaseTest_File = "/home/anrai/deploymentVoltdb/deployment/tests/geb_vdm/src/resources/create_DatabaseTest.csv"
    String cvsSplitBy = ","

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

    def addDatabase() {
        BufferedReader br = null
        String line = ""
        String[] extractedValue = ["two", "one"]
        int newValue

        expect: 'Expect the add database button'
        waitFor { buttonAddDatabase.isDisplayed() }

        when:
        for(count=1; count<numberOfTrials; count++) {
            try {
                waitFor { $(id:page.getIdOfDatabaseDeleteButton(count)).isDisplayed() }
            } catch(geb.waiting.WaitTimeoutException e) {
                break
            }
        }
        newValue = count
        then:
        println("The count is " + newValue)

        when: 'Click add database button to open popup'
        for(count=0; count<numberOfTrials; count++) {
            try {
                buttonAddDatabase.click()
                waitFor { popupAddDatabase.isDisplayed() }
                break
            } catch(geb.waiting.WaitTimeoutException e) {
                println("Unable to find the popup - Retrying")
            } catch(geb.error.RequiredPageContentNotPresent e) {
                println("Unable to find the add button - Retrying")
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element - Retrying")
            }
        }
        then: ''
        println()

        when: 'Extract Values from create_DatabaseTest.csv'
        try {
            br = new BufferedReader(new FileReader(create_DatabaseTest_File));
            for (count=0; (line = br.readLine()) != null; count++) {
                String[] extractedValues = line.split(cvsSplitBy)
                extractedValue[count] = extractedValues[1]
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        extractedValue[0] = extractedValue[0].substring(1, extractedValue[0].length() - 1);
        extractedValue[1] = extractedValue[1].substring(1, extractedValue[1].length() - 1);
        then: 'Provide value to the textfields'
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupAddDatabaseNameField.value(extractedValue[0])
                popupAddDatabaseDeploymentField.value(extractedValue[1])
                break
            } catch (geb.error.RequiredPageContentNotPresent e) {
                println("Unable to find the text fields - Retrying")
            } catch (org.openqa.selenium.StaleElementReferenceException e) {
                println("Stale Element - Retrying")
            }
        }

        when: ''
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupAddDatabaseButtonOk.click()
                waitFor { $(id:getIdOfDatabaseDeleteButton(newValue)).isDisplayed() }
                break
            } catch (geb.error.RequiredPageContentNotPresent e) {
                println("Unable to find the Ok button - Retrying")
            } catch (geb.waiting.WaitTimeoutException e) {
                println("Unable to find the created database - Retrying")
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
                try {
                    waitFor { $(id:getIdOfDatabaseDeleteButton(newValue)).isDisplayed() }
                    break
                } catch (geb.waiting.WaitTimeoutException exp) {
                    println("Unable to find the created database - Retrying")
                }
            }
        }
        then:
        println()
    }

    def deleteDatabase() {
        int newValue

        expect: 'Expect the add database button'
        waitFor { buttonAddDatabase.isDisplayed() }

        when:
        for(count=1; count<numberOfTrials; count++) {
            try {
                waitFor { $(id:page.getIdOfDatabaseDeleteButton(count)).isDisplayed() }
            } catch(geb.waiting.WaitTimeoutException e) {
                break
            }
        }
        newValue = count - 1
        then:
        println("The count is " + newValue)

        when:
        for(count=0; count<numberOfTrials; count++) {
            try {
                $(id: getIdOfDatabaseDeleteButton(newValue)).click()
                waitFor { popupDeleteDatabaseButtonOk.isDisplayed() }
                break
            } catch (geb.error.RequiredPageContentNotPresent e) {
                println("Unable to find the Delete button - Retrying")
            } catch (geb.waiting.WaitTimeoutException e) {
                println("Unable to find the Ok button - Retrying")
            }
        }
        then:
        for(count=0; count<numberOfTrials; count++) {
            try {
                popupDeleteDatabaseButtonOk.click()
                waitFor { !$(id: getIdOfDatabaseDeleteButton(newValue)).isDisplayed() }
                break
            } catch (geb.error.RequiredPageContentNotPresent e) {
                println("Unable to find the Delete button - Retrying")
            } catch (geb.waiting.WaitTimeoutException e) {
                println("Unable to find the Ok button - Retrying")
            }
        }
    }
}
