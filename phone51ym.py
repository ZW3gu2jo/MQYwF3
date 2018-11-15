import requests
import time
import myconfig as cfg

class whittime:
    def __init__(self):
        pass

    def dfun(self,fun,time = 5):
        count = 1
        while count <= time:
            r = fun()
            if "err" in r:
                count = count+1
            else:
                return r

class Phone:
    token = ""
    phonenum = ""
    itemid = "1404"
    def __init__(self):
        self.name = cfg.ymname
        self.password = cfg.ympass
        dengluhost = "http://api.fxhyd.cn/UserInterface.aspx?action=login&username="+self.name+"&password="+self.password
        r = requests.get(dengluhost)
        if "success" in r.text:
            self.token = r.text[8:]
            print("token = %s" % self.token)
        else:
            print("登录失败 " + r.text)
            exit()

    def getnum(self):
        # 获取东方财富网手机号
        self.phonenum = ""
        getphonenumhost = "http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token="+self.token+"&itemid="+self.itemid
        # print(getphonenumhost)
        r = requests.get(getphonenumhost)

        if "success" in r.text:
            phonenum = r.text[8:]
            print("phonenum = %s" % phonenum)
            self.phonenum = phonenum
            return phonenum
        else:
            print("获取手机号失败 " + r.text)
            return "err"

    def releasenum(self):
        # 释放手机号
        if self.phonenum != "":
            rehost = "http://api.fxhyd.cn/UserInterface.aspx?action=release&token="+self.token+"&itemid="+self.itemid+"&mobile="+self.phonenum
            r = requests.get(rehost)
            if "success" in r.text:
                self.phonenum = ""
                print("释放手机号成功")
                return "ok"
            else:
                print("释放手机号失败 " + r.text)
                return "err"

    def getsms(self,phonenum):
        getsmshost = "http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token="+self.token+"&itemid="+self.itemid+"&mobile="+phonenum+"&release=1"
        count = 1
        while count < 21:
            r = requests.get(getsmshost)
            print("第 %d 次获取" % count )
            r.encoding = 'utf-8'
            if "success" in r.text:
                # print(r.text)
                # print(r.text[18:24])
                self.releasenum()
                return r.text[18:24]
            else:
                time.sleep(5)
            count = count + 1

        return "err"


    def main(self):
        while True:
            if "1" in self.getnum():
                break
            else:
                print("getnum err")
                time.sleep(5)

        print(self.getsms(self.phonenum))

phone = Phone()

if __name__ == '__main__':
    yima = Phone()
    print(yima.getsms(yima.getnum()))
