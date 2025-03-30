from dataclasses import dataclass


@dataclass(frozen=True)
class LocalFileConfig:
    base_directory: str
    allowed_content_types: list[str]
