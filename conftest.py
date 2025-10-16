"""
conftest.py — pytest 的“项目级钩子/fixture 容器”
作用：集中管理全局的 fixture（前置/后置）、钩子（hook）、以及与 Playwright 的集成策略
注意：文件名和位置固定（任意包/目录下的 conftest.py 都会被 pytest 自动发现并生效）
"""
import os                                 # 用于读取环境变量（例如 BASE_URL）
import pathlib
import time                            # 跨平台路径/文件夹操作
import pytest                             # pytest 的主入口：fixture、hook 等都由它提供
import requests
from datetime import datetime

from api.login_api import LoginAPI
from pages.dashboard_page import DashboardPage
from ultilities.jsonReader import JsonReader



# ---------- 基础配置：被测系统的 Base URL ----------
# 从环境变量读取 BASE_URL；如果未设置，则使用一个安全的默认站点（example.com）
BASE_URL = os.getenv("BASE_URL", "https://rahulshettyacademy.com/client/#/auth/login")

# ---------- 会话级前置：确保 artifacts 目录存在 ----------
@pytest.fixture(scope="session", autouse=True)
def _ensure_artifacts_dir():
    """
    在整个测试会话开始之前自动执行：
    - 创建 artifacts/ 目录（若已存在则忽略）
    - 用于保存失败用例的截图、trace 等调试工件
    """
    pathlib.Path("artifacts").mkdir(exist_ok=True)

# ---------- 提供 base_url 给测试与 Page Object 使用 ----------
@pytest.fixture(scope="session")
def base_url() -> str:
    """
    返回被测系统的基础地址；将其做成 fixture 便于：
    - 在测试与 Page Object 中统一注入
    - 在 CI 中通过设置环境变量切换不同环境（dev/stage/prod）
    """
    return BASE_URL

# ---------- BrowserContext fixture：每条用例独立上下文 ----------
@pytest.fixture
def context(browser):
    """
    依赖于 pytest-playwright 提供的 `browser`（已经启动好的浏览器进程）
    这里为每条用例创建一个全新的 BrowserContext：
    - 隔离 cookie、localStorage、sessionStorage
    - 避免状态污染（提升用例之间的独立性）
    """
    ctx = browser.new_context()
    yield ctx

    ctx.close()  # 用例结束后关闭，释放资源

# ---------- Page fixture：每条用例一个新的标签页 ----------
@pytest.fixture
def page(context):
    """
    基于上面的 BrowserContext 创建一个 Page（浏览器标签页）供用例使用
    """
    return context.new_page()

@pytest.fixture(autouse=True)
def open_home(page, base_url):
    page.goto(base_url)


# ---------- Hook：收集每个阶段（setup/call/teardown）的执行结果 ----------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    用例执行完后，pytest 会调用该钩子生成阶段报告（rep）：
    - 我们用它来判断用例是否失败（rep.failed）
    - 再把报告挂到 item（测试节点）上，以便在 fixture 里访问
    """
    outcome = yield                    # 先让其他钩子/默认行为执行
    rep = outcome.get_result()         # 获取该阶段（setup/call/teardown）的报告对象
    setattr(item, f"rep_{rep.when}", rep)  # 动态挂属性：item.rep_call / item.rep_setup / item.rep_teardown

# ---------- 失败自动保存截图与 trace ----------
@pytest.fixture(autouse=True)
def _screenshot_and_trace_on_failure(request, context, page):
    """
    每条用例自动启用该 fixture：
    - 在用例开始前：启动 Playwright tracing（记录步骤快照/截图/源码）
    - 在用例结束后：若失败，则导出 trace.zip + 截图；若成功，则仅停止 tracing 不导出
    """
    # 启动 tracing：开启截图/快照/源码记录，便于后续使用 Trace Viewer 重放场景
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield  # 执行测试本体

    # 生成失败工件的文件名（包含测试名与时间戳）
    test_name = request.node.name.replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # 通过上面的 hook 附加的 rep_call 判断“执行阶段”是否失败
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:
        # 失败：保存整页截图与 trace.zip 到 artifacts/
        png_path = f"artifacts/{test_name}-{timestamp}.png"
        trace_path = f"artifacts/{test_name}-{timestamp}-trace.zip"
        page.screenshot(path=png_path, full_page=True)   # 整页截图更利于定位 UI 布局问题
        context.tracing.stop(path=trace_path)            # 导出 trace 文件，供 `playwright show-trace` 查看
    else:
        # 成功：停止 tracing，但不导出文件（节省磁盘空间）
        context.tracing.stop()

@pytest.fixture(autouse=True)
def ensure_logged_out(page):
    dashboard_Page = DashboardPage(page)

    yield dashboard_Page

    if dashboard_Page.userLoggedInCheck():
        dashboard_Page.logout()
        print("run logout process.")
        time.sleep(3) 

#—————————————————————Api fixtures——————————————————————
@pytest.fixture(scope="session")
def api_base_url() -> str:
    return os.getenv("API_BASE_URL", "https://rahulshettyacademy.com")


@pytest.fixture(scope="session")
def api_session() -> requests.Session:
    session = requests.Session()
    yield session
    session.close()    

@pytest.fixture(scope="session")
def login_api(api_base_url, api_session):
    return LoginAPI(base_url=api_base_url, session=api_session)

@pytest.fixture(scope="session")
def userApi_Cred(login_api):
    creds = JsonReader().get_user_credentials()
    return login_api.login(creds["login_email"], creds["login_password"])        
