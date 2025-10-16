# pages/base_page.py — Page Object 基类
# 目的：把页面通用能力（导航、等待、语义化操作、常用断言）集中封装

import re

from playwright.sync_api import Page, expect  # Page：浏览器标签页对象；expect：官方断言/等待

class BasePage:
    def __init__(self, page: Page):
        """
        :param page: Playwright 的 Page 对象（一次测试一个）
        :param base_url: 被测系统根地址（通过 fixture 注入，不写死）
        """
        self.page = page

    def goto(self, path: str = "/"):
        """
        统一导航方法：支持绝对 URL 和相对路径
        - 绝对 URL：直接跳转
        - 相对路径：自动拼接 base_url
        """
        if path.startswith("http"):
            self.page.goto(path)
        else:
            self.page.goto(f"{self.base_url}{path}")

    def expect_title_contains(self, text: str):
        """
        断言标题包含给定文本（忽略大小写），使用 expect 的等待式断言
        """
        pattern = re.compile(f".*{re.escape(text)}.*", re.IGNORECASE)
        expect(self.page).to_have_title(pattern)

    def wait_for_url_contains(self, fragment: str):
        """
        等待 URL 包含特定片段（使用 ** 通配）
        """
        self.page.wait_for_url(f"**{fragment}**")

    def click_by_role(self, role: str, name: str):
        """
        语义化点击：优先可访问性定位（更稳、更易维护）
        """
        self.page.get_by_role(role, name=name).click()

    def fill_by_label(self, label: str, value: str, exact: bool = True):
        """
        语义化输入：通过 label 文本定位输入框
        """
        self.page.get_by_label(label, exact=exact).fill(value)

    def click_and_verify_title(self,locator, expected_title: str, timeout: int = 5000):
        """
        点击一个链接，自动判断是否打开新标签页或当前页跳转，并验证标题。

        :param page: 当前 Page 对象
        :param locator: 定位器字符串或 Locator 对象
        :param expected_title: 期望的标题关键字
        :param timeout: 等待超时时间（毫秒）
        """
        # 保存点击前的所有页面
        context = self.page.context
        existing_pages = set(context.pages)

        # 如果 locator 是字符串，就转换成 locator 对象
        link = self.page.locator(locator) if isinstance(locator, str) else locator

        # 点击并尝试捕获新页
        with context.expect_page(timeout=timeout) as new_page_event:
            link.click()

        new_page = None
        try:
            new_page = new_page_event.value  # 如果确实打开了新页面
        except Exception:
            pass

        # 情况 ①：打开了新标签页
        if new_page and new_page not in existing_pages:
            new_page.wait_for_load_state("domcontentloaded")
            print(f"➡️ 新页面打开: {new_page.url}")
            pattern = re.compile(f".*{re.escape(expected_title)}.*", re.IGNORECASE)
            expect(new_page).to_have_title(pattern,
                timeout=timeout
            )

            
            print(f"✅ 验证通过: 标题包含 '{expected_title}'")

            new_page.close()
            print("🧹 已关闭新页面")
            return "new_page"

        # 情况 ②：当前页跳转
        else:
            self.page.wait_for_load_state("domcontentloaded")
            current_title = self.page.title()
            if expected_title in current_title:
                print(f"✅ 当前页跳转验证通过: 标题为 '{current_title}'")
            else:
                print(f"❌ 当前页标题不匹配: '{current_title}'")
            return "same_page"
        
    def clearInput(self, locator):
        locator.clear()


    
    
