from aiogram import Router, filters, types
from aiogram.filters.command import CommandObject

from services.database import DAO, models

router = Router()


@router.message(filters.Command("info"))
async def handler(message: types.Message, command: CommandObject, dao: DAO) -> None:
    if command.args and command.args.isdigit():
        user_id = int(command.args)
        user = await dao.get_user_by_id(user_id=user_id)

        if not user:
            text = "Пользователь не найден"
            await message.answer(text=text)

            return

        addresses: list[models.Address] = await user.awaitable_attrs.addresses
        if addresses:
            adresses_text = "\n".join(
                [f"{ind}. {address.value}" for ind, address in enumerate(addresses, 1)]
            )

            text = (
                f"Адреса пользователя <code>{user_id}</code>:\n{adresses_text}"
                f"\n\nВсего адресов: {len(addresses)}"
            )

        else:
            text = (
                f"Пользователь <code>{user_id}</code> ещё не добавил ни одного адреса"
            )

        await message.answer(text=text)

    else:
        text = (
            "Для получении информации по пользователю, укажите ID пользователя "
            "в формате <code>/info {user_id}</code>"
        )

        await message.answer(text=text)
