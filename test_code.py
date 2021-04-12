#使用page object：减少重复代码量，分离元素

#3.目标元素属性化:代码1.0
class IndexPage():
    def __init__(self,driver):

        self.driver = driver
        driver.get("https://www.mi.com/")
        self.driver.maximize_window()
        #元素属性化     #初始化找到yaml进行数据转化
        #1.eles=yaml.load(open("test_yaml.yaml").read(),Loader=yaml.FullLoader,'IndexPage')
        #2.self.__class__.__name__:取当前类的名字   
        eles=yaml.load(open("test_yaml.yaml").read(),Loader=yaml.FullLoader,self.__class__.__name__)
        self.login_list=eles['login_list']
        self.use_control=eles['use_control']
        self.search_goods=eles['search_goods']

    #定义方法，点击首页进入登录页
    def to_login(self):

        #点击登录页，还没跳转到登录页，首页完成的操作
        self.driver.find_element(*self.login_list).click()
        # driver.find_element_by_xpath("/html/body/div/div[1]/div/div[2]/div[1]/div[3]/a[1]").click()
        
        #处理用户协议
        self.driver.find_element(*self.use_control).click()
        time.sleep(2)

        #返回登录页的一个对象给登录页LoginPage
        #涉及到页面跳转，就返回一个对象，看你需要返回到哪个
        return LoginPage(self.driver)

    #搜索页面也是在首页中一起进行的，可以直接放在登录上一起执行操作
    def search_items(self,items="耳机"):

        self.driver.find_element(*search_goods).send_keys(items+'\n')
        #点击完，到商品详情页面  返回对象
        return GooditemsPage(self.driver)
        #因为一点击就跳转到商品详情页了,不是登录页中的功能
        #driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[2]/div[1]/a/img").click()

#登录页
class LoginPage():
    def __init__(self,driver):

        self.driver = driver
        eles=yaml.load(open("test_yaml.yaml").read(),Loader=yaml.FullLoader,'LoginPage')
        self.user=eles['user']
        self.pwd=eles['pwd']
        self.login_clicks=eles['login_clicks']


    def login(self,username,password):
        #输入账号密码
        self.driver.find_element(*user).click()
        self.driver.find_element(*user).send_keys(username)

        self.driver.find_element(*pwd).click()
        self.driver.find_element(*pwd).send_keys(password)

        #点击登录按钮
        self.driver.find_element(*login_clicks).click()

        #返回首页对象
        #涉及到页面跳转，就返回一个对象，看你需要返回到哪个
        #不加的话，需要拿着这个对象进行操作更麻烦
        return IndexPage(self.driver)   
#商品页
class GooditemsPage():
    def __init__(self,driver):
        self.driver = driver
        eles=yaml.load(open('test_yaml.yaml').read(),Loader=yaml.FullLoader,'GooditemsPage')
        item_search=eles['item_search']
    #查找耳机
    def goods_items(self):
        #点击商品查找
        time.sleep(2)
        self.driver.find_element(*item_search).click()

        #判断页面是否跳转
        for handle in self.driver.window_handles:
            self.driver.switch_to_window(handle)
            #判断标题，判断当前窗口是否相等
            if "小米真无线" in self.driver.title :
                #已经切换页面
                return ItemPage(self.driver)          

#点击后，商品详情页
class ItemPage():
    def __init__(self,driver):

        self.driver = driver
        eles=yaml.load(open('test_yaml.yaml').read(),Loader=yaml.FullLoader,'ItemPage')
        click_car=eles['click_car']

    def pick_shop_car(self):

        time.sleep(2)
        # self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[1]/div[2]/div[7]/div[1]/a").click()
        
        self.driver.find_element(*click_car).click()
        return ShopCarPage(self.driver)
        #判断是否发生页面跳转
        # for handle in driver.window_handles:
        #     self.driver.switch_to_window(handle)

        #     if "成功加入购物车" in self.driver.title :
        #         return ShopCarPage(self.driver)

#购物车页面
class ShopCarPage():
    def __init__(self,driver):
        self.driver = driver

    #设置断言，检查信息
    def check_message(self):
        time.sleep(1)
        res = self.driver.find_element_by_class_name("goods-info").text
        #断言
        assert "小米真无线" in res

if __name__=='__main__':
    #页面的初始化
    from selenium import webdriver
    import time
    from selenium.webdriver.common.by import By
    #获取浏览器驱动
    driver = webdriver.Chrome()
    #设置隐式等到时间
    driver.implicitly_wait(10)
    #获取地址
    driver.get("https://www.mi.com/")

    #定位到登录页---登录---首页---搜索商品--搜索页面---选择商品---商品详情页---添加购物车---购物车---检查

    # indexPage=IndexPage(driver)

    # loginPage =indexPage.to_login()
    # #输入登录账号密码
    # indexPage = loginPage.login("15960262793","wwt2328..")
    # #调用搜索商品
    # gooditemsPage =indexPage.search_items()
    # #商品查找 
    # good_items =gooditemsPage.goods_items()
    # #加入购物车
    # itemPage=good_items.pick_shop_car()
    # #检验
    # itemPage.check_message()

    ##定位到登录页---登录---首页---搜索商品--搜索页面---选择商品---商品详情页---添加购物车---购物车---检查
    #可以直接协程一整段代码
    indexPage=IndexPage(driver)
    indexPage.to_login().login("15960262793","wwt2328..").search_items().goods_items().pick_shop_car().check_message()