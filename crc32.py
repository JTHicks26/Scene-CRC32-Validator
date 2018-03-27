# TODO:
#       Add comments.
#       Add support for <10 and >99 .rXX files.
#       Multithreading? That'd be cool but also fuck that.

# Completed:
#       Make .sfv formatting less particular:
#           -read/store whole file at once. Search filenames as substrings to find correctCRC
#       Automatically scan current directory for files to check.

import binascii
import os

#Scan current directory and return the full filename of the highest .rXX file.
def get_last_file():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]   #Create list of files in the current directory.
    maxNum = 0
    
    #Search list of files for highest .rXX file.
    for f in files:     #For every file in the current directory
        try:
            if int(f[-2:]) > maxNum:    #If the last 2 characters of the file extension are a number greater than maxNum
                maxNum = int(f[-2:])        #Update maxNum to the new highest number
                filename = f                #Update filename to the new highest .rXX file
        except:                         #If the last 2 characters of the file extension are not numbers
            maxNum=maxNum                   #Do nothing
    return filename     #Return filename of highest .rXX file

#Calculate CRC32 checksum of a file.
def calculate_CRC32(filename):
    buf = open(filename,'rb').read()
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return "%08X" % buf

#Passed a filename, searches the .sfv file for a line containing the filename and returns the CRC32 checksum at the end of the line.
def read_correct_CRC32(filename):
    beginIndex = checksumFileContents.find(filename)
    endIndex = beginIndex + len(filename) + 9
    line = checksumFileContents[beginIndex:endIndex]
    line = line.split(' ')
    line = line[1]
    return line

#Passed a current number, completion number, and width. Computes and prints a progress bar for curNum.
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
    rarError = False
    if crc != correctCRC:
        rarError = True

    if len(fileErrors) == 0 and rarError == False:
        print("\nAll files passed.")
    else:
        print()
        print(str(len(fileErrors) + int(rarError) ) + " file(s) failed.\n")
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
