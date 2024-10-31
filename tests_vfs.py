import unittest
from vfs_emulator import VFS


class TestVFS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.tar_path = 'D:/PYTHON/cli_emulator/vfs_tests.tar'

    def setUp(self):
        self.vfs = VFS(self.tar_path)

    def test_ls_success(self):
        self.assertListEqual(sorted(self.vfs.ls()), sorted(['README.txt', 'home', 'etc']))

    def test_ls_empty(self):
        self.vfs.cd('home/user/documents')
        self.assertListEqual(self.vfs.ls(), ['notes.txt'])

    def test_cd_success(self):
        self.vfs.cd('etc')
        self.assertEqual(self.vfs.current_path, 'vfs/etc')

    def test_cd_invalid(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.cd('не_существующая_директория')

    def test_find_success(self):
        results = self.vfs.find('notes')
        self.assertIn('vfs/home/user/documents/notes.txt', results)

    def test_find_no_results(self):
        results = self.vfs.find('не_существующее_имя')
        self.assertEqual(results, [])

    def test_echo_success(self):
        result = self.vfs.echo('Привет', 'Мир')
        self.assertEqual(result, 'Привет Мир')

    def test_echo_empty(self):
        result = self.vfs.echo()  # Пустой вызов
        self.assertEqual(result, '')

    def test_cp_success(self):
        self.vfs.cp('home/user/documents/notes.txt', 'home/user/notes_copy.txt')
        self.assertIn('vfs/home/user/notes_copy.txt', self.vfs.file_structure)

    def test_cp_invalid_source(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.cp('не_существующий_файл.txt', 'dest.txt')

    def test_cp_invalid_destination(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.cp('home/user/documents/notes.txt', 'не_существующая_директория/notes_copy.txt')


if __name__ == '__main__':
    unittest.main()
