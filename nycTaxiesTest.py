import unittest


class TestSum(unittest.TestCase):

	def test_sum(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

	def test_sum_tuple(self):
		self.assertNotEqual(sum((1, 2, 2)), 6, "Should be 6")

	#Test, der überprüft, dass der Average richtig berechnet wird

	#Test, der überprüft, dass die Daten richtig geladen werden


if __name__ == '__main__':
	unittest.main()