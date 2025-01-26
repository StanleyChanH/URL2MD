import re
import openai

# 清理HTML的正则表达式模式
SCRIPT_PATTERN = r"<[ ]*script.*?\/[ ]*script[ ]*>"
STYLE_PATTERN = r"<[ ]*style.*?\/[ ]*style[ ]*>"
META_PATTERN = r"<[ ]*meta.*?>"
COMMENT_PATTERN = r"<[ ]*!--.*?--[ ]*>"
LINK_PATTERN = r"<[ ]*link.*?>"
BASE64_IMG_PATTERN = r'<img[^>]+src="data:image/[^;]+;base64,[^"]+"[^>]*>'
SVG_PATTERN = r"(<svg[^>]*>)(.*?)(<\/svg>)"

def clean_html(html: str, clean_svg: bool = False, clean_base64: bool = False) -> str:
    """
    清理HTML内容
    :param html: 原始HTML
    :param clean_svg: 是否清理SVG
    :param clean_base64: 是否清理Base64图片
    :return: 清理后的HTML
    """
    html = re.sub(SCRIPT_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    html = re.sub(STYLE_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    html = re.sub(META_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    html = re.sub(COMMENT_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    html = re.sub(LINK_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)

    if clean_svg:
        html = re.sub(SVG_PATTERN, "this is a placeholder", html, flags=re.DOTALL)
    if clean_base64:
        html = re.sub(BASE64_IMG_PATTERN, '<img src="#">', html)
    return html

def parse_html(html: str, output_format: str = "markdown", schema: str = None) -> str:
    """
    解析HTML内容
    :param html: 清理后的HTML
    :param output_format: 输出格式，支持markdown或json
    :return: 解析后的内容
    """
    # 初始化OLLAMA客户端
    openai.api_base = 'http://localhost:11434/v1'
    openai.api_key = 'ollama'

    # 清理HTML
    cleaned_html = clean_html(html)

    # 创建提示
    if output_format == "markdown":
        instruction = "Extract the main content from the given HTML and convert it to Markdown format. Return only the Markdown content, do not wrap it in any code blocks or JSON."
    else:
        if not schema:
            schema = """
            {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "metadata": {
                        "type": "object",
                        "properties": {
                            "author": {"type": "string"},
                            "date": {"type": "string"}
                        }
                    }
                },
                "required": ["title", "content"]
            }
            """
        instruction = f"Extract the specified information from the HTML and present it in a structured JSON format following this schema: {schema}"

    try:
        response = openai.ChatCompletion.create(
            model="readerlmv2",
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": cleaned_html}
            ],
            temperature=0,
            max_tokens=1024
        )
        result = response['choices'][0]['message']['content']
        # 去除所有格式的代码块标记
        result  = result.strip().replace("/n", "")
        if result.startswith("```json") and result.endswith("```"):
            result = result[len("```json"):][:-len("```")]
        return result
    except Exception as e:
        print(f"模型调用失败: {str(e)}")
        return "解析失败，请检查模型服务"

    return response.choices[0].message.content