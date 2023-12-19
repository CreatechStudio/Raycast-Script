import os
import json

word_files = os.walk('./words')

words_data = {}

for path, dirs, files in word_files:
    for file in files:
        file_name = '.'.join(file.split('.')[:-1])
        file_path = os.path.join(path, file)
        with open(file_path, 'r') as f:
            data = json.loads(f.read())
            for d in data:
                w = d['word']
                t = d['translations']
                if w in words_data.keys():
                    for i in t:
                        if i not in words_data[w]:
                            i['source'] = file_name
                            words_data[w].append(i)
                else:
                    for i in range(len(t)):
                        t[i]['source'] = file_name
                    words_data[w] = t

with open('words.json', 'w') as f:
    f.write(json.dumps(words_data, ensure_ascii=False))
