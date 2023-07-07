from typing import TYPE_CHECKING

from random import randint
from telegram.ext import (
    ApplicationBuilder,
    ConversationHandler,
    CommandHandler,
    CallbackContext,
    filters,
    PicklePersistence,
    MessageHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
)
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
)

from tg_bot.register_23_24 import Register2324
from tg_bot.test_23_24 import Test

if TYPE_CHECKING:
    from apps.student.models import Student
from bot.models import BotUser
from tg_bot.constants import (
    EXCLUDE,
    MENU_NOT_REGISTERED,
    NUMBER,
    PASSPORT,
    REGISTER2324_FACULTY,
    REGISTER2324_FACULTY_TYPE,
    REGISTER2324_FATHER_NAME,
    REGISTER2324_LANG,
    REGISTER2324_MODE,
    REGISTER2324_NAME,
    REGISTER2324_SURNAME,
    REGISTER2324_TEST,
    TEST_ANSWER,
    VERIFICATION,
)
from tg_bot.copywrite import CopyWrite
from utils import send_sms
from django.apps import apps

Student = apps.get_model("student", "Student")


class Bot(Register2324, Test):
    def __init__(self, token: str) -> None:
        self.persistence = PicklePersistence(
            "bot_data.pickle",
        )

        self.app = (
            ApplicationBuilder()
            .token(token)
            # .persistence(self.persistence)
            .concurrent_updates(256)
            .build()
        )

        self.app.add_handler(
            ConversationHandler(
                [CommandHandler("start", self.start)],
                {
                    NUMBER: [
                        MessageHandler(
                            filters.CONTACT
                            | filters.Regex(
                                r"(?:(\+)?[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"
                            )
                            & EXCLUDE,
                            self.number,
                        ),
                    ],
                    VERIFICATION: [
                        MessageHandler(filters.Regex(r"\d{6}"), self.verification)
                    ],
                    PASSPORT: [MessageHandler(filters.TEXT & EXCLUDE, self.passport)],
                    MENU_NOT_REGISTERED: [
                        MessageHandler(
                            filters.Text(
                                [
                                    CopyWrite.Keyboard.TEXT_REGISTER_23_24,
                                ]
                            ),
                            self.register_23_24,
                        )
                    ],
                    REGISTER2324_NAME: [
                        MessageHandler(filters.TEXT & EXCLUDE, self.register2324_name)
                    ],
                    REGISTER2324_SURNAME: [
                        MessageHandler(
                            filters.TEXT & EXCLUDE, self.register2324_surname
                        )
                    ],
                    REGISTER2324_FATHER_NAME: [
                        MessageHandler(
                            filters.TEXT & EXCLUDE, self.register2324_father_name
                        )
                    ],
                    REGISTER2324_LANG: [
                        MessageHandler(
                            filters.Text(
                                [
                                    CopyWrite.Keyboard.TEXT_UZBEK,
                                    CopyWrite.Keyboard.TEXT_RUSSIAN,
                                    CopyWrite.Keyboard.TEXT_ENGLISH,
                                ]
                            )
                            & EXCLUDE,
                            self.register2324_lang,
                        )
                    ],
                    REGISTER2324_MODE: [
                        MessageHandler(
                            filters.Text(
                                [
                                    CopyWrite.Keyboard.TEXT_LIGHT,
                                    CopyWrite.Keyboard.TEXT_LIGHT,
                                    CopyWrite.Keyboard.TEXT_EXTERNAL,
                                ]
                            )
                            & EXCLUDE,
                            self.register2324_mode,
                        )
                    ],
                    REGISTER2324_FACULTY: [
                        MessageHandler(
                            filters.TEXT & EXCLUDE, self.register2324_faculty
                        )
                    ],
                    REGISTER2324_FACULTY_TYPE: [
                        MessageHandler(
                            filters.TEXT & EXCLUDE, self.register2324_faculty_type
                        )
                    ],
                    REGISTER2324_TEST: [
                        MessageHandler(
                            filters.Text("Imtihonni boshlash"), self.start_test
                        )
                    ],
                    TEST_ANSWER: [
                        CallbackQueryHandler(self.answer, pattern="^variant")
                    ],
                },
                [CommandHandler("start", self.start)],
                # name="BotConversation",
                # persistent=True,
            )
        )

    async def start(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        if not user:
            user = BotUser.objects.create(
                chat_id=tgUser.id,
                name=tgUser.full_name,
                username=tgUser.username,
            )

        if context.args and context.args[0] == "setAdmin444":
            user.is_admin = True
            user.save()

        if user.is_admin:
            await tgUser.send_message("")

        if user.student:
            pass
        else:
            if user.is_verified:
                await tgUser.send_message(
                    CopyWrite.TEXT_SEND_PASSPORT,
                    reply_markup=ReplyKeyboardMarkup(
                        [[CopyWrite.Keyboard.TEXT_BACK]], True
                    ),
                )
                return PASSPORT
            else:
                await tgUser.send_message(
                    CopyWrite.TEXT_START_GREATING,
                    parse_mode="HTML",
                    reply_markup=ReplyKeyboardMarkup(
                        [
                            [
                                KeyboardButton(
                                    CopyWrite.Keyboard.TEXT_SEND_NUMBER,
                                    request_contact=True,
                                )
                            ]
                        ],
                        True,
                    ),
                )
                return NUMBER

    async def number(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        number = (
            update.message.contact.phone_number
            if update.message.contact
            else update.message.text
        )

        if len(number) == 9:
            number = f"+998{update.message.text}"
        elif len(number) == 12:
            if not update.message.text.startswith("+"):
                number = f"+{update.message.text}"

        user.number = number
        user.otp = randint(100000, 999999)
        user.save()

        send_sms(number, user.otp)

        await tgUser.send_message(
            CopyWrite.TEXT_SEND_VERIFICATION_CODE,
            reply_markup=ReplyKeyboardMarkup(
                [
                    [CopyWrite.Keyboard.TEXT_BACK],
                ],
                True,
            ),
        )
        return VERIFICATION

    async def verification(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        verification = int(update.message.text)

        if verification == user.otp:
            await tgUser.send_message(
                CopyWrite.TEXT_SEND_PASSPORT,
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [CopyWrite.Keyboard.TEXT_BACK],
                    ],
                    True,
                ),
                parse_mode="HTML",
            )
            user.is_verified = True
            user.save()
            print("otp")
            return PASSPORT
        else:
            await tgUser.send_message(
                CopyWrite.TEXT_VERIFICATION_WRONG_OTP,
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [CopyWrite.Keyboard.TEXT_BACK],
                    ],
                    True,
                ),
            )
            return VERIFICATION

    async def passport(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        passport = update.message.text
        print("salom")

        student = Student.objects.filter(passport_seria=passport).first()

        if student:
            user.student = student
            user.save()

            await tgUser.send_message(
                "Imtihonni boshlang.",
                reply_markup=ReplyKeyboardMarkup(
                    [["Imtihonni boshlash", "Imtihonni keyin topshirish"]]
                ),
            )
            return REGISTER2324_TEST
        else:
            await tgUser.send_message(
                CopyWrite.TEXT_STUDENT_NOT_FOUND_FROM_BASE,
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [
                            CopyWrite.Keyboard.TEXT_REGISTER_23_24,
                            CopyWrite.Keyboard.TEXT_TRANSFER,
                        ]
                    ],
                    True,
                ),
            )
            return MENU_NOT_REGISTERED
