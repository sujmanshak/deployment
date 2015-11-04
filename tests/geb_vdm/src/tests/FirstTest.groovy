import geb.spock.GebReportingSpec

class FirstTest extends TestBase {

    def "The first test"() {
        when:
        to ClusterSettingsPage
        then:
        page.clusterSettingsTab.isDisplayed()
        page.serverSettingsTab.isDisplayed()
    }

    def "Verify "() {
        int count = 0
        when:
        to ClusterSettingsPage
        and:
        at ClusterSettingsPage
        then:
        page.buttonAddServer.click()

        when:
        page.popupAddServer.isDisplayed()
        and:
        for(count=0; count<numberOfTrials; count++) {
            try {
                page.popupAddServerNameField.isDisplayed()
                page.popupAddServerNameField.value("new_name")
                page.popupAddServerButtonOk.isDisplayed()
                page.popupAddServerButtonCancel.isDisplayed()
                break
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
            }
        }
        then:
        page.popupAddServerButtonOk.click()

        when:
        page.deleteServer.isDisplayed()
        and:
        for(count=0;count<numberOfTrials;count++) {
            try {
                page.deleteServer.click()
                waitFor(waitTime) { page.popupDeleteServer.isDisplayed() }
                break
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
            }
        }
        then:
        for(count=0;count<numberOfTrials;count++) {
            try {
                page.popupDeleteServerButtonOk.click()
                waitFor(waitTime) { !page.testingPath.isDisplayed() }
                break
            } catch(org.openqa.selenium.StaleElementReferenceException e) {
            } catch(org.openqa.selenium.ElementNotVisibleException e) {
            }
        }
    }
}