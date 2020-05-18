


a = b'4;\x14\xda\x02\x149.=\xe6\xccI\xa9\xc9\xc8\x03'
print(a)

string = ''

for byte in a:
    string = string+'-'+ str(byte)
    print(byte, end=' ')

stringCut = string.split('-')
print(stringCut)
bytesCode = b''
for eachPos in stringCut:
    if eachPos != '':
        bytesCode = bytesCode + bytes([int(eachPos)]) 

print(bytesCode)

# print('\n')
# print(type(string))
# #print(bytes([int(string)]))
# print(string)

# by = bytes(string, 'utf-8')
# print(by)
# a = a.split('\\')
# tamaño = len(a)
# print(tamaño)

# string =''
# charProblematico = '\\'
# i=0
# for eachPos in a :
#     if i != tamaño -1 :
#         string = string + eachPos + charProblematico 
#     else:
#         string = string + eachPos
#     i = i+1    

# other = "b'"+string+"'"
# other = other.encode('utf-8')
# print(other)

# print(string)

# print(bytes(string, 'utf-8'))