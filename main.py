import asyncio
import logging
import platform
import gspread

from oauth2client.service_account import ServiceAccountCredentials

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeDefault, Message, ReplyKeyboardRemove

from core.commands import commands
from core.configs import envs
from core.filters import (
    RoomFilter,
    DataFilter,
    QualityFilter,
    QualityCommentFilter,
    CleanFilter,
    CleanCommentFilter,
    ComebackFilter,
)
from core.keyboards import number_button, choice_button
from core.states import StartState


async def start_bot(
        bot: Bot,
) -> None:
    await bot.send_message(
        chat_id=envs.bot_admin,
        text="Start bot 👍🏻",
        reply_markup=ReplyKeyboardRemove()
    )


async def stop_bot(
        bot: Bot,
        dispatcher: Dispatcher,
) -> None:
    ReplyKeyboardRemove()

    await dispatcher.storage.close()

    await bot.send_message(
        chat_id=envs.bot_admin,
        text="Stop bot 👎🏻",
        reply_markup=ReplyKeyboardRemove()
    )


start_router = Router()


@start_router.message(
    CommandStart(),
)
async def start(
        message: Message,
        state: FSMContext,
) -> None:
    await state.clear()

    await state.update_data({
        "user_id": message.from_user.id,
        "first_name": message.from_user.first_name,
        "room": None,
        "data": None,
        "quality": None,
        "quality_comment": None,
        "clean": None,
        "clean_comment": None,
        "comeback": None,
        "comeback_comment": None,
    })

    text = (
        "Дякуємо, що скористались нашими послугами. "
        "Будь ласка, дайте відповідь на кілька запитань, "
        "щоб ми могли покращити ваш досвід."
    )

    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardRemove()
    )

    await asyncio.sleep(1)

    text = (
        "Будь ласка, напишіть номер вашої "
        "кімнати в якій ви перебували"
    )

    await message.answer(
        text=text,
    )

    await state.set_state(StartState.ROOM)


@start_router.message(
    Command(commands=["restart"]),
)
async def restart(
        message: Message,
        state: FSMContext,
) -> None:
    await state.clear()

    text = (
        "✅ <b>Success:</b> Бот успішно перезапущено!"
    )

    await message.answer(
        text=text,
    )

    await asyncio.sleep(1)

    await state.update_data({
        "user_id": message.from_user.id,
        "first_name": message.from_user.first_name,
        "room": None,
        "data": None,
        "quality": None,
        "quality_comment": None,
        "clean": None,
        "clean_comment": None,
        "comeback": None,
        "comeback_comment": None,
    })

    text = (
        "Дякуємо, що скористались нашими послугами. "
        "Будь ласка, дайте відповідь на кілька запитань, "
        "щоб ми могли покращити ваш досвід."
    )

    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardRemove()
    )

    await asyncio.sleep(1)

    text = (
        "Будь ласка, напишіть номер вашої "
        "кімнати в якій ви перебували"
    )

    await message.answer(
        text=text,
    )

    await state.set_state(StartState.ROOM)


@start_router.message(
    StartState.ROOM,
    RoomFilter(),
)
async def data(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data({
        "room": int(message.text),
    })

    text = (
        "Вкажіть дату вашого заїзду (у форматі дд.мм.рррр)."
    )

    await message.answer(
        text=text,
    )

    await state.set_state(StartState.DATA)


@start_router.message(
    StartState.DATA,
    DataFilter(),
)
async def quality(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data({
        "data": message.text,
    })

    text = (
        "Як ви оцінюєте якість сервісу? "
        "Оберіть рейтинг від 1 до 5 зірочок (кнопки)."
    )

    reply_markup = await number_button()

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )

    await state.set_state(StartState.QUALITY)


@start_router.message(
    StartState.QUALITY,
    QualityCommentFilter(),
)
async def quality_comment(
        message: Message,
        state: FSMContext,
) -> None:
    quality_dict = {
        "1️⃣": 1,
        "2️⃣": 2,
        "3️⃣": 3,
        "4️⃣": 4,
    }

    await state.update_data({
        "quality": quality_dict[message.text],
    })

    text = (
        "Ми шкодуємо, що вам щось не сподобалось. "
        "Будь ласка, розкажіть, що саме пішло не так."
    )

    await message.answer(
        text=text,
    )

    await state.set_state(StartState.QUALITY_COMMENT)


@start_router.message(
    StartState.QUALITY_COMMENT,
)
async def pre_clean(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data({
        "quality_comment": message.text,
    })

    text = (
        "Як ви оцінюєте чистоту номеру? "
        "Оберіть рейтинг від 1 до 5 зірочок (кнопки)."
    )

    reply_markup = await number_button()

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )

    await state.set_state(StartState.CLEAN)


@start_router.message(
    StartState.QUALITY,
    QualityFilter(),
)
async def clean(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data({
        "quality": 5,
    })

    text = (
        "Як ви оцінюєте чистоту номеру? "
        "Оберіть рейтинг від 1 до 5 зірочок (кнопки)."
    )

    reply_markup = await number_button()

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )

    await state.set_state(StartState.CLEAN)


@start_router.message(
    StartState.CLEAN,
    CleanCommentFilter(),
)
async def clean_comment(
        message: Message,
        state: FSMContext,
) -> None:
    clean_dict = {
        "1️⃣": 1,
        "2️⃣": 2,
        "3️⃣": 3,
        "4️⃣": 4,
    }

    await state.update_data({
        "clean": clean_dict[message.text],
    })

    text = (
        "Нам дуже важливо знати, що саме було не так "
        "з чистотою номеру. Будь ласка, залиште коментар."
    )

    await message.answer(
        text=text,
    )

    await state.set_state(StartState.CLEAN_COMMENT)


@start_router.message(
    StartState.CLEAN_COMMENT,
)
async def pre_comeback(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data({
        "clean_comment": message.text,
    })

    text = (
        "Чи хотіли б ви повернутись до нашого готелю знову? "
        "Оберіть варіант: Так / Ні / Залишити коментар. (кнопки)."
    )

    reply_markup = await choice_button()

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )

    await state.set_state(StartState.COMEBACK)


@start_router.message(
    StartState.CLEAN,
    CleanFilter(),
)
async def comeback(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data({
        "clean": 5,
    })

    text = (
        "Чи хотіли б ви повернутись до нашого готелю знову? "
        "Оберіть варіант: Так / Ні / Залишити коментар. (кнопки)."
    )

    reply_markup = await choice_button()

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )

    await state.set_state(StartState.COMEBACK)


@start_router.message(
    StartState.COMEBACK,
    ComebackFilter()
)
async def comeback_comment(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data({
        "comeback": "Так" if message.text == "✅ Так" else "Ні",
    })

    text = (
        "Тепер залиште ваш загальний коментар - відгук."
    )

    await message.answer(
        text=text,
    )

    await state.set_state(StartState.COMEBACK_COMMENT)


@start_router.message(
    StartState.COMEBACK_COMMENT,
)
async def finish(
        message: Message,
        state: FSMContext,
) -> None:
    state_data = await state.get_data()

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open("Test Hotel Table").sheet1

    sheet.append_row([
        len(sheet.get_all_values()),
        state_data["user_id"],
        state_data["first_name"],
        state_data["room"],
        state_data["data"],
        state_data["quality"],
        state_data["quality_comment"] if state_data["quality_comment"] is not None else "---",
        state_data["clean"],
        state_data["clean_comment"] if state_data["clean_comment"] is not None else "---",
        state_data["comeback"],
        message.text,
    ])

    text = (
        "✅ <b>Success:</b> Дякуємо за ваш відгук! Ми цінуємо вашу "
        "думку та обов'язково врахуємо її, щоб "
        "зробити наші послуги ще кращими."
    )

    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()


@start_router.message(
    StateFilter(StartState),
)
async def error(
        message: Message,
        state: FSMContext,
) -> None:
    state_data = await state.get_state()

    reply_markup = None

    if state_data == StartState.ROOM:
        text = (
            "⛔️ <b>Error:</b> Нажаль кімнати з таким номером не існує. "
            "Напишіть коректний номер."
        )
    elif state_data == StartState.DATA:
        text = (
            "⛔️ <b>Error:</b> Отримана дата некоректна. Напишіть "
            "коректну дату (у форматі дд.мм.рррр)."
        )
    elif state_data == StartState.QUALITY:
        text = (
            "⛔️ <b>Error:</b> Отриман некоректний вибір. Зробіть "
            "вибір за допомогою кнопок."
        )

        reply_markup = await number_button()
    elif state_data == StartState.CLEAN:
        text = (
            "⛔️ <b>Error:</b> Отриман некоректний вибір. Зробіть "
            "вибір за допомогою кнопок."
        )

        reply_markup = await number_button()
    else:
        text = (
            "⛔️ <b>Error:</b> Отриман некоректний вибір. Зробіть "
            "вибір за допомогою кнопок."
        )

        reply_markup = await choice_button()

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )


async def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        filename="console.log",
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
    )

    bot = Bot(
        token=envs.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    storage = MemoryStorage()

    dispatcher = Dispatcher(
        bot=bot,
        storage=storage,
    )

    dispatcher.startup.register(start_bot)
    dispatcher.shutdown.register(stop_bot)

    dispatcher.include_router(start_router)

    try:
        await bot.delete_webhook(
            drop_pending_updates=True,
        )
        await bot.delete_my_commands(
            scope=BotCommandScopeDefault(),
        )
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeDefault(),
        )
        await dispatcher.start_polling(
            bot,
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(
                policy=asyncio.WindowsSelectorEventLoopPolicy(),
            )

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("This bot stopped 😈")
