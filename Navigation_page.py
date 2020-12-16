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
import re
from Scraping_things import scrap_data
app = wx.App()

def ChromeDriver():
    browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"))
    browser.maximize_window()
    # browser.get("""https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
    # wx.MessageBox(' -_-  Add Extension and Select Proxy Between 25 SEC -_- ','Info', wx.OK | wx.ICON_WARNING)
    # time.sleep(25)
    browser.get("https://compranet.hacienda.gob.mx/esop/guest/go/public/opportunity/current?locale=es_MX")
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
    time.sleep(8)
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
    for page_count in browser.find_elements_by_xpath('//*[@class="columnCenter"]'):
        page_count = page_count.get_attribute('innerText').strip()
        cleanr = re.compile('<.*?>')
        page_count = re.sub(cleanr, '', page_count)
        page_count = page_count.partition('de')[2].strip()
        break
    for i in range(int(page_count)):

        for links in browser.find_elements_by_xpath('//*[@id="cntList"]/form/div/table/tbody[2]/tr/td[4]/a'):
            links = links.get_attribute('outerHTML')
            links = links.partition('javascript:goToDetail')[2].partition(";")[0].strip()
            links = links.partition("'")[2].partition("',")[0].strip()
            links = f'https://compranet.hacienda.gob.mx/esop/toolkit/opportunity/opportunityDetail.do?opportunityId={links}&oppList=CURRENT'
            print(links)
            html_links.append(links)
        for next_page in browser.find_elements_by_xpath('//*[@class="NavBtnForward"]'):
            next_page.click()
            break
        time.sleep(5)
    print(f'Collect Links: {len(html_links)}')
    Global_var.Total = len(html_links)
    for href in html_links:
        browser.get(href)
        get_htmlSource = ''
        for get_htmlSource in browser.find_elements_by_xpath('//*[@id="cntAllPage"]'):
            get_htmlSource = get_htmlSource.get_attribute('outerHTML')
            get_htmlSource = get_htmlSource.partition('class="accessHidden">')[2].strip()
            get_htmlSource = get_htmlSource.replace('href="#content"',f'href="{href}#content"')
            get_htmlSource = get_htmlSource.replace('src="/','src="https://compranet.hacienda.gob.mx/')
            get_htmlSource = get_htmlSource.replace('href="/','href="https://compranet.hacienda.gob.mx/')
            get_htmlSource = get_htmlSource.replace('action="/','action="https://compranet.hacienda.gob.mx/')
            get_htmlSource = get_htmlSource.replace('<input type="text" disabled="disabled" class="displayNone">','')
            # iframe = '<iframe src="https://compranet.hacienda.gob.mx/esop/guest/go/public/opportunity/current?locale=es_MX" style="display:none;"></iframe>'
            # get_htmlSource = f'{iframe}<br>{get_htmlSource}'
            mainlink = f'<p style="color:red;"><b>Note:</b> For any problem in attachments.</p><br><a href="https://compranet.hacienda.gob.mx/esop/guest/go/public/opportunity/current?locale=es_MX" target="_blank" style="color:red;">1 ) First click here to create session.</a><br><a href="{href}" target="_blank" style="color:red;">2 ) After creating session click here for main document.</a>'
            get_htmlSource = f'{get_htmlSource}<br>{mainlink}'
            break
        if get_htmlSource != '':
            scrap_data(href,get_htmlSource)
            print(f'Total: {str(Global_var.Total)} Deadline Not given: {Global_var.deadline_Not_given} duplicate: {Global_var.duplicate} inserted: {Global_var.inserted} expired: {Global_var.expired} QC Tenders: {Global_var.QC_Tenders}')
            time.sleep(10)
        else:
            wx.MessageBox(' get_htmlSource Var Blank ','compranet.hacienda.gob.mx', wx.OK | wx.ICON_INFORMATION)

    wx.MessageBox(f'Total: {str(Global_var.Total)}\nDeadline Not given: {Global_var.deadline_Not_given}\nduplicate: {Global_var.duplicate}\ninserted: {Global_var.inserted}\nexpired: {Global_var.expired}\nQC Tenders: {Global_var.QC_Tenders}','compranet.hacienda.gob.mx', wx.OK | wx.ICON_INFORMATION)
    

ChromeDriver()