import geb.spock.GebReportingSpec
import java.text.SimpleDateFormat
import java.util.Date
import java.util.List
import java.util.concurrent.Callable
import java.util.concurrent.Executors
import java.util.concurrent.ExecutorService
import java.util.concurrent.Future
import java.util.concurrent.FutureTask
import java.util.concurrent.TimeUnit
import geb.Page
import geb.spock.GebReportingSpec

import org.junit.Rule
import org.junit.rules.TestName
import org.openqa.selenium.Dimension

class TestBase extends GebReportingSpec {
    static int numberOfTrials = 20
    static int waitTime = 20

    static final boolean DEFAULT_DEBUG_PRINT = false
    static final int DEFAULT_WINDOW_WIDTH  = 1500
    static final int DEFAULT_WINDOW_HEIGHT = 1000
    static final int MAX_SECS_WAIT_FOR_PAGE = 60
    static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS")

    def setupSpec() { // called once (per test class), before any tests
        def winSize = driver.manage().window().size
        driver.manage().window().setSize(new Dimension(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT))
    }
}