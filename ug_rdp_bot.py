from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8600733435:AAFBTbcHdsDDn9N29wPEuXS33NIXgiMyXxQ"
OWNER_ID = 7405675709  # Temporary — replace with client's Telegram ID later

# ── BROADCAST LIST ──────────────────────────────────────────
subscriber_ids = set()

# ── WAITING STATES ───────────────────────────────────────────
waiting_for_order = set()
waiting_for_support = set()

# ── MENU ────────────────────────────────────────────────────
main_menu = ReplyKeyboardMarkup(
    [["🖥️ Buy RDP/VPS", "💰 Pricing"],
     ["❓ FAQs", "📢 Subscribe to Updates"],
     ["🛠️ Support", "📞 Contact Us"]],
    resize_keyboard=True
)

# ── /start ───────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    subscriber_ids.add(update.effective_chat.id)
    await update.message.reply_text(
        f"👋 Welcome, {user}!\n\n"
        "I'm *UG RDP Server Bot* 🖥️\n\n"
        "We offer premium *Windows VPS / RDP* services.\n"
        "Fast. Reliable. Affordable.\n\n"
        "What would you like to do today?",
        parse_mode="Markdown",
        reply_markup=main_menu
    )

# ── MESSAGE HANDLER ──────────────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id
    user = update.effective_user
    subscriber_ids.add(chat_id)

    # ── Waiting for order details ──
    if chat_id in waiting_for_order:
        waiting_for_order.discard(chat_id)
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=(
                f"🛒 *New Order Received!*\n\n"
                f"👤 *From:* {user.full_name}\n"
                f"🆔 *Username:* @{user.username or 'no username'}\n"
                f"📩 *Order Details:*\n{text}"
            ),
            parse_mode="Markdown"
        )
        await update.message.reply_text(
            "✅ *Order Received!*\n\n"
            "Thank you! Our team will confirm your order and send your RDP details shortly.\n\n"
            "📱 You can also reach us directly at:\n"
            "*08068767013*",
            parse_mode="Markdown",
            reply_markup=main_menu
        )
        return

    # ── Waiting for support message ──
    if chat_id in waiting_for_support:
        waiting_for_support.discard(chat_id)
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=(
                f"🚨 *New Support Request!*\n\n"
                f"👤 *From:* {user.full_name}\n"
                f"🆔 *Username:* @{user.username or 'no username'}\n"
                f"📩 *Message:*\n{text}"
            ),
            parse_mode="Markdown"
        )
        await update.message.reply_text(
            "✅ *Support request received!*\n\n"
            "Our team will get back to you shortly.\n\n"
            "📱 For urgent issues call: *08068767013*",
            parse_mode="Markdown",
            reply_markup=main_menu
        )
        return

    if text == "🖥️ Buy RDP/VPS":
        waiting_for_order.add(chat_id)
        await update.message.reply_text(
            "🖥️ *Place Your Order*\n\n"
            "Please send your order details in this format:\n\n"
            "1️⃣ *Plan you want* (see 💰 Pricing for options)\n"
            "2️⃣ *Your full name*\n"
            "3️⃣ *Payment method* (Transfer or other)\n\n"
            "Type it below and send ⬇️",
            parse_mode="Markdown"
        )

    elif text == "💰 Pricing":
        await update.message.reply_text(
            "💰 *Our Pricing*\n\n"
            "🖥️ *Windows VPS / RDP*\n\n"
            "📦 *Standard Plan*\n"
            "   ₦35,000 / $30\n"
            "   ✅ Windows VPS (RDP Access)\n"
            "   ✅ Fast & Reliable Connection\n"
            "   ✅ Full Admin Access\n"
            "   ✅ 24/7 Uptime\n\n"
            "📩 Contact us for custom plans and bulk pricing!\n\n"
            "_Prices may vary. Contact us to confirm current rates._",
            parse_mode="Markdown"
        )

    elif text == "❓ FAQs":
        await update.message.reply_text(
            "❓ *Frequently Asked Questions*\n\n"
            "1️⃣ *What is RDP/VPS?*\n"
            "   RDP (Remote Desktop Protocol) lets you access a Windows computer remotely from anywhere in the world\n\n"
            "2️⃣ *What can I use it for?*\n"
            "   Running software 24/7, forex trading bots, browsing, remote work, gaming and more\n\n"
            "3️⃣ *How do I access it after purchase?*\n"
            "   We send you the IP address, username and password to connect via Windows Remote Desktop\n\n"
            "4️⃣ *How fast is the connection?*\n"
            "   Very fast — our servers are optimised for low latency\n\n"
            "5️⃣ *How do I pay?*\n"
            "   Bank transfer or other agreed payment methods\n\n"
            "6️⃣ *How quickly do I get access after payment?*\n"
            "   Within a few hours of confirmed payment",
            parse_mode="Markdown"
        )

    elif text == "📢 Subscribe to Updates":
        subscriber_ids.add(chat_id)
        await update.message.reply_text(
            "✅ *Subscribed!*\n\n"
            "You'll now receive updates on:\n"
            "• New plans & pricing\n"
            "• Special deals & discounts\n"
            "• Service announcements\n\n"
            "Stay tuned! 📡",
            parse_mode="Markdown"
        )

    elif text == "🛠️ Support":
        waiting_for_support.add(chat_id)
        await update.message.reply_text(
            "🛠️ *Technical Support*\n\n"
            "Please describe your issue:\n\n"
            "1️⃣ *What is the problem?*\n"
            "2️⃣ *Your RDP/VPS username or IP* (if you have one)\n"
            "3️⃣ *How long has it been happening?*\n\n"
            "Type it below and send ⬇️",
            parse_mode="Markdown"
        )

    elif text == "📞 Contact Us":
        await update.message.reply_text(
            "📞 *Contact UG RDP Server*\n\n"
            "📱 Phone/WhatsApp: 08068767013\n\n"
            "⚡ We typically respond within 1 hour!\n\n"
            "_For faster response send a message via WhatsApp_",
            parse_mode="Markdown"
        )

    else:
        await update.message.reply_text(
            "🤔 I didn't quite understand that.\n"
            "Please use the menu below 👇",
            reply_markup=main_menu
        )

# ── /broadcast (owner only) ──────────────────────────────────
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != OWNER_ID:
        await update.message.reply_text("⛔ You are not authorised to use this command.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast Your message here")
        return

    message = " ".join(context.args)
    count = 0
    for uid in subscriber_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 *UG RDP Server Update*\n\n{message}", parse_mode="Markdown")
            count += 1
        except:
            pass

    await update.message.reply_text(f"✅ Message sent to {count} subscriber(s).")

# ── RUN ──────────────────────────────────────────────────────
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 UG RDP Server Bot is running...")
app.run_polling()
