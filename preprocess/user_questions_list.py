from rowiterator import RowIter
from sys import argv

def clean_elem(elem):
    s = ""
    try:
        s = str(elem)
    except UnicodeEncodeError:
        s = s.encode("utf-8")
    except:
        return ""
    return s.replace("\t", " ").replace("\n", " ")

dirname = argv[1]

def write_tsv_row(f, l):
    stringified = [clean_elem(x) for x in l]
    f.write("\t".join(stringified) + "\n")

user_to_questions = {}


with open(dirname +'/Questions.xml') as qfile:
    for row, line in RowIter(qfile):
        if 'OwnerUserId' in row:
            user_id = row['OwnerUserId']
            if not user_id in user_to_questions:
                user_to_questions[user_id] = []
            user_to_questions[user_id].append(row['Id'])


with open(dirname + '/UserQuestions.tsv', 'w') as new_file:
    write_tsv_row(new_file, ['UserId', 'Questions'])
    for k, v in user_to_questions.iteritems():
        write_tsv_row(new_file, [k, ",".join(v)])
