from rowiterator import RowIter
from sys import argv
from datetime import date

dirname = argv[1]

DATA_DUMP_DAY = date(2018, 7, 18)
def clean_elem(elem):
    s = ""
    try:
        s = str(elem)
    except UnicodeEncodeError:
        s = s.encode("utf-8")
    except:
        return ""
    return s.replace("\t", " ").replace("\n", " ")

user_to_badges = {}
user_to_questions = {}
user_to_answers = {}

with open(dirname +'/UserQuestions.tsv') as uqfile:
    next(uqfile)
    for line in uqfile:
        user, questions = line.strip().split("\t")
        user_to_questions[user] = questions
# print("Finished UserQuestions")

with open(dirname +'/UserAnswers.tsv') as uafile:
    next(uafile)
    for line in uafile:
        user, answers = line.strip().split("\t")
        user_to_answers[user] = answers
# print("Finished UserAnswers")

with open(dirname +'/UserBadges.tsv') as ubfile:
    next(ubfile)
    for line in ubfile:
        user, gold, silver, bronze = line.strip().split("\t")
        user_to_badges[user] = (gold, silver, bronze)
# print("Finished UserBadges")

def write_tsv_row(f, l):
    stringified = [clean_elem(x) for x in l]
    f.write("\t".join(stringified) + "\n")

def get_network_age(creation_date):
    the_date, _ = creation_date.split("T")
    year, month, day = the_date.split("-")
    #https://stackoverflow.com/a/151211/5187393
    cdate = date(int(year), int(month), int(day))
    delta = DATA_DUMP_DAY - cdate
    return str(delta.days)

with open(dirname +'/RelUsers.xml') as ufile:
    with open(dirname + '/UserFeatures.tsv', 'w') as new_file:
        write_tsv_row(new_file, ['Id', 'Reputation', 'LastAccessDate', 'Location', 'AboutMe', 'Views', 'NetworkAge', 'Age', 'UpVotes', 'DownVotes', 'Gold', 'Silver', 'Bronze', 'Questions', 'Answers'])
        for row, line in RowIter(ufile):
            the_id = row['Id']
            rep = row['Reputation']
            last_access_data = get_network_age(row['LastAccessDate'])
            try:
                about_me = row['AboutMe']
            except:
                about_me = ","
            try:
                location = row['Location']
            except:
                location = ","
            views = row['Views']
            nage = get_network_age(row['CreationDate'])
            age = -1
            if 'Age' in row:
                age = row['Age']
            uv = row['UpVotes']
            dv = row['DownVotes']
            gold = 0
            silver = 0
            bronze = 0
            questions = ","
            answers = ","
            if the_id in user_to_badges:
                badges = user_to_badges[the_id]
                gold = badges[0]
                silver = badges[1]
                bronze = badges[2]
            if the_id in user_to_questions:
                questions = user_to_questions[the_id]
            if the_id in user_to_answers:
                answers = user_to_answers[the_id]
            write_tsv_row(new_file, [the_id, rep, last_access_data, location, about_me, views, nage, age, uv, dv, gold, silver, bronze, questions, answers])
