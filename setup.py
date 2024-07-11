#!/usr/bin/env python3
import os
import subprocess
import venv
from pathlib import Path

VENV_PATH = ".venv"


def get_binary_path(path: str | Path) -> Path:
    if not isinstance(path, Path):
        path = Path(path)
    for bin_dir in ["bin", "Scripts"]:
        binary_path = path / bin_dir
        if binary_path.exists():
            return binary_path
    raise FileNotFoundError("binary path of venv not found")


def rm(path: str | Path) -> None:
    if not isinstance(path, Path):
        path = Path(path)
    if path.exists():
        if path.is_dir() and not path.is_symlink():
            for sub_path in path.iterdir():
                rm(sub_path)
            path.rmdir()
        else:
            path.unlink()
    else:
        raise FileNotFoundError()


def create_venv(*args, **kwargs) -> None:
    path = Path(kwargs["env_dir"] if "env_dir" in kwargs else args[0])
    print(path)
    try:
        rm(path)
    except FileNotFoundError:
        pass
    venv.create(*args, **kwargs)


if __name__ != "__main__":
    raise NotImplementedError()

print("setup venv")
create_venv(
    VENV_PATH,
    with_pip=True,
    upgrade_deps=True,
)
binary_path = get_binary_path(VENV_PATH)
print("install packages")
subprocess.run(
    [binary_path / "pip", "install", "-r", "requirements.txt"], check=True
)
print("install browser")
subprocess.run([binary_path / "playwright", "install", "chromium"], check=True)
match os.name:
    case "nt":
        os.system(f"mklink {binary_path}/")
    case "posix":
        os.system(f"ln -s {binary_path}/")
    case _:
        raise NotImplementedError()
