from PIL import Image
import glob
import os
import argparse
import shutil


def jpg_to_png(input_path, output_path):
    try:
        # 打开 JPG 图片
        image = Image.open(input_path)
        # 保存为 PNG 格式
        image.save(output_path, 'PNG')
        print(f"成功将 {input_path} 转换为 {output_path}")
    except FileNotFoundError:
        print(f"错误：未找到文件 {input_path}")
    except Exception as e:
        print(f"发生未知错误：{e}")


def copy_file(input_path, output_path):
    try:
        shutil.copy2(input_path, output_path)
        print(f"成功将 {input_path} 复制到 {output_path}")
    except FileNotFoundError:
        print(f"错误：未找到文件 {input_path}")
    except Exception as e:
        print(f"发生未知错误：{e}")


if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='批量处理 JPG 转换为 PNG 及复制 PNG 文件')
    # 添加输入目录参数
    parser.add_argument('input_directory', type=str, help='包含图片的目录')
    # 添加输出目录参数
    parser.add_argument('output_directory', type=str, help='保存处理后图片的目录')
    # 解析命令行参数
    args = parser.parse_args()

    # 如果输出目录不存在，则创建它
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    # 使用 glob 查找指定目录下所有的 JPG 和 PNG 文件
    image_files = glob.glob(os.path.join(args.input_directory, '*.jpg')) + glob.glob(
        os.path.join(args.input_directory, '*.png'))

    for image_file in image_files:
        # 获取文件名（不包含路径）
        file_name = os.path.basename(image_file)
        file_ext = os.path.splitext(file_name)[1].lower()

        if file_ext == '.jpg':
            # 生成对应的 PNG 文件名
            png_file_name = os.path.splitext(file_name)[0] + '.png'
            # 生成输出的 PNG 文件完整路径
            output_png_path = os.path.join(args.output_directory, png_file_name)
            # 调用转换函数
            jpg_to_png(image_file, output_png_path)
        elif file_ext == '.png':
            # 生成输出的 PNG 文件完整路径
            output_png_path = os.path.join(args.output_directory, file_name)
            # 调用复制函数
            copy_file(image_file, output_png_path)