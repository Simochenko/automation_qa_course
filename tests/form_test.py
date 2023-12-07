import time

import allure

from pages.form_page import FormPage


@allure.suite('Forms')
class TestForm:
    @allure.feature('FormPage')
    class TestFormPage:
        @allure.title('Check form')
        def test_form(self, driver):
            form_page = FormPage(driver, 'https://demoqa.com/automation-practice-form')
            form_page.open()
            p = form_page.fill_form_fields()
            result = form_page.form_result()
            assert [(p.firstname.encode('utf-8') + ' '.encode('utf-8') + p.lastname.encode('utf-8')),
                    p.email.encode('utf-8')] == [result[0].encode('utf-8'), result[1].encode('utf-8')],\
                'the form has not been filled'
