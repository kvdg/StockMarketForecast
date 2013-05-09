'''
Created on 9 May 2013

@author: Floris
'''
def readData(sFile):
    matrix = []
    try:
        print "Read Data"
        f = open(sFile, "r")
        data = f.readlines()
        for line in data:
            #strip line from \n and \t
            row = line.strip().split("\t")
            #add row to data matrix
            matrix.append(row)
        print "Read Complete"
    except IOError:
        print 'Error: reading ' + str(sFile)
    finally:
        f.close()
    return matrix
    
def writeData(sFile, arr):
    try:
        print "Write Start"
        f = open(sFile, "a")
        for i in range(0, len(arr)):
            #datum, user, text
            #row = arr[i][0] + "\t" + arr[i][1] + "\t" + arr[i][2] + "\n"
            #Generalized
            row = ""
            width = len(arr[i])
            for j in range (0, width):
                row += str(arr[i][j]) + '\t'
            row = row[:-2] + '\n'      
            f.write(row)
        print "Write Complete"
    except IOError:
        print 'Error: writing tweets'
    finally:
        f.close()