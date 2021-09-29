import unittest

import main as student_solution
import solution as author_solution
import sys
from io import StringIO

student = student_solution
author = author_solution


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


class DirectorsTestCase(unittest.TestCase):
    def setUp(self):
        with Capturing() as self.student_func_output:
            student.main()
        with Capturing() as self.author_func_output:
            author.main()

    def test_result_is_correct(self):
        self.assertEqual(
            self.student_func_output, self.author_func_output,
            'Проверьте, правильно ли выбраны параметры запроса')

    def test_output_begins_from_new_line(self):
        self.assertGreater(
            len(self.student_func_output), 1,
            'Проверьте, что каждое значение выводится с новой строки')

    def test_output_not_contains_tuples(self):
        startssymbols = ('(', '[', '{')
        endssymbols = (')', ']', '}')
        for startsymb, endsymb in zip(startssymbols, endssymbols):
            self.assertFalse(
                self.student_func_output[0].startswith(startsymb) and
                self.student_func_output[0].endswith(endsymb),
                'Проверьте, что значения выводятся в правильном формате')

    def test_text_in_correct_format(self):
        for value in self.student_func_output:
            self.assertTrue(
                ('—' in value or '-' in value),
                'Проверьте, правильно ли оформлен вывод результата'
            )


if __name__ == "__main__":
    unittest.main()
