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
}