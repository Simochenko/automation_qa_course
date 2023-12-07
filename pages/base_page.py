import time

import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.__wait = WebDriverWait(driver, 4, 1, ignored_exceptions=StaleElementReferenceException)

    @allure.step('Open a browser')
    def open(self):
        self.driver.get(self.url)

    @allure.step('Find a get selenium by')
    def __get_selenium_by(self, find_by: str) -> str:
        find_by = find_by.lower()
        locators = {
            'css': By.CSS_SELECTOR,
            'xpath': By.XPATH,
            'id': By.ID,
            'name': By.NAME,
            'tag': By.TAG_NAME,
            'partial_link': By.PARTIAL_LINK_TEXT,
            'link': By.LINK_TEXT,
            'class': By.CLASS_NAME
        }
        return locators[find_by]

    @allure.step('Find a visible element')
    def element_is_visible(self, locator, timeout=5):
        self.go_to_element(self.element_is_present(locator))
        return wait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    @allure.step('Find visible elements')
    def element_are_visible(self, locator, timeout=5):
        return wait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))

    @allure.step('Find a present element')
    def element_is_present(self, locator, timeout=5):
        return wait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Find present elements')
    def elements_are_present(self, locator, timeout=5):
        return wait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    @allure.step('Find a not visible element')
    def element_is_not_visible(self, locator, timeout=5):
        return wait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    @allure.step('Find clickable elements')
    def element_is_clickable(self, locator, timeout=5):
        return wait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    @allure.step('Go to specified element')
    def go_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    @allure.step('Double click')
    def action_double_click(self, element):
        action = ActionChains(self.driver)
        action.double_click(element)
        action.perform()

    @allure.step('Right click')
    def action_right_click(self, element):
        action = ActionChains(self.driver)
        action.context_click(element)
        action.perform()

    @allure.step('Remove footer')
    def remove_footer(self):
        self.driver.execute_script("document.getElementsByTagName('footer')[0].remove();")
        ban1 = self.driver.find_element_by_xpath("//*[@id=\"close-fixedban\"]")
        ban2 = self.driver.find_element_by_xpath('//*[@id="fixedban"]')
        self.driver.execute_script("arguments[0].remove();arguments[1].remove();", ban1, ban2)

    @allure.step('Check opened new window or tab')
    def check_opened_new_window_or_tab(self):
        return self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step('Drag and drop by offset')
    def action_drag_and_drop_by_offset(self, element, x_coords, y_coords):
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(element, x_coords, y_coords)
        action.perform()

    @allure.step('Drag and drop element to element')
    def action_drag_and_drop_to_element(self, what, where):
        action = ActionChains(self.driver)
        action.drag_and_drop(what, where)
        action.perform()

    @allure.step('Move cursor to element')
    def action_move_to_element(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.perform()

    def is_visible(self, find_by: str, locator: str, locator_name=None) -> WebElement:
        return self.__wait.until(EC.visibility_of_element_located((self.__get_selenium_by(find_by), locator)),
                                 locator_name)

    def is_present(self, find_by: str, locator: str, locator_name=None) -> WebElement:
        return self.__wait.until(EC.presence_of_element_located((self.__get_selenium_by(find_by), locator)),
                                 locator_name)

    def get_text_from_webelements(self, elements: list[WebElement]) -> list[str]:
        return [element.text.lower() for element in elements]

    def are_visible(self, find_by: str, locator: str, locator_name=None) -> list[WebElement]:
        return self.__wait.until(EC.visibility_of_all_elements_located((self.__get_selenium_by(find_by), locator)),
                                 locator_name)

    def are_present(self, find_by: str, locator: str, locator_name=None) -> list[WebElement]:
        return self.__wait.until(EC.presence_of_all_elements_located((self.__get_selenium_by(find_by), locator)),
                                 locator_name)

    def drag_with_cursor(self, element, x_coord, y_coord):
        action = ActionBuilder(self.driver)
        action.pointer_action.click_and_hold(element)
        action.pointer_action.move_to_location(x_coord, y_coord)
        action.pointer_action.release()
        action.perform()

    def drag_and_drop_to_location(self, element: WebElement, x_cord: int, y_cord: int):
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(element, x_cord, y_cord)
        action.perform()