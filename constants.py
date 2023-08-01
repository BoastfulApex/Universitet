from re import compile
from telegram.ext import filters




(
    MENU,
    START_NUMBER,
    START_VERIFICATION,
    START_PASSPORT,
    REGISTER_2324_NAME,
    REGISTER_2324_MODE,
    REGISTER_2324_FACULTY,
    REGISTER_2324_FACULTY_DIR,
    REGISTER_2324_TEST_TIME
) = range(9)





BACK = "🔙 Ortga"



EXCLUDE = ~filters.Text([
    "/start", BACK
])


PASSPORT = compile(r"^(?!){0}([A-Za-z]{2}\s?[0-9]{7})$")







LIGHT = "Kunduzgi"
NIGHT = "Kechgi"
EXT = "Sirtqi"