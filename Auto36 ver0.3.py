# coding=utf-8 ##
#!/user/bin/env python

import os
import os.path
import bisect
from bisect import bisect_left, bisect_right

class point(object):
	def __init__(self, n):
		self.n = n
	x = []
	y = []
	r = []
	def push(self, values):
		i = 0
		j = 0
		p=1
		self.x = []
		self.y = []
		self.r = []
		for value in values:
			if i == 0:
				if p > 1:
					if self.x[-1]*value < 0:
						j += 1
				else:
					p += 1
				self.x.append(value)
				i = 1
			elif i == 1:
				self.y.append(j)
				i = 2
			else:
				self.r.append(value)
				i = 0
				self.n +=1
		return
		#压入值，使之正确按xyr的顺序依次压入，其中y以j参的形式
	def callfrom_y(self, j, ioset):
		i = 0
		imax = len(self.x)
		x_return = []
		r_return = []
		while i < imax:
			#print(self.y[i])
			if self.y[i]  == j:
				x_return.append(self.x[i])
				r_return.append(self.r[i])
			i += 1
		if ioset == 0:
			return x_return
		else:
			return r_return
		#输入j（y）的值返回此时的xlist和rlist,输入ioset==0时输出x_return,其余输出r_return

def fdefine():
	f_path = input("Plz Input the path of the files(.plt) u want to load(full,only fold): \n")
	files = os.listdir(f_path)
	print(files, "\nPlz ensure the files.")
	file_path = []
	for file in files:
		file_path.append("%s/%s" % (f_path, file))
	return file_path
#读取输入流给出的源目录，返回将要读的文件

def fread(n):
	 f = open(n)
	 lines = f.readlines()[3::3]
	 f.close()
	 L = []
	 dataset = []
	 for line in lines:
		 L.append(line.split())
	 for l1 in L:
		 for l2 in l1:
			 dataset.append(float(l2))
	 return dataset
#输入将要打开的文件路径，返回文件中所被需要的数据

def find(arr, i):
	n = 1
	la = len(arr)
	r_found = []
	while n <= la-1:
		if (arr[n-1]-i)*(arr[n]-i) < 0:
			r_found.append(n-1)
		n += 1
	return r_found
#输入arr=要检索的R的列表，以及i=希望找出的R的值

def probe(xlist, rlist, r_f_list, ixx=0):
	x_sum = 0
	x_list = []
	for ri in r_f_list:
		#if xlist[ri]*xlist[ri+1] > 0:
			#print(xlist[ri],xlist[ri+1],rlist[ri],rlist[ri])
			a = (2.1-rlist[ri])/(rlist[ri+1]-rlist[ri])
			x_cut = xlist[ri]+a*(xlist[ri+1]-xlist[ri])
			x_list.append(x_cut)
	for x_val in x_list:
		x_sum += x_val
	if ixx == 0:
#		print(x_sum/len(x_list),"sss")
#		return x_sum/len(x_list)
#		print(x_list)
		return x_list[0]
	else:
#		print(x_list,"ss")
		return x_list
#输入xlist=要检索的X列表，rlist=要检索的R列表，r_f_list=find函数找出的R的序数列表，ixx用于测试
#返回经线性插值得到的值
		
def mmain():
	ProbedData1 = []
	ProbedData2 = []
	ProbedDataTMP = []
	#PathForLoad = fdefine()
	f_path = input("请输入要处理的文件夹(如X:/Data/In_Out)，不输入即为当前目录: \n")
	if len(f_path) == 0:
		f_path = os.path.abspath('.')
	files = os.listdir(f_path)
	file_path = []
	for file in files:
		if ".plt" in file:
			file_path.append("%s/%s" % (f_path, file))
	print(file_path, "\n请确认要处理的文件.")
	logf = 0
	R_Data_To_Find = input("\n请输入等值线值:")
	R_Data_To_Find = float(R_Data_To_Find)
	jcell = input("请输入j参数（输入小于0的数以结束程序）：")
	jcell = int(jcell)
	Mode = input("请选择模式，0以线性模式，1以经典模式")
	while (jcell >= 0) :
		logfile = ("%s/OutPut_jecll=%s_%s.txt" % (f_path, jcell, str(R_Data_To_Find)))
		with open(logfile, 'w') as f:
			for Files in file_path:
				print("\n正在处理：", Files)
				ObPoint = point(0)
				DataSet = fread(Files)
				ObPoint.push(DataSet)
				if Mode == 1:
					X_List = ObPoint.callfrom_y(jcell,0)
					R_List = ObPoint.callfrom_y(jcell,1)
					PointNo = find(R_List, R_Data_To_Find)
					if len(PointNo) == 0:
						f.write("无法找到可行值于%s\n" % (Files))
						print("无法找到可行值于", Files,"\n")
					else :
						s = "%s\n" % str(probe(X_List, R_List, PointNo))
						f.write(s)
						print(s)
				else :
					X_List_min = ObPoint.callfrom_y(0,0)
					R_List_min = ObPoint.callfrom_y(0,1)
					X_List_max = ObPoint.callfrom_y(32,0)
					R_List_max = ObPoint.callfrom_y(32,1)
					PointNo_min = find(R_List_min, R_Data_To_Find)
					PointNo_max = find(R_List_max, R_Data_To_Find)
					s = "%s\n" % str(-(probe(X_List_max, R_List_max, PointNo_max)-probe(X_List_min, R_List_min, PointNo_min)))
					f.write(s)
					print(s)
		logf += 1
		jcell = input("请输入j参数（输入小于0的数以结束程序）：")
		jcell = int(jcell)

mmain()
input("按任意键退出程序...")
#x0 = []
#x2 = []
#x1 = point(0)
#x2 = fdefine()
#x3 = fread("f:/t/00000.plt")
#x1.push(x3)
#x_to = x1.callfrom_y(1, 0)
#r_to = x1.callfrom_y(1, 1)
#for xx in x_to:
#	print(xx)

#x4 = find(x1.r, 2.1)
#x0 = probe(x1, x4, 1)
#for x44 in x4:
#	print(x1.x[x44], x1.x[x44+1], x1.r[x44], x1.r[x44+1])
#for x00 in x0:
#	 print x00
#x_r = pprobe(x_to, r_to, 2.1)
#print(x_r)
#mmain()
