from smartcard.util import toHexString
expectedReaders = ['Gemalto PC Twin Reader 00 00']
expectedATRs = [[63, 47, 0, 128, 105, 175, 2, 4, 1, 49, 0, 0, 0, 14, 131, 62, 159, 22]]
expectedATRinReader = {}
for i in range(len(expectedReaders)):
    expectedATRinReader[expectedReaders[i]] = expectedATRs[i]
expectedReaderForATR = {}
for i in range(len(expectedReaders)):
    expectedReaderForATR[toHexString(expectedATRs[i])] = expectedReaders[i]
expectedReaderGroups = ['SCard$DefaultReaders']
