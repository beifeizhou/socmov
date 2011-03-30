""" Dataset used from http://archive.ics.uci.edu/ml/datasets/Adult """
"""
age: continuous.
workclass: string
fnlwgt: continuous.
education: string
education-num: continuous.
marital-status: string
occupation: string
relationship: string
race: string
sex: string
capital-gain: continuous.
capital-loss: continuous.
hours-per-week: continuous.
native-country: string
"""

import mvpa
from mvpa.datasets import *
from mvpa.clfs.svm import *
import random
from attr import *
import csv
def fabs(v):
	if v < 0:
		return -v
	return v
def targ_fun(x):
	if x.find("<=") == -1 :
		return 1
	return -1

type = [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, -1]
c = 0
attribs = []
for x in type:
	if x==0:
		attribs.append( cont_attribute(0,100) )
	elif x==1:
		attribs.append( abstract_attribute() )
	else:
		attribs.append( abstract_attribute() )

print "analysing attributes... "
dataf = csv.reader( open('adult/adult.data', 'rb') )
for line in dataf:
		if len(line) == 15:
			for i in xrange(len(line)):
				if type[i] == 0 or type[i] == 1:
					attribs[i].add_val( line[i] )
				else:
					attribs[i].add_val( line[i] )
print "complete"
samps = []
res = []
print "generating vectors... "
dataf = csv.reader( open('adult/adult.data', 'rb') )
for line in dataf:
	if len(line) == 15:
		sampvec = []
		resv = 0
		for i in xrange(len(line)):
			if type[i] == 0 or type[i] == 1:
					sampvec += attribs[i].get_vector( line[i] )
			else:
				resv = targ_fun( line[i] )
		samps.append( sampvec )
		res.append( resv )
		if len(samps) >= 2512:
			break

for i in xrange(len(attribs)):
	attribs[i].frozen = True
"""
for i in xrange(len(type)):
	if type[i] == 1:
		print attribs[i].attr_list
		print "########################################################"
		for x in range(0,5):
			print ""
"""

print "complete"
print "training SVM..."
ds = dataset_wizard( samples=samps, targets=res )
rsvm = RbfCSVMC(probability=1) #can also be like RbfCSVMC
rsvm.train(ds)
print "complete..."
print "reading test samples..."
dataf = csv.reader( open('adult/adult.test', 'rb') )

testsamps = []
testres = []
for line in dataf:
	if len(line) == 15:
		sampvec = []
		resv = 0
		for i in xrange(len(line)):
			if type[i] == 0 or type[i] == 1:
					sampvec += attribs[i].get_vector( line[i] )
			else:
				resv = targ_fun( line[i] )
		testsamps.append( sampvec )
		testres.append( resv )
		#if len(testres) >= 180:
		#	break

print "done"
print "predicting"
svmres = rsvm.predict( testsamps )

for i in xrange(len(svmres)):
	if svmres[i] < 0:
		svmres[i] = 'T'
	else:
		svmres[i] = 'F'
		
for i in xrange(len(testres)):
	if testres[i] < 0:
		testres[i] = 'T'
	else:
		testres[i] = 'F'

#print ''.join(testres)
#print ''.join(svmres)

y, n = 0, 0
fpos, fneg = 0, 0
fpos2, fneg2 = 0, 0
for i in xrange(len(testres)):
	if svmres[i] == 'T':
			fpos+=1
	else:
		fneg+=1
	if testres[i] == 'T':
		fpos2 += 1
	else:
		fneg2 += 1
	if testres[i] == svmres[i]:
		y += 1
	else:
		n += 1

print "error rate is ", n / (y + n*1.0) * 100.
#print n1 / (y1 + n1*1.0) * 100.
#print n2 / (y2 + n2*1.0) * 100.
print fpos, fneg
print fpos2, fneg2
