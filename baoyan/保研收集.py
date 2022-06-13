import selenium.webdriver as web
import re

class College:  #为夏令营创建一个类
    def __init__(self,wb):
        self.school=[]      #学校
        self.college=[]     #学院
        self.name=[]        #学校加学院
        #self.start_time=''
        self.final_time=[]   #报名截止时间
        self.a_start_time=[] #活动开始时间
        self.a_final_time=[] #活动结束时间
        self.surplus=[]      #活动剩余时间
        self.index=1         #当前页面位置
        self.wb=wb           #浏览器实例对象
        self.page=1          #当前页面页数
        self.status=1        #1表示当前仍然没截止 0相反

    def get_one_item(self):
        print(self.index)
        if self.index>25:#这个问题还没搞懂！
            return
        if wb.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div['+str(self.index)+']/div[2]/a/div[2]').text=='未开始':
            if self.page>30:
                self.status=0
                return

        name=self.wb.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div['+str(self.index)+']/div[1]/a').text
        self.name.append(name)
        try:
            p1 = re.compile(r'【.*?】', re.S)  # 最小匹配学校
            self.school.append(re.search(p1, name).group()[1:-1])
        except:
            try:
                p1 = re.compile(r'\[.*?\]', re.S)  # 最小匹配学校
                self.school.append(re.search(p1, name).group()[1:-1])
            except:
                self.school.append('NaN')
                print('第'+str(self.page)+'页'+'学校存在错误或空值')
        try:
            p2 = re.compile(r'—.*')            #匹配学院
            self.college.append(re.search(p2,name).group().strip('—'))
        except:
            self.college.append('NaN')
            print('第' + str(self.page) + '页' + '学院存在错误或空值')

        reg_time=self.wb.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div['+str(self.index)+']/div[1]/div[2]/div/div[1]/div[1]').text
        self.final_time.append(reg_time[16:])

        act_time=self.wb.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div['+str(self.index)+']/div[1]/div[2]/div/div[1]/div[2]').text
        self.a_start_time.append(act_time[5:15])
        self.a_final_time.append(act_time[16:])

        self.surplus.append(int(self.wb.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div['+str(self.index)+']/div[2]/div/div[2]/span[1]').text))

        self.index+=1

    def change_page(self):
        if self.page<6:
            self.wb.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[26]/div/ul/li['+str(self.page+1)+']').click()
            self.page+=1
            self.index=1

        else:
            self.wb.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[26]/div/ul/li[6]').click()
            self.page += 1
            self.index=1

    def FUN(self,page_num=500):
        for each_page in range(page_num):
            for each_index in range(25): #单页收集信息  为啥24？？
                if self.status==0:
                    break
                self.get_one_item()
            self.change_page()#翻页
            if self.status==0:
                break


wb=web.Chrome()
wb.implicitly_wait(10)
options=web.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"')
wb.get('http://pc.baoyanwang.com.cn/articles?category=%E4%BF%9D%E7%A0%94%E4%BF%A1%E6%81%AF')

###1.收集单个信息

ch=College(wb)
ch.get_one_item()
ch.FUN(50)
###2.单页循环收集
import  pandas as  pd

a=pd.DataFrame([ch.name,ch.school,ch.college,ch.final_time,ch.a_start_time,ch.a_final_time,ch.surplus])
final=pd.DataFrame(a.values.T, index=a.columns, columns=a.index)
final.columns=['夏令营名称','大学','学院','报名截止时间','活动开始时间','活动结束时间','剩余报名时间']
final.to_csv(r'D:\Documents\Desktop\夏令营.csv',encoding='utf_8_sig')

#wb.close()
###3.翻页 + 循环收集
