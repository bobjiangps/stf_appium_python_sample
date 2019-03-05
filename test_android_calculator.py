# -*- encoding:utf-8 -*-
import unittest
from appium import webdriver


class Login(unittest.TestCase):

    def setUp(self):
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '4.4.4',
            'deviceName': '0bad655c',
            # 'appPackage': 'com.android.calculator2',
            'appPackage': 'com.sec.android.app.popupcalculator',
            'appActivity': '.Calculator'
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def test_add(self):
        num_2 = self.driver.find_element_by_id('bt_02')
        num_6 = self.driver.find_element_by_id('bt_06')
        add_button = self.driver.find_element_by_id('bt_add')
        equal_button = self.driver.find_element_by_id('bt_equal')
        calc_text = self.driver.find_element_by_id('txtCalc')
        num_2.click()
        add_button.click()
        num_6.click()
        equal_button.click()
        actual_text = calc_text.text
        self.assertEqual(actual_text, "2+6\n=8. 轻敲两次以编辑。", "not equal, actual text is : %s" % actual_text)


if __name__ == '__main__':
    unittest.main()
