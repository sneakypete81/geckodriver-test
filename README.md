# Geckodriver Test

Quick test of the geckodriver API, showing WebExtension installation and interaction.

Expects geckodriver to be started with:
```
  geckodriver --port 4444
```

When the `geckodriver_test.py` script is run, it will then:
  1. Create a new session, with the `ui.popup.disable_autohide` preference set.
  1. Install the [Update Scanner](https://github.com/sneakypete81/updatescanner) WebExtension.
  1. Switch geckodriver to "chrome" context.
  1. Click the Update Scanner toolbar button, to open the popup.
  1. Wait for 5 seconds for everything to settle.
  1. Take a screenshot, and save it to `screenshot.png`.
  1. Close the geckodriver session.

Unfortunately the resulting screenshot doesn't include the popup or sidebar contents.
