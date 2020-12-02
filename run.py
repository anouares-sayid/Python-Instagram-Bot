from msedge.selenium_tools import Edge, EdgeOptions
import os
import time
import random
import spintax
import requests
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from credentials import username , password 


class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        profile = webdriver.Edge(executable_path='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe')
        self.InstaBot = profile
        self.InstaBot.set_window_size(500, 950)
        with open(r'tags.txt', 'r') as f:
            tagsl = [line.strip() for line in f]
        self.tags = tagsl
        self.urls = []

    def exit(self):
        InstaBot = self.InstaBot
        InstaBot.quit()

    def login(self):
        InstaBot = self.InstaBot
        InstaBot.get('https://instagram.com/')
        time.sleep(4)

        if check_exists_by_xpath(InstaBot, "//button[text()='Accept']"):
            print("No cookies")
        else:
            InstaBot.find_element_by_xpath("//button[text()='Accept']").click()
            print("Accepted cookies")

        time.sleep(1)
        '''
        InstaBot.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div/div/div/div[2]/button').click()
        print("Logging in...")
        
        time.sleep(1)
        '''
        username_field = InstaBot.find_element_by_xpath("//input[@name='username']")
        username_field.send_keys(self.username)
        time.sleep(1)
        find_pass_field = (
            By.XPATH, '//input[@name="password"]')
        WebDriverWait(InstaBot, 50).until(
            EC.presence_of_element_located(find_pass_field))
        pass_field = InstaBot.find_element(*find_pass_field)
        WebDriverWait(InstaBot, 50).until(
            EC.element_to_be_clickable(find_pass_field))
        pass_field.send_keys(self.password)
        time.sleep(2)
        InstaBot.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(10)

    def get_posts(self):
        print('Searching post by tag...')
        InstaBot = self.InstaBot
        tags = self.tags
        tag = tags.pop()
        link = 'https://www.instagram.com/explore/tags/' + tag
        InstaBot.get(link)

        time.sleep(4)

        for i in range(1):
            ActionChains(InstaBot).send_keys(Keys.END).perform()
            time.sleep(2)

        divs = InstaBot.find_elements_by_xpath("//a[@href]")

        first_urls = []

        for i in divs:
            if i.get_attribute('href') != None:
                first_urls.append(i.get_attribute('href'))
            else:
                continue

        for url in first_urls:
            if url.startswith('https://www.instagram.com/p/'):
                self.urls.append(url)
        return run.comment(random_comment())

    def comment(self, comment):

        if len(self.urls) == 0:
            print('Finished tag jumping to next one...')
            return run.get_posts()

        InstaBot = self.InstaBot
        url = self.urls.pop()
        print('commenting...')
        InstaBot.get(url)
        InstaBot.implicitly_wait(1)
        InstaBot.execute_script("window.scrollTo(0, window.scrollY + 300)")
        time.sleep(2)

        if check_exists_by_xpath(InstaBot, "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"):
            print("No comment section")
        else: 
            InstaBot.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button').click()
            time.sleep(2)
            InstaBot.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[2]/button').click()

        if check_exists_by_tag_name(InstaBot, 'textarea'):
            print("skiped")
            return run.comment(random_comment())

        find_comment_box = (
            By.TAG_NAME, 'textarea')
        WebDriverWait(InstaBot, 50).until(
            EC.presence_of_element_located(find_comment_box))
        comment_box = InstaBot.find_element(*find_comment_box)
        WebDriverWait(InstaBot, 50).until(
            EC.element_to_be_clickable(find_comment_box))
        comment_box.click()
        time.sleep(4)
        find_comment_box = (
            By.TAG_NAME, 'textarea')
        WebDriverWait(InstaBot, 50).until(
            EC.presence_of_element_located(find_comment_box))
        comment_box = InstaBot.find_element(*find_comment_box)
        WebDriverWait(InstaBot, 50).until(
            EC.element_to_be_clickable(find_comment_box))
        time.sleep(4)
        try:
           InstaBot.implicitly_wait(10)
           comment_box.send_keys(comment)
           comment_box.send_keys(Keys.RETURN)
        except StaleElementReferenceException:
           InstaBot.implicitly_wait(10)
           return run.comment(random_comment())
           comment_box.send_keys(Keys.RETURN)
        
       
        find_post_button = (
            By.XPATH, '/html/body/div[1]/section/main/section/div/form/button')
        WebDriverWait(InstaBot, 50).until(
            EC.presence_of_element_located(find_post_button))
        post_button = InstaBot.find_element(*find_post_button)
        WebDriverWait(InstaBot, 50).until(
            EC.element_to_be_clickable(find_post_button))
        post_button.click()
      
        # reduce the value of x to make InstaBot faster time.sleep(x)
        time.sleep(5)
        # ---------------------------------

        return run.comment(random_comment())


def random_comment():
    with open(r'comments.txt', 'r',encoding="utf-8") as f:
        commentsl = [line.strip() for line in f]
    comments = commentsl
    comment = random.choice(comments)
    return comment

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return True

    return False

def check_exists_by_tag_name(driver, tag_name):
    try:
        driver.find_element_by_tag_name(tag_name)
    except NoSuchElementException:
        return True

    return False


run = InstaBot(username, password)
run.login()

if __name__ == '__main__':
    if run.tags == []:
        print("Finished")
    else:
        run.get_posts()
