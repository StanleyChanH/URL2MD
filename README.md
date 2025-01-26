# HTML信息提取服务

基于ReaderLMv2模型的HTML信息提取服务，提供Markdown和JSON格式的输出。

## 功能特性

- 支持从URL获取HTML内容
- 提供HTML清理功能，去除脚本、样式等噪声
- 支持Markdown格式输出
- 支持JSON格式输出，可自定义schema
- 提供RESTful API接口

## 安装指南

1. 克隆项目仓库
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 确保OLLAMA服务已启动并加载readerlmv2模型

## 使用说明

### 启动服务

```bash
uvicorn api:app --reload --port 34567
```

### API文档

#### 健康检查

- 路径：`/health`
- 方法：GET
- 返回：服务状态

#### HTML解析

- 路径：`/parse`
- 方法：POST
- 请求体：
  ```json
  {
    "url": "目标URL",
    "output_format": "输出格式（markdown或json）",
    "schema": "可选的自定义JSON schema"
  }
  ```
- 返回：解析后的内容

## 测试说明

项目包含完整的单元测试：

```bash
python test_api.py
python test_parser.py
```

测试覆盖：
- 健康检查
- Markdown解析
- JSON解析
- 自定义schema解析

## 项目结构

```
.
├── api.py            # FastAPI接口
├── html_fetcher.py   # HTML获取模块
├── html_parser.py    # HTML解析模块
├── main.py           # 主程序入口
├── requirements.txt  # 依赖文件
├── test_api.py       # API测试
├── test_parser.py    # 解析模块测试
└── README.md         # 项目文档
```
