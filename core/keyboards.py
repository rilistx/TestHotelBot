from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder, KeyboardButton


async def number_button(
        *,
        sizes: tuple[int] = (5, ),
) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(
        KeyboardButton(
            text="1️⃣",
        )
    )

    keyboard.add(
        KeyboardButton(
            text="2️⃣"
        )
    )

    keyboard.add(
        KeyboardButton(
            text="3️⃣",
        )
    )

    keyboard.add(
        KeyboardButton(
            text="4️⃣",
        )
    )

    keyboard.add(
        KeyboardButton(
            text="5️⃣",
        )
    )

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def choice_button(
        *,
        sizes: tuple[int] = (2, ),
) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(
        KeyboardButton(
            text="✅ Так",
        )
    )

    keyboard.add(
        KeyboardButton(
            text="Ні ⛔️"
        )
    )

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
