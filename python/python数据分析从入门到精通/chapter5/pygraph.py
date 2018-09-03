#-*- coding:utf-8 -*-
#file:pygraph.py
#

def searchGraph(graph,start,end):
	results = []
	generatePath(graph,[start],end,results)
	results.sort(key=lambda x:len(x) )
	return results
def generatePath(graph,path,end,results):
	state = path[-1]
	if state == end:
		results.append(path)
	else:
		for arc in graph[state]:
			if arc not in path:
				generatePath(graph,path+[arc],end,results)

if __name__ == '__main__':
	graph = {'A':['B','C','D'],
		'B':['E'],
		'C':['D','F'],
		'D':['B','E','G'],
		'E':[],
		'F':['D','G'],
		'G':['E']}

	r = searchGraph(graph,'A','D')
	print('*****************************************')
	print('      path A to  D         ')
	print('******************************************')
	for i in r:
		print(i)
	r = searchGraph(graph,'A','E')
	print('*****************************************')
	print('      path A to E          ')
	print('******************************************')
	for i in r:
		print(i)
	r = searchGraph(graph,'C','E')
	print('*****************************************')
	print('      path C to E          ')
	print('******************************************')
	for i in r:
		print(i)
