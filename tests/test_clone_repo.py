import unittest
from doublex import Stub
from expects import expect, equal
import subprocess
from git_history_analyzer.clone import clone_repo

# We'll assume the function will be imported from src.git_tools (to be created)
# from src.git_tools import clone_repo

class TestCloneRepo(unittest.TestCase):
    def test_git_clone_is_called_with_url_and_target_dir(self):
        url = "https://github.com/octocat/Hello-World.git"
        target_dir = "some/target/dir"
        with Stub(subprocess) as stub_subprocess:
            stub_subprocess.run = lambda *args, **kwargs: None
            clone_repo(url, target_dir)
            self.fail("clone_repo does not call subprocess.run yet")

if __name__ == "__main__":
    unittest.main() 