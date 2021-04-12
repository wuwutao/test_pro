import yaml

#文件读取
items=[]

for line in goods_items:
    items.append(line.text)
print(line)

#更改yaml数据
class Test_yaml():
    def __init__(self,read_files):
        self.read_files = read_files

    def open_yaml(self):
        #打开
        with open(self.read_files,'r',encoding='utf-8') as f:
            #反序列化为字典
            data=yaml.load(f,Loader=yaml.FullLoader)      
        # print(data)
        return data
        
if __name__=='__main__':
    #封装读取数据的方法     #yaml文件路径
    Test_yaml('items_yaml.yaml').open_yaml()

#对象化:看有多少个界面 ：首页，登录页，搜索页，商品页，商品详情页，购物车页面，每个界面定义一个类  
#函数化：界面需要跳转，使用return 返回值
#元素属性化：封装元素，便于查找和修改，减少重复代码，增加代码的健壮性


