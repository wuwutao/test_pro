#使用page object：减少重复代码量，分离元素

#3.目标元素属性化：2.0：将重复代码分离
#首页


#定义一个基类，存储公共的方法
class BasePage():

    def __init__(self,driver):
        self.driver = driver

    #点击跳转到登录
    def click(self,*Locate):
        self.driver.find_element(*Locate).click()

    #用户确定协议点击
    def user_exsit(self,*Locate):

        self.driver.find_element(*Locate).click()
        time.sleep(2)
    #用户输入文本，点击操作
    def inputs_text(self,test,*Locate):
        self.driver.find_element(*Locate).send_keys(test)


    def switch_to(self,switch_title):
        #判断页面是否跳转
        for handle in self.driver.window_handles:

            self.driver.switch_to_window(handle)
            #判断标题，判断当前窗口是否相等
            if "小米真无线" in self.driver.title :
                #已经切换页面
                return True      

class IndexPage(BasePage):
    def __init__(self,driver):
        BasePage.__init__(self,driver)
        driver.get("https://www.mi.com/")
        self.driver.maximize_window()
        #元素属性化     #初始化找到yaml进行数据转化
        #1.eles=yaml.load(open("test_yaml.yaml").read(),Loader=yaml.FullLoader,'IndexPage')
        #2.self.__class__.__name__:取当前类的名字   

        #可以全部封装：
        #因为数据可以直接通过yaml就可以找到
        eles=yaml.load(open('test_yaml.yaml').read(),Loader=yaml.FullLoader)[self.__class__.__name__]
        self.login_list=eles['login_list']
        self.use_control=eles['use_control']
        self.search_goods=eles['search_goods']

    #定义方法，点击首页进入登录页
    def to_login(self):

        self.click(*self.login_list)
        self.user_exsit(*self.use_control)
        return LoginPage(self.driver)

    def search_items(self,items="耳机"):
        #点击输入查询    
        self.inputs_text(test+'\n',*self.search_goods)
        # self.driver.find_element(*search_goods).send_keys(items+'\n')
        #点击完，到商品详情页面  返回对象
        return GooditemsPage(self.driver)

#登录页
class LoginPage(BasePage):
    def __init__(self,driver):
        BasePage.__init__(self,driver)    
        eles=yaml.load(open('test_yaml.yaml').read(),Loader=yaml.FullLoader)[self.__class__.__name__]
        self.user=eles['user']
        self.pwd=eles['pwd']
        self.login_clicks=eles['login_clicks']

    def login(self,username,password):
        #输入密码
        self.inputs_text(username,*self.search_goods)

        #输入密码
        self.inputs_text(password,*self.search_goods)
        #点击登录按钮
        self.click(*self.login_clicks)

        return IndexPage(self.driver)   
#商品页
class GooditemsPage(BasePage):
    def __init__(self,driver):
        BasePage.__init__(self,driver)
        eles=yaml.load(open('test_yaml.yaml').read(),Loader=yaml.FullLoader)[self.__class__.__name__]
        item_search=eles['item_search']
    #查找耳机
    def goods_items(self):
        #点击商品查找
        time.sleep(2)    
        #点击耳机查找
        self.click(*self.item_search)
    
        if self.switch_to("小米真无线"):
            return  ItemPage(self.driver)  

#点击后，商品详情页
class ItemPage(BasePage):
    def __init__(self,driver):
        BasePage.__init__(self,driver)
        #初始化，拿到需要的数据
        eles=yaml.load(open('test_yaml.yaml').read(),Loader=yaml.FullLoader)[self.__class__.__name__]
        click_car=eles['click_car']

    def pick_shop_car(self):
        #点击加入购物车
        time.sleep(2)
        self.click(*self.click_car)
        return ShopCarPage(self.driver)

#购物车页面
class ShopCarPage(BasePage):
    def __init__(self,driver):
        BasePage.__init__(self,driver)

    #设置断言，检查信息
    def check_message(self):
        time.sleep(1)   
        res = self.driver.find_element_by_class_name("goods-info").text
        #断言
        assert "小米真无线" in res

if __name__=='__main__':
    #页面的初始化
    import yaml
    from selenium import webdriver
    import time
    from selenium.webdriver.common.by import By
    #获取浏览器驱动
    driver = webdriver.Chrome()
    #设置隐式等到时间
    driver.implicitly_wait(10)
    #获取地址
    driver.get("https://www.mi.com/")

    ##定位到登录页---登录---首页---搜索商品--搜索页面---选择商品---商品详情页---添加购物车---购物车---检查
    #可以直接协程一整段代码
    IndexPage(driver).to_login().login("15960262793","wwt2328..").search_items().goods_items().pick_shop_car().check_message()