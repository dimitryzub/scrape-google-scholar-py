# # This script is a starting point.

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.expected_conditions import presence_of_element_located
# from selenium.webdriver.common.by import By

# options = Options()
# options.page_load_strategy = 'normal'
# driver = webdriver.Chrome(options = options)
# wait = WebDriverWait(driver, 10)

# # Proxy is needed https://www.selenium.dev/documentation/en/webdriver/http_proxies
# # https://stackoverflow.com/a/40628176/15164646
# def selenium_scrape_cite_results():
#   query = "samsung"

#   driver.get(f'https://scholar.google.com.ua/scholar?hl=en&as_sdt=0%2C5&as_vis=1&q={query}')
#   cite = wait.until(presence_of_element_located(By.XPATH, '//*[@id="gs_res_ccl_mid"]/div[1]/div[2]/div[3]/a[2]')).click

#   container = driver.find_element_by_css_selector('#gs_citt').text
#   print(container)

# # Proxy method. Still throws a CAPTCHA
# PROXY = "HOST:PORT"
# webdriver.DesiredCapabilities.CHROME['proxy'] = {
#     "httpProxy": PROXY,
#     "proxyType": "MANUAL",
# }

# with webdriver.Chrome() as driver:
#     wait = WebDriverWait(driver, 10)

#     query = "samsung"
#     driver.get('https://scholar.google.com.ua/scholar?hl=en&as_sdt=0%2C5&as_vis=1&q=samsung')
#     cite = wait.until(EC.element_to_be_clickable(By.XPATH, "//*[@id='gs_res_ccl_mid']/div[1]/div[2]/div[3]/a[2]")).click

#     container = driver.find_element_by_css_selector('#gs_citt').text
#     print(container)
