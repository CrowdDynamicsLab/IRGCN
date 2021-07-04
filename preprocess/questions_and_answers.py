from rowiterator import RowIter
from sys import argv

dirname = argv[1]
with open(dirname +'/Posts.xml') as infile:
    with open(dirname + '/Questions.xml', 'w') as qfile:
        with open(dirname + '/AllAnswers.xml', 'w') as afile:
            c = 0
            for row, line in RowIter(infile):
                if c % 1000 == 0:
                    print('Questions and answers', c)
                #if row['PostTypeId'] == '1' and 'AcceptedAnswerId' in row:
                if row['PostTypeId'] == '1':
                    qfile.write(line + '\n')
                elif row['PostTypeId'] == '2':
                    afile.write(line + '\n')
                else:
                    print line,'\n'
                c+=1
