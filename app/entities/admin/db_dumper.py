import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path

from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseUtils:

    backups_dir: Path = Path.home() / "SyncProject" / "backups"
    db_name: str = settings.DB_NAME

    @classmethod
    def setup_test(cls):
        cls.backups_dir = Path.home() / "SyncProject" / "tests" / "backups"
        cls.db_name = settings.TEST_DB_NAME

    @classmethod
    def do_backup(cls, compress=True, include_data=True):
        timestamp = datetime.now().strftime(r"%Y%m%d_%H%M%S")
        filename = f"backup_sync_db_{timestamp}"
        try:
            cmd = [
                "pg_dump",
                "-h",
                settings.DB_HOST,
                "-p",
                settings.DB_PORT,
                "-U",
                settings.DB_USER,
                "-d",
                cls.db_name,
                "-v",
            ]

            if not include_data:
                cmd.append("--schema-only")

            env = os.environ.copy()

            if compress:
                dst = cls.backups_dir / f"{filename}.sql.gz"
                process1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)
                with open(dst, "wb") as f:
                    process2 = subprocess.Popen(
                        ["gzip"], stdin=process1.stdout, stdout=f
                    )
                    process1.stdout.close()  # type: ignore
                    process2.communicate()
            else:
                dst = cls.backups_dir / f"{filename}.sql"
                with open(dst, "w") as f:
                    subprocess.run(cmd, stdout=f, env=env, check=True)

            logger.info(f"Backup created successfully: {dst}")
            return dst
        except subprocess.CalledProcessError as e:
            logger.error(f"Backup failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during backup: {e}")
