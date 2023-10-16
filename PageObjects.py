from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from time import sleep
class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def override_over_timeout(self, timeout):
        self.driver.implicitly_wait(timeout)

    # Common actions for browser
    def open_page_by_url(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
    
    def get_page_title(self):
        return self.driver.title

    def get_page_url(self):
        return self.driver.current_url

    def get_page_sourse(self):
        return self.driver.page_source

    def back_to_page(self):
        self.driver.back()

    def forward_to_page(self):
        self.driver.forward()

    def refresh_current_page(self):
        self.driver.refresh()

    def open_new_tab_with_url(self, url):
        self.driver.execute_script("window.open()")
        self.driver.switch_to.window('new')
        self.driver.get(url)

    def select_to_new_tab(self):
        self.driver.switch_to.window('new')
        sleep(1)

    def select_to_main_tab(self):
        self.driver.switch_to.window('main')

    def select_to_tab_by_title(self, title):
        self.driver.switch_to.window(title)

    def close_the_currect_tab(self):
        self.driver.execute_script("window.close()")
        self.select_to_main_tab()

    def scroll_up_to_the_top(self):
        self.driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")

    def scroll_down_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_middle_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")

    # handle alert
    def wait_for_alert_presence(self) -> Alert:
        return WebDriverWait(self.driver, 30).until(ExpectedConditions.alert_is_present())

    def accept_alert(self):
        self.wait_for_alert_presence().accept()

    def cancel_alert(self):
        self.wait_for_alert_presence().dismiss()

    def get_alert_text(self):
        return self.wait_for_alert_presence().text

    def send_keys_to_alert(self, value):
        self.wait_for_alert_presence().send_keys(value)
    
    # handle dynamic locator
    def get_locator(self, locator):
        if (locator.startswith('xpath') or locator.startswith('Xpath') or locator.startswith('XPATH')):
            locator = locator[6:]
        elif (locator.startswith('css') or locator.startswith('Css') or locator.startswith('CSS')):
            locator = locator[4:]
        elif (locator.startswith('name') or locator.startswith('Name') or locator.startswith('Name')):
            locator = locator[5:]
        elif (locator.startswith('class') or locator.startswith('Class') or locator.startswith('CLASS')):
            locator = locator[6:]
        else:
            RuntimeError('Locator type is not supported!')
        return locator
    
    def get_locator(self, locator, *dynamic_args):
        locator = locator.format(*dynamic_args)
        if (locator.startswith('xpath') or locator.startswith('Xpath') or locator.startswith('XPATH')):
            locator = locator[6:]
        elif (locator.startswith('css') or locator.startswith('Css') or locator.startswith('CSS')):
            locator = locator[4:]
        elif (locator.startswith('name') or locator.startswith('Name') or locator.startswith('Name')):
            locator = locator[5:]
        elif (locator.startswith('class') or locator.startswith('Class') or locator.startswith('CLASS')):
            locator = locator[6:]
        else:
            RuntimeError('Locator type is not supported!')
        return locator

    # get web element
    def get_web_element(self, locator) -> WebElement:
        return self.driver.find_element(By.XPATH, self.get_locator(locator))
    
    def get_web_element(self, locator, *dynamic_args) -> WebElement:
        return self.driver.find_element(By.XPATH, self.get_locator(locator, dynamic_args))
    
    def get_web_elements(self, locator):
        return self.driver.find_elements(By.XPATH, self.get_locator(locator))

    def get_web_elements(self, locator, *dynamic_args):
        return self.driver.find_elements(By.XPATH, self.get_locator(locator, dynamic_args))

    # common actions for elements
    def scroll_to_element_ontop_by_js(self, locator):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', self.get_web_element(locator))

    def scroll_to_element_ontop_by_js(self, locator, *dynamic_args):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', self.get_web_element(locator, *dynamic_args))

    def scroll_to_element_ondown_by_js(self, locator):
        self.driver.execute_script('arguments[0].scrollIntoView(false);', self.get_web_element(locator))

    def scroll_to_element_ondown_by_js(self, locator, *dynamic_args):
        self.driver.execute_script('arguments[0].scrollIntoView(false);', self.get_web_element(locator, *dynamic_args))

    def switch_to_frame_by_locator(self, locator):
        name_attribute_value = self.get_attribute_value_by_locator("name", locator)
        self.driver.switch_to.frame(name_attribute_value)

    def switch_to_frame_by_locator(self, locator, *dynamic_args):
        name_attribute_value = self.get_attribute_value_by_locator("name", locator, *dynamic_args)
        self.driver.switch_to.frame(name_attribute_value)

    def click_to_element_by_locator(self, locator):
        self.scroll_to_element_ontop_by_js(locator)
        self.get_web_element(locator).click()

    def click_to_element_by_locator(self, locator, *dynamic_args):
        self.scroll_to_element_ontop_by_js(locator, *dynamic_args)
        self.get_web_element(locator, *dynamic_args).click()

    def click_to_element_if_visible(self, locator):
        self.scroll_to_element_ontop_by_js(locator)
        status = self.get_web_element(locator).is_displayed()
        if (status == True):
            self.click_to_element_by_locator(locator)

    def click_to_element_if_visible(self, locator, *dynamic_args):
        self.scroll_to_element_ontop_by_js(locator, *dynamic_args)
        status = self.get_web_element(locator, *dynamic_args).is_displayed()
        if (status == True):
            self.click_to_element_by_locator(locator, *dynamic_args)

    def send_keys_to_element_by_locator(self, value, locator):
        self.scroll_to_element_ontop_by_js(locator)
        element = self.get_web_element(locator)
        element.clear()
        element.send_keys(value)

    def send_keys_to_element_by_locator(self, value, locator, *dynamic_args):
        self.scroll_to_element_ontop_by_js(locator, *dynamic_args)
        element = self.get_web_element(locator, *dynamic_args)
        element.clear()
        element.send_keys(value)

    def send_keys_to_date_textbox(self, value, locator, *dynamic_args):
        pass
        # waiting remove attribute function

    def select_item_in_default_dropdown(self, option_text, locator):
        self.scroll_to_element_ontop_by_js(locator)
        select = Select(self.get_web_element(locator))
        select.select_by_visible_text(option_text)

    def select_item_in_default_dropdown(self, option_text, locator, *dynamic_args):
        self.scroll_to_element_ontop_by_js(locator, *dynamic_args)
        select = Select(self.get_web_element(locator, *dynamic_args))
        select.select_by_visible_text(option_text)

    def select_custom_dropdown(self, parent_locator, child_locator, expected_item):
        self.click_to_element_by_locator(parent_locator)
        self.wait_for_all_element_presence(child_locator)
        element_count = self.get_element_count(child_locator)
        for index in range [1, element_count]:
            text = self.get_element_text((child_locator)[index])
            if(text == expected_item):
                self.scroll_to_element_ontop_by_js((child_locator)[index])
                self.click_to_element_by_locator((child_locator)[index])
                break

    # common actions to get value
    def get_element_count(self, locator):
        return len(self.get_web_elements(locator))

    def get_element_count(self, locator, *dynamic_args):
        return len(self.get_web_elements(locator, *dynamic_args))

    def get_attribute_value_by_locator(self, attribute_name, locator):
        return self.get_web_element(locator).get_attribute(attribute_name)

    def get_attribute_value_by_locator(self, attribute_name, locator, *dynamic_args):
        return self.get_web_element(locator, *dynamic_args).get_attribute(attribute_name)

    def get_element_text(self, locator):
        return self.get_web_element(locator).text

    def get_element_text(self, locator, *dynamic_args):
        return self.get_web_element(locator, *dynamic_args).text

    def get_default_text_in_textbox(self, locator):
        return self.get_web_element(locator).get_attribute("value")

    def get_default_text_in_textbox(self, locator, *dynamic_args):
        return self.get_web_element(locator, *dynamic_args).get_attribute("value")

    # common wait functions
    def wait_for_all_element_presence(self, locator):
        explicit_wait = WebDriverWait(self.driver, 30)
        explicit_wait.until(ExpectedConditions.presence_of_all_elements_located(self.get_locator(locator)))

    def wait_for_all_element_presence(self, locator, *dynamic_args):
        explicit_wait = WebDriverWait(self.driver, 30)
        explicit_wait.until(ExpectedConditions.presence_of_all_elements_located(self.get_locator(locator, *dynamic_args)))

    def wait_for_element_visible(self, locator):
        explicit_wait = WebDriverWait(self.driver, 30)
        explicit_wait.until(ExpectedConditions.visibility_of_element_located((self.get_locator(locator))))

    def wait_for_element_visible(self, locator, *dynamic_args):
        explicit_wait = WebDriverWait(self.driver, 30)
        explicit_wait.until(ExpectedConditions.visibility_of_element_located((self.get_locator(locator, *dynamic_args))))


class LoginPage(BasePage):
    def __init__(self, driver):
        self.driver = driver

class HomePage(BasePage):
    def __init__(self, driver):
        self.driver = driver

class MailPage(BasePage):
    def __init__(self, driver):
        self.driver = driver