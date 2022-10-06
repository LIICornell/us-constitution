import pytest

from usconstitution.models import Section, Amendment, Article, Preamble, Clause
from usconstitution.models import from_loc_id


class TestClause:
    def test_clause(self):
        clause = Clause(content="test", index=1, article_number=1, section_number=1)
        assert clause.content == "test"
        assert clause.index == 1
        assert clause.path("/const") == "/const/article-1/section-1/clause-1"

    def test_cleanpath(self):
        clause = Clause(content="test", index=1, article_number=1, section_number=1)
        assert clause.cleanpath == "/constitution-conan/article-1/section-1/clause-1"

    def test_from_loc_id(self):
        clause, rest = from_loc_id("ArtIII.S2.C2.4")
        assert clause.article_number == 3
        assert clause.section_number == 2
        assert clause.index == 2
        assert rest == "4"
        assert isinstance(clause, Clause)


class TestArticle:
    def test_load_article(self):
        article_json = {
            "identifer": 1,
            "num": "Article I ",
            "type": "article",
            "name": " The Legislative Branch",
            "path": "/constitution/article-1",
            "sections": [
                {
                    "identifer": 2,
                    "num": "Section 1 ",
                    "article_number": 1,
                    "type": "section",
                    "name": " The Legislature",
                    "clauses": [
                        {
                            "content": [
                                "All legislative Powers herein granted shall be vested in a Congress of the United States, which shall consist of a Senate and House of Representatives."
                            ],
                            "num": " ",
                            "article_number": 1,
                            "section_number": 1,
                            "type": "paragraph",
                            "name": " ",
                            "clauses": [],
                        }
                    ],
                }
            ],
        }
        article = Article(**article_json)
        assert (
            article.sections[0].path(prefix="/constitution")
            == "/constitution/article-1/section-1"
        )

    def test_from_loc_id(self):
        article, rest = from_loc_id("ArtIII.1.2")
        assert article.index == 3
        assert rest == "1.2"
        assert isinstance(article, Article)


class TestAmendment:
    def test_from_loc_id(self):
        amendment, rest = from_loc_id("Amdt7.1.1")
        assert amendment.index == 7
        assert rest == "1.1"
        assert isinstance(amendment, Amendment)


class TestPreamble:
    def test_from_loc_id(self):
        preamble, rest = from_loc_id("Pre.3")
        assert rest == "3"
        assert isinstance(preamble, Preamble)


class TestSection:
    def test_from_loc_id(self):
        section, rest = from_loc_id("ArtIII.S2.1")
        assert section.article_number == 3
        assert section.index == 2
        assert rest == "1"
        assert isinstance(section, Section)

    def test_cannot_parse(self):
        with pytest.raises(ValueError):
            section, rest = from_loc_id("AnnIII.X2.Y1")
