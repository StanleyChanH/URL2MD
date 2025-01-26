import requests
import json

BASE_URL = "http://localhost:34567"

def test_health_check():
    """测试健康检查接口"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("健康检查测试通过")

def test_parse_markdown():
    """测试解析Markdown格式"""
    test_url = "https://example.com"
    payload = {
        "url": test_url,
        "output_format": "markdown"
    }
    response = requests.post(f"{BASE_URL}/parse", json=payload)
    assert response.status_code == 200
    result = response.json()
    print("Markdown解析结果：")
    print(result["result"])
    assert result["status"] == "success"
    assert isinstance(result["result"], str)
    print("Markdown解析测试通过")

def test_parse_json():
    """测试解析JSON格式"""
    test_url = "https://example.com"
    payload = {
        "url": test_url,
        "output_format": "json"
    }
    response = requests.post(f"{BASE_URL}/parse", json=payload)
    assert response.status_code == 200
    result = response.json()
    print("JSON解析结果：")
    print(result["result"])
    assert result["status"] == "success"
    try:
        json.loads(result["result"])  # 验证是否为有效JSON
        print("JSON解析测试通过")
    except json.JSONDecodeError:
        print("JSON解析测试失败")

def test_parse_with_custom_schema():
    """测试使用自定义schema解析"""
    test_url = "https://example.com"
    custom_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "keywords": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["title", "description"]
    }
    payload = {
        "url": test_url,
        "output_format": "json",
        "schema": json.dumps(custom_schema)
    }
    response = requests.post(f"{BASE_URL}/parse", json=payload)
    assert response.status_code == 200
    result = response.json()
    print("自定义schema解析结果：")
    print(result["result"])
    assert result["status"] == "success"
    try:
        parsed_json = json.loads(result["result"])
        assert "title" in parsed_json
        assert "description" in parsed_json
        print("自定义schema解析测试通过")
    except json.JSONDecodeError as e:
        print(f"自定义schema解析测试失败：{str(e)}")

if __name__ == "__main__":
    print("开始API测试...")
    test_health_check()
    test_parse_markdown()
    test_parse_json()
    test_parse_with_custom_schema()
    print("所有测试完成")