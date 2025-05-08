# AIGame2025

## 环境配置

`Python`版本：`3.12.5`

依赖库：

```bash
langchain==0.3.25
langchain_community==0.3.23
openai==1.77.0
Pillow==11.2.1
python_docx==1.1.2
volcengine==1.0.183
```

## 运行方式

在`AIGame2025`目录下补充`api_key.py`文件：

```python
deepseek_api_key = "<your_deepseek_api_key>"
doubao_api_key = "<your_doubao_api_key>"
doubao_access_key = "<your_doubao_access_key>"
doubao_secret_key = "<your_doubao_secret_key>"
```

然后在`AIGame2025`目录下运行：

```bash
python main.py <input_path>
```

输出文件将保存到`AIGame2025/output/output_{time_stamp}`目录下，其中`log`文件记录了一些中间过程。

## 数据集构建方式

对于`docx`数据，可使用`docx2txt.py`转化为`txt`格式，再使用`remove_empty_line.py`去除空行。

收集数据时，将新加入的未清洗的数据写入`ref/tmp`文件中，再在`reference.py`中运行以下代码。清洗后的数据会被追加到`data`文件之后，可以手动删除空行，也可调用`remove_empty_line.py`。

```python
clean_agent = DataCleaner()
with open("./ref/tmp", "r", encoding='utf-8') as f:
    data = f.read()
cleaned_data = clean_agent.clear(data)
with open("./ref/data", "a", encoding='utf-8') as f:
    print(cleaned_data, file=f)
```

对于文生图数据，先使用`jpg2png.py`将图片转化为`png`格式，再手动缩小一下尺寸过大的图片，然后运行`image_reference`文件。