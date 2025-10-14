# anonymize.py
import os

if os.getenv("GIT_AUTHOR_EMAIL") == "parthbrajput30@gmail.com":
    os.environ["GIT_AUTHOR_NAME"] = "mad7"
    os.environ["GIT_AUTHOR_EMAIL"] = "dave.madhav07@gmail.com"

if os.getenv("GIT_COMMITTER_EMAIL") == "parthbrajput30@gmail.com":
    os.environ["GIT_COMMITTER_NAME"] = "mad7"
    os.environ["GIT_COMMITTER_EMAIL"] = "dave.madhav07@gmail.com"
