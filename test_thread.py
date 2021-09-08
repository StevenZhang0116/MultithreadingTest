#!/usr/bin/python
#coding=UTF-8

import threading

class t_runner:
	'''
	'''
	def __init__(self):
		'''
		'''
		self.cmds=[]
		return

	class worker(threading.Thread):
		'''
		'''
		def __init__(self,name):
			'''
			'''
			threading.Thread.__init__(self)
			self.name=name
			self.cmds=[]
			self.emsg=None	
			return

		def add_cmd(self,cmd):
			'''
			'''
			self.cmds.append(cmd)
			return

		def wlog(self,msg):
			'''
			'''
			print(f'[worker({self.name})]{msg}')
			return

		def run(self):
			'''
			'''
			self.wlog(f'[run]:cmds({len(self.cmds)}).')

			self.emsg=None
			for cmd in self.cmds:
				try:
					fobj=cmd[0]
					args=cmd[1]
					kwargs=cmd[2]
					fobj(*args,**kwargs)
				except Exception as ex:
					self.emsg=f'{ex}'
					break

			self.wlog(f'[run]:done.emsg({self.emsg})')

			return

	def wlog(self,msg):
		'''
		'''
		print(f'[t_runner]{msg}')
		return

	def add_cmd(self,*args,**kwargs):
		'''
		'''
		fobj=args[0]
		a=args[1:]
		k=kwargs

		self.cmds.append([fobj,a,k])

		return

	def run(self):
		'''
		'''
		wcnt=3
		tws=[]

		self.wlog(f'[run]:workers({wcnt}) cmds({len(self.cmds)}).')

		for index in range(wcnt):
			name=f'w{index}'
			tw=t_runner.worker(name)
			tws.append(tw)

		num=0
		for cmd in self.cmds:
			widx=num%3
			tws[widx].add_cmd(cmd)
			num+=1

		for tw in tws:
			tw.setDaemon(True)
			tw.start()

		for tw in tws:
			tw.join()

		self.wlog(f'[run]:done.')

		return

##
# testing code from here
##

class Individual:
	'''
	'''
	def __init__(self,mid):
		'''
		'''
		self.id=mid
		self.fitness=None
		return

	def __repr__(self):
		'''
		'''
		ret=f'Individual(id:{self.id},fitness:{self.fitness})'
		return ret


def main_test():
	'''
	'''

	data_train_list=['ddd']
	data_train_future_returns=['ttt']

	population=[]
	for mid in range(5):
		population.append(Individual(mid))

	tc=t_runner()

	for individual in population:
		if individual.fitness is None:
			tc.add_cmd(f_optimize,individual,
				minibatch_data_list=data_train_list, minibatch_future_returns=data_train_future_returns)

	tc.run()

	return

import time

def f_optimize(individual,minibatch_data_list=[],minibatch_future_returns=[]):
	'''
	'''
	print(f'[f_optimize]:individual({individual})')
	time.sleep(3)
	print(f'[f_optimize]:individual({individual}) done.')

	return

if __name__=='__main__':
	main_test()

