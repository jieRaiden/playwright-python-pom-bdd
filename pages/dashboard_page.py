from collections import defaultdict
import time
from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)  # 初始化基类
        # 定位器定义：尽量语义化（label/role），退而求其次 data-testid / CSS
        self.menuBarBtn = self.page.locator("//ul//button[@routerlink]")
        self.logoutBtn = self.page.get_by_role("button", name=" Sign Out ")
        self.cartNumberLocator = self.page.locator("button[routerlink='/dashboard/cart'] label")
        self.addedToCartMap = defaultdict(int)
        self.continue_Shopping_btn = self.page.locator("a[href='#/dashboard']")


    def logout(self):
        self.logoutBtn.click()
        

    def userLoggedInCheck(self):
        if self.logoutBtn.is_visible():
            return True
        else:
            return False
        
    def verifyUserLoggedin(self):
        assert(self.userLoggedInCheck())

    def navigateTo(self, pageTitle):
        target = self.menuBarBtn.filter(has_text=pageTitle)
        target.first.click()

    def addItemToCart(self, item:str):
        self.addToCartBtn = self.page.locator(f"//h5/b[text()='{item}']/../..//button[text()=' Add To Cart']")
        self.addToCartBtn.click()

        self.addedToCartMap[item] += 1

    def verifyCartNumber(self):
        self.addItemToCart("ZARA COAT 3")
        self.addItemToCart("ADIDAS ORIGINAL")
        self.addItemToCart("iphone 13 pro")
        time.sleep(3)
        y = sum(self.addedToCartMap.values())
        badge_value = self.cartNumberLocator.text_content(timeout=5000).strip()
        assert int(badge_value) == y

    def verifyItem_Dashboard_To_Detail(self):
        self.itemTitle = self.page.locator("//h5/b[text()]")
        self.itemPrice = self.page.locator("//h5/b[text()]/../..//following-sibling::div/div")
        self.viewBtn = self.page.locator("//button[text()=' View']")

        count = self.itemTitle.count()
        self.itemDetail_list = {}
        for x in range(count):
            title = self.itemTitle.nth(x).inner_text().strip()
            price = self.itemPrice.nth(x).inner_text().strip()
            self.itemDetail_list[title] = price
            self.viewBtn.nth(x).click()
            time.sleep(3)
            self.page.wait_for_url("**/product-details/**")

            self.itemTitle_DetailPage = self.page.locator("//h2[text()]").inner_text().strip()
            self.itemPrice_DetailPage = self.page.locator("//a[@routerlink]//following-sibling::div/h3").inner_text().strip()
            assert self.itemTitle_DetailPage == title
            print("Expected num: " + self.itemPrice_DetailPage)
            print("Actual num: " + price)
            assert self.itemPrice_DetailPage == price
            self.continue_Shopping_btn.click()
            self.page.wait_for_url("**/dash")
            





