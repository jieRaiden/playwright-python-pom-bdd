# Playwright Python POM + BDD（含详细注释）

本模板包含完整注释，解释每个文件与关键行的作用，便于快速理解并二次开发。

## 使用方式
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install

export BASE_URL="https://your-app.example.com"  # 可选
pytest -q --headed
```
