import os.path
from pathlib import Path
from typing import List
import httpx
from nicegui import ui
import configparser
import importlib

def select_tree(e):
    ui.notify(e.value)
    if str(e.value).isdigit():
        ui.navigate.to(f'/{e.value}')


def root():
    with ui.left_drawer().style('background-color: #d7e3f4'):
        f = ui.input('搜索')
        r = httpx.get('http://127.0.0.1:5000/apps')
        t = ui.tree(r.json(), node_key='id', label_key='label', on_select=select_tree)
        f.bind_value_to(t, 'filter')

    ui.sub_pages({
        "/": code_page,
        "/code": code_page,
        "/cmd": cmd_page,
        "/exe": exe_page,
        "/{app_id}": app_page,
    })



def app_page(app_id: int):
    # 动态加载页面
    # 检查目录和版本
    app_name = f"apps/app_{app_id}"
    if os.path.exists(app_name):
        ui.notify(f"存在{app_name}")
    # 获取值
    try:
        # 检查版本
        config = configparser.ConfigParser()
        conf = os.path.abspath(f'{app_name}/config.ini')
        config.read(conf)

        version = config.getfloat('app', 'version')
        ui.label(str(version))
        if version < float():
            pass
            # todo 版本校验升级
        # 加载动态页面
        module_name = f"apps.app_{app_id}"
        module = importlib.import_module(module_name)
        importlib.reload(module)
        module.run()
    except (configparser.NoSectionError, configparser.NoOptionError):
        ui.button("配置读取失败")
    except Exception as e:
        ui.button("错误")

    # 升级
    async def download_app():
        r = httpx.get(f'http://127.0.0.1:5000/app/{app_id}')
        data = r.json()
        for file in data:
            print(file)
            r = httpx.get(f'http://127.0.0.1:5000/download/{file}')
            p_file = Path(file)
            p_file.parent.mkdir(parents=True, exist_ok=True)
            p_file.write_bytes(r.content)
            ui.notify(f'Downloaded {file}')
    ui.button("升级", on_click=download_app)

def code_page():
    pass

def cmd_page():
    pass


def exe_page():
    pass


ui.run(root, reload=False)
