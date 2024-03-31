import os

_file_dir = os.path.dirname(__file__)
REPO_DIR = os.path.split(_file_dir)[0]
DATA_DIR = os.path.join(REPO_DIR, "data")
ARTIFACT_DIR = os.path.join(REPO_DIR, "artifacts")
TESTS_DIR = os.path.join(REPO_DIR, "tests")
