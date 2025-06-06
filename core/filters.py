from aiogram.types import Message
from aiogram.filters import BaseFilter


class RoomFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text.isdigit():
            if 1 <= int(message.text) <= 55:
                return True

        return False


class DataFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        data = message.text.split(".")

        if len(data) == 3:
            if data[0].isdigit() and data[1].isdigit() and data[2].isdigit():
                if 1 <= int(data[0]) <= 31:
                    if 1 <= int(data[1]) <= 12:
                        if len(data[2]) == 4:
                            return True

        return False


class QualityCommentFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        quality = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]

        if message.text in quality:
            return True

        return False


class QualityFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text == "5️⃣":
            return True

        return False


class CleanCommentFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        quality = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]

        if message.text in quality:
            return True

        return False


class CleanFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text == "5️⃣":
            return True

        return False


class ComebackFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        comeback = ["✅ Так", "Ні ⛔️"]

        if message.text in comeback:
            return True

        return False
