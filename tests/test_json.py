from usconstitution.load_data import load_from_json


class TestLoadFromJSON:
    def test_load(self):
        constitution = load_from_json()
        assert len(constitution.amendments) == 27
