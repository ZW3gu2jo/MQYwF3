import time
from selenium import webdriver
from PIL import Image
import lianzhong_api as lz
import json
import phone51ym as ph

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://passport2.eastmoney.com/pub/reg');
driver.implicitly_wait(8)
tel_box = driver.find_element_by_name('reg_tel')

phonenum = ph.phone.getnum()
tel_box.send_keys(phonenum)

# search_box.submit()
confirm = driver.find_element_by_css_selector("input.button1")
confirm.click()
time.sleep(3)#等待三秒获取验证码
captchaimg = driver.find_element_by_css_selector("img.captchaimg")#找到验证码
imgsrc = captchaimg.get_attribute("src")


captchaimgdriver =  webdriver.Chrome()
captchaimgdriver.get(imgsrc);
captchaimgdriver.implicitly_wait(5)
captchaimgdriver.get_screenshot_as_file('./screenshot.png')

captchacookie = captchaimgdriver.get_cookie("EmPaVCodeCo")
print(captchacookie)

captchaimgdriverelement = captchaimgdriver.find_element_by_css_selector('img')
left = int(captchaimgdriverelement.location['x'])
top = int(captchaimgdriverelement.location['y'])
right = int(captchaimgdriverelement.location['x'] + captchaimgdriverelement.size['width'])
bottom = int(captchaimgdriverelement.location['y'] + captchaimgdriverelement.size['height'])
im = Image.open('./screenshot.png')
im = im.crop((left, top, right, bottom))
im.save('./code.png')
# time.sleep(5)

driver.add_cookie(captchacookie)
captchaimgdriver.quit()

captchastr = lz.main('./code.png')
captchadic = json.loads(captchastr)

rege =  driver.find_element_by_name("reg_checkNub")
rege.send_keys(captchadic["data"]["val"])
confirm.click()

smscode = ph.phone.getsms(phonenum)
telsms_box = driver.find_element_by_name("reg_teljhm")
telsms_box.send_keys(smscode)

pass_box = driver.find_element_by_name("reg_telPassword")
pass_box.send_keys(phonenum)

xieyi_box = driver.find_element_by_id("readWebRule")
xieyi_box.click()

tongyi_box = driver.find_element_by_id("btn_reg")
tongyi_box.click()

time.sleep(30)
driver.quit()
