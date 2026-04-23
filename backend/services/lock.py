import fcntl
import os
from pathlib import Path


LOCKFILE = Path.home() / ".rclone-bisync.lock"


class LockError(Exception):
    pass


class SyncLock:
    def __init__(self):
        self.lockfile = LOCKFILE
        self._fd = None

    def __enter__(self):
        self._fd = open(self.lockfile, "w")
        try:
            fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self._fd.close()
            raise LockError("Sync já está em execução")
        return self

    def __exit__(self, *args):
        if self._fd:
            fcntl.flock(self._fd, fcntl.LOCK_UN)
            self._fd.close()
            self.lockfile.unlink(missing_ok=True)