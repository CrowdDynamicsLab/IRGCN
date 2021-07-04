from rowiterator import RowIter
from sys import argv
from datetime import datetime

dirname = argv[1]

DATA_DUMP_DAY = datetime(2018, 7, 18, 0, 0, 0, 0)
def clean_elem(elem):
    s = ""
    try:
        s = str(elem)
    except UnicodeEncodeError:
        s = elem.encode("utf-8")
    except:
        print "=",# to mark any exceptions
        return ""
    return s.replace("\t", " ").replace("\n", " ")

def write_tsv_row(f, l):
    stringified = [clean_elem(x) for x in l]
    f.write("\t".join(stringified) + "\n")

def parse_tags(tag_string):
    return tag_string.replace("><", ",").replace("<", "").replace(">", "")

def get_answer_age(creation_date):
    the_date, the_date2 = creation_date.split("T")
    year, month, day = the_date.split("-")
    hour, minute, second = the_date2.split(":")
    second1, second2 = second.split(".")
    #https://stackoverflow.com/a/151211/5187393
    cdate = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second1), int(second2))
    delta = DATA_DUMP_DAY - cdate
    return str(delta.days*24*3600+delta.seconds)

with open(dirname +'/Answers.xml') as afile:
    with open(dirname + '/AnswerFeatures.tsv', 'w') as new_file:
        write_tsv_row(new_file, ['Id', 'ParentId', 'AnswerAge', 'Score', 'Body', 'OwnerUserId', 'CommentCount'])
        for row, line in RowIter(afile):
            if 'OwnerUserId' in row:
                the_id = row['Id']
                parent_id = row['ParentId']
                answer_age = get_answer_age(row['CreationDate'])
                score = row['Score']
                body = row['Body'] #text
                owner_user_id = row['OwnerUserId']
                comment_count = row['CommentCount']
                write_tsv_row(new_file, [the_id, parent_id, answer_age, score, body, owner_user_id, comment_count])
