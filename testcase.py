import time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_until_element_is_visible(timeout, xpath):
    try:
        wait = WebDriverWait(driver, timeout)
        _element_locator = (By.XPATH, xpath)
        wait.until(EC.element_to_be_clickable(_element_locator))
    except Exception as e:
        print(f"ERROR: 找不到xpath: {xpath}")

def click_button_by_xpath(driver, xpath):
    try:
        wait_until_element_is_visible(10, xpath)
        driver.find_element_by_xpath(xpath).click()
    except Exception as e:
        print(f"ERROR: 找不到xpath: {xpath}")

def take_screenshot(driver, caseNumber, fileName):
    if not os.path.exists(".\\screenshots"):
        os.makedirs(".\\screenshots")
    if not os.path.exists(f".\\screenshots\\{caseNumber}"):
        os.makedirs(f".\\screenshots\\{caseNumber}")
    try:
        time.sleep(1)
        driver.save_screenshot(f".\\screenshots\\{caseNumber}\\{fileName}")
        print(f"截圖: .\screenshots\{caseNumber}\{fileName}.png")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    options = Options()
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)

    driver.set_window_size(414, 896)        # iphone XR size
    driver.get("https://www.cathaybk.com.tw/cathaybk/")

    print('---------------------------------')

    # Test case 1
    try:
        main_buttons_xpath = '//*[@class="cubre-o-quickLink__item"]//*[contains(@id, "lnk_Link")]'
        wait_until_element_is_visible(10, main_buttons_xpath)
        take_screenshot(driver, "1", "1.png")

        print("\ntest case 1: ok\n")
    except Exception as e:
        print(e)

    print('---------------------------------')

    # Test case 2
    try:
        burger_xpath = '//*[@class="cubre-a-burger"]'
        click_button_by_xpath(driver, burger_xpath)

        menu1_item1_xpath = '//*[@class="cubre-o-menu__btn"]//*[@class="cubre-a-menuSortBtn -l1" and normalize-space()="產品介紹"]'
        click_button_by_xpath(driver, menu1_item1_xpath)

        menu2_item1_xpath = '//*[@class="cubre-a-menuSortBtn" and normalize-space()="信用卡"]'
        click_button_by_xpath(driver, menu2_item1_xpath)

        menu3_xpath = '//*[@class="cubre-o-menuLinkList__item is-L2open"]//*[@class="cubre-o-menuLinkList__content"]'
        wait_until_element_is_visible(10, menu3_xpath)

        take_screenshot(driver, "2", "2.png")

        item_count = driver.find_element_by_xpath(menu3_xpath).find_elements_by_tag_name("a")
        print(f"信用卡選單下有 {len(item_count)} 個項目")

        print("\ntest case 2: ok\n")
    except Exception as e:
        print(e)

    print('---------------------------------')

    # Test case 3
    try:
        m3_item1_xpath = '//*[@class="cubre-o-menuLinkList__content"]//*[contains(@id, "lnk_Link") and normalize-space()="卡片介紹"]'
        click_button_by_xpath(driver, m3_item1_xpath)

        js = 'window.scrollTo(0, 3700);'
        driver.execute_script(js)

        item_xpath = '//*[@class="cubre-a-iconTitle__text" and normalize-space()="停發卡"]'
        wait_until_element_is_visible(10, item_xpath)

        items_xpath = '//*[@data-anchor-block="blockname06"]//*[contains(@class, "cubre-o-slide__page")]//*[contains(@class, "swiper-pagination-bullet")]'
        items_count = len(driver.find_elements_by_xpath(items_xpath))
        print(f"已停發信用卡數量: {items_count}")

        for i in range(1, items_count+1):
            item1_xpath = f'//*[@data-anchor-block="blockname06"]//*[contains(@class, "cubre-o-slide__page")]//*[contains(@class, "swiper-pagination-bullet") and @aria-label="Go to slide {i}"]'
            click_button_by_xpath(driver, item1_xpath)
            take_screenshot(driver, "3", f"3-{i}.png")

        result = 0
        for i in range(1, items_count+1):
            if os.path.isfile(f"screenshots/3/3-{i}.png"):
                result += 1

        count_file_in_folder_3 = len(os.listdir("screenshots/3"))
        if result == count_file_in_folder_3:
            print("已停發信用卡數量與截圖數量相同")

        print("\ntest case 3: ok\n")
    except Exception as e:
        print(e)

    print('---------------------------------')

    driver.quit()