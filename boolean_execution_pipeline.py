import time

def run_pipeline(p, sleep_time):
	print(p)
	for f in p:
		print(f)
		if f():
			print('true')
			time.sleep(sleep_time)
		else:
			raise RuntimeError
	return True

class BooleanExecutionPipeline:

	def __init__(self, func_list, except_list=[], sleep_time=0):
		self.func_list = func_list
		self.except_list = except_list
		self.sleep_time = sleep_time


	def execute(self):
		try:
			return run_pipeline(self.func_list, self.sleep_time)
		except RuntimeError:
			return run_pipeline(self.except_list, self.sleep_time)
