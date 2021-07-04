#Only users which have interacted with a question with an accepted answer
from rowiterator import RowIter
from sys import argv

dirname = argv[1]
user_ids = set()
with open(dirname +'/Questions.xml') as qfile:
    for row, line in RowIter(qfile):
        if 'OwnerUserId' in row:
            user_ids.add(row['OwnerUserId'])
        else:
            #print(line)
	    pass

with open(dirname +'/Answers.xml') as afile:
    for row, line in RowIter(afile):
        if 'OwnerUserId' in row:
            user_ids.add(row['OwnerUserId'])
        else:
            #print(line)
            pass

with open(dirname + '/Users.xml') as old_ufile:
    with open(dirname + '/RelUsers.xml', 'w') as new_ufile:
        for row, line in RowIter(old_ufile):
            if row['Id'] in user_ids:
                new_ufile.write(line + '\n')

