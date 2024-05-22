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
    os.system(f"git pull --all")
    os.system("git push down")
    os.chdir("../")


def create(repo):
    os.system(f"git clone {repo.up_stream} ./{repo.name}")
    os.chdir(f"./{repo.name}")
    os.system(f"git remote add down {repo.down_stream}")
    os.system("git push down")
    os.chdir("../")

if __name__ == '__main__':
    repos = read_config()

    for repo in repos:
        if (not os.path.isdir(f'./{repo.name}')):
            print(f"creating {repo.name}")
            create(repo)
        else:
            print(f"updating {repo.name}")
            update(repo)

