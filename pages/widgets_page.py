import random
import time
from typing import Tuple, Any, List

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from generator.generator import generated_color, generated_date
from locators.widgets_page_locators import AccordianPageLocators, AutoCompletePageLocators, DatePickerPageLocators, \
    SliderPageLocators, ProgressBarPageLocators, TabsPageLocators, ToolTipsPageLocators, MenuPageLocators, \
    SelectMenuLocators
from pages.base_page import BasePage


class AccordianPage(BasePage):
    locators = AccordianPageLocators()

    # @allure.step('check accordian widget')
    def check_accordian(self, accordian_num):
        accordian = {'first':
                         {'title': self.locators.SECTION_FIRST,
                          'content': self.locators.SECTION_CONTENT_FIRST},
                     'second':
                         {'title': self.locators.SECTION_SECOND,
                          'content': self.locators.SECTION_CONTENT_SECOND},
                     'third':
                         {'title': self.locators.SECTION_THIRD,
                          'content': self.locators.SECTION_CONTENT_THIRD},
                     }

        section_title = self.element_is_visible(accordian[accordian_num]['title'])
        section_title.click()
        try:
            section_content = self.element_is_visible(accordian[accordian_num]['content']).text
        except TimeoutException:
            section_title.click()
            section_content = self.element_is_visible(accordian[accordian_num]['content']).text
        return [section_title.text, len(section_content)]


class AutoCompletePage(BasePage):
    locators = AutoCompletePageLocators()

    # @allure.step('fill multi autocomplete input')
    def fill_input_multi(self):
        colors = random.sample(next(generated_color()).color_name, k=random.randint(2, 5))
        for color in colors:
            input_multi = self.element_is_clickable(self.locators.MULTI_INPUT)
            input_multi.send_keys(color)
            input_multi.send_keys(Keys.ENTER)
        return colors

    #     # @allure.step('remove value from multi autocomplete')
    def remove_value_from_multi(self):
        count_value_before = len(self.elements_are_present(self.locators.MULTI_VALUE))
        remove_button_list = self.element_are_visible(self.locators.MULTI_VALUE_REMOVE)
        for value in remove_button_list:
            value.click()
            break
        count_value_after = len(self.elements_are_present(self.locators.MULTI_VALUE))
        return count_value_before, count_value_after

    #     # @allure.step('check colors in multi autocomplete')
    def check_color_in_multi(self):
        color_list = self.elements_are_present(self.locators.MULTI_VALUE)
        colors = []
        for color in color_list:
            colors.append(color.text)
        return colors

    #     # @allure.step('fill single autocomplete input')
    def fill_input_single(self):
        color = random.sample(next(generated_color()).color_name, k=1)
        input_single = self.element_is_clickable(self.locators.SINGLE_INPUT)
        input_single.send_keys(color)
        input_single.send_keys(Keys.ENTER)
        return color[0]

    # @allure.step('check color in single autocomplete')
    def check_color_in_single(self):
        color = self.element_is_visible(self.locators.SINGLE_VALUE)
        return color.text


class DatePickerPage(BasePage):
    locators = DatePickerPageLocators()

    # @allure.step('change date')
    def select_date(self):
        date = next(generated_date())
        input_date = self.element_is_visible(self.locators.DATE_INPUT)
        value_date_before = input_date.get_attribute('value')
        input_date.click()
        self.set_date_by_text(self.locators.DATE_SELECT_MONTH, date.month)
        self.set_date_by_text(self.locators.DATE_SELECT_YEAR, date.year)
        self.set_date_item_from_list(self.locators.DATE_SELECT_DAY_LIST, date.day)
        value_date_after = input_date.get_attribute('value')
        return value_date_before, value_date_after

    # @allure.step('change select date and time')
    def select_date_and_time(self):
        date = next(generated_date())
        input_date = self.element_is_visible(self.locators.DATE_AND_TIME_INPUT)
        value_date_before = input_date.get_attribute('value')
        input_date.click()
        self.element_is_clickable(self.locators.DATE_AND_TIME_MONTH).click()
        self.set_date_item_from_list(self.locators.DATE_AND_TIME_MONTH_LIST, date.month)
        self.element_is_clickable(self.locators.DATE_AND_TIME_YEAR).click()
        self.set_date_item_from_list(self.locators.DATE_AND_TIME_YEAR_LIST, '2025')
        self.set_date_item_from_list(self.locators.DATE_SELECT_DAY_LIST, date.day)
        self.set_date_item_from_list(self.locators.DATE_AND_TIME_TIME_LIST, date.time)
        input_date_after = self.element_is_visible(self.locators.DATE_AND_TIME_INPUT)
        value_date_after = input_date_after.get_attribute('value')
        return value_date_before, value_date_after

    # @allure.step('select date by text')
    def set_date_by_text(self, element, value):
        select = Select(self.element_is_present(element))
        select.select_by_visible_text(value)

    # @allure.step('select date item from list')
    def set_date_item_from_list(self, elements, value):
        item_list = self.elements_are_present(elements)
        for item in item_list:
            if item.text == value:
                item.click()
                break


class SliderPage(BasePage):
    locators = SliderPageLocators()

    # @allure.step('change slider value')
    def change_slider_value(self):
        value_before = self.element_is_visible(self.locators.SLIDER_VALUE).get_attribute('value')
        slider_input = self.element_is_visible(self.locators.INPUT_SLIDER)
        self.action_drag_and_drop_by_offset(slider_input, random.randint(1, 100), 0)
        value_after = self.element_is_visible(self.locators.SLIDER_VALUE).get_attribute('value')
        return value_before, value_after


class ProgressBarPage(BasePage):
    locators = ProgressBarPageLocators()

    # @allure.step('change progress bar value')
    def change_progress_bar_value(self):
        value_before = self.element_is_present(self.locators.PROGRESS_BAR_VALUE).text
        progress_bar_button = self.element_is_clickable(self.locators.PROGRESS_BAR_BUTTON)
        progress_bar_button.click()
        time.sleep(random.randint(4, 6))
        progress_bar_button.click()
        value_after = self.element_is_present(self.locators.PROGRESS_BAR_VALUE).text
        return value_before, value_after


class TabsPage(BasePage):
    locators = TabsPageLocators()

    # @allure.step('check tabs')
    def check_tabs(self, name_tab):
        tabs = {'what':
                    {'title': self.locators.TABS_WHAT,
                     'content': self.locators.TABS_WHAT_CONTENT},
                'origin':
                    {'title': self.locators.TABS_ORIGIN,
                     'content': self.locators.TABS_ORIGIN_CONTENT},
                'use':
                    {'title': self.locators.TABS_USE,
                     'content': self.locators.TABS_USE_CONTENT},
                'more':
                    {'title': self.locators.TABS_MORE,
                     'content': self.locators.TABS_MORE_CONTENT},
                }

        button = self.element_is_visible(tabs[name_tab]['title'])
        button.click()
        what_content = self.element_is_visible(tabs[name_tab]['content']).text
        return button.text, len(what_content)


class ToolTipsPage(BasePage):
    locators = ToolTipsPageLocators()

    # @allure.step('get text from tool tip')
    def get_text_from_tool_tips(self, hover_elem, wait_elem):
        element = self.element_is_present(hover_elem)
        self.action_move_to_element(element)
        time.sleep(0.3)
        self.element_is_visible(wait_elem)

        tool_tip_text = self.element_is_visible(self.locators.TOOL_TIPS_INNERS)
        text = tool_tip_text.text
        return text

    # @allure.step('check tool tip')
    def check_tool_tips(self):
        tool_tip_text_button = self.get_text_from_tool_tips(self.locators.BUTTON, self.locators.TOOL_TIP_BUTTON)
        tool_tip_text_field = self.get_text_from_tool_tips(self.locators.FIELD, self.locators.TOOL_TIP_FIELD)
        tool_tip_text_contrary = self.get_text_from_tool_tips(self.locators.CONTRARY_LINK,
                                                              self.locators.TOOL_TIP_CONTRARY)
        tool_tip_text_section = self.get_text_from_tool_tips(self.locators.SECTION_LINK, self.locators.TOOL_TIP_SECTION)
        return tool_tip_text_button, tool_tip_text_field, tool_tip_text_contrary, tool_tip_text_section


class MenuPage(BasePage):
    locators = MenuPageLocators()

    # @allure.step('check menu item')
    def check_menu(self):
        menu_item_list = self.elements_are_present(self.locators.MENU_ITEM_LIST)
        data = []
        for item in menu_item_list:
            self.action_move_to_element(item)
            data.append(item.text)
        return data


class SelectMenuPage(BasePage):
    locators = SelectMenuLocators()

    # @allure.step("Selecting random options in select menu")
    def check_select_value(self) -> tuple[str, Any]:
        single_select_values = [
            "Group 1, option 1",
            "Group 1, option 2",
            "Group 2, option 1",
            "Group 2, option 2",
            "A root option",
            "Another root option"
        ]
        random_value = single_select_values[random.randint(0, 5)]
        single_select = self.is_visible('css', self.locators.SELECT_VALUE_DROPDOWN, "Select value input")
        single_select.send_keys(random_value)
        single_select.send_keys(Keys.RETURN)
        current_value = self.is_present('xpath', self.locators.SELECT_VALUE_DROPDOWN_RESULT, "Select value result").text
        return random_value, current_value

    # @allure.step("Selecting one option in select menu")
    def check_one_value(self) -> tuple[str, Any]:
        select_one_values = ["Dr.", "Mr.", "Mrs.", "Ms.", "Prof.", "Other"]
        random_select_one_value = select_one_values[random.randint(0, 5)]
        select_one = self.is_visible('css', self.locators.SELECT_ONE_DROPDOWN, "Select one input")
        select_one.send_keys(random_select_one_value)
        select_one.send_keys(Keys.RETURN)
        current_select_one_value = self.is_present('xpath', self.locators.SELECT_ONE_DROPDOWN_RESULT,
                                                   "Select one result").text
        return random_select_one_value, current_select_one_value

    # @allure.step("Selecting in old style select")
    def check_old_style_select(self) -> tuple[Any, Any]:
        color_names = {
            "1": "Blue", "2": "Green", "3": "Yellow", "4": "Purple", "5": "Black", "6": "White", "7": "Voilet",
            "8": "Indigo", "9": "Magenta",
            "10": "Aqua"
        }
        random_value = str(random.randint(1, 10))
        old_select = self.is_visible('css', self.locators.OLD_SELECT, "Getting old style select")
        Select(old_select).select_by_value(random_value)
        selected_colors_list = Select(old_select).all_selected_options
        selected_colors = self.get_text_from_webelements(selected_colors_list)
        return color_names[random_value].lower(), selected_colors[0]

    # @allure.step("Selecting in multiselect dropdown")
    def check_multiselect_dropdown(self) -> tuple[list[str], list[Any]]:
        color_names = ["Red", "Blue", "Green", "Black"]
        multiselect_dropdown = self.is_visible('css', self.locators.MULTISELECT_DROPDOWN,
                                               "Getting multiselect dropdown")
        for color in color_names:
            multiselect_dropdown.send_keys(color)
            multiselect_dropdown.send_keys(Keys.RETURN)
        selected_colors = self.are_present('css', self.locators.MULTISELECT_DROPDOWN_RESULTS, "Multiselect results")
        return color_names, [color.text for color in selected_colors]

    # @allure.step("Are items removed from selection")
    def are_multiselected_items_removed(self) -> bool:
        remove_buttons = self.are_visible('css', self.locators.REMOVE_ELEMENT_FROM_MULTISELECT,
                                          "Getting remove buttons")
        for button in remove_buttons:
            button.click()
            time.sleep(1)  # For some reason it is necessary to click each button
        try:
            self.are_visible('css', self.locators.MULTISELECT_DROPDOWN_RESULTS, "Multiselect results")
            return False
        except TimeoutException as error:
            print(f'{error}\n Items of multiselect dropdown are removed')
            return True

    #
    # @allure.step("Selecting in standard multiselect")
    def check_standart_multiselect(self) -> tuple[list[str], Any]:
        option_values = ["volvo", "saab", "opel", "audi"]
        standard_select = self.is_visible('css', self.locators.STANDART_SELECT, "Getting standard select")
        self.go_to_element(standard_select)
        for option in option_values:
            Select(standard_select).select_by_value(option)
        selected_options_list = Select(standard_select).all_selected_options
        selected_options = self.get_text_from_webelements(selected_options_list)
        return option_values, selected_options
