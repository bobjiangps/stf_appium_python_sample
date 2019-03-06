# -*- encoding:utf-8 -*-
import unittest
import os
from appium import webdriver
from stf_api import StfDevices


class Login(unittest.TestCase):

    def setUp(self):
        self.remote_device = StfDevices("10.109.1.65")
        self.device_serial = self.remote_device.get_single_device()["serial"]
        print(self.device_serial)
        print(self.remote_device.rent_single_device(self.device_serial).text)
        self.remote_connect_url = self.remote_device.get_user_device_remote_connect_url(self.device_serial)
        os.system("adb connect " + self.remote_connect_url)

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
        os.system("adb disconnect " + self.remote_connect_url)
        print(self.remote_device.return_rented_device(self.device_serial).text)

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
