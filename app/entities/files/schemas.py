from pathlib import Path

from pydantic import computed_field

from app.entities.common.filename_gen import HashedFilenameGenerator
from app.entities.common.schema import SchemaBase


class FileBase(SchemaBase):
    filename: str
    content_type: str


class SNewFile(FileBase):

    def __init__(self, **data):
        super().__init__(**data)
        self._server_filename = HashedFilenameGenerator.generate_unique_name(
            self.filename
        )

    @computed_field
    @property
    def extension(self) -> str:
        return Path(self.filename).suffix.lower()

    @computed_field
    @property
    def hashname(self) -> str:
        print(self._server_filename)
        return self._server_filename

    @computed_field
    @property
    def source(self) -> str:
        return "/" + self.hashname
