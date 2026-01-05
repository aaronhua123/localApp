from nicegui import ui
import httpx
def run():
    r = httpx.get("https://www.baidu.com")
    ui.label(r.text)