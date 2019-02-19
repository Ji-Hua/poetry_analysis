import os
import csv
import pdb
from preprocessor import *

file_path = os.path.join(os.path.dirname(__file__), 'tang_poetries.txt')
output_path = 'formatted_tang_poetries.csv'

with open(output_path, 'w+') as outf:
    writer = csv.writer(outf)
    writer.writerow(['title', 'author', 'content', 'volume'])
    text = ''
    count = 0
    with open(file_path) as f:
        for line in f:
            # has no clue why can't match line directly
            if re.match(r'卷\d+_\d+', line.strip()):
                # pdb.set_trace()
                if text != '':
                    # import pdb; pdb.set_trace()
                    poems = parse(text)
                    if poems is not None:
                        for poem in poems:
                            row = list(poem.values())
                            writer.writerow(row)
                            count += 1
                            if count % 100 == 0:
                                print(count)
                text = f'{line}'
            else:
                text = f'{text}{line}'
        if text != '':
            poems = parse(text)
            if poems is not None:
                for poem in poems:
                    row = list(poem.values())
                    writer.writerow(row)

print(count)