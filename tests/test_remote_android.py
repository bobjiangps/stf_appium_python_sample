# -*- encoding:utf-8 -*-
import unittest
import os
import yaml
import configparser
from appium import webdriver
from stf_api import StfDevices


class CalAdd(unittest.TestCase):

    def setUp(self):
        self.load_config()
        self.remote_device = StfDevices(self.ip)
        self.device_serial = self.remote_device.get_single_device()["serial"]
        print(self.device_serial)
        print(self.remote_device.rent_single_device(self.device_serial).text)
        self.remote_connect_url = self.remote_device.get_user_device_remote_connect_url(self.device_serial)
        os.system("adb connect " + self.remote_connect_url)
        self.load_caps()
        print(self.desired_caps)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)

    def tearDown(self):
        self.driver.quit()
        os.system("adb disconnect " + self.remote_connect_url)
        print(self.remote_device.return_rented_device(self.device_serial).text)

    def load_config(self):
        config_file = os.path.join(os.path.join(os.getcwd(), "config", "run_config.ini"))
        cf = configparser.ConfigParser()
        cf.read(config_file)
        self.ip = dict(cf.items("Run Test"))["host"]

    def load_caps(self):
        cap_file = open(os.path.join(os.getcwd(), "config", "caps.yaml"), "rb")
        result = yaml.load(cap_file)
        cap_file.close()
        for device in result.values():
            if device["deviceName"] == self.device_serial:
                self.desired_caps = device
                break

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
        expect_list = ["2+6\n=8. 轻敲两次以编辑。", "8. Editing"]
        self.assertTrue(actual_text in expect_list, "not equal, actual text is : %s" % actual_text)

