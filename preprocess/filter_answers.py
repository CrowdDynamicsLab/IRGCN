#Only answers which belong to a question with an accepted answer
from rowiterator import RowIter
from sys import argv

dirname = argv[1]
question_ids = set()
with open(dirname +'/Questions.xml') as qfile:
    for row, line in RowIter(qfile):
        question_ids.add(row['Id'])

with open(dirname + '/AllAnswers.xml') as old_afile:
    with open(dirname + '/Answers.xml', 'w') as new_afile:
        for row, line in RowIter(old_afile):
            if row['ParentId'] in question_ids:
                new_afile.write(line + '\n')

