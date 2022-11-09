from usconstitution.load_data import load_from_json


class TestLoad:
    model = load_from_json(prefix="/constitution-conan")

    def test_load(self):
        paths = list(self.model.paths())
        assert paths[0] == "/constitution-conan"
        assert paths[1] == "/constitution-conan/preamble"
        assert paths[-1] == "/constitution-conan/amendment-27"

    def test_load_headings(self):
        headings = list(self.model.headings())
        assert headings[0] == "US Constitution"
        assert headings[1] == "US Constitution, Preamble"
        assert headings[-1] == "US Constitution, Amendment 27"
        am5 = list(self.model.amendments[14].headings())[-1]
        assert am5 == "Amendment 15, Section 2"

    def test_load_citations(self):
        citations = list(self.model.citations())
        assert citations[0] == "U.S. Const."
        assert citations[1] == "U.S. Const., Preamble"
        assert citations[-1] == "U.S. Const., amend. XXVII"
        am5 = list(self.model.amendments[4].citations())[-1]
        assert am5 == "amend. V"

    def test_amendment_cite(self):
        am15 = self.model.amendments[14].sections[0]
        assert am15.citation() == "amend. XV, sec. 1"

    def test_amendment_heading(self):
        am8 = self.model.amendments[7]
        assert am8.heading() == "Amendment 8"
        assert am8.heading(prefix="US Constitution") == "US Constitution, Amendment 8"
        am5 = self.model.amendments[4]
        assert am5.heading() == "Amendment 5"

    def test_load_name(self):
        am8 = self.model.amendments[7]
        assert am8.name == "Cruel and Unusual Punishment"
        assert am8.num == "Amendment 8"

    def test_load_loc_id_amdt(self):
        am8 = self.model.amendments[7]
        assert am8.loc_id == "Amdt8"
        assert "cruel and unusual" in am8.content.lower()

    def test_load_loc_id_section(self):
        am5 = self.model.articles[4].sections[0]
        assert am5.loc_id == "ArtV.S1"

    def test_load_loc_id_clause(self):
        am5 = self.model.articles[0].sections[7].clauses[0]
        assert am5.loc_id == "ArtI.S8.C1"

    def test_load_section_content(self):
        art5 = self.model.articles[4].sections[0]
        assert art5.content.startswith("The Congress, whenever")

    def test_load_section_fulltext(self):
        art6 = self.model.articles[3].sections[0]
        assert art6.fulltext.startswith("Full Faith and Credit")
        assert art6.fulltext.endswith("Effect thereof.")

    def test_load_article_6_clause(self):
        assert len(self.model.articles[5].sections) == 0
        clause = self.model.articles[5].clauses[0]
        assert clause.content.startswith("All Debts contracted")
        assert clause.path() == "/article-6/clause-1"

    def test_load_article_7_clause(self):
        art7 = self.model.articles[6]
        assert len(art7.sections) == 0
        assert art7.content.startswith("The Ratification")
        assert art7.path() == "/article-7"
