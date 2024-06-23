import tempfile
import os
import subprocess
import shutil
import os
# import stat

# def handle_remove_readonly(func, path, exc_info):
#     exc_type, exc_value, exc_traceback = exc_info
#     if func in (os.remove, os.rmdir) and exc_type is PermissionError:
#         os.chmod(path, stat.S_IWRITE)
#         func(path)
#     else:
#         raise exc_value

# def change_permissions_recursively(directory_path):
#     for root, dirs, files in os.walk(directory_path):
#         for dir_name in dirs:
#             os.chmod(os.path.join(root, dir_name), stat.S_IWRITE)
#         for file_name in files:
#             os.chmod(os.path.join(root, file_name), stat.S_IWRITE)

# def delete_directory(directory_path):
#     try:
#         change_permissions_recursively(directory_path)
#         shutil.rmtree(directory_path, onerror=handle_remove_readonly)
#         print(f"Successfully deleted {directory_path}")
#     except PermissionError as e:
#         print(f"PermissionError: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")


class Github():
    def __init__(self, link):
        self.link = link
        
    def clone_repo(self):
        #make a temp repo
        temp_dir = tempfile.mkdtemp()
        print(temp_dir)
        
        os.chdir(temp_dir)
        #clone the repo
        subprocess.run(['git', 'clone', self.link])
        
        #read and write in a variable and put it in database
        
        #os.remove(temp_dir)
        os.chdir(os.getcwd())
        shutil.rmtree(temp_dir, ignore_errors=True)
        #delete_directory(temp_dir)
        #read and store it
        
if __name__ == "__main__":
    g = Github(r'https://github.com/BhusareHarshad/Chrome-Extension-v2.git')
    g.clone_repo()

