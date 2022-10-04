from load_data import load_from_json


class TestLoad:
    model = load_from_json(prefix="/constitution-conan")

    def test_load(self):
        paths = list(self.model.paths())
        assert paths[0] == "/constitution-conan"
        assert paths[1] == "/constitution-conan/preamble"
        assert paths[-1] == "/constitution-conan/amendment-27/clause-1"

    def test_load_headings(self):
        headings = list(self.model.headings())
        assert headings[0] == "US Constitution"
        assert headings[1] == "US Constitution, Preamble"
        assert headings[-1] == "US Constitution, Amendment 27, Clause 1"
        am5 = list(self.model.amendments[4].headings())[-1]
        assert am5 == "Amendment 5, Clause 4"

    def test_load_citations(self):
        citations = list(self.model.citations())
        assert citations[0] == "U.S. Const."
        assert citations[1] == "U.S. Const., Preamble"
        assert citations[-1] == "U.S. Const., amend. XXVII, cl. 1"
        am5 = list(self.model.amendments[4].citations())[-1]
        assert am5 == "amend. V, cl. 4"

    def test_amendment_cite(self):
        am5 = self.model.amendments[4].clauses[0]
        assert am5.citation() == "amend. V, cl. 1"

    def test_amendment_heading(self):
        am8 = self.model.amendments[7]
        assert am8.heading() == "Amendment 8"
        assert am8.heading(prefix="US Constitution") == "US Constitution, Amendment 8"
        am5 = self.model.amendments[4].clauses[0]
        assert am5.heading() == "Amendment 5, Clause 1"

    def test_load_name(self):
        am8 = self.model.amendments[7]
        assert am8.name == "Cruel and Unusual Punishment"
        assert am8.num == "Amendment 8"
