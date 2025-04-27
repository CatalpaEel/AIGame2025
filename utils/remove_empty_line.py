import glob
import sys


def remove_empty_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 过滤掉空行
        non_empty_lines = [line for line in lines if line.strip()]

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(non_empty_lines)
        print(f"已清除 {file_path} 中的空行。")
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}。")
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {e}")


def batch_remove_empty_lines(input_pattern):
    txt_files = glob.glob(input_pattern)
    for txt_file in txt_files:
        remove_empty_lines(txt_file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <docx_path_pattern> <output_dir>")
        sys.exit(1)
    input_pattern = sys.argv[1]
    batch_remove_empty_lines(input_pattern)
    