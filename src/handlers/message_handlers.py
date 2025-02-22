from handlers.handlers import (
    admins_page,
    settings_page,
    notif_page,
    return_to_main_menu,
    plans_page,
    show_plans_with_button,
    save_new_help_message,
    save_new_register_message,
    add_user_step1,
    send_emails_,
    renew_user_step1,
    admins_menu,
    delete_user_step1,
    get_admin_info,
)
from db.query import admins_query, help_message_query, registering_message
from messages.messages import messages_setting
from config import bot, Admin_chat_id
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from api import *


# message handler
@bot.message_handler(func=lambda call: True)
def message_handler(message):
    chat_id = message.chat.id
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="👤 Register 👤", callback_data="Register")
    button2 = InlineKeyboardButton(text="👤 Login 👤", callback_data="login")
    markup.add(button1, button2)

    if message.text == "👤 نمایندگان" and message.chat.id == Admin_chat_id:
        return admins_page(message)

    if message.text == "⚙️ تنظیمات" and message.chat.id == Admin_chat_id:
        settings_page(message)
    if message.text == "🔙 بازگشت" and message.chat.id == Admin_chat_id:
        return_to_main_menu(message)
    if message.text == "💵 پلن ها" and message.chat.id == Admin_chat_id:
        plans_page(message)

    if message.text == "📘 متن راهنما" and message.chat.id == Admin_chat_id:
        help_message = help_message_query.show_message()
        help_message = help_message["message"]

        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("❌ بازگشت ❌"))
        msg = bot.send_message(
            chat_id,
            f"*\n📘متن قبلی:*\n\n```\n{help_message}```\n\n ♻️لطفا متن جدید خود را وارد کنید:",
            parse_mode="markdown",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, save_new_help_message)

    if message.text == "🧾 متن ثبت نام" and message.chat.id == Admin_chat_id:
        register_text = registering_message.show_message()
        register_text = register_text["message"]

        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("❌ بازگشت ❌"))
        msg = bot.send_message(
            chat_id,
            f"*\n🧾متن ثبت نام قبلی:*\n\n```\n{register_text}```\n\n ♻️لطفا متن جدید خود را وارد کنید:",
            parse_mode="markdownv2",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, save_new_register_message)

    if message.text == "🔔 نوتیف ها" and message.chat.id == Admin_chat_id:
        notif_page(message)

    if message.text == "👤 افزودن کاربر 👤":
        if not admins_query.admin_approval(chat_id):
            bot.send_message(
                chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup
            )
            return
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(KeyboardButton("❌ بازگشت ❌"))
            bot.send_message(chat_id, messages_setting.ADD_USER_STEP1, reply_markup=markup)
            bot.register_next_step_handler(message, lambda msg: add_user_step1(msg))

    if message.text == "🪪 نمایش کاربران 🪪":
        if not admins_query.admin_approval(chat_id):
            bot.send_message(
                chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup
            )
            return
        else:
            send_emails_(chat_id)

    if message.text == "⌛ تمدید کاربر ⌛":
        if not admins_query.admin_approval(chat_id):
            bot.send_message(
                chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup
            )
            return
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(KeyboardButton("❌ بازگشت ❌"))
            msg = bot.send_message(
                chat_id, f"*{messages_setting.RENEW_SUER}*", parse_mode="markdown", reply_markup=markup
            )
            bot.register_next_step_handler(msg, renew_user_step1)

    if message.text == "🎯 راهنما 🎯":
        help_message = help_message_query.show_message()
        help_message = help_message["message"]
        bot.reply_to(
            message,
            f"*{help_message}*",
            parse_mode="markdown",
            reply_markup=admins_menu(),
        )

    if message.text == "🗑️ حذف کاربر 🗑️":
        if not admins_query.admin_approval(chat_id):
            bot.send_message(
                chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup
            )
            return
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(KeyboardButton("❌ بازگشت ❌"))
            msg = bot.send_message(
                chat_id,
                "⚠️نام کاربر مورد نظر رو جهت حذف کاربر ارسال کنید:",
                reply_markup=markup,
            )
            bot.register_next_step_handler(msg, delete_user_step1)

    if message.text == "💵 خرید ترافیک 💵":
        if not admins_query.admin_approval(chat_id):
            bot.send_message(
                chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup
            )
            return
        else:
            show_plans_with_button(chat_id)

    if message.text == "❌ خارج شدن ❌":
        if admins_query.remove_chat_id(chat_id):
            bot.send_message(
                chat_id,
                "❌ شما از پنل مدیریتی خود خارج شدید ، جهت استفاده مجدد لاگین کنید:",
                reply_markup=markup,
            )
            return
        else:
            pass

    if message.text == "💎 مشخصات من 💎":
        if not admins_query.admin_approval(chat_id):
            bot.send_message(
                chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup
            )
            return
        else:
            get_admin_info(chat_id)
