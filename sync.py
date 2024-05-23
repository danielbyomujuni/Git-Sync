from dataclasses import dataclass
import os

@dataclass
class Repo:
    name: str
    up_stream: str
    down_stream: str


#Reads in the folders and the source urls
def read_config():
    repos = []

    f = open("sync.conf", "r")
    for x in f:
        if (x.startswith("#")):
            continue
        if (x.strip()):
            args = x.split()
            if (len(args) != 3):
                print(f'ERROR with: {x}')
                continue

            repos.append(Repo(args[0], args[1], args[2]))
    return repos


def update(repo):
    os.chdir(f"./{repo.name}")

    print("Verifying branches")
    os.system("git branch -r | grep -v '\\->' | sed \"s,\\x1B\\[[0-9;]*[a-zA-Z],,g\" | while read remote; do git branch --track \"${remote#origin/}\"; done")
    os.system(f"git pull --all")
    os.system("git push down --tags")
    os.system("git push down --all")
    os.chdir("../")


def create(repo):
    os.system(f"git clone {repo.up_stream} ./{repo.name}")
    os.chdir(f"./{repo.name}")
    os.system("git branch -r | grep -v '\\->' | sed \"s,\\x1B\\[[0-9;]*[a-zA-Z],,g\" | while read remote; do git branch --track \"${remote#origin/}\"; done")
    os.system(f"git remote add down {repo.down_stream}")
    os.system("git push down --tags")
    os.system("git push down --all")

    os.chdir("../")

if __name__ == '__main__':
    repos = read_config()

    for repo in repos:
        if (not os.path.isdir(f'./{repo.name}')):
            print(f"\033[0;35mCREATING LINK FOR: {repo.name}\033[0;37m")
            create(repo)
        else:
            print(f"\033[0;35mUPDATING LINK FOR: {repo.name}\033[0;37m")
            update(repo)

