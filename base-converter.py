#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Base Converter
# @raycast.mode compact
# @raycast.packageName com.createchstudio.raycast.base-converter

# Optional parameters:
# @raycast.icon ♻️
# @raycast.argument1 {"type": "text", "placeholder": "origin base", "optional": false}
# @raycast.argument2 {"type": "text", "placeholder": "target base", "optional": false}
# @raycast.argument3 {"type": "text", "placeholder": "origin text", "optional": false}

# Documentation:
# @raycast.description Usage: base <original base> <target base> <number>

import sys

args = sys.argv[1:]

while ' ' in args:
    args.remove(' ')

if len(args) != 3:
    print('Usage: base <original base> <target base> <number>')
    exit()

def main(args):
    original, target, number = int(args[0]), int(args[1]), args[2]

    def trans_map(cint):
        if cint < 0:
            return None
        elif cint < 10:
            return str(cint)
        elif cint >= 10:
            return chr(cint - 10 + 65)

    ten_num = int(number, base=original)

    def ten_to_any(n, origin):
        res = ''
        while origin:
            res = trans_map(origin % n) + res
            origin = origin // n

        return res

    target_num = ten_to_any(target, ten_num)

    print(f'Base {original} to Base {target}: {target_num}')

if __name__ == '__main__':
    try:
        main(args)
    except Exception as e:
        print(e)