import os
import re
import subprocess

def get_project_path():
    return os.path.dirname(os.path.abspath(__file__))

def get_version():
    """
    Always return base tag version like 1.1.2 (no .devN / .postN).
    WARNING: PyPI will reject re-uploading the same version.
    """
    repo_dir = get_project_path()

    def _run_git(args):
        try:
            return subprocess.check_output(
                ["git"] + args,
                cwd=repo_dir,
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
        except Exception:
            return ""

    desc = _run_git(["describe", "--tags", "--long", "--always"])
    if not desc:
        return "0.0.0"

    # Accept: v1.1.2-3-gxxxx / v1.1.2 / 1.1.2-3-gxxxx / 1.1.2
    m = re.match(r"^v?(\d+(?:\.\d+)*)(?:-(\d+)-g([0-9a-f]+))?$", desc)
    if not m:
        return "0.0.0"

    base = m.group(1)
    return base
