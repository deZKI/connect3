from aiogram.fsm.state import State, StatesGroup

class RegistrationForm(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_last_name = State()
    waiting_for_phone_number = State()
    waiting_for_church = State()
    waiting_for_know_from = State()
