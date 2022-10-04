from typing import Iterator, List

from pydantic import BaseModel, validator
from roman import toRoman


class Clause(BaseModel):
    content: str
    article_number: int
    section_number: int
    index: int = 0

    @validator("content", pre=True)
    def validate_content(cls, v):
        if isinstance(v, List):
            return " ".join(v)
        return v

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Art{toRoman(self.article_number)}.S{self.section_number}.C{self.index}"

    def citation(self, prefix: str = "") -> str:
        sec_cite = f"art. {toRoman(self.article_number)}, § {self.section_number}"
        cite = f"{sec_cite}, cl. {self.index}"
        if prefix:
            return f"{prefix}, {cite}"
        return cite

    def heading(self, prefix: str = "") -> str:
        artnum = toRoman(self.article_number)
        section_heading = f"Article {artnum}, Section {self.section_number}"
        heading = f"{section_heading}, Clause {self.index}"
        if prefix:
            return f"{prefix}, {heading}"
        return heading

    def path(self, prefix: str = "") -> str:
        section_path = f"/article-{self.article_number}/section-{self.section_number}"
        return f"{prefix}{section_path}/clause-{self.index}"


class AmendClause(BaseModel):
    content: str
    amendment_number: int
    index: int = 0

    @validator("content", pre=True)
    def validate_content(cls, v):
        if isinstance(v, List):
            return " ".join(v)
        return v

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Amdt{self.amendment_number}.{self.index}"

    def citation(self, prefix: str = "") -> str:
        cite = f"amend. {toRoman(self.amendment_number)}, cl. {self.index}"
        if prefix:
            return f"{prefix}, {cite}"
        return cite

    def heading(self, prefix: str = "") -> str:
        heading = f"Amendment {self.amendment_number}, Clause {self.index}"
        if prefix:
            return f"{prefix}, {heading}"
        return heading

    def path(self, prefix: str = "") -> str:
        return f"{prefix}/amendment-{self.amendment_number}/clause-{self.index}"


class Amendment(BaseModel):
    clauses: List[AmendClause] = []
    index: int = 0
    num: str
    name: str

    @validator("num")
    def set_num(cls, v):
        return v.strip()

    @validator("name")
    def set_name(cls, v):
        return v.strip()

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Amdt{self.index}"

    def citation(self, prefix: str = "") -> str:
        roman_index = toRoman(self.index)
        if prefix:
            return f"{prefix}, amend. {roman_index}"
        return f"amend. {roman_index}"

    def citations(self, prefix: str = "") -> Iterator[str]:
        yield self.citation(prefix)
        for clause in self.clauses:
            yield clause.citation(prefix)

    def heading(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Amendment {self.index}"
        return f"Amendment {self.index}"

    def headings(self, prefix: str = "") -> Iterator[str]:
        yield self.heading(prefix)
        for clause in self.clauses:
            yield clause.heading(prefix)

    def path(self, prefix: str = ""):
        return f"{prefix}/amendment-{self.index}"

    def paths(self, prefix: str = "") -> Iterator[str]:
        yield self.path(prefix)
        for clause in self.clauses:
            yield clause.path(prefix)

    def tree(self) -> Iterator[BaseModel]:
        yield self
        for clause in self.clauses:
            yield clause


class Preamble(BaseModel):
    content: str

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Pre"

    def citation(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Preamble"
        return "Preamble"

    def path(self, prefix: str) -> str:
        return f"{prefix}/preamble"

    def heading(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Preamble"
        return "Preamble"


class Section(BaseModel):
    clauses: List[Clause] = []
    article_number: int
    index: int = 0
    content: str = ""
    num: str
    name: str

    @validator("clauses")
    def set_clause_paths(cls, values):
        for i, clause in enumerate(values):
            clause.index = i + 1
        return values

    @validator("content", pre=True)
    def validate_content(cls, v):
        if isinstance(v, List):
            return " ".join(v)
        return v

    @validator("num")
    def set_num(cls, v):
        return v.strip()

    @validator("name")
    def set_name(cls, v):
        return v.strip()

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Art{toRoman(self.article_number)}.S{self.index}"

    def citation(self, prefix: str = "") -> str:
        cite = f"art. {toRoman(self.article_number)}, § {self.index}"
        if prefix:
            return f"{prefix}, {cite}"
        return cite

    def citations(self, prefix: str = "") -> Iterator[str]:
        yield self.citation(prefix)
        for clause in self.clauses:
            yield clause.citation(prefix)

    def heading(self, prefix: str = "") -> str:
        heading = f"Article {toRoman(self.article_number)}, Section {self.index}"
        if prefix:
            return f"{prefix}, {heading}"
        return heading

    def headings(self, prefix: str = "") -> Iterator[str]:
        yield self.heading(prefix)
        for clause in self.clauses:
            yield clause.heading(prefix)

    def path(self, prefix: str) -> str:
        return f"{prefix}/article-{self.article_number}/section-{self.index}"

    def paths(self, prefix: str = "") -> Iterator[str]:
        yield self.path(prefix)
        for clause in self.clauses:
            yield clause.path(prefix)

    def tree(self) -> Iterator[BaseModel]:
        yield self
        for clause in self.clauses:
            yield clause


class Article(BaseModel):
    sections: List[Section] = []
    index: int = 0
    num: str
    name: str

    @validator("num")
    def set_num(cls, v):
        return v.strip()

    @validator("name")
    def set_name(cls, v):
        return v.strip()

    @validator("sections")
    def set_section_paths(cls, values):
        for i, section in enumerate(values):
            section.index = i + 1
        return values

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Art{toRoman(self.index)}"

    def citation(self, prefix: str = "") -> str:
        roman_index = toRoman(self.index)
        if prefix:
            return f"{prefix} art. {roman_index}"
        return f"art. {roman_index}"

    def citations(self, prefix: str = "") -> Iterator[str]:
        yield self.citation(prefix)
        for section in self.sections:
            yield from section.citations(prefix)

    def heading(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Article {self.index}"
        return f"Article {self.index}"

    def headings(self, prefix: str = "") -> Iterator[str]:
        yield self.heading(prefix)
        for section in self.sections:
            yield from section.headings(prefix)

    def path(self, prefix: str) -> str:
        return f"{prefix}/article-{self.index}"

    def paths(self, prefix: str = "") -> Iterator[str]:
        yield self.path(prefix)
        for section in self.sections:
            yield from section.paths(prefix)

    def tree(self) -> Iterator[BaseModel]:
        yield self
        for section in self.sections:
            yield from section.tree()


class Constitution(BaseModel):
    name: str
    preamble: Preamble
    articles: List[Article]
    amendments: List[Amendment]
    path_prefix: str = ""

    def tree(self) -> Iterator[BaseModel]:
        yield self
        yield self.preamble
        for article in self.articles:
            yield from article.tree()
        for amendment in self.amendments:
            yield from amendment.tree()

    def citation(self, prefix: str = "U.S. Const.") -> str:
        return prefix

    def citations(self, prefix: str = "U.S. Const.") -> Iterator[str]:
        for leaf in self.tree():
            yield leaf.citation(prefix)

    def heading(self, prefix: str = "US Constitution") -> str:
        return prefix

    def headings(self, prefix: str = "US Constitution") -> Iterator[str]:
        for leaf in self.tree():
            yield leaf.heading(prefix=prefix)

    def path(self, prefix: str = "/constitution-conan") -> str:
        return prefix

    def paths(self, prefix: str = "/constitution-conan") -> Iterator[str]:
        for leaf in self.tree():
            yield leaf.path(prefix=prefix)
