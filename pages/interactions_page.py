import random
import re
import time

import allure
import numpy as numpy

from locators.interactions_page_locators import SortablePageLocators, SelectablePageLocators, ResizablePageLocators, \
    DroppablePageLocators, DraggablePageLocators
from pages.base_page import BasePage


class SortablePage(BasePage):
    locators = SortablePageLocators()

    @allure.step('get sortable items')
    def get_sortable_items(self, elements):
        item_list = self.element_are_visible(elements)
        return [item.text for item in item_list]

    @allure.step('change list order')
    def change_list_order(self):
        self.element_is_visible(self.locators.TAB_LIST).click()
        order_before = self.get_sortable_items(self.locators.LIST_ITEM)
        item_list = random.sample(self.element_are_visible(self.locators.LIST_ITEM), k=2)
        item_what = item_list[0]
        item_where = item_list[1]
        self.action_drag_and_drop_to_element(item_what, item_where)
        order_after = self.get_sortable_items(self.locators.LIST_ITEM)
        return order_before, order_after

    @allure.step('change grade order')
    def change_grid_order(self):
        self.element_is_visible(self.locators.TAB_GRID).click()
        order_before = self.get_sortable_items(self.locators.GRID_ITEM)
        item_list = random.sample(self.element_are_visible(self.locators.GRID_ITEM), k=2)
        item_what = item_list[0]
        item_where = item_list[1]
        self.action_drag_and_drop_to_element(item_what, item_where)
        order_after = self.get_sortable_items(self.locators.GRID_ITEM)
        return order_before, order_after


class SelectablePage(BasePage):
    locators = SelectablePageLocators()

    @allure.step('click selectable item')
    def click_selectable_item(self, elements):
        item_list = self.element_are_visible(elements)
        random.sample(item_list, k=1)[0].click()

    @allure.step('select list item')
    def select_list_item(self):
        self.element_is_visible(self.locators.TAB_LIST).click()
        self.click_selectable_item(self.locators.LIST_ITEM)
        active_element = self.element_is_visible(self.locators.LIST_ITEM_ACTIVE)
        return active_element.text

    @allure.step('select grid item')
    def select_grid_item(self):
        self.element_is_visible(self.locators.TAB_GRID).click()
        self.click_selectable_item(self.locators.GRID_ITEM)
        active_element = self.element_is_visible(self.locators.GRID_ITEM_ACTIVE)
        return active_element.text


class ResizablePage(BasePage):
    locators = ResizablePageLocators()

    @allure.step('get px from width and height')
    def get_px_from_width_height(self, value_of_size):
        width = value_of_size.split(';')[0].split(':')[1].replace(' ', '')
        height = value_of_size.split(';')[1].split(':')[1].replace(' ', '')
        return width, height

    @allure.step('get max and min size')
    def get_max_min_size(self, element):
        size = self.element_is_present(element)
        size_value = size.get_attribute('style')
        return size_value

    @allure.step('change size resizable box')
    def change_size_resizable_box(self):
        self.action_drag_and_drop_by_offset(self.element_is_present(self.locators.RESIZABLE_BOX_HANDLE), 400, 200)
        max_size = self.get_px_from_width_height(self.get_max_min_size(self.locators.RESIZABLE_BOX))
        self.action_drag_and_drop_by_offset(self.element_is_present(self.locators.RESIZABLE_BOX_HANDLE), -500, -300)
        min_size = self.get_px_from_width_height(self.get_max_min_size(self.locators.RESIZABLE_BOX))
        return max_size, min_size

    @allure.step('change size resizable')
    def change_size_resizable(self):
        self.action_drag_and_drop_by_offset(self.element_is_visible(self.locators.RESIZABLE_HANDLE),
                                            random.randint(1, 300), random.randint(1, 300))
        max_size = self.get_px_from_width_height(self.get_max_min_size(self.locators.RESIZABLE))
        self.action_drag_and_drop_by_offset(self.element_is_visible(self.locators.RESIZABLE_HANDLE),
                                            random.randint(-200, -1), random.randint(-200, -1))
        min_size = self.get_px_from_width_height(self.get_max_min_size(self.locators.RESIZABLE))
        return max_size, min_size


class DroppablePage(BasePage):
    locators = DroppablePageLocators()

    @allure.step('drop simple div')
    def drop_simple(self):
        self.element_is_visible(self.locators.SIMPLE_TAB).click()
        drag_div = self.element_is_visible(self.locators.DRAG_ME_SIMPLE)
        drop_div = self.element_is_visible(self.locators.DROP_HERE_SIMPLE)
        self.action_drag_and_drop_to_element(drag_div, drop_div)
        return drop_div.text

    @allure.step('drop accept div')
    def drop_accept(self):
        self.element_is_visible(self.locators.ACCEPT_TAB).click()
        acceptable_div = self.element_is_visible(self.locators.ACCEPTABLE)
        not_acceptable_div = self.element_is_visible(self.locators.NOT_ACCEPTABLE)
        drop_div = self.element_is_visible(self.locators.DROP_HERE_ACCEPT)
        self.action_drag_and_drop_to_element(not_acceptable_div, drop_div)
        drop_text_not_accept = drop_div.text
        self.action_drag_and_drop_to_element(acceptable_div, drop_div)
        drop_text_accept = drop_div.text
        return drop_text_not_accept, drop_text_accept

    @allure.step('drop prevent propogation div')
    def drop_prevent_propogation(self):
        self.element_is_visible(self.locators.PREVENT_TAB).click()
        drag_div = self.element_is_visible(self.locators.DRAG_ME_PREVENT)
        not_greedy_inner_box = self.element_is_visible(self.locators.NOT_GREEDY_INNER_BOX)
        greedy_inner_box = self.element_is_visible(self.locators.GREEDY_INNER_BOX)
        self.action_drag_and_drop_to_element(drag_div, not_greedy_inner_box)
        text_not_greedy_box = self.element_is_visible(self.locators.NOT_GREEDY_DROP_BOX_TEXT).text
        text_not_greedy_inner_box = not_greedy_inner_box.text
        self.action_drag_and_drop_to_element(drag_div, greedy_inner_box)
        text_greedy_box = self.element_is_visible(self.locators.GREEDY_DROP_BOX_TEXT).text
        text_greedy_inner_box = greedy_inner_box.text
        return text_not_greedy_box, text_not_greedy_inner_box, text_greedy_box, text_greedy_inner_box

    @allure.step('drag revert draggable div')
    def drop_revert_draggable(self, type_drag):
        drags = {
            'will':
                {'revert': self.locators.WILL_REVERT, },
            'not_will':
                {'revert': self.locators.NOT_REVERT},
        }
        self.element_is_visible(self.locators.REVERT_TAB).click()
        revert = self.element_is_visible(drags[type_drag]['revert'])
        drop_div = self.element_is_visible(self.locators.DROP_HERE_REVERT)
        self.action_drag_and_drop_to_element(revert, drop_div)
        position_after_move = revert.get_attribute('style')
        time.sleep(1)
        position_after_revert = revert.get_attribute('style')
        return position_after_move, position_after_revert


class DraggablePage(BasePage):
    locators = DraggablePageLocators()

    @allure.step('get before and after positions')
    def get_before_and_after_position(self, drag_element):
        self.action_drag_and_drop_by_offset(drag_element, random.randint(0, 50), random.randint(0, 50))
        before_position = drag_element.get_attribute('style')
        self.action_drag_and_drop_by_offset(drag_element, random.randint(0, 50), random.randint(0, 50))
        after_position = drag_element.get_attribute('style')
        return before_position, after_position

    @allure.step('simple drag and drop')
    def simple_drag_box(self):
        self.element_is_visible(self.locators.SIMPLE_TAB).click()
        drag_div = self.element_is_visible(self.locators.DRAG_ME)
        before_position, after_position = self.get_before_and_after_position(drag_div)
        return before_position, after_position

    @allure.step('get top position')
    def get_top_position(self, positions):
        return re.findall(r'\d[0-9]|\d', positions.split(';')[2])

    @allure.step('get left position')
    def get_left_position(self, positions):
        return re.findall(r'\d[0-9]|\d', positions.split(';')[1])

    @allure.step('drag only_x')
    def axis_restricted_x(self):
        self.element_is_visible(self.locators.AXIS_TAB).click()
        only_x = self.element_is_visible(self.locators.ONLY_X)
        position_x = self.get_before_and_after_position(only_x)
        top_x_before = self.get_top_position(position_x[0])
        top_x_after = self.get_top_position(position_x[1])
        left_x_before = self.get_left_position(position_x[0])
        left_x_after = self.get_left_position(position_x[1])
        return [top_x_before, top_x_after], [left_x_before, left_x_after]

    @allure.step('drag only_y')
    def axis_restricted_y(self):
        self.element_is_visible(self.locators.AXIS_TAB).click()
        only_y = self.element_is_visible(self.locators.ONLY_Y)
        position_x = self.get_before_and_after_position(only_y)
        top_y_before = self.get_top_position(position_x[0])
        top_y_after = self.get_top_position(position_x[1])
        left_y_before = self.get_left_position(position_x[0])
        left_y_after = self.get_left_position(position_x[1])
        return [top_y_before, top_y_after], [left_y_before, left_y_after]

    @allure.step("Dragging restricted draggable")
    def drag_restricted_draggable(self):
        self.is_visible('css', self.locators.CONTAINER_RESTRICTED_TAB, "Switching tab").click()
        r_box = self.is_visible('css', self.locators.RESTRICTED_BOX, "Get restricted box")
        r_text = self.is_visible('css', self.locators.RESTRICTED_TEXT, "Get restricted text")
        self.drag_with_cursor(r_box, 1050, 650)
        box_bot_right_clamp = tuple(r_box.location.values())
        self.go_to_element(r_text)
        self.drag_with_cursor(r_text, 1000, 500)
        text_bot_right_clamp = tuple(r_text.location.values())
        return box_bot_right_clamp, text_bot_right_clamp

    @allure.step("Dragging cursor style draggable")
    def drag_cursor_style_draggable(self):
        self.is_visible('css', self.locators.CURSOR_STYLE_TAB, "Switching tab").click()
        box_center = self.is_visible('css', self.locators.CURSOR_CENTER, "Getting center cursor")
        box_top_left = self.is_visible('css', self.locators.CURSOR_TOP_LEFT, "Getting top left cursor")
        box_bottom = self.is_visible('css', self.locators.CURSOR_BOTTOM, "Getting bottom cursor")
        draggable_boxes = [box_center, box_top_left, box_bottom]
        diffs = []
        for box in draggable_boxes:
            initial_loc = tuple(box.location.values())
            self.drag_and_drop_to_location(box, 200, 0)
            updated_loc = tuple(box.location.values())
            diff = numpy.subtract(updated_loc, initial_loc)
            diffs.append(diff[1])
        return diffs

    @allure.step("Dragging with box restricted axis")
    def drag_axis_restricted_draggable(self):
        self.is_visible('css', self.locators.AXIS_RESTRICTED_TAB, "Switching tab").click()
        x_draggable = self.is_visible('css', self.locators.DRAG_BOX_ONLY_X, "Getting only x draggable")
        y_draggable = self.is_visible('css', self.locators.DRAG_BOX_ONLY_Y, "Getting only y draggable")

        random_offset_x = random.randint(100, 200)
        random_offset_y = random.randint(100, 200)
        self.drag_and_drop_to_location(x_draggable, random_offset_x, random_offset_y)
        self.drag_and_drop_to_location(y_draggable, random_offset_x, random_offset_y)
        updated_x_draggable_location = tuple(x_draggable.location.values())
        updated_y_draggable_location = tuple(y_draggable.location.values())
        return updated_x_draggable_location, updated_y_draggable_location

    @allure.step("Dragging simple draggable")
    def drag_simple_draggable(self):
        self.is_visible('css', self.locators.SIMPLE_T, "Switching tab").click()
        drag_box = self.is_visible('css', self.locators.DRAG_BOX, "Getting draggable")
        initial_drag_box_loc = tuple(drag_box.location.values())
        random_offset_x = random.randint(100, 300)
        random_offset_y = random.randint(100, 300)
        self.drag_and_drop_to_location(drag_box, random_offset_x, random_offset_y)
        updated_drag_box_loc = tuple(drag_box.location.values())
        return initial_drag_box_loc, updated_drag_box_loc