

"""
	@desc: Groups the data of a dictionary
	@param: dataDict(Dictionary conataining the data)
	@return: Dictionary conataining the grouped data
	@complexity: O(n*log(n))



"""
def groupDicts(dataDict):
	totalSize = len(dataDict)
	
	groupLimit = 15

	#List of pairs of key and values of dictionary
	dataList = []

	for key, val in dataDict.items():
		dataList.append((val, key))

	dataList.sort(reverse=True)

	
 
	topGroup = []
	topGroupSize = min(15, (len(dataDict)/10)%15)

	print(dataList)

mainData = {
	'a': 34, 'b': 40, 'c': 40, 'd': 35, 'e': 33,
	'f': 13, 'g': 12, 'h': 16, 'i': 12, 'j': 20,
	'k': 2, 'l': 2, 'm': 2, 'n': 4, 'o': 1, 'p': 4,
	'q': 4, 'r': 2, 's': 1, 't': 1, 'u': 4, 'v': 3,
	'w': 2, 'x': 3, 'y': 2, 'z': 1
}
groupDicts(mainData)