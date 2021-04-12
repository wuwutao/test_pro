
#解析yaml文件 low 版
import yaml
#修改yaml进行反序列化

# class Test_yaml():

#     #初始化一个变量用来接收yaml数据,需要传一个文件给这个变量
#     def __init__(self,reads_file):
#         self.reads_file = reads_file

#     def test_read(self):
#         with open(self.reads_file,'r',encoding='gbk') as f:
#             data = yaml.load(f,Loader=yaml.FullLoader)    
#         return data
#         print(data)
# if __name__=='__main__':

#     Test_yaml("test_yaml.yaml").test_read()
#     print(Test_yaml("test_yaml.yaml").test_read())


#pro 版，升级解析yaml 数据,就只需要一行代码
# eles=yaml.load(open("test_yaml.yaml").read(),Loader=yaml.FullLoader)
# print(eles)

if __name__=='__main__':
    eles=yaml.load(open("test_yaml.yaml").read(),Loader=yaml.FullLoader)
    print(eles['IndexPage']['login_list'])