from typing import NamedTuple
from urllib.parse import (
    urlsplit,
    urlunsplit,
)


class URL(NamedTuple):
    scheme: str
    host: str
    path: str
    query: str
    fragment: str

    @classmethod
    def from_string(cls, url_string: str) -> 'Url':
        split_result = urlsplit(url_string)
        return cls(
            scheme=split_result.scheme,
            host=split_result.netloc,
            path=split_result.path,
            query=split_result.query,
            fragment=split_result.fragment,
        )

    def to_string(self) -> str:
        return urlunsplit(
            (
                self.scheme,
                self.host,
                self.path,
                self.query,
                self.fragment,
            )
        )
