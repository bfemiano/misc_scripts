from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


"""
Runs on Current google-chrome version is 87.0.4280

"""

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.maximize_window()
action = ActionChains(browser)
lag_seconds = 3

try:
    browser.get('https://www.walmart.com/ip/Thomas-Friends-Wood-Harvey-Industrial-Crane-Engine-Train/535197390')

    # click accounts tab in upper right
    account = browser.find_element_by_id('hf-account-flyout')
    action.move_to_element(account)
    action.perform()
    account.click()

    # open sign-in form.
    account_root = browser.find_element_by_id("vh-account-menu-root")
    sign_in_form = account_root.find_element_by_class_name("w_a")
    sign_in_form.click()

    # enter email/password and sign in.
    email = browser.find_element_by_id("email")
    email.send_keys("REDACTED")
    passwd = browser.find_element_by_id("password")
    passwd.send_keys("REDACTED")
    sign_in_btn = browser.find_element_by_class_name("m-margin-top")
    sign_in_btn.click()
    sleep(lag_seconds)

    # add harvey train to cart
    add_to_cart = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "prod-product-cta-add-to-cart")))
    add_to_cart.click()

    #checkout
    button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart-pos-proceed-to-checkout")))
    button.click()
    sleep(lag_seconds)

    # #delivery
    delivery_btn = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "shipping-button-0")))
    delivery_btn.click()
    continue_btn = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cxo-continue-btn")))
    sleep(lag_seconds)
    continue_btn.click()

    address = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".address-tile-clickable")))
    address.click()
    continue_btn = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".u-size-1-12-m")))
    continue_btn.click()

    # #credit card should be default-entered.
    cvv_confirm = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "cvv-confirm")))
    cvv_confirm.send_keys("123") # TODO this is a fake CVV
    review_order = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".fulfillment-opts-continue")))
    review_order.click()
except:
    raise
finally:
    browser.close()