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
)
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
)

if TYPE_CHECKING:
    from apps.university.models import FacultyType
    from apps.student.models import Student
    from apps.university.models import Subject
    from apps.university.models import Faculty
from bot.models import BotUser
from tg_bot.constants import (
    EXCLUDE,
    MENU_NOT_REGISTERED,
    NUMBER,
    PASSPORT,
    REGISTER2324_FACULTY,
    REGISTER2324_FACULTY_SUBJECT,
    REGISTER2324_FACULTY_TYPE,
    REGISTER2324_FATHER_NAME,
    REGISTER2324_LANG,
    REGISTER2324_MODE,
    REGISTER2324_NAME,
    REGISTER2324_SURNAME,
    REGISTER2324_TEST,
    VERIFICATION,
)
from tg_bot.copywrite import CopyWrite
from utils import distribute, send_sms
from django.apps import apps

Student = apps.get_model("student", "Student")
Faculty = apps.get_model("university", "Faculty")
Subject = apps.get_model("university", "Subject")
FacultyType = apps.get_model("university", "FacultyType")


class Register2324:
    async def register_23_24(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        await tgUser.send_message("Iltimos ismingizni yuboring.")

        context.user_data["register2324"] = {}

        return REGISTER2324_NAME

    async def register2324_name(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        context.user_data["register2324"]["name"] = update.message.text
        await tgUser.send_message("Familyangizni yuboring.")
        return REGISTER2324_SURNAME

    async def register2324_surname(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        context.user_data["register2324"]["surname"] = update.message.text
        await tgUser.send_message("Otangizni ismini yuboring.")
        return REGISTER2324_FATHER_NAME

    async def register2324_father_name(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        context.user_data["register2324"]["father_name"] = update.message.text

        # await tgUser.send_message(
        #     "Iltimos fakultetni tanlang.",
        #     reply_markup=ReplyKeyboardMarkup(
        #         distribute([fac.site_name for fac in Faculty.objects.all()], 2), True
        #     ),
        # )
        # return REGISTER2324_FACULTY

        await tgUser.send_message(
            "Iltimos talim tilini tanlang.",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [CopyWrite.Keyboard.TEXT_UZBEK, CopyWrite.Keyboard.TEXT_RUSSIAN],
                    [CopyWrite.Keyboard.TEXT_ENGLISH],
                ],
                True,
            ),
        )
        return REGISTER2324_LANG

    async def register2324_lang(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        lang = (
            1
            if update.message.text == CopyWrite.Keyboard.TEXT_UZBEK
            else (
                2
                if update.message.text == CopyWrite.Keyboard.TEXT_RUSSIAN
                else (
                    3 if update.message.text == CopyWrite.Keyboard.TEXT_ENGLISH else -1
                )
            )
        )

        if lang:
            context.user_data["register2324"]["lang"] = lang
            await tgUser.send_message(
                CopyWrite.TEXT_SELECT_MDOE,
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [
                            CopyWrite.Keyboard.TEXT_LIGHT,
                            CopyWrite.Keyboard.TEXT_NIGHT,
                        ],
                        [CopyWrite.Keyboard.TEXT_EXTERNAL],
                    ],
                    True,
                ),
            )
            return REGISTER2324_MODE
        else:
            await tgUser.send_message(
                CopyWrite.TEXT_WRONG_LANG,
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [
                            CopyWrite.Keyboard.TEXT_UZBEK,
                            CopyWrite.Keyboard.TEXT_RUSSIAN,
                        ],
                        [CopyWrite.Keyboard.TEXT_ENGLISH],
                    ],
                    True,
                ),
            )
            return REGISTER2324_LANG

    async def register2324_mode(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        mode = (
            1
            if update.message.text == CopyWrite.Keyboard.TEXT_LIGHT
            else (
                2
                if update.message.text == CopyWrite.Keyboard.TEXT_NIGHT
                else (
                    3 if update.message.text == CopyWrite.Keyboard.TEXT_EXTERNAL else -1
                )
            )
        )

        if mode:
            context.user_data["register2324"]["mode"] = mode
            await tgUser.send_message(
                CopyWrite.TEXT_SELECT_FACULTY,
                reply_markup=ReplyKeyboardMarkup(
                    distribute([fac.site_name for fac in Faculty.objects.all()], 2),
                    True,
                ),
            )
            return REGISTER2324_FACULTY
        else:
            await tgUser.send_message(
                CopyWrite.TEXT_WRONG_MODE,
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [
                            CopyWrite.Keyboard.TEXT_LIGHT,
                            CopyWrite.Keyboard.TEXT_NIGHT,
                        ],
                        [CopyWrite.Keyboard.TEXT_EXTERNAL],
                    ],
                    True,
                ),
            )
            return REGISTER2324_MODE

    async def register2324_faculty(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        faculty = Faculty.objects.filter(site_name=update.message.text).first()

        if faculty:
            context.user_data["register2324"]["faculty"] = faculty.id
            await tgUser.send_message(
                "Yo'nalishni tanlang.",
                reply_markup=ReplyKeyboardMarkup(
                    distribute(
                        [
                            fact.name
                            for fact in FacultyType.objects.filter(faculty=faculty)
                        ],
                        2,
                    ),
                    True,
                ),
            )
            return REGISTER2324_FACULTY_TYPE
        else:
            await tgUser.send_message(
                "Kechirasiz fakultet topilmadi.",
                reply_markup=ReplyKeyboardMarkup(
                    distribute([fac.site_name for fac in Faculty.objects.all()], 2),
                    True,
                ),
            )
            return REGISTER2324_FACULTY

    async def register2324_faculty_type(self, update: Update, context: CallbackContext):
        tgUser, user = BotUser.get(update)

        faculty = Faculty.objects.filter(
            id=context.user_data["register2324"]["faculty"]
        ).first()

        fact = FacultyType.objects.filter(faculty=faculty).first()

        if fact:
            context.user_data["register2324"]["fact"] = fact.id

            subjects = [
                sub.site_name
                for sub in [
                    fact.subject1,
                    fact.subject2,
                    fact.subject3,
                    fact.subject4,
                    fact.subject5,
                ]
                if sub is not None
            ]

            await tgUser.send_message(
                f"Imtihon davomiyligi: {fact.test_minute} daqiqa\n\nTopshiriladigan fanlar: {','.join(subjects)}"
            )
            await tgUser.send_message(
                "Imtihonni hozir boshlash uchun `Imtihonni boshlash` tugmasini bosing.\n\nKeyinroqqa qoldirish uchun `Imtihonni keyin topshirish` tugmasini bosing.",
                reply_markup=ReplyKeyboardMarkup(
                    [["Imtihonni boshlash", "Imtihonni keyin topshirish"]], True
                ),
            )
            return REGISTER2324_TEST

            # context.user_data["register2324"]["fact"] = fact.id
            # await tgUser.send_message(
            #     "Iltimos fanni tanlang",
            #     reply_markup=ReplyKeyboardMarkup(distribute(keyboard, 2)),
            # )
            # return REGISTER2324_FACULTY_SUBJECT
        else:
            await tgUser.send_message(
                "Kechirasiz yo'nalish topilmadi.",
                reply_markup=ReplyKeyboardMarkup(
                    distribute(
                        [
                            fact.site_name
                            for fact in FacultyType.objects.filter(faculty=faculty)
                        ]
                    ),
                    True,
                ),
            )
            return REGISTER2324_FACULTY_TYPE

    # async def register2324_subject(self, update: Update, context: CallbackContext):
    #     tgUser, user = BotUser.get(update)

    #     fact: FacultyType = FacultyType.objects.filter(
    #         id=context.user_data["register2324"]["fact"]
    #     ).first()

    #     subject: Subject = (
    #         fact.subject1
    #         if fact.subject1 is not None
    #         and fact.subject1.site_name == update.message.text
    #         else (
    #             fact.subject2
    #             if fact.subject2 is not None
    #             and fact.subject2.site_name == update.message.text
    #             else (
    #                 fact.subject3
    #                 if fact.subject3 is not None
    #                 and fact.subject3.site_name == update.message.text
    #                 else (
    #                     fact.subject4
    #                     if fact.subject4 is not None
    #                     and fact.subject4.site_name == update.message.text
    #                     else (
    #                         fact.subject5
    #                         if fact.subject5 is not None
    #                         and fact.subject5.site_name == update.message.text
    #                         else None
    #                     )
    #                 )
    #             )
    #         )
    #     )

    #     if subject:
    #         await tgUser.send_message(f"Imtihon davomiyligi: {fact.test_minute} daqiqa\nTopshiriladigan")
