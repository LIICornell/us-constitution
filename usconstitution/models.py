from typing import Iterator, List, Optional, Tuple

from pydantic import BaseModel, validator
from roman import fromRoman, toRoman


class EssayLink(BaseModel):
    """Link to an essay in the US Constitution Annotated."""

    cleanpath: str
    title: str
    loc_id: str
    idnums: str = ""
    extid: str = ""
    govlink: Optional[str] = None
    children: List["EssayLink"]


class Provision(BaseModel):
    num: str = ""
    name: str = ""
    content: str = ""
    index: int = 0
    essay_links: List[EssayLink] = []

    @validator("num", check_fields=False)
    def whitespace_num(cls, v):
        return v.strip()

    @validator("name", check_fields=False)
    def whitespace_name(cls, v):
        return v.strip()

    @validator("content", check_fields=False)
    def whitespace_content(cls, v):
        return v.strip()

    @property
    def cleanpath(self) -> str:
        return self.path(prefix="/constitution-conan")

    def path(self, prefix: str = "") -> str:
        raise NotImplementedError


class Clause(Provision):
    content: str = ""
    article_number: int
    section_number: Optional[int] = None
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

    @property
    def slug(self) -> str:
        return f"clause-{self.index}"

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
        section_path = f"/article-{self.article_number}"
        if self.section_number:
            section_path += f"/section-{self.section_number}"
        return f"{prefix}{section_path}/{self.slug}"


class AmendSection(Provision):
    content: str = ""
    article_number: int
    index: int = 0

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Amdt{self.article_number}.S{self.index}"

    @property
    def slug(self) -> str:
        return f"section-{self.index}"

    @validator("content", pre=True)
    def validate_content(cls, v) -> str:
        if isinstance(v, List):
            return " ".join(v)
        return v

    def citation(self, prefix: str = "") -> str:
        cite = f"amend. {toRoman(self.article_number)}, sec. {self.index}"
        if prefix:
            return f"{prefix}, {cite}"
        return cite

    def heading(self, prefix: str = "") -> str:
        heading = f"Amendment {self.article_number}, Section {self.index}"
        if prefix:
            return f"{prefix}, {heading}"
        return heading

    def path(self, prefix: str = "") -> str:
        return f"{prefix}/amendment-{self.article_number}/{self.slug}"


class Amendment(Provision):
    sections: List[AmendSection] = []
    content: str = ""
    index: int = 0

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Amdt{self.index}"

    @property
    def slug(self) -> str:
        return f"amendment-{self.index}"

    def citation(self, prefix: str = "") -> str:
        roman_index = toRoman(self.index)
        if prefix:
            return f"{prefix}, amend. {roman_index}"
        return f"amend. {roman_index}"

    def citations(self, prefix: str = "") -> Iterator[str]:
        for clause in self.tree():
            yield clause.citation(prefix)

    def heading(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Amendment {self.index}"
        return f"Amendment {self.index}"

    def headings(self, prefix: str = "") -> Iterator[str]:
        for clause in self.tree():
            yield clause.heading(prefix)

    def path(self, prefix: str = ""):
        return f"{prefix}/{self.slug}"

    def paths(self, prefix: str = "") -> Iterator[str]:
        for clause in self.tree():
            yield clause.path(prefix)

    def tree(self) -> Iterator[Provision]:
        yield self
        for clause in self.sections:
            yield clause


class Preamble(Provision):
    content: str = ""

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Pre"

    @property
    def slug(self) -> str:
        return "preamble"

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


class Section(Provision):
    clauses: List[Clause] = []
    article_number: int
    index: int = 0
    content: str = ""

    @validator("clauses")
    def set_clause_paths(cls, clause_values):
        for i, clause in enumerate(clause_values):
            clause.index = i + 1
        return clause_values

    @validator("content", pre=True)
    def validate_content(cls, v):
        if isinstance(v, List):
            return " ".join(v)
        return v

    @property
    def fulltext(self) -> str:
        clause_text = " ".join([c.content.strip() for c in self.clauses])
        if self.content:
            return f"{self.content.strip()} {clause_text}".strip()
        return clause_text.strip()

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Art{toRoman(self.article_number)}.S{self.index}"

    @property
    def slug(self) -> str:
        return f"section-{self.index}"

    def citation(self, prefix: str = "") -> str:
        cite = f"art. {toRoman(self.article_number)}, § {self.index}"
        if prefix:
            return f"{prefix}, {cite}"
        return cite

    def citations(self, prefix: str = "") -> Iterator[str]:
        for clause in self.tree():
            yield clause.citation(prefix)

    def heading(self, prefix: str = "") -> str:
        heading = f"Article {toRoman(self.article_number)}, Section {self.index}"
        if prefix:
            return f"{prefix}, {heading}"
        return heading

    def headings(self, prefix: str = "") -> Iterator[str]:
        for clause in self.tree():
            yield clause.heading(prefix)

    def path(self, prefix: str) -> str:
        return f"{prefix}/article-{self.article_number}/{self.slug}"

    def paths(self, prefix: str = "") -> Iterator[str]:
        for clause in self.tree():
            yield clause.path(prefix)

    def tree(self) -> Iterator[BaseModel]:
        yield self
        for clause in self.clauses:
            yield clause


class Article(Provision):
    sections: List[Section] = []
    index: int = 0
    clauses: List[Clause] = []

    @validator("sections")
    def set_section_paths(cls, section_values):
        for i, section in enumerate(section_values):
            section.index = i + 1
        return section_values

    @property
    def loc_id(self) -> str:
        """Identifier used by the Library of Congress."""
        return f"Art{toRoman(self.index)}"

    @property
    def slug(self) -> str:
        return f"article-{self.index}"

    def citation(self, prefix: str = "") -> str:
        roman_index = toRoman(self.index)
        if prefix:
            return f"{prefix} art. {roman_index}"
        return f"art. {roman_index}"

    def citations(self, prefix: str = "") -> Iterator[str]:
        for section in self.tree():
            yield section.citation(prefix)

    def heading(self, prefix: str = "") -> str:
        if prefix:
            return f"{prefix}, Article {self.index}"
        return f"Article {self.index}"

    def headings(self, prefix: str = "") -> Iterator[str]:
        for section in self.tree():
            yield from section.heading(prefix)

    def path(self, prefix: str = "") -> str:
        return f"{prefix}/{self.slug}"

    def paths(self, prefix: str = "") -> Iterator[str]:
        for section in self.tree():
            yield section.path(prefix)

    def tree(self) -> Iterator[BaseModel]:
        yield self
        for section in self.sections:
            yield from section.tree()


class Constitution(Provision):
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


def from_loc_id(link_text: str) -> Tuple[Provision, str]:
    """Parse link text into a provision and an essay path."""
    if link_text.startswith("Pre"):
        return Preamble(), link_text[4:]
    if link_text.startswith("Art"):
        art_num = fromRoman(link_text[3 : link_text.find(".")])
        if ".S" in link_text:
            section_num = int(link_text.split(".S")[1][0])
            if ".C" in link_text:
                clause_num = int(link_text.split(".C")[1][0])
                return (
                    Clause(
                        article_number=art_num,
                        section_number=section_num,
                        index=clause_num,
                    ),
                    link_text[link_text.find(".C") + 4 :],
                )
            section = Section(article_number=art_num, index=section_num)
            return section, link_text.split(".", maxsplit=2)[2]
        return Article(index=art_num), link_text.split(".", maxsplit=1)[1]
    if link_text.startswith("Amdt"):
        amendment = Amendment(index=int(link_text[4 : link_text.find(".")]))
        return amendment, link_text.split(".", maxsplit=1)[1]
    raise ValueError(f"Could not parse link text: {link_text}")
