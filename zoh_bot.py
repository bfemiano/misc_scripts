import time
from selenium import webdriver
import random
import string
for i in range(1000):
    n = random.randint(1,6)
    print "pausing for %i seconds" % n
    r = random.randint(10,20)
    email = ""
    for j in range(r):
        email += random.choice(string.letters)
    print "using %s" % email
    time.sleep(n)
    driver = webdriver.PhantomJS()
    driver.get('https://bubbasnacks.hscampaigns.com/#submissions')
    gallery = driver.find_element_by_id('gal-2811')
    gallery.click()
    zoh_section = driver.find_element_by_class_name('_modalVoteContainer')
    zoh_section2 = zoh_section.find_element_by_class_name('_VotesContainer')
    zoh_section2.click()
    driver.save_screenshot('after_voted.jpg')
    email_field = driver.find_element_by_class_name("_enterEmailInput")
    email_field.send_keys('%s@gmail.com' % email)
    send_button = driver.find_element_by_class_name("_enterEmailSubmit")
    spinner = send_button.find_element_by_class_name("spinner")
    spinner.click()
    driver.save_screenshot("after_all.jpg")
