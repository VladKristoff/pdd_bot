from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice

donate_router = Router()

@donate_router.callback_query(F.data == "donate_1")
@donate_router.callback_query(F.data == "donate_25")
@donate_router.callback_query(F.data == "donate_50")
async def donate(callback: CallbackQuery):
    amount = int(callback.data.split("_")[1])

    prices = [LabeledPrice(label="XTR", amount=amount)]
    await callback.message.answer_invoice(
        title=l10n.format_value("invoice-title"),
        description=l10n.format_value(
            "invoice-description",
            {"starsCount": amount}
        ),
        prices=prices,
        # provider_token Должен быть пустым
        provider_token="",
        # В пейлоайд можно передать что угодно,
        # например, айди того, что именно покупается
        payload=f"{amount}_stars",
        # XTR - это код валюты Telegram Stars
        currency="XTR"
    )