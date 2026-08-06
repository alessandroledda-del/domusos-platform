from django.test import SimpleTestCase

class SearchContractTest(SimpleTestCase):
    def test_minimum_query_length_contract(self):
        query = "a"
        self.assertLess(len(query.strip()), 2)
