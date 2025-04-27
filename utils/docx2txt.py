import glob
import sys
import docx
import os


def docx_to_txt(input_file_path, output_file_path):
    try:
        doc = docx.Document(input_file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        text = '\n'.join(full_text)

        with open(output_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        print(f"成功将 {input_file_path} 转换为 {output_file_path}")
    except FileNotFoundError:
        print(f"错误：未找到文件 {input_file_path}")
    except Exception as e:
        print(f"处理 {input_file_path} 时发生错误: {e}")


def batch_docx_to_txt(input_pattern, output_dir):
    docx_files = glob.glob(input_pattern)

    for docx_file in docx_files:
        # 获取文件名（不包含扩展名）
        base_name = os.path.basename(os.path.splitext(docx_file)[0])
        # 生成对应的 TXT 文件名
        txt_file = os.path.join(output_dir, base_name + ".txt")
        print(f"Converting {docx_file} to {txt_file}")
        try:
            docx_to_txt(docx_file, txt_file)
            print(f"Successfully converted {docx_file} to {txt_file}")
        except Exception as e:
            print(f"Error converting {docx_file}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <docx_path_pattern> <output_dir>")
        sys.exit(1)
    input_pattern = sys.argv[1]
    output_dir = sys.argv[2]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    batch_docx_to_txt(input_pattern, output_dir)
    