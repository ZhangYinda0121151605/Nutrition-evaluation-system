#coding=utf-8

from aip import AipOcr
import re
APP_ID = '14358252'
API_KEY = 'wW74XknvLtD3sXpxDYyE60HM'
SECRET_KEY = 'DUA8G4ekCbGiLrrTlNFY2v1wyqiEji9O'

nutrilist = ['energy', 'protein', 'fat', 'tfat', 'sugar', 'vita', 'vitc', 'vitd', 'vite', 'vitb1', 'cal', 'pho', 'pot', 'sod', 'mag', 'iro', 'zin']
nutrilistcn = ['能量', '蛋白质', '脂肪', '反式脂肪酸', '碳水化合物', '维生素A', '维生素C', '维生素D', '维生素E', '维生素B1', '钙', '磷', '钾', \
               '钠', '镁', '铁', '锌']
nutristd = [1000, 30, 50, 0, 300, 500, 40, 10, 3, 0.2, 0.4, 0.1, 0.4, 300, 150, 500, 200, 30, 0.3, 1.5]
        
nutridata = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
stdnutridata = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def read_nutrition(inputstr, weight):

    for index in range(len(nutrilist)):
        nutrishow = re.findall(nutrilistcn[index]+'\d+',inputstr) #匹配字符串
        if len(nutrishow):
            nutrishow[0] = nutrishow[0].strip(nutrilistcn[index]) #删除文字，保留数字部分
            nutridata[index] = weight*((int(nutrishow[0])))/100
    return

#乘10修正是因为识别不出来小数点，因此食品营养表上小数点后一位的标准也乘10
def init_standard_table(age, gender):

    stdnutridata[0] = 3200-25*(abs(age-40))-50*gender
    stdnutridata[1] = (80-1.5*(abs(age-40))-5*gender)*10
    stdnutridata[2] = (60-0.6*(abs(age-40))-2*gender)*10
    stdnutridata[3] = 0.0001
    stdnutridata[4] = (400-5*(abs(age-40)))*10
    stdnutridata[5] = 800-7*(abs(age-40))-50*gender
    stdnutridata[6] = 110-2*(abs(age-40))
    stdnutridata[7] = (5+0.1*(abs(age-40)))*10
    stdnutridata[8] = 14-0.1*(abs(age-40))
    stdnutridata[9] = (1.4-0.03*(abs(age-40)))*10
    stdnutridata[10] = 1000-10*(abs(age-60))
    stdnutridata[11] = 1000-12*(abs(age-60))
    stdnutridata[12] = 2000-20*(abs(age-60))
    stdnutridata[13] = 2000-20*(abs(age-60))
    stdnutridata[14] = 350-5*(abs(age-40))
    stdnutridata[15] = (max(20-0.2*(abs(age-20)),10))*10
    stdnutridata[16] = 12-0.1*(abs(age-40))
    
    return
        

def cmp_nutrition():
    for index in range(len(nutrilist)):
        if nutridata[index]!=-1:
            disppercent = float(nutridata[index]-stdnutridata[index])/float(stdnutridata[index]+0.001)
            if disppercent>0.4:
                print('请额外摄入'+nutrilistcn[index]+'高的食物！')
            elif disppercent<-0.4:
                print('请减少'+nutrilistcn[index]+'的摄入')
            else:
                print(nutrilistcn[index]+'含量适中')
            #print(nutridata[index])
    return

#年龄性别体重让用户输入
age = 20
gender = 0
weight = 500

aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

result = aipOcr.basicGeneral(get_file_content('6.jpg'))
resultstr = str(result)

read_nutrition(resultstr,weight)
#stdtable = read_nutrition(resultstr,weight)
init_standard_table(age, gender)
cmp_nutrition()


