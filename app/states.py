from aiogram.fsm.state import State, StatesGroup

class Phone(StatesGroup):
    get_branch = State()
    name = State()
    number = State()

class Specialists(StatesGroup):
    specialist = State()
    kind_of_pet = State()
    text = State()
    contact = State()

    


