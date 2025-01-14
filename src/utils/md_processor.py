import re
from pathlib import Path
from typing import Optional

import yaml


class MdProcessor:
    def __init__(self, md_file_path: str | Path):
        self.md_file_path = Path(md_file_path)
        self._content: str = ""
        self._metadata: Optional[dict] = None
        self._neighbors: list[str] = []

    @property
    def neighbors(self) -> list[str]:
        return self._neighbors
    
    @property
    def content(self) -> str:
        return self._content
    
    @property
    def metadata(self) -> Optional[dict]:
        return self._metadata

    def process(self, neighbor_key: str = "association") -> None:
        """Process the markdown file and extract the metadata and neighbors.
        
        Args:
            neighbor_key (str): The key in the metadata to extract the neighbors from.
        """
        with open(self.md_file_path, "r") as file:
            self._content = file.read()

        self._metadata = self._extract_metadata()
        if self._metadata and self._metadata.get(neighbor_key):
            for item in self._metadata[neighbor_key]:
                self._neighbors.append(item.lstrip("[[").rstrip("]]").split("|")[0])
    
    def _extract_metadata(self) -> Optional[dict]:
        yaml_match = re.match(r"---\n(.*?)\n---", self._content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            self._content = self._content[yaml_match.end():].lstrip()
            return yaml.safe_load(yaml_content)
        return None
