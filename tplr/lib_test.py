import pathlib
import unittest
import lib as tplr

TEST_ROOT = pathlib.Path(__file__).parent / "test"


class LibTest(unittest.TestCase):

  def test_process_file(self):
    output = tplr.process_template_content(
        content=(TEST_ROOT / "content.txt").read_text(),
        root_path=TEST_ROOT,
        variables=dict(NAME="World"),
        keep_tags=True,
    )
    expected = (TEST_ROOT / "expected.txt").read_text()
    self.assertEqual(output, expected)


if __name__ == "__main__":
  unittest.main()
