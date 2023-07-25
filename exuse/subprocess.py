import subprocess


def run_ordered_commands(*commands, **kwargs):
    """
    按顺序在子进程中执行命令。

    Args:
      - `skip_failed`: 某条命令执行错误时是否跳过它继续执行后续命令。默认 `False`。
    """
    skip_failed = kwargs.get("skip_failed", False)
    for command in commands:
        process = subprocess.run(command, shell=True)
        if skip_failed:
            continue
        if process.returncode != 0:
            return False
    return True
