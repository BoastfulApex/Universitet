from typing import TYPE_CHECKING
from telegram import (
    Update,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
)


from telegram.ext import (
    # Application,
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# from apps.university.models import Faculty
from bot.models import BotApplication, BotUser
from constants import (
    BACK,
    EXCLUDE,
    EXT,
    LIGHT,
    NIGHT,
    REGISTER_2324_FACULTY,
    REGISTER_2324_FACULTY_DIR,
    REGISTER_2324_MODE,
    REGISTER_2324_NAME,
    REGISTER_2324_TEST_TIME,
)
from django.apps import apps

from utils import ReplyKeyboardMarkup, distribute


Faculty = apps.get_model("university", "Faculty")
Question = apps.get_model("university", "Question")
StudyType = apps.get_model("university", "StudyType")
Subject = apps.get_model("university", "Subject")
FacultyType = apps.get_model("university", "FacultyType")
Application = apps.get_model("student", "Application")
Student = apps.get_model("student", "Student")
Test = apps.get_model("student", "Test")
TestQuestion = apps.get_model("student", "TestQuestion")
TestSubject = apps.get_model("student", "TestSubject")
User = apps.get_model("users", "User")

if TYPE_CHECKING:
    from apps.university.models import (
        FacultyType, 
        Subject, 
        Faculty,
        Question,
        StudyType
    )
    from apps.student.models import (
        Student,
        Application,
        Test,
        TestQuestion,
        TestSubject,
    )
    from apps.users.models import User


class Register2324:
    def register_23_24_handlers(self):
        return ConversationHandler(
            [MessageHandler(filters.Text("Qabul 2023-2024"), self.register_23_24)],
            {
                REGISTER_2324_NAME: [
                    MessageHandler(filters.TEXT & EXCLUDE, self.register_2324_name)
                ],
                REGISTER_2324_MODE: [
                    MessageHandler(
                        filters.Text([LIGHT, NIGHT, EXT]), self.register_2324_mode
                    )
                ],
                REGISTER_2324_FACULTY: [
                    MessageHandler(filters.TEXT & EXCLUDE, self.register_2324_faculty)
                ],
                REGISTER_2324_FACULTY_DIR: [
                    MessageHandler(
                        filters.TEXT & EXCLUDE, self.register_2324_faculty_dir
                    )
                ],
                REGISTER_2324_TEST_TIME: [
                    MessageHandler(filters.Text("Hozir topshirish"), self.start_now),
                    MessageHandler(filters.Text("Keyinga qoldirish"), self.now_now),
                ],
            },
            [],
            map_to_parent={},
        )

    async def register_23_24(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        await tgUser.send_message(
            "Iltimos to'liq yuboring.",
            reply_markup=ReplyKeyboardMarkup([[BACK]]),
        )
        return REGISTER_2324_NAME

    async def register_2324_name(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        context.user_data["full_name"] = update.message.text

        await tgUser.send_message(
            "Talim turini tanlang.",
            reply_markup=ReplyKeyboardMarkup([[LIGHT, NIGHT], [EXT]]),
        )
        return REGISTER_2324_MODE

    async def register_2324_mode(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        mode = (
            1
            if update.message.text == LIGHT
            else (
                2
                if update.message.text == NIGHT
                else (3 if update.message.text == EXT else -1)
            )
        )

        if mode > 0:
            temp.mode = mode
            temp.save()
            facultys = Faculty.objects.all()
            await tgUser.send_message(
                "Iltimos fakultetni tanlang.",
                reply_markup=ReplyKeyboardMarkup(
                    distribute([fac.site_name for fac in facultys], 2)
                ),
            )
            return REGISTER_2324_FACULTY
        else:
            await tgUser.send_message(
                "Kechirasiz talim turi topilmadi.",
                reply_markup=ReplyKeyboardMarkup([[LIGHT, NIGHT], [EXT]]),
            )

    async def register_2324_faculty(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        faculty = Faculty.objects.filter(site_name=update.message.text).first()

        if faculty:
            temp.faculty = faculty
            temp.save()
            await tgUser.send_message(
                "Iltimos yo'nalishni tanlang.",
                reply_markup=ReplyKeyboardMarkup(
                    distribute(
                        [
                            f.name
                            for f in FacultyType.objects.filter(faculty=faculty)
                        ],2
                    )
                ),
            )
            return REGISTER_2324_FACULTY_DIR

    async def register_2324_faculty_dir(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

        faculty = FacultyType.objects.filter(
            name=update.message.text,
            faculty=temp.faculty,
        ).first()

        if faculty:
            await tgUser.send_message(
                "Test topshirish vaqtini tanlang.",
                reply_markup=ReplyKeyboardMarkup(
                    [["Hozir topshirish", "Keyinga qoldirish"]]
                ),
            )

            print(

            )

            dbUser = user.user or User.objects.create(
                full_name=context.user_data["full_name"], phone=user.number
            )

            user.user = dbUser
            user.save()

            application = Application.objects.create(
                user=dbUser,
                full_name=context.user_data["full_name"],
                phone=user.number,
                passport_seria=user.passport,
                faculty=temp.faculty,
                type=faculty,
                study_type=StudyType.objects.filter(id=temp.mode).first(),
                application_type="Ro'yxatdan o'tish",
            )

            test = Test.objects.create(application=application)

            for i in range(1, 6):
                subject: Subject = getattr(faculty, f"subject{i}")
                if not subject:
                    continue
                test_subject = TestSubject.objects.create(
                    test=test, subject=subject, wrong_answers=subject.question_number
                )
                for j in range(0, subject.question_number):
                    question = (
                        Question.objects.filter(
                            subject=subject,
                        )
                        .order_by("?")
                        .first()
                    )
                    if question:
                        test_question = TestQuestion.objects.create(
                            subject=subject, question=question
                        )
                    else:
                        break

                user.pending_test = test
                user.save()

            BotApplication.objects.create(
                user=dbUser, application=application, test=test
            )

            return REGISTER_2324_TEST_TIME
        else:
            pass

    async def start_now(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)

    async def now_now(self, update: Update, context: CallbackContext):
        tgUser, user, temp = BotUser.get(update)
