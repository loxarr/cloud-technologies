import os
import sys
import subprocess
import ctypes
from pathlib import Path
import json

CLONE_NEWNS = 0x00020000   # Mount namespace
CLONE_NEWUTS = 0x04000000  # UTS namespace
CLONE_NEWPID = 0x20000000  # PID namespace

libc = ctypes.CDLL('libc.so.6', use_errno=True)

def unshare(flags):
    if libc.unshare(flags) == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, f"unshare failed: {os.strerror(errno)}")

def run_container(container_id):
    with open('config.json', 'r') as f:
        config = json.load(f)

    base_path = Path(f"/var/lib/python_tool/{container_id}")
    upper = base_path / "upper"
    work = base_path / "work"
    merged = base_path / "merged"
    lower = "/tmp/alpine-rootfs"

    for d in [upper, work, merged]:
        d.mkdir(parents=True, exist_ok=True)

    unshare(CLONE_NEWNS | CLONE_NEWUTS | CLONE_NEWPID)

    pid = os.fork()
    if pid != 0:
        _, status = os.waitpid(pid, 0)
        sys.exit(os.waitstatus_to_exitcode(status))

  
    libc.sethostname(config['hostname'].encode(), len(config['hostname']))

    opts = f"lowerdir={lower},upperdir={upper},workdir={work}"
    subprocess.run([
        "mount", "-t", "overlay", "overlay", "-o", opts, str(merged)
    ], check=True)

    proc_path = merged / "proc"
    proc_path.mkdir(exist_ok=True)
    subprocess.run(["mount", "-t", "proc", "proc", str(proc_path)], check=True)

    os.chroot(str(merged))
    os.chdir("/")

    cmd_args = config['process']['args']
    os.execvp(cmd_args[0], cmd_args)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 container_tool.py <id>")
        sys.exit(1)
    
    run_container(sys.argv[1])
