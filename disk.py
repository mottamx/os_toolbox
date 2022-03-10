#!/usr/bin/env python3
import shutil
import psutil

def check_disk_usage(disk):
	du = shutil.disk_usage(disk) #'/'
	free = du.free/du.total*100
	#print("Espacio libre {}".format(du.free/du.total*100))
	return free >20
	
def check_cpu_usage():
	usage = psutil.cpu_percent(0.5) 
	'''Regresa la carga de trabajo del procesador durante 0.5segs'''
	return usage < 75
	
if not check_cpu_usage() or not check_disk_usage("/"):
	print("ERROR!")
else:
	print("Everything is ok")
