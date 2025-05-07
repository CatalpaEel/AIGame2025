import os
import time
from openai import OpenAI

# 配置信息
deepseek_api_key = "[api_key]"
deepseek_base_url = "https://chat.noc.pku.edu.cn/v1"
DATA_DIR = "datatvss_txt"
OUTPUT_FILE = f"PKU_Commentary_{int(time.time())}.json"

class AcademicCritiqueEngine:
    """
    北京大学信息科学传播内容批判性分析引擎
    提供结构化战略分析框架
    """
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt =  """
作为北京大学新媒体内容战略分析师，请基于学院往期推文进行深度解构分析，输出包含传播学洞察和创作方法论的结构化JSON。

格式要求：
{
  "结构解构": {
    "框架": ["争议话题切入", "教授深度解读", "校友成就举证"],
    "解读": "采用霍尔的编码/解码理论构建认知路径，开篇危机叙事形成强吸引..."
  },
  "风格画像": {
    "特征矩阵": ["学术权威性50%", "青年文化共鸣30%"],
    "修辞分析": "通过三联追问法建立对话感，产业界案例与学术术语形成对仗修辞..."
  },
  "符号体系": {
    "核心符号": ["自主芯片", "交叉学科"],
    "符号转化": "将电竞术语'超神'转译为'算法突破阈值'，实现青年亚文化嫁接..."
  },
  "参与设计": {
    "互动机制": "悬念阶梯：行业难题→本院方案→开放验证",
    "行为引导": "从认知共鸣到身份认同的转化路径设计..."
  },
  "战略建议": {
    "改进方向": "增加产业界失败案例反衬本院成果",
    "理论依据": "参照格伯纳的培养理论强化品牌形象..."
  }
}

分析要求：
1. 每个字段需包含50字左右的专业解读
2. 突出学院"硬核+亲和"的品牌二元性
3. 揭示内容设计的传播心理学原理
4. 标注可复用的创作模因(内容基因)
"""

    def generate_critique(self, text):
        """执行结构化内容分析"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"分析以下文本：\n{text}"}
                ],
                temperature=0.3,
                top_p=0.95,
                max_tokens=3000,
                response_format={"type": "json_object"}
            )

            if response.choices[0].message.content:
                # 验证JSON格式
                json.loads(response.choices[0].message.content)
                return response.choices[0].message.content
            raise Exception("Empty response")

        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON format"})
        except Exception as e:
            return json.dumps({"error": str(e)})

def generate_metadata():
    """生成报告元数据"""
    return {
        "project": "PKU-IST内容战略分析",
        "version": "2.1",
        "timestamp": int(time.time()),
        "analyst": "AcademicCritiqueEngine",
        "data_source": DATA_DIR
    }

if __name__ == "__main__":
    analyzer = AcademicCritiqueEngine()
    report = {
        "metadata": generate_metadata(),
        "analyses": []
    }

    # 遍历数据文件
    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(DATA_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="gbk") as f:
                content = f.read()

        analysis_entry = {
            "filename": filename,
            "content_hash": hash(content),
            "preview": content[:200] + "...[truncated]",
            "analysis": None,
            "error": None
        }

        try:
            critique = analyzer.generate_critique(content)
            analysis_entry["analysis"] = json.loads(critique)
        except Exception as e:
            analysis_entry["error"] = str(e)

        report["analyses"].append(analysis_entry)
        print(f"Processed: {filename}")

    # 写入JSON文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n分析报告已生成：{OUTPUT_FILE}")
    print(f"总分析文件数：{len(report['analyses'])}")
    print(f"错误文件数：{len([x for x in report['analyses'] if x['error']])}")