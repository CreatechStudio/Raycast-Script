#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Word Translation
# @raycast.mode fullOutput
# @raycast.packageName word-translation

# Optional parameters:
# @raycast.icon images/trans-icon.png
# @raycast.argument1 { "type": "text", "placeholder": "word", "optional": false}

# Documentation:
# @raycast.description Word Translate

# 安装依赖
import importlib
import pip
depends = [
    ('requests', 'requests'),
    ('pycryptodome', 'Crypto')
]
for pack_name, imp_name in depends:
    try:
        importlib.import_module(imp_name)
    except:
        pip.main(['install', pack_name])


import json
import os
import sys

def youdao_translate(word: str):
    import youdao
    result = youdao.translate(word)
    if result['code'] == 0:
        if 'dictResult' in result.keys():
            r = result['dictResult']
            if r != {}:
                r = r[list(r.keys())[0]]

                # 词汇种类
                if 'exam_type' in r.keys():
                    types = ', '.join(r['exam_type'])
                else:
                    types = ''

                # 读取临时文件
                with open('youdao.json', 'r') as f:
                    cache = json.loads(f.read())

                cache[word] = []

                # 词汇解释
                translations = r['word']['trs']
                for translation in translations:
                    if 'pos' in translation.keys():
                        pos = translation['pos']
                    else:
                        pos = ''

                    if 'tran' in translation.keys():
                        tran = translation['tran']
                    else:
                        tran = translation['#text']

                    print(tran, f'{pos} {types} - 有道')

                    cache[word].append({"translation": tran, "type": pos, "source": types})

                # 写入临时文件
                with open('youdao.json', 'w') as f:
                    f.write(json.dumps(cache, indent=4))

        if 'translateResult' in result.keys():
            translation = result['translateResult'][0][0]['tgt']
            print(f'{translation} - 有道')

    else:
        print(f"有道未查找到单词 '{word}'")


def find_word(words_path, words_list, come_from, need_err=True):
    if os.path.exists(words_path):
        with open(words_path, 'r') as f:
            words_data = json.loads(f.read())

        for word in words_list:
            if word:
                if word not in words_data.keys() and word.lower() in words_data.keys():
                    word = word.lower()
                if word in words_data.keys():
                    translations = words_data[word]
                    for trans in translations:
                        if trans['type']:
                            t = trans['type'] + ('' if trans['type'].strip()[-1] == '.' else '.') + '  '
                        else:
                            t = ''
                        print(f"{word}: {trans['translation'].strip()} - {t + trans['source']} - {come_from}")
                else:
                    if need_err:
                        print(f"{come_from}未查找到单词 '{word}'")
                    return False
        return True
    else:
        return False


def main(words):
    flag = True
    words_list = words.strip().split(' ')
    if len(words_list) == 1:
        flag = find_word('words.json', words_list, '本地') or find_word('youdao.json', words_list, '有道', False)
    else:
        flag = False

    if not flag:
        youdao_translate(words)


if __name__ == '__main__':
    try:
        words = sys.argv[1]
    except IndexError:
        print("无法正常获得提供的参数")
    else:
        print("查找中...", end="\r")
        main(words)
