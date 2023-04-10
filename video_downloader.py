# import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os


def download_video(link):
    options = webdriver.ChromeOptions()
    preferences = {"download.default_directory": os.getcwd()}
    options.add_experimental_option("prefs", preferences)

    # open https://www.downloadvideosfrom.com/ru/VK.php
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://www.downloadvideosfrom.com/ru/VK.php")

    # paste link to video
    link_input = driver.find_element(By.ID, 'url')
    link_input.send_keys(link)

    # click download button
    download_button = driver.find_element(By.ID, 'DownloadMP4HD_text')
    download_button.click()

    # wait till .mp4 file appears
    downloaded = False
    current_amount = len([f for f in os.listdir('.') if f.endswith('.mp4')])

    while True:
        if len([f for f in os.listdir('.') if f.endswith('.mp4')]) - current_amount > 0:
            downloaded = True
            break
        time.sleep(0.5)

    # close browser
    driver.close()
    return downloaded
