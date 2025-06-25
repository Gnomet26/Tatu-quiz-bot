from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, PollAnswerHandler
from const import admin_id, token
from file_to_json import process_questions_from_text
from Questions import set_test,get_test
from Users import insert, get_all_user, delete, delete_all,get_user,update_user
from RandomGenerator import generate

savollar = {}
true_list = {}


async def go_test(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:

    first_name = update.effective_user.first_name
    last_name = update._effective_user.last_name
    user_id = update.effective_user.id

    try:
        message = insert(first_name, last_name, user_id,0)
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
            index = 0

            for i in dat:
                mass = []
                varint_ = {}
                index2 = 0
                for j in i.options:
                    mass.append(j.text)
                dat = generate(mass)
                mass = dat['new_variant']
                true_list[index] = dat['true_index']
                varint_['savol'] = i.text
                for j in mass:
                    varint_[index2] = str(j)
                    index2 += 1

                savollar[index] = varint_

                del varint_
                del mass
                index += 1
                  
            for i in users:
                m = []
                for j in range(4):
                    m.append(savollar[0][j])
                    
                await context.bot.send_poll(
                    chat_id = i.telegram_id, 
                    question=savollar[0]['savol'], 
                    options=m,type='quiz', 
                    correct_option_id=true_list[0], 
                    is_anonymous=False, 
                    allows_multiple_answers=False
                    )  
                 

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
    
    poll_answer = update.poll_answer
    print(poll_answer.option_ids[0])
    print(poll_answer.poll_id)
    print(poll_answer.user.first_name)
    print(poll_answer.user.last_name)
    print(poll_answer.user.id)
    print(get_user(poll_answer.user.id).question_number)

    if int(poll_answer.option_ids[0]) == true_list[int(get_user(poll_answer.user.id).question_number)]:
        new_answer = get_user(poll_answer.user.id).question_number + 1
        trues = get_user(poll_answer.user.id).true_answer_number
        falses = get_user(poll_answer.user.id).false_answer_number
        update_user(poll_answer.user.id, new_answer,trues+1,falses)
        if int(new_answer) < len(true_list):
            m = []
            for j in range(4):
                m.append(savollar[new_answer][j])
            await context.bot.send_poll(
                chat_id = poll_answer.user.id, 
                question=savollar[new_answer]['savol'], 
                options=m,type='quiz', 
                correct_option_id=true_list[new_answer], 
                is_anonymous=False, 
                allows_multiple_answers=False
                ) 
        else:
            await context.bot.send_message(chat_id=poll_answer.user.id ,text=f"{poll_answer.user.first_name} Siz testni tugatdingiz")
            await context.bot.send_message(chat_id=poll_answer.user.id ,text=f"Natijangiz\nJami savollar soni: {len(true_list)}\nTo'g'ri javoblar soni:{get_user(poll_answer.user.id).true_answer_number}\nXato javoblar soni: {get_user(poll_answer.user.id).false_answer_number}")
            
    else:
        new_answer = get_user(poll_answer.user.id).question_number + 1
        trues = get_user(poll_answer.user.id).true_answer_number
        falses = get_user(poll_answer.user.id).false_answer_number
        update_user(poll_answer.user.id, new_answer,trues,falses+1)

        if int(new_answer) < len(true_list):
            m = []
            for j in range(4):
                m.append(savollar[new_answer][j])
            await context.bot.send_poll(
                chat_id = poll_answer.user.id, 
                question=savollar[new_answer]['savol'], 
                options=m,type='quiz', 
                correct_option_id=true_list[new_answer], 
                is_anonymous=False, 
                allows_multiple_answers=False
                ) 
        else:
            await context.bot.send_message(chat_id=poll_answer.user.id ,text=f"{poll_answer.user.first_name} Siz testni tugatdingiz")
            await context.bot.send_message(chat_id=poll_answer.user.id ,text=f"Natijangiz\nJami savollar soni: {len(true_list)}\nTo'g'ri javoblar soni:{get_user(poll_answer.user.id).true_answer_number}\nXato javoblar soni: {get_user(poll_answer.user.id).false_answer_number}")
            
        
        

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        delete_all()
        await context.bot.send_message(admin_id, "test to'xtatildi")
    except:
        await context.bot.send_message(admin_id, "Xatolik, test yakunlanmadi")

app.add_handler(CommandHandler("go", go))
app.add_handler(CommandHandler("stop",stop))
app.add_handler(CommandHandler("start", go_test))
app.add_handler(CommandHandler("stop_test", stop_test))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
app.add_handler(PollAnswerHandler(poll_answer_handler))

app.run_polling()