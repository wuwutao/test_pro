#使用page object：减少重复代码量，分离元素

#3.目标元素属性化：3.0：将重复代码分离,重复代码函数封装
#首页

#代码逻辑：
import time
import yaml

#定义一个基类，存储公共的方法
class BasePage():

    def __init__(self,driver):
        self.driver = driver

        #遍历所有需要的数据，在初始化时，后面的内容中就不用添加
        eles=yaml.load(open('test_yaml.yaml','rb').read(),Loader=yaml.FullLoader)[self.__class__.__name__]
        #动态复制，循环遍历所有的值
        for ele in eles:
            self.__setattr__(ele,eles[ele])

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

