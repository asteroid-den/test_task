from aiogram import F, Router, filters, types
from aiogram.fsm.context import FSMContext

import states
from keyboards import buttons_text, keyboards
from services.database import DAO, models

router = Router()


@router.message(filters.CommandStart())
async def handler(message: types.Message, dao: DAO) -> None:
    user_id = message.from_user.id
    user = await dao.get_user_by_id(user_id=user_id)

    if not user:
        user = models.User(id=user_id)

        dao.add(instance=user)
        await dao.commit()

    mention = message.from_user.mention_html()
    text = f"Добро пожаловать, {mention}"
    await message.answer(text=text, reply_markup=keyboards.menu)


@router.message(F.text == buttons_text.my_addresses)
async def handler(message: types.Message, dao: DAO) -> None:
    user_id = message.from_user.id
    user = await dao.get_user_by_id(user_id=user_id)
    addresses: list[models.Address] = await user.awaitable_attrs.addresses

    if addresses:
        adresses_text = "\n".join(
            [f"{ind}. {address.value}" for ind, address in enumerate(addresses, 1)]
        )

        text = f"Твои адреса:\n{adresses_text}"

    else:
        text = "Ты ещё не добавил ни одного адреса"

    await message.answer(text=text)


@router.message(F.text == buttons_text.add_address)
async def handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(state=states.AddAddress.request_address)

    text = "Введи адрес"
    await message.answer(text=text, reply_markup=keyboards.cancel)
