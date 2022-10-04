from load_data import load_from_json


class TestLoad:
    def test_load(self):
        model = load_from_json(prefix="/constitution-conan")
        paths = list(model.paths())
        assert paths[0] == "/constitution-conan"
        assert paths[1] == "/constitution-conan/preamble"
        assert paths[-1] == "/constitution-conan/amendment-27/clause-1"

    def test_load_headings(self):
        model = load_from_json(prefix="/constitution-conan")
        headings = list(model.headings())
        assert headings[0] == "US Constitution"
        assert headings[1] == "US Constitution, Preamble"
        assert headings[-1] == "US Constitution, Amendment 27, Clause 1"
        am5 = list(model.amendments[4].headings())[-1]
        assert am5 == "Amendment 5, Clause 4"

    def test_load_citations(self):
        model = load_from_json(prefix="/constitution-conan")
        citations = list(model.citations())
        assert citations[0] == "U.S. Const."
        assert citations[1] == "U.S. Const., Preamble"
        assert citations[-1] == "U.S. Const., amend. XXVII, cl. 1"
        am5 = list(model.amendments[4].citations())[-1]
        assert am5 == "amend. V, cl. 4"
