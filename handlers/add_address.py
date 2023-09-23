from aiogram import F, Router, filters, types
from aiogram.fsm.context import FSMContext

import states
from keyboards import buttons_text, keyboards
from services.database import DAO, models

router = Router()
router.message.filter(filters.StateFilter(states.AddAddress.request_address))


@router.message(F.text == buttons_text.cancel)
async def handler(message: types.Message, state: FSMContext) -> None:
    await state.clear()

    text = "✅ Добавление адреса отменено"
    await message.answer(text=text, reply_markup=keyboards.menu)


@router.message(F.text)
async def handler(message: types.Message, dao: DAO, state: FSMContext) -> None:
    user_id = message.from_user.id
    address = models.Address(value=message.text, user_id=user_id)

    dao.add(instance=address)
    await dao.commit()

    await state.clear()

    text = "✅ Адрес добавлен"
    await message.answer(text=text, reply_markup=keyboards.menu)
