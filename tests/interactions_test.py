import allure

from pages.interactions_page import SortablePage, SelectablePage, ResizablePage, DroppablePage, DraggablePage


@allure.suite('Interactions')
class TestInteractions:
    @allure.feature('Sortable Page')
    class TestSortablePage:
        @allure.title('Check changed sortable list and grid')
        def test_sortable(self, driver):
            sortable_page = SortablePage(driver, 'https://demoqa.com/sortable')
            sortable_page.open()
            list_before, list_after = sortable_page.change_list_order()
            grid_before, grid_after = sortable_page.change_grid_order()
            assert list_before != list_after, 'the order of the list has not been changed'
            assert grid_before != grid_after, 'the order of the grid has not been changed'

    @allure.feature('Selectable Page')
    class TestSelectablePage:
        @allure.title('Check changed selectable list and grid')
        def test_selectable(self, driver):
            selectable_page = SelectablePage(driver, 'https://demoqa.com/selectable')
            selectable_page.open()
            item_list = selectable_page.select_list_item()
            item_grid = selectable_page.select_grid_item()
            assert len(item_list) > 0, "no elements were selected"
            assert len(item_grid) > 0, "no elements were selected"

    @allure.feature('Resizable Page')
    class TestResizablePage:
        @allure.title('Check changed resizable boxes')
        def test_resizable(self, driver):
            resizable_page = ResizablePage(driver, 'https://demoqa.com/resizable')
            resizable_page.open()
            max_box, min_box = resizable_page.change_size_resizable_box()
            max_resize, min_resize = resizable_page.change_size_resizable()
            assert ('500px', '300px') == max_box, "maximum size not equal to '500px', '300px'"
            assert ('150px', '150px') == min_box, "minimum size not equal to '150px', '150px'"
            assert min_resize != max_resize, "resizable has not been changed"

    @allure.feature('Droppable Page')
    class TestDroppablePage:
        @allure.title('Check simple droppable')
        def test_simple_droppable(self, driver):
            droppable_page = DroppablePage(driver, 'https://demoqa.com/droppable')
            droppable_page.open()
            text = droppable_page.drop_simple()
            assert text == 'Dropped!', "the elements has not been dropped"

        @allure.title('Check accept droppable')
        def test_accept_droppable(self, driver):
            droppable_page = DroppablePage(driver, 'https://demoqa.com/droppable')
            droppable_page.open()
            not_accept, accept = droppable_page.drop_accept()
            assert not_accept == 'Drop here', "the dropped element has been accepted"
            assert accept == 'Dropped!', "the dropped element has not been accepted"

        @allure.title('Check prevent propogation droppable')
        def test_prevent_propogation_droppable(self, driver):
            droppable_page = DroppablePage(driver, 'https://demoqa.com/droppable')
            droppable_page.open()
            not_greedy, not_greedy_inner, greedy, greedy_inner = droppable_page.drop_prevent_propogation()
            assert not_greedy == 'Dropped!', "the elements texts has not been changed"
            assert not_greedy_inner == 'Dropped!', "the elements texts has not been changed"
            assert greedy == 'Outer droppable', "the elements texts has been changed"
            assert greedy_inner == 'Dropped!', "the elements texts has not been changed"

        @allure.title('Check revert draggable droppable')
        def test_revert_draggable_droppable(self, driver):
            droppable_page = DroppablePage(driver, 'https://demoqa.com/droppable')
            droppable_page.open()
            will_after_move, will_after_revert = droppable_page.drop_revert_draggable('will')
            not_will_after_move, not_will_after_revert = droppable_page.drop_revert_draggable('not_will')
            assert will_after_move != will_after_revert, 'the elements has not reverted'
            assert not_will_after_move == not_will_after_revert, 'the elements has  reverted'

    @allure.feature("Draggable")
    class TestDraggablePage:
        @allure.title("Draggable test")
        def test_draggable(self, driver):
            draggable_page = DraggablePage(driver, 'https://demoqa.com/dragabble')
            draggable_page.open()
            X_ONLY_INITIAL_LOC = (851, 407)
            Y_ONLY_INITIAL_LOC = (569, 407)
            MAX_BOT_RIGHT_BOX_LOC = (934, 510)
            MAX_BOT_RIGHT_TEXT_LOC = (441, 711)
            x_only_loc, y_only_loc = draggable_page.drag_axis_restricted_draggable()
            assert x_only_loc[0] != X_ONLY_INITIAL_LOC[0] and x_only_loc[1] != X_ONLY_INITIAL_LOC[1], \
                "Validating x restricted draggable"
            assert y_only_loc[0] != Y_ONLY_INITIAL_LOC[0] and y_only_loc[1] != Y_ONLY_INITIAL_LOC[1], \
                "Validating y restricted draggable"

            initial_loc, updated_loc = draggable_page.drag_simple_draggable()
            assert updated_loc != initial_loc, "Validating that box is dragged"

            box_loc, text_loc = draggable_page.drag_restricted_draggable()
            assert box_loc != MAX_BOT_RIGHT_BOX_LOC, "Validating that box is constrained"
            assert text_loc != MAX_BOT_RIGHT_TEXT_LOC, "Validating that text is constrained"

            y_axis_deviations = draggable_page.drag_cursor_style_draggable()

            assert y_axis_deviations[0] in range(-10, 0), "Validating that center box has allowed deviation"
            assert y_axis_deviations[1] in range(0, 60), "Validating that center box has allowed deviation"
            assert y_axis_deviations[2] in range(-60, 0), "Validating that center box has allowed deviation"
