from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, PollAnswerHandler
from const import admin_id, token
from file_to_json import process_questions_from_text
from Questions import set_test,get_test
from Users import insert, get_all_user, delete, delete_all


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def go_test(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:

    first_name = update.effective_user.first_name
    last_name = update._effective_user.last_name
    user_id = update.effective_user.id

    try:
        message = insert(first_name, last_name, user_id)
        if message == 'ok':
            await update.message.reply_text("✅ Testga qo'shildingiz, admin boshlashini kuting...")

        else:
            await update.message.reply_text(f"⚠️ {message}")
    except ValueError as e:
        await update.message.reply_text(e)
    

async def test_fun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("hello")



async def stop_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    try:
        delete(user_id)
        await context.bot.send_message(user_id, "Siz testdan chiqib ketdingiz")
    except:
        await context.bot.send_message(user_id, "Nimadir xato bo'ldi, qayta urinib ko'ring")



async def go(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("⚠️ To'g'ri foydalanish: /go <raqam>")
        return

    if str(update.effective_user.id) == str(admin_id):
        
        number = int(context.args[0])
        print(f"Admin yuborgan raqam: {number}")
        await update.message.reply_text(f"✅ Qabul qilindi: {number}")

        users = get_all_user()

        for i in users:
            try:
                await context.bot.send_message(i.telegram_id, "Test boshlandi")
            except: 
                await context.bot.send_message(int(admin_id), f"{i.ism} {i.familya} xabar yuborilmadi")
        try:
            dat = get_test(number=number)

            for i in users:
                try:
                    await context.bot.send_poll(
                        chat_id=i.telegram_id,
                        question="O'zbekiston poytaxti qaysi?",
                        options=["Toshkent", "Buxoro", "Samarqand", "Navoiy"],
                        type='quiz',
                        correct_option_id=0,
                        is_anonymous=False
                    )
                except:
                    pass


        except ValueError as e:
            print(e)
    else:
        await update.message.reply_text("⚠️ Ruxsat yo'q")




async def handle_document(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if str(user_id) == admin_id:
        file = update.message.document
        with open('savollar.txt', 'r', encoding='utf-8') as file:
            data = file.read()

        results, errors = process_questions_from_text(data)
        error_result = ""
        if errors:
            error_result += "‼️ Xatoliklar:\n\n"
            for e in errors:
                error_result += str(" - " + e)
            await update.message.reply_text(error_result)
        else:
            await update.message.reply_text("✅ Barcha savollar muvaffaqiyatli o‘qildi!\n✅ Barcha savollar va variantlar bazaga muvaffaqiyatli yuklandi.")
            
            set_test(results)
    else:
        pass

app = ApplicationBuilder().token(token).build()






async def poll_answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    poll_id = update.poll_answer.poll_id
    poll_answer = update.poll_answer
    selected_option = update.poll_answer.option_ids[0]
    user = update.poll_answer.user  # Telegram foydalanuvchisi
    selected_option = poll_answer.option_ids[0]
    print(poll_answer)

    # To‘g‘ri yoki xato aniqlanadi
'''is_correct = selected_option == correct_option_id

    # 🔍 Natijani chiqaramiz
    print("📥 Yangi javob:")
    print(f"👤 Foydalanuvchi: {user.first_name} {user.last_name or ''} (Telegram ID: {user.id})")
    print(f"📊 Javobi: {'✅ To‘g‘ri' if is_correct else '❌ Xato'} (Tanlangan: {selected_option}, To‘g‘ri: {correct_option_id})")'''







async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        delete_all()
        await context.bot.send_message(admin_id, "test to'xtatildi")
    except:
        await context.bot.send_message(admin_id, "Xatolik, test yakunlanmadi")

app.add_handler(CommandHandler("go", go))
app.add_handler(CommandHandler("stop",stop))
app.add_handler(CommandHandler("go_test", go_test))
app.add_handler(CommandHandler("stop_test", stop_test))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
app.add_handler(PollAnswerHandler(poll_answer_handler))

app.run_polling()