#!/bin/python

#VT property transfer XML loader

from pymongo import MongoClient
from lxml import etree
import glob

class VtMongoParser:
	def __init__(self):
		self.cl = MongoClient()
		self.coll = self.cl["proptrans"]["collectionname"]
		self.coll.remove()

	#def xmlToDict(self, parentDict, xmlElement):
	#	if len(xmlElement.getchildren()) > 0:
	#		if xmlElement.tag == "sellerList" or xmlElement.tag == "buyerList":
	#			parentDict[xmlElement.tag]=[]
	#			for c in xmlElement.getchildren():
	#				self.xmlToDict(parentDict[xmlElement.tag], c)
	#		else:
	#			parentDict[xmlElement.tag]={}
	#			for c in xmlElement.getchildren():
	#				self.xmlToDict(parentDict[xmlElement.tag], c)
	#	else:
	#		parentDict[xmlElement.tag]=xmlElement.text
	def xmlToDict(self, xmlElement):
		elementDict={}
		if len(xmlElement.getchildren()) > 0:
			#if xmlElement.tag == "sellerList" or xmlElement.tag == "buyerList":
			#	elementDict[xmlElement.tag]=[]
			#	for c in xmlElement.getchildren():
			#		listDict=self.xmlToDict(c)
			#		elementDict[xmlElement.tag].append(listDict)
			#else:
				elementDict[xmlElement.tag]={}
				for c in xmlElement.getchildren():
					if c.tag == "sellerList" or c.tag == "buyerList":
						elementDict[xmlElement.tag][c.tag]=[]
						for t in c.getchildren():
							listDict=self.xmlToDict(t)
							elementDict[xmlElement.tag][c.tag].append(listDict)
					else:	
						elementDict[xmlElement.tag][c.tag]=self.xmlToDict(c)
		else:
			return xmlElement.text
		return elementDict

	def loadMongo(self, filepath):
		print "Digesting XML file: "+str(filepath)
		xml=etree.parse(filepath)
		i = 0
		for event in xml.getroot().xpath("//formData"):
			i+=1
			proptransrecord = self.xmlToDict(event)
			#print "inserting record #"+str(i)
			#self.coll.insert(proptransrecord)
			self.coll.insert(proptransrecord)


parser = VtMongoParser()
for filename in glob.glob("/Users/tcarr/proptrans/PT201401*.xml"):
	parser.loadMongo(filename)

results=parser.coll.find({"formData.buyerList.buyer.lastName": "HAYES"})
#results=parser.coll.collectionname.find({"lastName": "SMITH"})
print results.count()
for item in results:
	print str(item)
#db.collectionname.aggregate([
#    { "$project": { "name": { "$concat" : [ "formData.sellerList.seller.lastName", " ", "formData.sellerList.seller.firstName" ] } } },  
#    { "$match" : { "name": /smith glori/i } }  
#])
