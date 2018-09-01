#-*- coding:utf-8 -*-
#file:pystack.py
#

import unittest
import HTMLTestRunner,xmlrunner


class PyStack:
	def __init__(self,size=30):
		self.stack = []
		self.size=size
		self.top = -1
	def setSize(self,size):
		self.size = size
	def push(self,element):
		if self.isFull():
			raise StackException('PyStackOverflow')
		else:
			self.stack.append(element)
			self.top = self.top + 1
	def pop(self):
		if self.isEmpty():
			raise StackException('PyStackUnderflow')
		else:
			element = self.stack[-1]
			self.top = self.top -1
			del self.stack[-1]
			return element
	def Top(self):
		return self.top
	def empty(self):
		self.stack = []
		self.top = -1
	def isEmpty(self):
		if self.top == -1:
			return True
		else:
			return False
	def isFull(self):
		if self.top == self.size -1:
			return True
		else:
			return False
class StackException(Exception):
	def __init__(self,data):
		self.data = data
	def __str__(self):
		return self.data
class MyTest(unittest.TestCase):
	def test_isEmpty(self):
		self.stack = PyStack()
		self.assertEqual(True,self.stack.isEmpty())
	def test_isFull(self):
		self.stack = PyStack()
		for i in range(30):
			self.stack.push(i)
		self.assertEqual(True,self.stack.isFull())
	def test_pop(self):
		self.stack =PyStack()
		for i in range(10):
			self.stack.push(i)
		self.assertEqual(9,self.stack.pop())

		self.assertEqual(8,self.stack.pop())

	def test_raise(self):
		self.stack = PyStack()
		for i in range(30):
			self.stack.push(i)
		self.assertRaises(StackException,self.stack.push,31)
	def test_raiseoverflow(self):
		self.stack = PyStack()
		self.assertRaises(StackException,self.stack.pop)

if __name__ == '__main__':
	"""
	stack = PyStack()
	for i in range(10):
		stack.push(i)
	print(stack.Top())
	for i in range(10):
		print(stack.pop())
	stack.empty()
	for i in range(31):
		stack.push(i)
	"""
	suite = unittest.TestSuite()#定义一个测试套件
	suite.addTest(unittest.makeSuite(MyTest))#往测试套件里添加这个类下的所有测试用例
	runner=xmlrunner.XMLTestRunner(output='.')
	runner.run(suite)

