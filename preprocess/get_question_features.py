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
        s = s.encode("utf-8")
    except:
        return ""
    return s.replace("\t", " ").replace("\n", " ")

def write_tsv_row(f, l):
    stringified = [clean_elem(x) for x in l]
    f.write("\t".join(stringified) + "\n")

def parse_tags(tag_string):
    return tag_string.replace("><", ",").replace("<", "").replace(">", "")

def get_question_age(creation_date):
    the_date, the_date2 = creation_date.split("T")
    year, month, day = the_date.split("-")
    hour, minute, second = the_date2.split(":")
    second1, second2 = second.split(".")
    #https://stackoverflow.com/a/151211/5187393
    cdate = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second1), int(second2))
    delta = DATA_DUMP_DAY - cdate
    return str(delta.days*24*3600+delta.seconds)


with open(dirname +'/Questions.xml') as qfile:
    with open(dirname + '/QuestionFeatures.tsv', 'w') as new_file:
        write_tsv_row(new_file, ['Id', 'AcceptedAnswerId', 'QuestionAge', 'Score', 'ViewCount', 'Body', 'OwnerUserId', 'Title', 'Tags', 'AnswerCount', 'CommentCount'])
        for row, line in RowIter(qfile):
            if 'OwnerUserId' in row:
                the_id = row['Id']
                try:
                    accepted_answer = row['AcceptedAnswerId']
                except:
                    accepted_answer = ","
                question_age = get_question_age(row['CreationDate'])
                score = row['Score']
                view_count = row['ViewCount']
                body = row['Body'] #text
                owner_user_id = row['OwnerUserId']
                title = row['Title']
                tags = parse_tags(row['Tags'])
                answer_count = row['AnswerCount']
                comment_count = row['CommentCount']
                write_tsv_row(new_file, [the_id, accepted_answer, question_age, score, view_count, body, owner_user_id, title, tags, answer_count, comment_count])
