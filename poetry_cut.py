import csv
import jieba
import sqlite3
from preprocessor import is_chinese

db_file = 'poetry.db'
db = sqlite3.connect(db_file)

# Filter poets
thres = 10
select_sql = f'''
    SELECT poet_id
    FROM (
        SELECT poet_id, count(*) as count
        FROM poems
        GROUP BY poet_id
    ) t
    WHERE count >= {thres}
'''
sql_result = db.execute(select_sql)
valid_poet_ids = [t[0] for t in sql_result]

# print(len(valid_poet_ids))
# print(valid_poet_ids[0])
vocabulary = set()
poet_sentence_pairs = {}
poet_word_pairs = {}
poet_title_pairs = {}
for poet_id in valid_poet_ids:
    poem_sql = f'SELECT title, content FROM poems WHERE poet_id={poet_id}'
    poet_sql = f'SELECT name FROM poets WHERE id={poet_id}'
    poet = list(db.execute(poet_sql))[0][0]
    poet_vocabulary = {}
    poems = db.execute(poem_sql)
    sentences = []
    for poem in poems:
        title = poem[0]
        content = poem[1]
        # remove multi-author poems
        if '--' in content:
            continue
        if poet_title_pairs.get(poet) is None:
            poet_title_pairs[poet] = set([title])
        else:
            poet_title_pairs[poet].add(title)
        sentence = ''
        for char in content:
            if is_chinese(char):
                sentence += char
            else:
                if sentence != '':
                    sentences.append(sentence)
                    words = list(sentence)
                    for word in words:
                        vocabulary.add(word)
                        count = poet_vocabulary.get(word, 0)
                        poet_vocabulary[word] = count + 1
                sentence = ''
    poet_sentence_pairs[poet] = sentences
    poet_word_pairs[poet] = poet_vocabulary

# insert_words = "('" + "'),('".join(vocabulary) + "')"
# db.executemany('INSERT INTO vocabulary (word) VALUES (?)', insert_words)

with open('character.csv', 'w+') as vf:
    writer = csv.writer(vf)
    writer.writerow(['word'])
    for word in vocabulary:
        writer.writerow([word])


with open('poet_char_cout.csv', 'w') as vf:
    writer = csv.writer(vf)
    writer.writerow(['poet', 'word', 'count'])
    for poet, vocab in poet_word_pairs.items():
        for word, count in vocab.items():
            row = [poet, word, count]
            writer.writerow(row)
