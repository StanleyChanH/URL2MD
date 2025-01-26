from html_parser import parse_html

def test_parse_markdown():
    """测试HTML转Markdown"""
    test_html = """
    <html>
        <body>
            <h1>Test Title</h1>
            <p>This is a test paragraph.</p>
        </body>
    </html>
    """
    result = parse_html(test_html, "markdown")
    print("Markdown解析结果：")
    print(result)

def test_parse_json():
    """测试HTML转JSON"""
    test_html = """
    <html>
        <body>
            <h1>Test Title</h1>
            <p>This is a test paragraph.</p>
        </body>
    </html>
    """
    result = parse_html(test_html, "json")
    print("JSON解析结果：")
    print(result)

if __name__ == "__main__":
    print("开始解析模块测试...")
    test_parse_markdown()
    test_parse_json()
    print("测试完成")