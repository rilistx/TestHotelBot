from aiogram.fsm.state import StatesGroup, State


class StartState(StatesGroup):
    ROOM = State()
    DATA = State()
    QUALITY = State()
    QUALITY_COMMENT = State()
    CLEAN = State()
    CLEAN_COMMENT = State()
    COMEBACK = State()
    COMEBACK_COMMENT = State()
