from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import html
import sys, os
from datetime import datetime
import Global_var
import wx
import string
import html
from Scraping_things import scrap_data
app = wx.App()

def ChromeDriver():
    browser = webdriver.Chrome(executable_path=str(f"F:\\chromedriver.exe"))
    browser.get("https://compranet.hacienda.gob.mx/esop/guest/go/public/opportunity/current?locale=es_MX")
    browser.maximize_window()
    time.sleep(2)
    for select_dropdown in browser.find_elements_by_xpath('//*[@id="widget_filterPickerSelect"]/div[1]/input'):
        select_dropdown.click()
        break
    time.sleep(2)
    for select_publication_date in browser.find_elements_by_xpath('//*[@id="filterPickerSelect_popup3"]/span'):
        select_publication_date.click()
        break
    time.sleep(2)
    for select_After in browser.find_elements_by_xpath('//*[@id="firstPublishingDate_FILTER_OPERATOR_ID"]/option[3]'):
        select_After.click()
        break
    time.sleep(2)
    for send_date in browser.find_elements_by_xpath('//*[@id="firstPublishingDate_FILTER_fromDate"]'):
        send_date.send_keys(str(Global_var.date))
        break
    time.sleep(2)
    for Search_btn in browser.find_elements_by_xpath('//*[@id="filterSearchButton"]'):
        Search_btn.click()
        break
    time.sleep(5)
    for data_found_OR_not in browser.find_elements_by_xpath('//*[@id="cntList"]/form/div/div[2]'):
        data_found_OR_not = data_found_OR_not.get_attribute('innerText')
        if 'Sin resultado' in str(data_found_OR_not):
            wx.MessageBox(' No Tender Found ','compranet.hacienda.gob.mx', wx.OK | wx.ICON_INFORMATION)
            browser.close()
            sys.exit()
        break
    collect_links(browser)

def collect_links(browser):
    html_links = []
    for links in browser.find_elements_by_xpath("/html/body/div/div[6]/div/div[2]/div[4]/form/div/table/tbody/tr/td[5]/a"):
        links = links.get_attribute('outerHTML')
        links = links.partition('javascript:goToDetail')[2].partition(";")[0].strip()
        links = links.partition("'")[2].partition("',")[0].strip()
        links = f'https://compranet.hacienda.gob.mx/esop/toolkit/opportunity/opportunityDetail.do?opportunityId={links}&oppList=CURRENT'
        html_links.append(links)
    
    for href in html_links:
        browser.get(href)
        get_attribute = ''
        for get_attribute in browser.find_elements_by_xpath('//*[@id="cntAllPage"]'):
            get_attribute = get_attribute.get_attribute('outerHTML')
            break
        scrap_data(get_attribute)

ChromeDriver()