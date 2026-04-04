import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
# --- НАСТРОЙКИ ---
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не найдена!")
# Нужные медиафайлы 
VIDEO_CURATOR = "___"
VIDEO_REVIEWS = "___"
VIDEO_PROFESSIONS = "___"
VIDEO_TRAILER = "___"
VIDEO_CAMPUS = "___"
VIDEO_SPORT = "___"
# --- Логирование (для отладки) ---
logging.basicConfig(level=logging.INFO)
# --- Инициализация бота и диспетчера ---
bot = Bot(token=TOKEN)
dp = Dispatcher()
# --- Состояния для теста ---
class TestState(StatesGroup):
    waiting_for_answer = State()
    answers = State()  # будем хранить список ответов
# --- Вспомогательные функции ---
def main_menu_keyboard():
    """Клавиатура главного меню"""
    builder = InlineKeyboardBuilder()
    builder.button(text="📘 Поступление и обучение", callback_data="block1")
    builder.button(text="⚖️ Профориентация", callback_data="block2")
    builder.button(text="🎓 Жизнь студента", callback_data="block3")
    builder.adjust(1)
    return builder.as_markup()
def back_to_main_keyboard():
    """Кнопка возврата в главное меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
def back_to_block_keyboard(block: str):
    """Кнопка возврата в подменю блока"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_to_{block}")]
    ])
# --- Обработчики команд ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в чат-бот для абитуриентов УрФУ!\n"
        "Выберите интересующий раздел:",
        reply_markup=main_menu_keyboard()
    )
# --- Обработчики навигации ---
@dp.callback_query(F.data == "main_menu")
async def main_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите интересующий раздел:",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()
# ---- БЛОК 1: Поступление и обучение ----
def block1_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Юридические направления в УрФУ", callback_data="block1_directions")
    builder.button(text="Как поступить на ПОНБ", callback_data="block1_admission")
    builder.button(text="🏠 Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()
@dp.callback_query(F.data == "block1")
async def block1_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📘 Информация о поступлении и дальнейшем обучении\n\n"
        "Здесь вы узнаете о направлениях подготовки, как поступить, какие экзамены сдавать и где работать после выпуска.",
        reply_markup=block1_menu()
    )
    await callback.answer()
# 1.1 Юридические направления
@dp.callback_query(F.data == "block1_directions")
async def directions(callback: types.CallbackQuery):
    text = (
        "Юридические направления в УрФУ:\n\n"
        "Правовое обеспечение национальной безопасности\n"
        "Бюджет: 6 мест | Платно: 110 мест\n"
        "Проходной балл: 86 (бюджет) / 43 (платно)\n"
        "Стоимость: 241 000 ₽/год\n\n"
        "Речеведческая экспертиза\n"
        "5/40, от 87/48, 241 000 ₽\n\n"
        "Экономические экспертизы\n"
        "6/100, от 89/47, 241 000 ₽\n\n"
        "Предпринимательское право\n"
        "нет/100, от 45, 216 000 ₽\n\n"
        "Международное право\n"
        "нет/60, от 43, 216 000 ₽\n\n"
        "Юриспруденция\n"
        "нет/110, от 41, 216 000 ₽"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Чем отличаются направления?", callback_data="block1_diff")],
        [InlineKeyboardButton(text="Кем работать после ПОНБ?", callback_data="block1_jobs")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block1")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
@dp.callback_query(F.data == "block1_diff")
async def diff(callback: types.CallbackQuery):
    text = (
        "Чем отличаются юристы от экономических экспертов и ПОНБ?\n\n"
        "• Юриспруденция (базовая программа): готовит универсальных специалистов для нормотворческой, правоприменительной и экспертной деятельности. \n"
        "• Правовое обеспечение национальной безопасности (ПОНБ): Специализация на решении задач в сфере государственной безопасности.\n"
        "• Судебная экономическая экспертиза: Подготовка специалистов для проведения экспертиз и проверки финансово-хозяйственной деятельности компаний.\n"
        "• Предпринимательское право: Углубленное изучение правового регулирования бизнеса и решения правовых проблем коммерческих структур.\n"
        "• Международное право: Подготовка юристов для работы с иностранными клиентами и защиты их интересов в международном правовом поле."
    )
    kb = back_to_block_keyboard("block1_directions")
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
@dp.callback_query(F.data == "block1_jobs")
async def jobs(callback: types.CallbackQuery):
    text = (
        "Кем можно работать после ПОНБ?\n\n"
        "Выпускники работают в:\n"
        "• Органах государственной и муниципальной власти\n"
        "• Силовых структурах (Росгвардия, полиция и др.)\n"
        "• Судебных органах и прокуратуре\n"
        "• Адвокатских бюро и юридических компаниях\n"
        "• Правовых департаментах крупных предприятий (Уралвагонзавод и др.)\n"
        "• Коммерческих структурах"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Смотреть трейлер", callback_data="watch_trailer")],
        [InlineKeyboardButton(text="◀ Назад", callback_data="block1_directions")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
@dp.callback_query(F.data == "watch_trailer")
async def watch_trailer(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block1_jobs")]
    ])
    await callback.message.answer_video(
        VIDEO_TRAILER,
        caption="Короткое видео о будущих профессиях",
        reply_markup=kb
    )
    await callback.answer()
# 1.2 Как поступить на ПОНБ (подменю)
def admission_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Какие экзамены сдавать?", callback_data="admission_exams")
    builder.button(text="Проходной балл (2023/2024)", callback_data="admission_scores")
    builder.button(text="Индивидуальные достижения", callback_data="admission_achievements")
    builder.button(text="Сроки и документы", callback_data="admission_docs")
    builder.button(text="◀️ Назад", callback_data="block1")
    builder.adjust(1)
    return builder.as_markup()
@dp.callback_query(F.data == "block1_admission")
async def admission_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Как поступить на ПОНБ?\n\nВыберите интересующий вопрос:",
        reply_markup=admission_menu()
    )
    await callback.answer()
@dp.callback_query(F.data == "admission_exams")
async def exams(callback: types.CallbackQuery):
    text = (
        "Вступительные испытания (ЕГЭ):\n"
        "1. Обществознание (мин. 45 баллов)\n"
        "2. Русский язык (мин. 40)\n"
        "3. История (мин. 36) или Иностранный язык (мин. 30) или Информатика (мин. 44)"
    )
    kb = back_to_block_keyboard("block1_admission")
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
@dp.callback_query(F.data == "admission_scores")
async def scores(callback: types.CallbackQuery):
    text = "Проходной балл на ПОНБ:\n\n2023 год: 133 балла (платное)\n2024 год: 115 баллов (платное)"
    kb = back_to_block_keyboard("block1_admission")
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
@dp.callback_query(F.data == "admission_achievements")
async def achievements(callback: types.CallbackQuery):
    text = (
        "Индивидуальные достижения (максимум 10 баллов):\n\n"
        "🔹 10 баллов — служба в армии (включая СВО)\n"
        "🔹 7 баллов — победа в региональном этапе Всероссийской олимпиады / олимпиадах из перечня Минобрнауки\n"
        "🔹 6 баллов — аттестат с отличием (медаль), диплом СПО с отличием, победа в «Большой перемене»\n"
        "🔹 5 баллов — участие в региональном этапе Всеросса, победа в конкурсе проектных работ и др.\n"
        "🔹 4 балла — участие в очных этапах олимпиад, «Тест-драйв в УрФУ», «Открытый конкурс инженерных решений»\n"
        "🔹 3 балла — звание КМС/МС, призёр «Большой перемены», обучение в УНИЛ\n"
        "🔹 2 балла — золотой знак ГТО, участие в интенсивных курсах «Золотое сечение»\n"
        "🔹 1 балл — волонтёрство (не менее 100 часов на dobro.ru)"
    )
    kb = back_to_block_keyboard("block1_admission")
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
@dp.callback_query(F.data == "admission_docs")
async def docs(callback: types.CallbackQuery):
    text = (
        "Сроки подачи документов в 2025 году:\n"
        "• Для поступающих по ЕГЭ: с 20 июня по 25 июля\n"
        "• Для поступающих по внутренним экзаменам: с 20 июня по 18 июля\n"
        "• Завершение подачи оригиналов: 5 августа (1 августа для приоритетного зачисления)\n\n"
        "Список документов:\n"
        "• Паспорт\n"
        "• Аттестат/диплом\n"
        "• СНИЛС\n"
        "• Документы об индивидуальных достижениях (при наличии)\n\n"
        "Куда подавать:\n"
        "📍 Лично: г. Екатеринбург, ул. Мира, 19 (главный корпус) и филиалы\n"
        "💻 Электронно: priem.urfu.ru (личный кабинет), Госуслуги\n"
        "📧 priem@urfu.ru | ☎️ (343) 375-44-74"
    )
    kb = back_to_block_keyboard("block1_admission")
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
# ---- БЛОК 2: Профориентация ----
def block2_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🎬 Видео от куратора программы", callback_data="block2_curator")
    builder.button(text="🎓 Видеоотзывы выпускников", callback_data="block2_reviews")
    builder.button(text="👥 Знакомство с представителями профессий", callback_data="block2_professions")
    builder.button(text="❓ Тест «Тебе подходит юриспруденция?»", callback_data="start_test")
    builder.button(text="📚 Другие тесты для самоопределения", callback_data="block2_other_tests")
    builder.button(text="🏠 Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()
@dp.callback_query(F.data == "block2")
async def block2_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "⚖️ Профориентация по специальности\n\n"
        "Поможем вам определиться с выбором и познакомиться с профессией.",
        reply_markup=block2_menu()
    )
    await callback.answer()
@dp.callback_query(F.data == "block2_curator")
async def curator_video(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block2")]
    ])
    await callback.message.answer_video(
        VIDEO_CURATOR,
        caption="Видео от куратора программы ПОНБ",
        reply_markup=kb
    )
    await callback.answer()
@dp.callback_query(F.data == "block2_reviews")
async def reviews_video(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block2")]
    ])
    await callback.message.answer_video(
        VIDEO_REVIEWS,
        caption="Отзывы выпускников о программе",
        reply_markup=kb
    )
    await callback.answer()
@dp.callback_query(F.data == "block2_professions")
async def professions_video(callback: types.CallbackQuery):
    text = (
        "В УрФУ на программе ПОНБ вас ждут не просто заурядные лекции, "
        "а полное погружение в профессию. На каждой паре по введению в специальность "
        "вы встретитесь с представителями разных профессий: адвокат, прокурор, юрист и многие другие. "
        "Приходи к нам учиться и на личном опыте познавай разные профессии. "
        "Благодаря такому подходу каждый сможет определиться с тем, что ему больше интересно."
    )
    kb_text = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block2")]
    ])
    await callback.message.edit_text(text, reply_markup=kb_text)
    kb_video = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block2")]
    ])
    await callback.message.answer_video(
        VIDEO_PROFESSIONS,
        caption="Встречи с представителями профессий",
        reply_markup=kb_video
    )
    await callback.answer()
@dp.callback_query(F.data == "block2_other_tests")
async def other_tests(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Тест «Ikigai»", url="https://ikigaitest.com/ru/")],
        [InlineKeyboardButton(text="Тест на профориентацию", url="https://testometrika.com/career/test-to-determine-career/")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block2")]
    ])
    await callback.message.edit_text(
        "Для более глубокого изучения профориентационных предпочтений советуем пройти тесты по ссылкам:",
        reply_markup=kb
    )
    await callback.answer()
# --- Тест ---
# Вопросы теста (13 вопросов)
questions = [
    "1. Как вы обычно решаете спор или конфликт с друзьями/коллегами?\n\n1️⃣ Анализирую ситуацию, ищу справедливое решение, опираясь на факты и договоренности.\n2️⃣ Стараюсь найти компромисс, чтобы все остались довольны.\n3️⃣ Предпочитаю избегать конфликтов и уступаю.\n4️⃣ Отстаиваю свои интересы любой ценой.",
    "2. Ваше отношение к чтению большого количества сложных текстов (законов, договоров, документов)?\n\n1️⃣ Это интересная интеллектуальная задача, я люблю вникать в детали и нюансы.\n2️⃣ Это необходимая работа, если она ведёт к результату, я готов это делать.\n3️⃣ Это скучно и утомительно, я быстро теряю концентрацию.\n4️⃣ «Чат GPT, перескажи этот текст коротко и понятно, как пятилетнему».",
    "3. Насколько важно для вас четкое следование правилам, инструкциям и процедурам?\n\n1️⃣ Крайне важно. Правила создают порядок, и их нужно соблюдать и правильно толковать.\n2️⃣ Важно, но иногда правила можно гибко трактовать под ситуацию.\n3️⃣ Не очень. Часто правила только мешают живому общению и делу.\n4️⃣ Я человек дела, инструкции не читаю.",
    "4. Как вы ведете себя, когда нужно публично отстоять свою точку зрения перед несогласными?\n\n1️⃣ Готовлюсь, строю логичную аргументацию, сохраняю спокойствие и уверенность.\n2️⃣ Волнуюсь, но могу выступить, если тема мне хорошо знакома.\n3️⃣ Сильно нервничаю, стараюсь избегать таких ситуаций.\n4️⃣ Быстро перехожу на личности и оскорбления, без прелюдий.",
    "5. Что вы думаете о работе с рисками и ответственностью за чужие судьбы или крупные деньги?\n\n1️⃣ Это серьёзно, но именно такая ответственность делает профессию значимой.\n2️⃣ Это давит, но с опытом, наверное, можно к этому привыкнуть.\n3️⃣ Мне было бы очень тяжело и страшно нести такую ношу.\n4️⃣ Я и за себя не всегда отвечаю, но за дело — запросто.",
    "6. Ваш любимый предмет в школе?\n\n1️⃣ История, обществознание, право — анализ событий и систем.\n2️⃣ Иностранные языки, литература — работа с текстами и смыслами.\n3️⃣ Творческие предметы или естественные науки.\n4️⃣ Перемены между уроками.",
    "7. Насколько вы усидчивы и внимательны к деталям?\n\n1️⃣ Очень. Могу подолгу работать с информацией, замечаю малейшие несоответствия.\n2️⃣ Достаточно, но периодически нуждаюсь в смене деятельности.\n3️⃣ Не очень, мне трудно долго концентрироваться на одном.\n4️⃣ Схватываю все на лету, действую по ситуации.",
    "8. Как вы относитесь к необходимости постоянно учиться и отслеживать изменения в профессиональной деятельности?\n\n1️⃣ Это естественная и даже интересная часть профессии.\n2️⃣ Это необходимость, к которой можно приспособиться.\n3️⃣ Это звучит утомительно, хочется однажды выучить и работать.\n4️⃣ Надо уметь закон под себя гнуть, пусть в обновлениях кто-то другой роется, а я ответ по факту дам.",
    "9. Ваша реакция на несправедливость (в жизни, в кино)?\n\n1️⃣ Я горячо желаю восстановить справедливость законными методами.\n2️⃣ Я переживаю и думаю, как можно было бы всё исправить.\n3️⃣ Я расстраиваюсь, но чувствую, что мало что могу изменить.\n4️⃣ Если это не касается меня, то равнодушие.",
    "10. Что для вас важнее в работе?\n\n1️⃣ Статус, интеллектуальный вызов, влияние, чёткость.\n2️⃣ Стабильность, доход, уважение в обществе.\n3️⃣ Творческая реализация, свободный график, комфортная атмосфера.\n4️⃣ Чувство власти, ощущение важности, идея «избранности, превосходства».",
    "11. Приходилось ли вам замечать логические ошибки или неточности в чужих высказываниях?\n\n1️⃣ Постоянно, я сразу их вижу и мысленно исправляю.\n2️⃣ Довольно часто, особенно если тема мне знакома.\n3️⃣ Иногда, но обычно я слушаю общий смысл.\n4️⃣ Редко, я обычно не вслушиваюсь.",
    "12. Как вы принимаете важные решения?\n\n1️⃣ Взвешиваю все «за» и «против», изучаю информацию, советуюсь с экспертами.\n2️⃣ Долго сомневаюсь, но в итоге принимаю решение на основе чувств и фактов.\n3️⃣ Часто полагаюсь на интуицию или совет.\n4️⃣ Обычно я знаю правильный ответ, либо мне так кажется.",
    "13. Как, по вашему мнению, следует поступать с теми, кто систематически нарушает установленные законом порядки?\n\n1️⃣ Применить к нему предусмотренные законом меры, соблюдая процедуры и права человека.\n2️⃣ Делать ставку на неотвратимость и суровость наказания.\n3️⃣ Найти корень проблемы и работать на профилактику.\n4️⃣ Такие антиобщественные индивиды неисправимы, их усыплять надо."
]
@dp.callback_query(F.data == "start_test")
async def start_test(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(TestState.waiting_for_answer)
    await state.update_data(answers=[], current=0)
    await callback.message.edit_text(
        "❓ Тест «Тебе подходит юриспруденция?»\n\n" + questions[0],
        reply_markup=get_test_keyboard(0)
    )
    await callback.answer()
def get_test_keyboard(question_index: int):
    """Клавиатура для ответа на вопрос (варианты 1-4)"""
    builder = InlineKeyboardBuilder()
    for i in range(1, 5):
        builder.button(text=str(i), callback_data=f"test_answer_{i}")
    builder.button(text="❌ Прервать тест", callback_data="cancel_test")
    # ИСПРАВЛЕНО: adjust вызывается ПОСЛЕ добавления всех кнопок
    builder.adjust(4, 1)
    return builder.as_markup()
@dp.callback_query(F.data.startswith("test_answer_"), TestState.waiting_for_answer)
async def process_answer(callback: types.CallbackQuery, state: FSMContext):
    answer = int(callback.data.split("_")[-1])
    data = await state.get_data()
    answers = data.get("answers", [])
    current = data.get("current", 0)
    answers.append(answer)
    current += 1
    if current < len(questions):
        await state.update_data(answers=answers, current=current)
        await callback.message.edit_text(
            questions[current],
            reply_markup=get_test_keyboard(current)
        )
    else:
        counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for ans in answers:
            counts[ans] += 1
        most_common = max(counts, key=counts.get)
        if most_common == 1:
            result = (
                "Большинство ответов «1» — Прирождённый юрист.\n\n"
                "Ваш склад ума — аналитический, ваша стихия — тексты и процедуры. Вы цените справедливость, умеете аргументировать и не боитесь ответственности. Юриспруденция — ваш осознанный и правильный выбор."
            )
        elif most_common == 2:
            result = (
                "Большинство ответов «2» — Гибкий гуманитарий.\n\n"
                "Профессия юриста вам подходит, но, возможно, не в самой жёсткой её форме. Вам стоит присмотреться к смежным направлениям: политологии, государственному управлению или менеджменту."
            )
        elif most_common == 3:
            result = (
                "Большинство ответов «3» — Свободный художник.\n\n"
                "Юридическое образование, скорее всего, будет для вас источником стресса. Присмотритесь к творческим, социальным или научным профессиям."
            )
        else:
            result = (
                "Большинство ответов «4» — Идейный госслужащий.\n\n"
                "Ваши личные качества поразительны, однако требуют доработки. Юридическая догматика — не ваш путь, но ваша решимость и прагматичный взгляд на правопорядок бесценны. "
                "Специально для вас в нашем университете есть программа «Правовое обеспечение национальной безопасности». Мы научим вас применять ваши способности на благо государства."
            )
        await callback.message.edit_text(
            f"✅ Результаты теста\n\n{result}\n\n"
            "Для более глубокого самоопределения рекомендуем пройти дополнительные тесты в разделе «Профориентация».",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
                [InlineKeyboardButton(text="📚 Другие тесты", callback_data="block2_other_tests")]
            ])
        )
        await state.clear()
    await callback.answer()
@dp.callback_query(F.data == "cancel_test")
async def cancel_test(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Тест прерван. Выберите раздел:", reply_markup=main_menu_keyboard())
    await callback.answer()
# ---- БЛОК 3: Студенческая жизнь ----
def block3_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🏛 Корпуса и учебные здания", callback_data="block3_buildings")
    builder.button(text="🏋️ Физкультура и спорт", callback_data="block3_sport")
    builder.button(text="🏠 Общежития", callback_data="block3_dorms")
    builder.button(text="🔗 Полезные интернет-порталы", callback_data="block3_links")
    builder.button(text="🏠 Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()
@dp.callback_query(F.data == "block3")
async def block3_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎓 Блок 3. Жизнь студента\n\n"
        "Узнайте, где проходят занятия, как заниматься спортом и где живут студенты.",
        reply_markup=block3_menu()
    )
    await callback.answer()
@dp.callback_query(F.data == "block3_buildings")
async def buildings(callback: types.CallbackQuery):
    text = "Основные корпуса для юридических специальностей:\n\n• Ленина 13Б\n• Чапаева 16\n• Чапаева 20\n• Мира 19\n• Мира 28"
    # ИСПРАВЛЕНО: добавлена кнопка «Назад»
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block3")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)
    kb_video = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block3")]
    ])
    await callback.message.answer_video(
        VIDEO_CAMPUS,
        caption="Обзор корпусов, аудиторий, коворкингов",
        reply_markup=kb_video
    )
    await callback.answer()
@dp.callback_query(F.data == "block3_sport")
async def sport(callback: types.CallbackQuery):
    # ИСПРАВЛЕНО: добавлена кнопка «Назад»
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block3")]
    ])
    await callback.message.edit_text("*видео про физкультуру, её корпуса, выбор...*", reply_markup=kb)
    kb_video = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block3")]
    ])
    await callback.message.answer_video(
        VIDEO_SPORT,
        caption="Спортивные объекты УрФУ (стадион, манеж, бассейн)",
        reply_markup=kb_video
    )
    await callback.answer()
@dp.callback_query(F.data == "block3_dorms")
async def dorms(callback: types.CallbackQuery):
    # ИСПРАВЛЕНО: добавлена кнопка «Назад» и ссылка вынесена в кнопку
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Сайт студенческого городка", url="https://campus.urfu.ru/ru/")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block3")]
    ])
    await callback.message.edit_text(
        "Все общежития студенческого городка — по ссылке ниже:",
        reply_markup=kb
    )
    await callback.answer()
@dp.callback_query(F.data == "block3_links")
async def links(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="VK ИНЭУ", url="https://vk.com/ineu_urfu")],
        [InlineKeyboardButton(text="VK ПОС ИНЭУ", url="https://vk.com/pos.ineu")],
        [InlineKeyboardButton(text="VK Поселение ИНЭУ", url="https://vk.com/poselenie_ineu")],
        [InlineKeyboardButton(text="Telegram Нацбез УрФУ", url="https://t.me/nazbez_urfu")],
        [InlineKeyboardButton(text="VK Абитуриент УрФУ", url="https://vk.com/abiturient_urfu")],
        [InlineKeyboardButton(text="VK УрФУ", url="https://vk.com/ural.federal.university")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="block3")]
    ])
    await callback.message.edit_text(
        "Полезные сообщества и каналы:",
        reply_markup=kb
    )
    await callback.answer()
# --- Обработка всех "назад" через back_to_ ---
@dp.callback_query(F.data.startswith("back_to_"))
async def back_to_block(callback: types.CallbackQuery):
    # ИСПРАВЛЕНО: используем срез строки вместо split("_")[-1],
    # чтобы корректно обрабатывать составные имена вроде "block1_directions"
    target = callback.data[len("back_to_"):]
    if target == "block1_directions":
        await directions(callback)
    elif target == "block1_admission":
        await admission_main(callback)
    elif target == "block1_jobs":
        await jobs(callback)
    elif target == "block2":
        await block2_handler(callback)
    elif target == "block3":
        await block3_handler(callback)
    else:
        await main_menu(callback)
# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())