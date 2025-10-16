import time
from pages import dashboard_page
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage

class CartsPage(BasePage):
    def __init__(self, page, dashboard_page: DashboardPage):
        super().__init__(page)  # 初始化基类
        # 定位器定义：尽量语义化（label/role），退而求其次 data-testid / CSS
        self.countinue_Shopping_Btn = self.page.get_by_role("button", name="Continue Shopping")
        self.inCartItemCards = self.page.locator("//div[@class='cart']")
        self.checkoutBtn = self.page.get_by_role("button", name="Checkout")
        self.dashboard_Page = dashboard_page

    


