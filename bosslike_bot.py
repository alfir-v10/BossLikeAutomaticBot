from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
import config
import random
import datetime
import os
import pickle
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json
from contextlib import contextmanager
from pprint import pprint
from selenium.webdriver.firefox.options import Options


class BossLike():

    def __init__(self, driver, config_logpass_acc, test=False, headless = True):

        if driver == 'Firefox':
            self.options = Options()
            self.options.headless = headless
            self.browser = webdriver.Firefox(options=self.options, executable_path=config.drivers[driver])

        if driver == 'Chrome':
            self.browser = webdriver.Firefox(executable_path=config.drivers[driver])
        self.test = test
        self.cookies_insta = config_logpass_acc['cookies']['insta']
        self.cookies_boss = config_logpass_acc['cookies']['boss']

        self.login_insta = config_logpass_acc['insta']['login']
        self.password_insta = config_logpass_acc['insta']['password']

        self.login_boss = config_logpass_acc['boss']['login']
        self.password_boss = config_logpass_acc['boss']['password']

    def capcha_pause(self):
        input('Press Enter after capcha')

    """BOSSLIKE"""
    def boss_login(self):
        if self.test: print('Run boss_login')
        WebDriverWait(self.browser, 100).until(EC.presence_of_element_located((By.NAME, 'UserLogin[login]')))
        self.browser.find_element_by_name('UserLogin[login]').send_keys(self.login_boss)
        self.browser.find_element_by_name('UserLogin[password]').send_keys(self.password_boss)
        self.capcha_pause()
        self.browser.find_element_by_xpath('//*[@id="formLogin"]/input').click()
        self.cookies_save(self.cookies_boss)

    def boss_open(self, url=config.urls['boss_like']):
        if self.test: print('Run boss_open')
        self.browser.get(config.urls['boss_login'])
        if self.cookies_add(self.cookies_boss):
            print('Cookies add')
        else:
            self.browser.get(config.urls['boss_login'])
            self.boss_login()
        self.browser.get(url)
        try:
            WebDriverWait(self.browser, 30, ignored_exceptions=False).until\
                (EC.presence_of_element_located((By.CLASS_NAME, 'tasks')))
        except TimeoutException: print("boss_open_like_url")

    """INSTAGRAM"""
    def insta_login(self):
        if self.test: print('Run insta_login')
        try:
            WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
        except TimeoutException: print('insta_login')
        self.browser.find_element_by_name('username').send_keys(self.login_insta)
        sleep(2)
        self.browser.find_element_by_name('password').send_keys(self.password_insta)
        sleep(2)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
        # self.capcha_pause()
        sleep(5)
        self.cookies_save(self.cookies_insta)

    def insta_open(self):
        if self.test: print('Run insta_open')
        self.browser.get(config.urls['insta'])
        if self.cookies_add(cookies_path = self.cookies_insta):
            print('Cookies add')
        else:
            self.insta_login()

    """COOKIES"""
    def cookies_add(self, cookies_path):
        if self.test: print('Run cookies_add')
        if os.path.exists(cookies_path):
            cookies = pickle.load(open(cookies_path, "rb"))
            for cookie in cookies:
                self.browser.add_cookie(cookie)
            return True
        else:
            return False

    def cookies_save(self, cookies_path):
        if self.test: print('Run cookies_save')
        pickle.dump(self.browser.get_cookies(), open(cookies_path, "wb"))
        print('Cookies is saved')


    """BOT COMMAND"""

    def like_from_insta(self):
        if self.test: print('Run like_from_insta')
        # WebDriverWait(self.browser, 30, ignored_exceptions=False).until(EC.url_contains('instagram'))
        # self.browser.implicitly_wait(10)
        try:
            elem = WebDriverWait(self.browser, 1, ignored_exceptions=False).until(EC.presence_of_element_located((By.CLASS_NAME, 'fr66n')))
            print(elem)
            elem.click()
            try:
                WebDriverWait(self.browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.HoLwm")))
                return False
            except TimeoutException:
                pass
        except (TimeoutException, TypeError): print('like from insta')
        # self.browser.find_element_by_class_name('fr66n').click()
        self.browser.close()
        return True

    def like_from_boss(self, index):
        if self.test: print('Run like_from_boss')
        try:
            WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[5]/div[1]/div/div[1]/div/div[2]/article[{index}]/div/div/div/div[4]/a')))
            self.browser.find_element_by_xpath( f'/html/body/div[5]/div[1]/div/div[1]/div/div[2]/article[{index}]/div/div/div/div[4]/a').click()
        except TimeoutException: print("like_from_boss")

    def subscribe_from_insta(self):
        pass

    def subscribe_from_boss(self):
        self.browser.get(config.urls['boss_subscribe'])

    """MAIN COMMAND BY SELENIUM"""
    def close_all(self):
        if self.test: print('Run close_all')
        self.browser.quit()

    def close_window(self):
        if self.test: print('Run close_window')
        self.browser.close()

    def get_windows(self):
        if self.test: print('Run get_window')
        return self.browser.window_handles

    def choose_window(self, window_handle):
        if self.test: print('Run choose_window')
        self.browser.implicitly_wait(2)
        self.browser.switch_to.window(window_handle)

    @contextmanager
    def wait_for_new_window(self, timeout=10):
        if self.test: print('Run wait_for_new_window')
        handles_before = self.browser.window_handles
        yield
        WebDriverWait(self.browser, timeout).until(
            lambda driver: len(handles_before) != len(driver.window_handles))

    def refresh(self, url=config.urls['boss_like']):
        self.browser.get(config.urls['boss_like'])


if "__name__" == "main":
    CHANGE_FLAG = False

    def test_2(log = config.logpass['acc2']):
        print(f"Log: {log}")
        bike = BossLike(driver='Firefox', config_logpass_acc=log, test=True, headless=False)
        bike.insta_open()
        bike.boss_open(url=config.urls['boss_like'])
        flag = 1
        count = 0
        while (flag < 50):
            flag += 1
            index = random.randint(2, 20)
            bike.refresh()
            sleep(1)
            try:
                with bike.wait_for_new_window(2):
                    bike.like_from_boss(index)
                    windows = bike.get_windows()
                    print(f"1 {windows}")
                    sleep(2)
                    if len(windows) == 2:
                        # try:
                        windows = bike.get_windows()
                        print(f"2 {windows}")
                        try:
                            bike.choose_window(windows[1])
                            WebDriverWait(driver=bike.browser, timeout=30, ignored_exceptions=False).until(EC.url_contains("instagram"))
                            print(f"3 {bike.browser.current_url}", )
                            if not bike.like_from_insta():
                                bike.cookies_save(bike.cookies_insta)
                                print("INSTAGRAM LIMITS STOP")
                                global CHANGE_FLAG
                                CHANGE_FLAG = True
                                break
                            sleep(5)
                            count+=1
                            print(f"Count {count}")
                            # print(f"2 {bike.browser.current_url}")
                            #bike.close_window()
                            win = bike.browser.window_handles
                            print("win ", win)
                            # except TimeoutException:
                            print("browsing save")
                        except TimeoutException: pass
            except (TimeoutException):
                print("Like from boss dosnt open new window")
            win = bike.browser.window_handles[0]
            print("win ", win)
            bike.choose_window(win)
        bike.close_all()
        del bike
        # if CHANGE_FLAG:
        #     return log
        return count

    def change_login(acc):
        if acc == config.logpass['acc1']:
            return config.logpass['acc2']
        if acc == config.logpass['acc2']:
            return config.logpass['acc1']

    i = 2
    like_count = 0
    changes_count = 0
    acc = config.logpass['acc1']
    while (i < 10):
        # try:
        if CHANGE_FLAG:
            path = acc['cookies']['insta']
            if os.path.exists(path):
                os.remove(path)
            acc = change_login(acc)
            acc = config.logpass['acc1']
            CHANGE_FLAG = False
            changes_count += 1
            sleep(10*60)
            if changes_count == 50:
                print("too mane changes")
                break
        count = test_2(acc)
        like_count += count
        print("Like count: ", like_count)
        sl = random.randint(5, 10)
        print(f"Sleep time {sl} min")
        sleep(sl * 60)
        # except NoSuchWindowException:
        #     print("STOP")
        #     break
        i+=1

    path = acc['cookies']['insta']
    if os.path.exists(path):
        os.remove(path)
    print("Like count: ", like_count)

    # i = 0
    # index = 0
    # max_index = 10
    # like_count = 0
    # while (True):
    #     op = 1
    #     while op:
    #         try:
    #             index += 1
    #             print("index", index)
    #             if index == max_index:
    #                 index = 1
    #                 bike.browser.refresh()
    #             with bike.wait_for_new_window(timeout=3):
    #                 bike.like_from_boss(index=index)
    #                 op = 0
    #         except:
    #             bike.browser.refresh()
    #     windows = bike.get_windows()
    #     print("Len windows ", len(windows))
    #     print('windows ', windows)
    #     wind_len = len(windows)
    #     if wind_len == 2:
    #         bike.choose_window(windows[1])
    #         if bike.like_from_insta():
    #             like_count += 1
    #             print("like_count: ", like_count)
    #         if len(bike.get_windows()) == 2:
    #             bike.close_window()
    #         sleep(3)
    #         bike.choose_window(windows[0])
    #     index += 1
    #     print("index", index)
    #     if index == max_index:
    #         index = 1
    #         bike.browser.refresh()
    #     if like_count == 100:
    #         break
    # bike.cookies_save(cookies_path=bike.cookies_boss)
    # bike.cookies_save(cookies_path=bike.cookies_insta)
    # bike.close()
