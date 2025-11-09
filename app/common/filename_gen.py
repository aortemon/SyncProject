import uuid
from datetime import datetime
from pathlib import Path


class HashedFilenameGenerator:

    @staticmethod
    def generate_unique_name(original_filename: str) -> str:
        extension = Path(original_filename).suffix.lower()
        unique_id = uuid.uuid4().hex[:12]
        timestamp = str(datetime.now().strftime("%Y%m%d_%H%m%S"))

        return f"{unique_id}_{timestamp}{extension}"
