from nicegui import ui
import httpx

def run():
    r = httpx.get("https://www.google.com")
    ui.label(r.text)