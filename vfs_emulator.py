import os
import tarfile
import sys


class VFS:
    def __init__(self, tar_path):
        self.tar_path = tar_path
        self.current_path = 'vfs'
        self.file_structure = self._load_tar()

    def _load_tar(self):
        with tarfile.open(self.tar_path, 'r') as tar:
            return {member.name: member for member in tar.getmembers()}

    def ls(self, path=None):
        # Если путь не передан, используем текущую директорию
        if path is None:
            target_path = self.current_path
        else:
            # Определяем целевой путь (абсолютный или относительный)
            if path.startswith('/'):
                # Абсолютный путь
                target_path = 'vfs' + path
            else:
                # Относительный путь
                target_path = os.path.join(self.current_path, path).replace('\\', '/')

        # Проверка, существует ли целевая директория
        if not any(item.startswith(target_path + '/') for item in self.file_structure):
            raise FileNotFoundError(f"ls: no such file or directory: {path}")

        # Возвращаем список файлов и папок в целевой директории
        return [os.path.basename(name) for name in self.file_structure
                if name.startswith(target_path + '/') and
                name[len(target_path) + 1:].count('/') == 0]

    def cd(self, path):
        if path == '..':
            if self.current_path == 'vfs':
                return
            self.current_path = '/'.join(self.current_path.split('/')[:-1]) or 'vfs'
            return

        if path.startswith('/'):
            if path == '/' or path == '/vfs':
                self.current_path = 'vfs'
                return

            new_path = path.strip('/')
            new_path = 'vfs/' + new_path
        else:
            new_path = os.path.join(self.current_path, path).replace('\\', '/')

        if any(item.startswith(new_path + '/') for item in self.file_structure) or new_path in self.file_structure:
            self.current_path = new_path
        else:
            raise FileNotFoundError(f"cd: no such file or directory: {path}")

    def find(self, name):
        return [item for item in self.file_structure if name in item]

    def echo(self, *args):
        return ' '.join(args)

    def cp(self, source, destination):
        src_path = os.path.join(self.current_path, source).replace('\\', '/')
        if src_path not in self.file_structure:
            raise FileNotFoundError(f"cp: no such file or directory: {source}")

        if destination.endswith('/'):
            dest_path = os.path.join(destination, os.path.basename(source)).replace('\\', '/')
        else:
            dest_path = os.path.join(self.current_path, destination).replace('\\', '/')

        dest_dir = os.path.dirname(dest_path)
        if dest_dir not in self.file_structure and dest_dir != self.current_path:
            raise FileNotFoundError(f"cp: no such directory: {dest_dir}")

        self.file_structure[dest_path] = self.file_structure[src_path]


def main():
    if len(sys.argv) != 3:
        print("Usage: python vfs_emulator.py <hostname> <tar_file_path>")
        return

    hostname, tar_file_path = sys.argv[1], sys.argv[2]
    vfs = VFS(tar_file_path)

    while True:
        try:
            command = input(f"{hostname}:{vfs.current_path}$ ").strip().split()
            if not command:
                continue

            cmd = command[0]

            if cmd == "exit":
                break
            elif cmd == "ls":
                if len(command) > 1:
                    print(' '.join(vfs.ls(command[1])))
                else:
                    print(' '.join(vfs.ls()))
            elif cmd == "cd":
                if len(command) < 2:
                    print("cd: missing argument")
                else:
                    vfs.cd(command[1])
            elif cmd == "find":
                if len(command) < 2:
                    print("find: missing argument")
                else:
                    results = vfs.find(command[1])
                    print('\n'.join(results))
            elif cmd == "echo":
                print(vfs.echo(*command[1:]))
            elif cmd == "cp":
                if len(command) < 3:
                    print("cp: missing file operands")
                else:
                    vfs.cp(command[1], command[2])
            else:
                print(f"{cmd}: command not found")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
