from datetime import datetime, timedelta
from random import randint
from telegram import (
    Update,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
)


from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    Job,
    ExtBot,
    ContextTypes,
)
from bot.models import BotUser
from constants import (
    BACK,
    EXCLUDE,
    MENU,
    START_NUMBER,
    START_PASSPORT,
    START_VERIFICATION,
    PASSPORT,
)
from tg_bot.register_23_24 import Register2324
from utils import norm, send_sms, ReplyKeyboardMarkup


class Bot(Register2324):
    def __init__(self, token: str):
        self.token = token

        self.app = (
            ApplicationBuilder().token(self.token).concurrent_updates(128).build()
        )

        self.app.add_handler(
            ConversationHandler(
                [CommandHandler("start", self.start)],
                {
                    START_NUMBER: [
                        MessageHandler(
                            filters.Regex(
                                r"(?:(\+)?[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})|([\d]{2}[0-9]{3}[0-9]{2}[0-9]{2})"
                            )
                            | filters.CONTACT,
                            self.start_number,
                        )
                    ],
                    START_VERIFICATION: [
                        MessageHandler(
                            filters.Regex(r"^[\d+]{6}$"),
                            self.start_verification_code,
                        ),
                        MessageHandler(
                            filters.Text("Qayta yuborish 📧"),
                            self.resend_code,
                        ),
                    ],
                    START_PASSPORT: [
                        MessageHandler(
                            filters.TEXT & EXCLUDE,
                            self.start_passport,
                        ),
                    ],
                    MENU: [self.register_23_24_handlers()],
                },
                [],
            )
        )

    async def start(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        if not user:
            user = BotUser.objects.create(
                chat_id=tgUser.id, name=tgUser.full_name, username=tgUser.username
            )
            temp = user.temp

        if not user.is_verified:
            await tgUser.send_message("Iltimos raqamingizni yuboring.")
            return START_NUMBER

        if not user.is_registered:
            await tgUser.send_message("Iltimos passport raqamingizni yuboring.")
            return START_PASSPORT

        if user.is_registered and user.is_verified:
            await tgUser.send_message(
                "Assalomu alaykum xush kelibsiz.",
                reply_markup=ReplyKeyboardMarkup(
                    [["Qabul 2023-2024", "O'qishni ko'chirish"]]
                ),
            )

            return MENU

    async def start_number(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        number_t = (
            update.message.contact.phone_number
            if update.message.contact
            else update.message.text
        )

        number = norm(number_t)
        print("Salom")
        utp = randint(111111, 999999)

        send_sms(number, f"Telegram bot uchun tasdiqlash ko'di: {utp}")

        temp.utp = utp
        temp.save()
        user.number = number
        user.save()
        print(datetime.now() + timedelta(minutes=1))
        job = context.job_queue.run_once(
            self.remember_utp,
            timedelta(minutes=1),
            name=f"remember_utp_{user.id}",
            data=user.id,
        )
        print(job)
        print(job)

        await tgUser.send_message("Iltimos tasdiqlash kodini yuboring.")

        # await tgUser.send_message("Iltimos raqamingizga yuborilgan tasdiqlash ko'dini yuboring.",reply_markup=ReplyKeyboardMarkup([
        #     [
        #         "Qayta yuborish"
        #     ]
        # ]))

        return START_VERIFICATION

    async def remember_utp(self, context: ContextTypes.DEFAULT_TYPE):
        job: Job = context.job
        user_id = job.data

        user = BotUser.objects.filter(id=user_id).first()

        print("Ishladi")

        if not user:
            return

        await context.bot.send_message(
            user.chat_id,
            "Tasdiqlash kodi kelmadimi?\n\nPastdagi <code>Qayta yuborish</code> tugmasini bosing",
            reply_markup=ReplyKeyboardMarkup([["Qayta yuborish 📧"]]),
            parse_mode="HTML",
        )

    async def resend_code(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        send_sms(
            user.number,
            f"Telegram bot uchun tasdiqlash ko'di: {temp.utp}",
        )

        await tgUser.send_message("Tasdiqlash kodi qayta yuborildi.")
        return START_VERIFICATION

    async def start_verification_code(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        utp = int(update.message.text)

        if temp.utp == utp:
            user.is_verified = True
            temp.utp = 0
            user.save()
            for j in context.job_queue.get_jobs_by_name(f"remember_utp_{user.id}"):
                j.schedule_removal()

            await tgUser.send_message(
                "Siz tasdiqlandingiz.",
            )
            await tgUser.send_message(
                "Iltimos passport seriyangizni yuboring.",
                reply_markup=ReplyKeyboardMarkup([[BACK]]),
            )
            return START_PASSPORT
        else:
            await tgUser.send_message(
                "Tasdiqlash kodi to'g'ri kelmadi.\n\nIltimos qaytadan urinib ko'ring."
            )
            for j in context.job_queue.get_jobs_by_name(f"remember_utp_{user.id}"):
                j.schedule_removal()

            return START_VERIFICATION

    async def start_passport(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        if PASSPORT.search(update.message.text.replace(" ", "").upper()) is None:
            return await self.register_wrong_passport(update, context)

        user.passport = update.message.text.upper()
        user.is_registered = True
        user.save()

        await tgUser.send_message(
            "Menu", reply_markup=ReplyKeyboardMarkup([["Qabul 2023-2024"]])
        )

        return MENU

    async def register_wrong_passport(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        await tgUser.send_message(
            "Pasport raqamingizni <b>AB1234567</b> shaklida kiriting",
            reply_markup=ReplyKeyboardMarkup([[BACK]]),
            parse_mode="HTML",
        )
        return START_PASSPORT
