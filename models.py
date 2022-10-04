from typing import Iterator, List

from pydantic import BaseModel, validator


class Clause(BaseModel):
    content: str
    index: int = 0

    @validator("content", pre=True)
    def validate_content(cls, v):
        if isinstance(v, List):
            return " ".join(v)
        return v

    def heading(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Clause {self.index}"
        return f"Clause {self.index}"

    def path(self, prefix: str = "") -> str:
        return f"{prefix}/clause-{self.index}"


class Amendment(BaseModel):
    clauses: List[Clause] = []
    index: int = 0
    num: str
    name: str

    @validator("clauses")
    def set_clause_paths(cls, values):
        for i, clause in enumerate(values):
            clause.index = i + 1
        return values

    def heading(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Amendment {self.index}"
        return f"Amendment {self.index}"

    def headings(self, prefix: str = "") -> Iterator[str]:
        yield self.heading(prefix)
        for clause in self.clauses:
            yield clause.heading(self.heading(prefix))

    def path(self, prefix: str = ""):
        return f"{prefix}/amendment-{self.index}"

    def paths(self, prefix: str = "") -> Iterator[str]:
        yield self.path(prefix)
        for clause in self.clauses:
            yield clause.path(self.path(prefix))


class Preamble(BaseModel):
    clauses: List[Clause] = []

    def path(self, prefix: str) -> str:
        return f"{prefix}/preamble"

    def heading(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Preamble"
        return "Preamble"


class Section(BaseModel):
    clauses: List[Clause] = []
    index: int = 0
    num: str
    name: str

    @validator("clauses")
    def set_clause_paths(cls, values):
        for i, clause in enumerate(values):
            clause.index = i + 1
        return values

    def heading(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Section {self.index}"
        return f"Section {self.index}"

    def headings(self, prefix: str = "") -> Iterator[str]:
        yield self.heading(prefix)
        for clause in self.clauses:
            yield clause.heading(self.heading(prefix))

    def path(self, prefix: str) -> str:
        return f"{prefix}/section-{self.index}"

    def paths(self, prefix: str = "") -> Iterator[str]:
        yield self.path(prefix)
        for clause in self.clauses:
            yield clause.path(self.path(prefix))


class Article(BaseModel):
    sections: List[Section] = []
    index: int = 0
    num: str
    name: str

    @validator("sections")
    def set_section_paths(cls, values):
        for i, section in enumerate(values):
            section.index = i + 1
        return values

    def heading(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Article {self.index}"
        return f"Article {self.index}"

    def headings(self, prefix: str = "") -> Iterator[str]:
        yield self.heading(prefix)
        for section in self.sections:
            yield from section.headings(self.heading(prefix))

    def path(self, prefix: str) -> str:
        return f"{prefix}/article-{self.index}"

    def paths(self, prefix: str = "") -> Iterator[str]:
        yield self.path(prefix)
        for section in self.sections:
            yield from section.paths(self.path(prefix))


class Constitution(BaseModel):
    name: str
    preamble: Preamble
    articles: List[Article]
    amendments: List[Amendment]
    path_prefix: str = ""

    @validator("articles")
    def set_article_paths(cls, values):
        for i, article in enumerate(values):
            article.index = i + 1
        return values

    @validator("amendments")
    def set_amendment_paths(cls, values):
        for i, amendment in enumerate(values):
            amendment.index = i + 1
        return values

    def headings(self) -> Iterator[str]:
        yield self.name
        yield self.preamble.heading(prefix=self.name)
        for article in self.articles:
            yield from article.headings(prefix=self.name)
        for amendment in self.amendments:
            yield from amendment.headings(prefix=self.name)

    def paths(self) -> Iterator[str]:
        yield self.path_prefix
        yield self.preamble.path(self.path_prefix)
        for article in self.articles:
            yield from article.paths(self.path_prefix)
        for amendment in self.amendments:
            yield from amendment.paths(self.path_prefix)
