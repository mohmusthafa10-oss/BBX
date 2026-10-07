When I start a new Python project, I first create a separate folder for the project. Then I create a virtual environment inside that folder using `python -m venv venv` and activate it.

I use a virtual environment because it keeps the project’s Python packages separate from my system Python and from other projects. When I activate the environment, its `Scripts` folder is added to the front of the PATH. This means when I run `python` or `pip`, my computer uses the Python and packages from the virtual environment first. I checked this by comparing the Python paths inside and outside the environment.

After that, I install the packages I need, such as `requests` and `rich`. I use `pip freeze > requirements.txt` to save the installed packages and their exact versions. The versions are pinned so that if someone else sets up the project, they can install the same versions and avoid unexpected package changes.

Finally, I initialize Git and create a `.gitignore` file to ignore `venv/` and `__pycache__/`. I then make my first Git commit.

One real problem a virtual environment prevents is dependency conflicts. For example, one project might need an older version of a package while another project needs a newer version.

Collecting rich
  Using cached rich-15.0.0-py3-none-any.whl.metadata (18 kB)
Collecting charset_normalizer<4,>=2 (from requests)
  Downloading charset_normalizer-3.5.1-cp313-cp313-win_amd64.whl.metadata (46 kB)
Collecting idna<4,>=2.5 (from requests)
  Downloading idna-3.20-py3-none-any.whl.metadata (7.2 kB)
Collecting urllib3<3,>=1.26 (from requests)
  Downloading urllib3-2.8.0-py3-none-any.whl.metadata (7.4 kB)
Collecting certifi>=2023.5.7 (from requests)
  Downloading certifi-2026.7.22-py3-none-any.whl.metadata (2.5 kB)
Collecting markdown-it-py>=2.2.0 (from rich)
  Using cached markdown_it_py-4.2.0-py3-none-any.whl.metadata (7.4 kB)
Collecting pygments<3.0.0,>=2.13.0 (from rich)
  Downloading pygments-2.21.0-py3-none-any.whl.metadata (2.5 kB)
Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich)
  Using cached mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
Using cached requests-2.34.2-py3-none-any.whl (73 kB)
Downloading charset_normalizer-3.5.1-cp313-cp313-win_amd64.whl (199 kB)
Downloading idna-3.20-py3-none-any.whl (69 kB)
Downloading urllib3-2.8.0-py3-none-any.whl (135 kB)
Using cached rich-15.0.0-py3-none-any.whl (310 kB)
Downloading pygments-2.21.0-py3-none-any.whl (1.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 4.2 MB/s  0:00:00
Downloading certifi-2026.7.22-py3-none-any.whl (136 kB)
Using cached markdown_it_py-4.2.0-py3-none-any.whl (91 kB)
Using cached mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Installing collected packages: urllib3, pygments, mdurl, idna, charset_normalizer, certifi, requests, markdown-it-py, rich
Successfully installed certifi-2026.7.22 charset_normalizer-3.5.1 idna-3.20 markdown-it-py-4.2.0 mdurl-0.1.2 pygments-2.21.0 requests-2.34.2 rich-15.0.0 urllib3-2.8.0

[notice] A new release of pip is available: 25.2 -> 26.2.1
[notice] To update, run: python.exe -m pip install --upgrade pip
(venv) PS D:\bbx\repositories\BBX\PYTHON\day1-interview-demo> python -m pip freeze
certifi==2026.7.22
charset-normalizer==3.5.1
idna==3.20
markdown-it-py==4.2.0
mdurl==0.1.2
Pygments==2.21.0
requests==2.34.2
rich==15.0.0
urllib3==2.8.0
(venv) PS D:\bbx\repositories\BBX\PYTHON\day1-interview-demo> python -m pip freeze > requirements.txt
(venv) PS D:\bbx\repositories\BBX\PYTHON\day1-interview-demo> git init
Initialized empty Git repository in D:/bbx/repositories/BBX/PYTHON/day1-interview-demo/.git/
(venv) PS D:\bbx\repositories\BBX\PYTHON\day1-interview-demo> New-Item .gi                              tignore -ItemType File


    Directory: D:\bbx\repositories\BBX\PYTHON\day1-interview-demo


Mode                 LastWriteTime         Length Name                                                 
----                 -------------         ------ ----                                                 
-a----        18-09-2026  12:18 PM              0 .gitignore                                           


(venv) PS D:\bbx\repositories\BBX\PYTHON\day1-interview-demo> code .gitignore
(venv) PS D:\bbx\repositories\BBX\PYTHON\day1-interview-demo> git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore
        requirements.txt

nothing added to commit but untracked files present (use "git add" to track)
(venv) PS D:\bbx\repositories\BBX\PYTHON\day1-interview-demo> git add .gitignore requirements.txt
(venv) PS D:\bbx\repositories\BBX\PYTHON\day1-interview-demo> git status                         
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .gitignore
        new file:   requirements.txt

(venv) PS D:\bbx\repositories\BBX\PYTHON\day1-interview-demo> git commit -m "Initial Python project setup"
[master (root-commit) 50a87ce] Initial Python project setup
 2 files changed, 2 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 requirements.txt
(venv) PS D:\bbx\repositories\BBX\PYTHON\day1-interview-demo> git status                                
On branch master
nothing to commit, working tree clean