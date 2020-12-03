from seleniumwire.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

opts = Options()
opts.set_preference("browser.download.dir", os.getcwd())
opts.set_preference("browser.download.folderList", 2)
opts.set_preference(
    "browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")


driver = Firefox(options=opts)
driver.get("https://euroleague.tv/video/164898")

for request in driver.requests:
    if request.response:
        print(
            request.url,
        )
