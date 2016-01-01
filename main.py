import operator
from kivy.app import App
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class Calc(BoxLayout):
	current_num = StringProperty('0')
	current_operator = StringProperty(None, allownone=True)
	last_pressed = StringProperty(None, allownone=True)
	previous = StringProperty(None, allownone=True)
	operator_dict = DictProperty({'+': operator.add,
								  '-': operator.sub,
								  '*': operator.mul,
								  '/': operator.truediv,
								  '=': None})
	def backspace_callback(self):
		if self.last_pressed == '=':
			# Makes the calculator behave more logically
			self.current_num = '0'
			return
		if self.last_pressed in self.operator_dict.keys():
			return
		if len(self.current_num) == 1:
			self.current_num = '0'
		else:
			self.current_num = self.current_num[:-1]

	def clear_callback(self):
		self.current_num = '0'
		if self.last_pressed == 'c':
			self.current_operator = None
			self.last_pressed = None
			self.previous = None
		self.last_pressed = 'c'


	def equals_callback(self):
		if self.previous != None and self.last_pressed != '=':
			self.current_num = str(self.evaluate())
			self.previous = None
			self.current_operator = None
			if self.current_num[-2:] == '.0':
				self.current_num = self.current_num[:-2]
		self.last_pressed = '='
		
	def error_callback(self, message):
		self.previous = None
		self.last_pressed = 'err'
		self.current_num = message
		
	def evaluate(self):
		if self.last_pressed == '.':
			self.current_num = self.current_num[:-1]

		prev = float(self.previous)
		curr = float(self.current_num)
		return str(self.operator_dict[self.current_operator](prev, curr))


	def operand_callback(self,input_number):
		if float(self.current_num) == 0 or self.last_pressed in self.operator_dict.keys():
			self.current_num = input_number
		else:
			self.current_num += input_number
		self.last_pressed = input_number


	def operator_callback(self,operator_type):
		try:
			if self.last_pressed == 'err':
				return
			if self.last_pressed == '.':
				self.current_num = self.current_num[:-1]

			if self.previous == None:
				self.previous = self.current_num
			elif self.last_pressed in self.operator_dict.keys():
				pass
			else:
				self.current_num = self.evaluate()
				self.previous = self.current_num

			self.last_pressed = operator_type
			self.current_operator = operator_type
		except Exception:
			return self.error_callback(message='Divide by 0 error')
		

	def sign_change_callback(self):
		if float(self.current_num) == 0 or self.last_pressed == 'err':
			return
		if self.current_num[0] == '-':
			self.current_num = self.current_num[1:]

			if self.last_pressed in self.operator_dict.keys():
				self.previous = self.previous[1:]

		else:
			self.current_num = '-' + self.current_num
			print('else')
			if self.last_pressed in self.operator_dict.keys() and \
											self.previous != None:
				self.previous = '-' + self.previous
				
	def sqrt_callback(self):
		if self.current_num[0] == '-':
			return self.error_callback(message='SQRT of negative')
		if self.last_pressed in self.operator_dict and \
							self.last_pressed != '=':
			return
		self.current_num = str(float(self.current_num)**0.5)
		self.last_pressed = 'sqrt'
		
	def quit_callback(self):
		CalculatorApp.get_running_app().stop()


class CalculatorApp(App):
	def build(self):
		return Calc()

if __name__ == '__main__':
	CalculatorApp().run()
