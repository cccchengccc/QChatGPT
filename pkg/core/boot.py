from __future__ import print_function

import traceback

from . import app
from ..audit import identifier
from . import stage

# 引入启动阶段实现以便注册
from .stages import load_config, setup_logger, build_app, migrate, show_notes


stage_order = [
    "LoadConfigStage",
    "MigrationStage",
    "SetupLoggerStage",
    "BuildAppStage",
    "ShowNotesStage"
]


async def make_app() -> app.Application:

    # 生成标识符
    identifier.init()

    ap = app.Application()

    # 执行启动阶段
    for stage_name in stage_order:
        stage_cls = stage.preregistered_stages[stage_name]
        stage_inst = stage_cls()

        await stage_inst.run(ap)

    await ap.initialize()

    return ap


async def main():
    try:
        app_inst = await make_app()
        await app_inst.run()
    except Exception as e:
        traceback.print_exc()
