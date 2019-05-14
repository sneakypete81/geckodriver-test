#!/usr/bin/env python3
import requests
import base64
import time
from pathlib import Path

BASE_URI = "http://localhost:4444"
US_ID = "c07d1a49-9894-49ff-a594-38960ede8fb9"


def main():
    print()
    gecko = GeckoDriver(BASE_URI)
    gecko.new_session()
    try:
        gecko.install_addon(Path("update_scanner-4.4.0-an.fx.xpi").resolve())
        gecko.set_context("chrome")

        button = gecko.find_element("#_" + US_ID + "_-browser-action")
        gecko.click_element(button)

        time.sleep(5)

        with open("screenshot.png", "wb") as f:
            f.write(base64.b64decode(gecko.take_screenshot()))

        input("Press <ENTER> to exit...")

    finally:
        gecko.delete_session()


class GeckoDriver:
    def __init__(self, base_uri):
        self.base_uri = base_uri
        self.session_id = None

    def new_session(self):
        print("New Session")
        resp = requests.post(
            self.base_uri + "/session",
            json={
                "capabilities": {
                    "alwaysMatch": {
                        "browserName": "firefox",
                        "moz:firefoxOptions": {
                            "prefs": {
                                "ui.popup.disable_autohide": True,
                            },
                        },
                    },
                    "firstMatch": [{}],
                },
            },
        )
        self.session_id = self._process_resp(resp)['value']['sessionId']

    def delete_session(self):
        print("Delete Session")
        resp = requests.delete(self.base_uri + "/session/" + self.session_id)
        self._process_resp(resp)

    def install_addon(self, path):
        print("Install Addon")
        resp = requests.post(
            self.base_uri + "/session/" + self.session_id +
            "/moz/addon/install",
            json={
                "path": str(path),
                "temporary": True,
            },
        )
        return self._process_resp(resp)["value"]

    def set_context(self, context):
        print("Set Context: " + context)
        resp = requests.post(
            self.base_uri + "/session/" + self.session_id + "/moz/context",
            json={
                "context": context,
            },
        )
        self._process_resp(resp)

    def find_element(self, selector):
        print("Find Element: " + selector)
        resp = requests.post(
            self.base_uri + "/session/" + self.session_id + "/element",
            json={
                "using": "css selector",
                "value": selector,
            },
        )
        return list(self._process_resp(resp)["value"].values())[0]

    def click_element(self, element_id):
        print("Click Element: " + element_id)
        resp = requests.post(
            self.base_uri + "/session/" + self.session_id +
            "/element/" + element_id + "/click",
            json={},
        )
        self._process_resp(resp)

    def get_window_handles(self):
        print("Get Window Handles")
        resp = requests.get(
            self.base_uri + "/session/" + self.session_id + "/window/handles"
        )
        return self._process_resp(resp)["value"]

    def take_screenshot(self):
        print("Take Screenshot")
        resp = requests.get(
            self.base_uri + "/session/" + self.session_id + "/screenshot"
        )
        return self._process_resp(resp)["value"]

    def take_element_screenshot(self, element_id):
        print("Take Element Screenshot: " + element_id)
        resp = requests.get(
            self.base_uri + "/session/" + self.session_id +
            "/element/" + element_id + "/screenshot"
        )
        return self._process_resp(resp)["value"]

    @staticmethod
    def _process_resp(resp):
        if resp.status_code != 200:
            print(resp.json()['value'])
            raise resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    main()
