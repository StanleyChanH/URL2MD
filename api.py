from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Literal, Optional
from html_fetcher import fetch_html
from html_parser import parse_html

app = FastAPI()

class ParseRequest(BaseModel):
    url: HttpUrl
    output_format: Literal["markdown", "json"] = "markdown"
    schema: Optional[str] = None

@app.post("/parse")
async def parse_url(request: ParseRequest):
    """
    解析URL并返回指定格式的内容
    :param request: 包含URL、输出格式和可选schema的请求体
    :return: 解析后的内容
    """
    try:
        html = fetch_html(str(request.url))
        result = parse_html(html, request.output_format, request.schema)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    健康检查接口
    :return: 服务状态
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=34567)