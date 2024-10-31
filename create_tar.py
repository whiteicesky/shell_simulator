import tarfile
import os

def create_tar_from_directory(directory_path, tar_name):
    with tarfile.open(tar_name, 'w') as tar:
        tar.add(directory_path, arcname=os.path.basename(directory_path))
    print(f"Тар-архив успешно создан: {tar_name}")

if __name__ == "__main__":
    directory_to_archive = 'vfs'
    tar_file_name = 'vfs.tar'

    create_tar_from_directory(directory_to_archive, tar_file_name)
