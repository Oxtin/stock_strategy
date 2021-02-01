import pandas as pd
import numpy as np

def per(data, eps, low, high):
	res = data[-1] / eps
	if res > low and res < high: return 1
	elif res > high: return -1
	else: return 0

def kd(data, val):
	days = 9
	k = 50; d = 50 #init
	for i in range(9, len(data)):
		nowData = data[:i]
		rsv = nowData[-1] - nowData[-days:].min()
		rsv /= nowData[-days:].max() - nowData[-days:].min()
		rsv *= 100
		k = (k*2 + rsv*1) / 3
		d = (d*2 + k*1) / 3
	if k < 20 and d < 20: return 1
	elif k > 80 and d > 80: return -1
	else: return 0

def vol(data, val):
	days = 5
	avg = data[-days:].sum() / days
	if avg > val: return 1
	elif avg < val: return -1
	else: return 0

def ma(data, sdays, ldays):
	sma = data[-sdays:].sum() / sdays
	lma = data[-ldays:].sum() / ldays
	if sma > lma: return 1
	elif lma > sma: return -1
	else: return 0

def dealer(data):
	close = np.array(data["Close"])
	volume = np.array(data["Volume"])

	res = [0, 0, 0, 0]
	name = ["moving average:", "volume index:", "KD index:", "PER index:"]

	# ma
	print(name[0])
	s = int(input("short days: "))
	l = int(input("long days: "))
	res[0] = ma(close, s, l)

	# vol
	print(name[1])
	lim = int(input("limit: "))
	res[1] = vol(volume, lim)

	#kd
	print(name[2])
	t = int(input("threshold: "))
	res[2] = kd(close, t)

	#per
	print(name[3])
	eps = float(input("EPS: "))
	lb = int(input("lower bound: "))
	hb = int(input("higher bound: "))
	res[3] = per(close, eps, lb, hb)

	print("== 建議結果 ==")
	for _ in range(4):
		print(name[_], end=" ")
		if res[_] == 1: print("buy")
		elif res[_] == -1: print("sell")
		else: print("nothing")


if __name__ == '__main__':
	path = "./data/"
	path += input("enter the file name: ")
	try:
		df = pd.read_csv(path)
		# print(df)
	except:
		print("Can not find", path)
		exit(1)

	df = df[["Date", "Close", "Volume"]]
	dealer(df)
