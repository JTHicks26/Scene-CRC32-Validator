# TODO:
#               Add support for <10 and >99 .rXX files.
#		Multithreading? That'd be cool but also fuck that.

# Completed:
#		Make .sfv formatting less particular:
#			-read/store whole file at once. Search filenames as substrings to find correctCRC
#		Automatically scan current directory for files to check.

import binascii
import os

def get_last_file():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    maxNum = 0
    for f in files:
        try:
            if int(f[-2:]) > maxNum:
                maxNum = int(f[-2:])
                filename = f
        except:
            maxNum = maxNum
    return filename

def calculate_CRC32(filename):
    buf = open(filename,'rb').read()
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return "%08X" % buf

def read_correct_CRC32(filename):
    beginIndex = checksumFileContents.find(filename)
    line = checksumFileContents[beginIndex : beginIndex+len(filename)]
    endIndex = beginIndex + len(filename) + 1
    curChar = checksumFileContents[endIndex]
    endOfFile = False
    while curChar != '\n':
        if endIndex == len(checksumFileContents):
            endOfFile = True
            break
        curChar = checksumFileContents[endIndex]
        endIndex += 1
    if(endOfFile):
        line = checksumFileContents[beginIndex : endIndex]
    else:
        line = checksumFileContents[beginIndex : endIndex-1]
    line = line.split(' ')
    line = line[1]
    return line

def progress_bar(curNum, completeNum, width): 
    percentComplete = (curNum / completeNum) * width
    numDashes = int(percentComplete)
    numSpaces = width - numDashes
    print("|", end='')
    x=0
    while x<numDashes:
        print('=', end='')
        x+=1
    y=0
    while y<numSpaces:
        print(' ', end='')
        y+=1
    print("| " + str(curNum) + '/' + str(completeNum), end='\r')
    if curNum == completeNum:
        print()


def main():
    lastFilename = get_last_file()
    numFiles = int(lastFilename[-2:]) + 1
    
    unformattedFilename = lastFilename[:-4]
    checksumFile = open(unformattedFilename + '.sfv')
    global checksumFileContents
    checksumFileContents = checksumFile.read()
    
    
    fileErrors = []
    crcList = []
    correctCRCList = []
    x=0
    while x < numFiles:
        formattedFilename = unformattedFilename + ".r" + "%02d" % x
        crc = calculate_CRC32(formattedFilename).lower()
        correctCRC = read_correct_CRC32(formattedFilename)
        if crc != correctCRC:
            fileErrors.append(x)
            crcList.append(crc)
            correctCRCList.append(correctCRC)
        progress_bar(x+1, numFiles, 40)
        x+=1

    crc = calculate_CRC32(unformattedFilename + '.rar').lower()
    correctCRC = read_correct_CRC32(unformattedFilename + '.rar')
    rarError = 0
    if crc != correctCRC:
        rarError = 1

    if len(fileErrors) == 0 and rarError == 0:
        print("\nAll files passed.")
    else:
        print()
        print(str(len(fileErrors) + rarError ) + " file(s) failed.\n")
        i=0
        for num in fileErrors:
            print("ERROR for .r" + "%02d" % num)
            print('Expected value: \t' + correctCRCList[i])
            print('Received value: \t' + crcList[i] + '\n')
            i+=1
        if rarError:
            print("ERROR for .rar")
            print('Expected value: \t' + correctCRC)
            print('Received value: \t' + crc + '\n')
    
    

main()
input("Press Enter to continue...")
