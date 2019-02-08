from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import time
import random
import selenium.webdriver.support.ui as ui
import time
import json
import re

def investigate_by_xpath(driver, time_wait, object, message):
	# input : 等待時間, 確認目標的xpath內容, 成功回報訊息
    # target : 因驗證帳密會有延遲時間, 故此function為確認有無正常進入下一動作
    # print(message)
    wait = ui.WebDriverWait(driver, time_wait)
    wait.until(lambda driver: driver.find_element_by_xpath(object).is_displayed())
def back_to_menu(driver):
    driver.find_element_by_xpath('//a[contains(text(),"  回到菜單")]').click()
    investigate_by_xpath(driver, 10, '//a[contains(text(),"瀏覽菜單")]', '回到菜單')
def filter_cost(cost_str):
    return int(re.findall(r'\d+',cost_str)[0])

def parser_main_food(soup, items):
    product_name_list = soup.find_all('h5',{'class': 'product-title'})
    product_cost_list = soup.find_all('span',{'class': 'starting-price'})

    for name, cost in zip(product_name_list, product_cost_list):
        items["主餐"][name.text] = filter_cost(cost.text)
    return items
def parser_append(soup, items):
    append_name_list = soup.find_all('div',{'class': 'colsize-5'})

    for item in append_name_list:
        name = item.div.div.h5.text
        cost = item.div.find('div',{'class':'product-cost'}).text
        cost = filter_cost(cost)
        items["追加"][name] = cost
    return items
def parser_coffee(soup, items):
    coffee_name_list = soup.find_all('h5',{'class': 'coffee-title'})
    coffee_cost_list = soup.find_all('span',{'class': 'starting-price'})

    for name, cost in zip(coffee_name_list, coffee_cost_list):
        items["咖啡"][name.text] = int(re.findall(r'\d+',cost.text)[0])
    
    return items
def parser_combination(soup, items):
    
    combination_name_list = soup.find_all('h4',{'class': 'item-title'})
    combination_cost_list = soup.find_all('td',{'class': 'cost-column'})

    single = filter_cost(combination_cost_list[-1].text)
    for name, cost in zip(combination_name_list[:-1], combination_cost_list[:-1]): #最後一行單點不要
        name = name.text.split(' - ')[0]
        cost = filter_cost(cost.text) - single # 減去單點的
        items["組合"][name] = cost
    return items
def parser_drink(soup, items):
    drink_name_list = soup.find_all('h4',{'class': 'item-title'})
    drink_cost_list = soup.find_all('td',{'class': 'cost-column'})

    for name, cost in zip(drink_name_list, drink_cost_list): #最後一行單點不要\
        name = name.text
        cost = filter_cost(cost.text)
        items["飲料"][name] = cost
    return items
def load_account(json_data = 'crawling/account.json'):
    with open(json_data, 'r') as f:
        data = json.load(f)
    if data['username'] == 'yourmail' or data['password'] == 'yourpassword':
        raise Exception('請至account.json更新可使用帳號跟密碼')
    return data['username'], data['password']
def start_crawling():
    # 前置
    username, password = load_account()

    driver = webdriver.Chrome()
    url = 'https://www.mcdelivery.com.tw/tw/browse/menu.html'
    driver.get(url) 

    driver.find_element_by_xpath('//a[contains(text(),"登入")]').click()
    investigate_by_xpath(driver, 10, '//h2[@id="modal-title"]', '進入登入畫面')
    
    driver.find_element_by_xpath('//input[@placeholder="電子郵件"]').send_keys(username)
    driver.find_element_by_xpath('//input[@placeholder="密碼"]').send_keys(password)
    driver.find_element_by_xpath('//button[contains(text(),"登入")]').click()
    investigate_by_xpath(driver, 10, '//a[contains(text(),"開始訂餐")]', '登入成功!')

    driver.get('https://www.mcdelivery.com.tw/tw/menu.html')
    investigate_by_xpath(driver, 10, '//a[contains(text(),"瀏覽菜單")]', '進入點餐畫面')

    items = {"主餐":{},"組合":{'主餐':0},"追加":{"無":0},"咖啡":{},"飲料":{}}

    # 主餐
    driver.find_element_by_xpath('//span[contains(text(),"超值全餐和主餐單點")]').click()
    investigate_by_xpath(driver, 10, '//li[contains(text(),"超值全餐和主餐單點")]', '進入-超值全餐和主餐單點')

    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = parser_main_food(soup, items)

    # 組合
    driver.find_element_by_xpath('//a[contains(text(),"訂購")]').click()
    investigate_by_xpath(driver, 10, '//h3[contains(text(),"選擇您的餐點")]', '進入訂購畫面')

    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = parser_combination(soup, items)

    # 追加
    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = parser_append(soup, items)

    # 咖啡‘
    back_to_menu(driver)
    #time.sleep(5)
    driver.find_element_by_xpath('//span[contains(text(),"McCafé")]').click()
    #time.sleep(5)
    #investigate_by_xpath(driver, 10, '//li[contains(text(),"McCafé")]', '進入-McCafé')

    # coffee
    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = parser_coffee(soup, items)

    # 飲料
    driver.find_element_by_xpath('//span[contains(text(),"飲料")]').click()
    #time.sleep(5)
    #investigate_by_xpath(driver, 10, '//li[contains(text(),"飲料")]', '進入-飲料')


    for item in driver.find_elements_by_xpath('//a[contains(text(),"訂購")]'):
        item.click()
        investigate_by_xpath(driver, 10, '//h3[contains(text(),"選擇您的餐點")]', '進入訂購畫面')
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = parser_drink(soup, items)
            
        back_to_menu(driver)
        
    driver.close()

    with open('crawling/items.json', 'w') as f:
        json.dump(items, f)

    with open('crawling/items.json', 'r') as f:
        items = json.load(f)