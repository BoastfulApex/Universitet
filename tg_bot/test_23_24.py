from time import sleep
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
from random import shuffle

if TYPE_CHECKING:
    from apps.university.models import FacultyType
    from apps.student.models import Student
    from apps.university.models import Subject
    from apps.university.models import Faculty
    from apps.university.models import Question
    from apps.university.models import Answer
from bot.models import BotUser, TestSession
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
    TEST_ANSWER,
    VERIFICATION,
)
from tg_bot.copywrite import CopyWrite
from utils import distribute, send_sms
from django.apps import apps

Student = apps.get_model("student", "Student")
Faculty = apps.get_model("university", "Faculty")
Subject = apps.get_model("university", "Subject")
Question = apps.get_model("university", "Question")
Answer = apps.get_model("university", "Answer")
FacultyType = apps.get_model("university", "FacultyType")


class Test:
    async def start_test(self, update, context):
        tgUser, user = BotUser.get(update)

        fact = FacultyType.objects.filter(
            id=context.user_data["register2324"]["faculty"]
        ).first()

        questions = []
        subjects = [
            sub
            for sub in [
                fact.subject1,
                fact.subject2,
                fact.subject3,
                fact.subject4,
                fact.subject5,
            ]
            if sub is not None
        ]
        testSession = TestSession.objects.create(user=user)

        for sub in subjects:
            qs = list(
                Question.objects.filter(subject=sub).order_by("?")[
                    : sub.question_number
                ]
            )
            for q in qs:
                questions.append(q)
                testSession.questions.add(q)
        testSession.questionCount = testSession.questions.count()
        testSession.save()
        await tgUser.send_message(f"Savollar soni: {testSession.questions.count()}")

        # sleep(1)
        await tgUser.send_message("3...")
        sleep(1)
        await tgUser.send_message("2...")
        sleep(1)
        await tgUser.send_message("1...")

        sleep(0.5)
        question = testSession.question
        variants = question.variants
        # testSession.current_question = testSession.questions.first()
        # testSession.save()
        # testSession.questions.remove(testSession.current_question)

        await tgUser.send_message(
            f"""{testSession.questionIndex}-Savol: {question.question}\n\nA: {variants[0].answer}\nB: {variants[1].answer}\nC: {variants[2].answer}\nD: {variants[3].answer}""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "A", callback_data=f"variant:{variants[0].id}"
                        ),
                        InlineKeyboardButton(
                            "B", callback_data=f"variant:{variants[1].id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "C", callback_data=f"variant:{variants[2].id}"
                        ),
                        InlineKeyboardButton(
                            "D", callback_data=f"variant:{variants[3].id}"
                        ),
                    ],
                ]
            ),
        )

        return TEST_ANSWER




    async def answer(self,update:Update,context:CallbackContext):
        tgUser, user = BotUser.get(update)

        testSession = TestSession.objects.filter(user=user).first()


        action,answer_id = update.callback_query.data.split(":")


        answer = Answer.objects.filter(id=int(answer_id)).first()


        if answer:
            if answer.is_correct:
                await update.callback_query.answer("Javob to'g'ri")
                testSession.ball += answer.question.subject.one_question_ball
                testSession.trueAnswersCount += 1
                testSession.save()


            else:
                await update.callback_query.answer("Javob noto'g'ri")
        else:
            await update.callback_query.answer("Variant topilmadi.")
        

        question = testSession.question


        if question:
            testSession.questionIndex += 1
            testSession.save()
            variants = question.variants


            await update.callback_query.message.edit_text(
                f"""{testSession.questionIndex}-Savol: {question.question}\n\nA: {variants[0].answer}\nB: {variants[1].answer}\nC: {variants[2].answer}\nD: {variants[3].answer}""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "A", callback_data=f"variant:{variants[0].id}"
                            ),
                            InlineKeyboardButton(
                                "B", callback_data=f"variant:{variants[1].id}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "C", callback_data=f"variant:{variants[2].id}"
                            ),
                            InlineKeyboardButton(
                                "D", callback_data=f"variant:{variants[3].id}"
                            ),
                        ],
                    ]
                ),
            )

            return TEST_ANSWER
        else:
            testSession.is_active = False
            testSession.save()

            fact = FacultyType.objects.filter(id=context.user_data["register2324"]["faculty"]).first()

            await tgUser.send_message(f"{testSession.questionCount} dan {testSession.trueAnswersCount} savolga to'g'ri javob berdingiz va {testSession.ball} ball yeg'dingiz.")


            if testSession.ball > fact.passing_score:
                testSession.is_passed = True
                testSession.save()
                await tgUser.send_message("TABRIKLAYMIZ!!! Siz {Universitet nomi} ga qabul qilindizgiz.")
            else:
                pass
                await tgUser.send_message("Ming afsus siz to'plagan balingiz bu yo'nalish uchun yetmaydi.")