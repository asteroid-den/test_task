from aiogram.fsm.state import State, StatesGroup

class AddAddress(StatesGroup):
    request_address = State()

