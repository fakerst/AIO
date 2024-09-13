import os
import shutil
import sys


def find_duplicate_files(folder1, folder2):
    # 获取文件夹中的所有文件列表
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))

    # 找到重复的文件列表
    duplicates = files1.intersection(files2)

    #print(len(duplicates))
    # 创建保存重复文件的文件夹
    #if not os.path.exists(output_folder):
    #    os.makedirs(output_folder)

    # 复制重复的文件到新的文件夹中
    #for file in duplicates:
    #    shutil.copy(os.path.join(folder1, file), output_folder)

        # 如果文件夹2中也有重复文件，可以取消下面的注释来复制到新的文件夹中
        # shutil.copy(os.path.join(folder2, file), output_folder)

    #print(f"找到 {len(duplicates)} 个重复文件，并已保存到 {output_folder} 文件夹中。")


def remove_unique_files(folder1, folder2):
    # 获取文件夹中的所有文件列表
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))

    # 找到不重复的文件列表
    unique_files = files1.symmetric_difference(files2)
    #print(unique_files)
    #print(len(unique_files))

    # 删除不重复的文件
    for file in unique_files:
        file_path1 = os.path.join(folder1, file)
        file_path2 = os.path.join(folder2, file)

        if os.path.isfile(file_path1):
            os.remove(file_path1)

        if os.path.isfile(file_path2):
            os.remove(file_path2)

    print(f"已删除 {len(unique_files)} 个不重复的文件。")




if __name__ == "__main__":

    # 示例用法
    folder1 = sys.argv[1]  # 第一个文件夹的路径
    folder2 = sys.argv[2]  # 第二个文件夹的路径

    find_duplicate_files(folder1, folder2)

    remove_unique_files(folder1, folder2)