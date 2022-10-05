from usconstitution.models import Constitution, Amendment, Article, Preamble, Clause


class TestClause:
    def test_clause(self):
        clause = Clause(content="test", index=1, article_number=1, section_number=1)
        assert clause.content == "test"
        assert clause.index == 1
        assert clause.path("/const") == "/const/article-1/section-1/clause-1"

    def test_cleanpath(self):
        clause = Clause(content="test", index=1, article_number=1, section_number=1)
        assert clause.cleanpath == "/constitution-conan/article-1/section-1/clause-1"


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
