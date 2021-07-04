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

user_to_badges = {}
with open(dirname +'/Badges.xml') as bfile:
    for row, line in RowIter(bfile):
       the_class = row['Class'] 
       user_id = row['UserId']
       if not user_id in user_to_badges:
           user_to_badges[user_id] = [0, 0, 0]
       user_to_badges[user_id][int(the_class)-1] += 1


with open(dirname + '/UserBadges.tsv', 'w') as new_file:
    write_tsv_row(new_file, ['UserId', 'Gold', 'Silver', 'Bronze'])
    for k, v in user_to_badges.iteritems():
        write_tsv_row(new_file, [k, v[0], v[1], v[2]])
