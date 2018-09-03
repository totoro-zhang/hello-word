#-*- coding:utf-8 -*-
#file:pyqueue.py
#

import unittest
import HTMLTestRunner,xmlrunner


class PyQueue:
	def __init__(self,size=20):	#create queue
		self.queue = []
		self.size = size
		self.end = -1
	def setSize(self,size):
		self.size = size
	def In(self,element):
		if self.end < self.size -1:
			self.queue.append(element)
			self.end = self.end+1
		else:
			raise QueueException('PyQueueFull')
	def Out(self):
		if self.end != -1:
			element = self.queue[0]
			self.queue = self.queue[1:]
			self.end = self.end - 1
			return element
		else:
			raise QueueException('PyQueueEmpty')
	def End(self):
		return self.end
	def empty(self):
		self.queue = []
		self.end = -1
class QueueException(Exception):
	def __init__(self,data):
		self.data = data
	def _str_(self):
		return self.data
class MyTest(unittest.TestCase):
	def test_empty(self):
		self.queue = PyQueue()
		for i in range(10):
			self.queue.In(i)
		self.queue.empty()
		self.assertEqual(-1,self.queue.End())
	def test_In(self):
		self.queue = PyQueue()
		self.queue.In(1)
		self.assertEqual(1,self.queue.Out())
	def test_QueueException(self):
		self.queue = PyQueue()
		for i in range(20):
			self.queue.In(i)
		self.assertRaises(QueueException,self.queue.In,21)
if __name__ == '__main__':
	'''	
	queue = PyQueue()
	for i in range(10):
		queue.In(i)
	print(queue.End())
	for i in range(10):
		print(queue.Out())
	print(queue.End())
	for i in range(20):
		queue.In(i)
	queue.empty()
	for i in range(20):
		print(queue.Out())
	'''
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(MyTest))
	runner = xmlrunner.XMLTestRunner(output = '.')
	runner.run(suite)

