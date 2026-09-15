import unittest

from json_toolkit import collect_stats, get_path


class JsonToolkitTests(unittest.TestCase):
    def setUp(self):
        self.data = {
            "user": {"profile": {"name": "Monica"}},
            "items": [{"id": 1}, {"id": 2}],
        }

    def test_nested_key_lookup(self):
        self.assertEqual(get_path(self.data, "user.profile.name"), "Monica")

    def test_list_index_lookup(self):
        self.assertEqual(get_path(self.data, "items.1.id"), 2)

    def test_missing_key(self):
        with self.assertRaises(KeyError):
            get_path(self.data, "user.email")

    def test_stats(self):
        stats = collect_stats(self.data)
        self.assertEqual(stats["objects"], 5)
        self.assertEqual(stats["arrays"], 1)
        self.assertEqual(stats["values"], 3)
        self.assertEqual(stats["max_depth"], 3)


if __name__ == "__main__":
    unittest.main()
