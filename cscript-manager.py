#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Createch Script Manager
# @raycast.mode inline
# @raycast.refreshTime 1s

# Optional parameters:
# @raycast.icon images/createch.png

import sys
args = sys.argv[1:]

import importlib
import subprocess
depends = [
    ('gitpython', 'git')
]
for pack_name, imp_name in depends:
    try:
        importlib.import_module(imp_name)
    except:
        p = subprocess.Popen(f'/usr/bin/env python3 -m pip install {pack_name}', stdout=subprocess.PIPE, shell=True)
        p.wait()

import os
import sys
from git import Repo

def is_repo_up_to_date(repo):
    try:
        return not repo.is_dirty() and len(repo.remote().pull()) == 0
    except Exception as e:
        print(f"无法检查Git状态：{e}")
        return False

def update_current_git_repo():
    print("正在更新当前Git仓库...")
    repo = Repo(os.getcwd())

    if is_repo_up_to_date(repo):
        print("仓库已经是最新的，无需更新。")
    else:
        try:
            origin = repo.remote(name='origin')
            origin.pull()
            print("更新完成。")
        except Exception as e:
            print(f"更新失败：{e}")

# def main():
#     args = sys.argv[1:]
#     if args and args[0] == 'update':
#         update_current_git_repo()
#     else:
#         print("Invalid arguments.")

if __name__ == "__main__":
    # main()
    update_current_git_repo()

