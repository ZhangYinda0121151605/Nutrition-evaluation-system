#coding=utf-8

from aip import AipOcr
import re
from flask import Flask, render_template, request 

APP_ID = '14358252'
API_KEY = 'wW74XknvLtD3sXpxDYyE60HM'
SECRET_KEY = 'DUA8G4ekCbGiLrrTlNFY2v1wyqiEji9O'

nutrilist = ['energy', 'protein', 'fat', 'tfat', 'sugar', 'vita', 'vitc', 'vitd', 'vite', 'vitb1', 'cal', 'pho', 'pot', 'sod', 'mag', 'iro', 'zin']
nutrilistcn = ['能量', '蛋白质', '脂肪', '反式脂肪酸', '碳水化合物', '维生素A', '维生素C', '维生素D', '维生素E', '维生素B1', '钙', '磷', '钾', \
               '钠', '镁', '铁', '锌']
nutristd = [1000, 30, 50, 0, 300, 500, 40, 10, 3, 0.2, 0.4, 0.1, 0.4, 300, 150, 500, 200, 30, 0.3, 1.5]
        
nutridata = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
stdnutridata = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# Default setting:
# 年龄性别体重让用户输入
AGE = 20
GEND = 0
WEIGHT = 500
FILEPATH = 'img/2.jpg'
    
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
        

def cmp_nutrition(f):
    for index in range(len(nutrilist)):
        if nutridata[index]!=-1:
            disppercent = float(nutridata[index]-stdnutridata[index])/float(stdnutridata[index]+0.001)
            if disppercent>0.4:
                f.write('<center><h3>'+'请额外摄入'+str(nutrilistcn[index])+'高的食物！'+'</h3></center>'+'\n')
            elif disppercent<-0.4:
                f.write('<center><h3>'+'请减少'+str(nutrilistcn[index])+'的摄入'+'</h3></center>'+'\n')
            else:
                f.write('<center><h3>'+str(nutrilistcn[index])+'含量适中'+'</h3></center>'+'\n')
            #print(nutridata[index])
    return

def write_html():
	f = open("templates/result.html","w",encoding="utf-8")
	message1 = """
	<!DOCTYPE html>
	<html lang="en">
	<head>
	<meta charset="UTF-8">
	<title> Result </title>
	</head>
	<body>
	"""
	f.write(message1)
	cmp_nutrition(f)
	message2 = """
	</body>
	</html>
	"""
	f.write(message2)
	f.close()



def init_and_ocr(age=AGE, gender=GEND, weight=WEIGHT, filepath=FILEPATH):

	aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

	result = aipOcr.basicGeneral(get_file_content(filepath))
	resultstr = str(result)

	read_nutrition(resultstr,weight)
	#stdtable = read_nutrition(resultstr,WEIGHT)
	init_standard_table(age, gender)


def show_result():
	app = Flask(__name__)

	@app.route('/')
	def hello_world():
		return 'Hello fucking world!'

	@app.route('/input')
	def index():
		return render_template('input.html')

	@app.route('/Evaluation', methods = ['GET','POST'])
	def success():
		if request.method == 'POST':
			age = request.form['age']
			gender = request.form['gender']
			if gender == "男":
				gend = 0
			elif gender == "女":
				gend = 1
			else:
				pass
			weight = request.form['weight']
			filepath = request.form['filepath']
			init_and_ocr(int(age), int(gend), int(weight), filepath)
			write_html()
			return render_template('result.html')
			#return render_template('result.html', age = age, gender = gend, weight = weight, filepath = filepath)
		else:
			pass
	app.run()
	return


if __name__ == "__main__":
	show_result()
'''
	aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

	result = aipOcr.basicGeneral(get_file_content(FILEPATH))
	resultstr = str(result)

	read_nutrition(resultstr,WEIGHT)
	#stdtable = read_nutrition(resultstr,WEIGHT)
	init_standard_table(AGE, GENDER)
	
	write_html()
'''
	
