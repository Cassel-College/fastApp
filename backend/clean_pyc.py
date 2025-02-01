import os
import shutil

def delete_pyc_files_and_dirs(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname == '__pycache__':
                shutil.rmtree(os.path.join(dirpath, dirname))
                print(f"Deleted directory: {os.path.join(dirpath, dirname)}")
        for filename in filenames:
            if filename.endswith('.pyc'):
                os.remove(os.path.join(dirpath, filename))
                print(f"Deleted file: {os.path.join(dirpath, filename)}")


if __name__ == "__main__":
    
    print("Cleaning up .pyc files and __pycache__ directories...")
    project_root = os.path.dirname(os.path.abspath(__file__))
    delete_pyc_files_and_dirs(project_root)
    
