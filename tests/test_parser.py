import unittest
from app.shell.parser import parse_command

class TestParser(unittest.TestCase):

    def test_simple_command(self):
        result = parse_command("ls -l")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['command'], ['ls', '-l'])

    def test_pipe_command(self):
        result = parse_command("ls -l | grep test")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['command'], ['ls', '-l'])
        self.assertEqual(result[1]['command'], ['grep', 'test'])

    def test_redirection_command(self):
        result = parse_command("echo hello > test.txt")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['command'], ['echo', 'hello'])
        self.assertEqual(result[0]['stdout'], 'test.txt')

if __name__ == '__main__':
    unittest.main()
