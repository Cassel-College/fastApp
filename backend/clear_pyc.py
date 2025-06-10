import os
import shutil

import os
import shutil

def get_file_size(path):
    """
    获取文件或文件夹的大小。
    :param path: 文件或文件夹路径
    :return: 文件或文件夹的大小（字节）
    """
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
        return total_size
    return 0

def find_and_delete_pyc_and_pycache(target_dir):
    """
    找到指定文件夹及所有嵌套文件夹中的 .pyc 文件并删除，同时删除所有 __pycache__ 文件夹，
    并输出删除的文件或文件夹的大小。

    :param target_dir: 目标文件夹路径
    """
    if not os.path.isdir(target_dir):
        print(f"{target_dir} 不是一个有效的文件夹路径。")
        return

    for root, dirs, files in os.walk(target_dir, topdown=False):  # topdown=False 确保删除子目录
        # 删除 __pycache__ 文件夹
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                pycache_size = get_file_size(pycache_path)  # 获取 __pycache__ 文件夹的大小
                shutil.rmtree(pycache_path)  # 删除 __pycache__ 文件夹及其内容
                pycache_path = pycache_path.replace(target_dir, "")  # 仅显示相对路径
                print(f"已删除 __pycache__ 文件夹: {pycache_path}，大小: {pycache_size} 字节")
            except Exception as e:
                print(f"无法删除 {pycache_path}: {e}")

        # 删除 .pyc 文件
        for file in files:
            if file.endswith(".pyc"):
                file_path = os.path.join(root, file)
                try:
                    file_size = get_file_size(file_path)  # 获取 .pyc 文件的大小
                    os.remove(file_path)
                    file_path = file_path.replace(target_dir, "")  # 仅显示相对路径
                    print(f"已删除: {file_path}，大小: {file_size} 字节")
                except Exception as e:
                    print(f"无法删除 {file_path}: {e}")




if __name__ == "__main__":
    # 指定目标文件夹路径
    # target_folder = input("请输入目标文件夹路径: ").strip()
    target_folder = "/Users/pengliu/Code/fastApp/backend"
    find_and_delete_pyc_and_pycache(target_folder)
