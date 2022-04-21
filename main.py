from handlaers.admin_panel import *
from handlaers.startFor import *
from langlist import *
from deep_translator import GoogleTranslator

@dp.message_handler(commands='help')
async def help(message: types.Message):
	await message.reply(f"""<b>Assalomu alaykum {message.from_user.first_name}</b>.\n\n

Botdan to'g'ri foydalanish:

✅Tilni tanlash bo'limida ikki ustunda tillar berilgan, bular:
1️⃣ - ustunga siz yuboradigan matn tilini belgilaysiz
2️⃣ - ustunga siz yuborgan matnizni tarjima qilish kerak bo'lgan  tilni belgilaysiz


♻️Tilni almashtirish uchun /lang kommondasini yuboring

👨‍💻Agarda botda biror muammo sezsangiz adminga murojaat qiling: @coder_admin_py

〽️Tijoriy xamkorlik uchun admin: @coder_admin_py""")

@dp.message_handler(commands="lang")
async def qayt(message: types.Message):
	user_id = message.from_user.id
	changeLangs = InlineKeyboardMarkup(row_width=2)
	check = sql.execute(f"""SELECT * FROM choosLang WHERE user_id = {user_id}""").fetchone()
	buttons = []
	for button in lang_list:
		if check == None:
			buttons.append(InlineKeyboardButton(text=button, callback_data=button))
		else:
			if button in check:
				buttons.append(InlineKeyboardButton(text=f"✅{button}", callback_data=button))
			else:
				buttons.append(InlineKeyboardButton(text=button, callback_data=button))
	changeLangs.add(*buttons)

	await message.reply("""Botdan to'g'ri foydalanish:

✅Tilni tanlash bo'limida ikki ustunda tillar berilgan, bular:
1️⃣ - ustunga siz yuboradigan matn tilini belgilaysiz
2️⃣ - ustunga siz yuborgan matnizni tarjima qilish kerak bo'lgan  tilni belgilaysiz


♻️Tilni almashtirish uchun /lang kommondasini yuboring""", reply_markup=changeLangs)

@dp.callback_query_handler(text="✅Tilni tanlash")
async def checkl(call: types.CallbackQuery):
	await call.answer("✅Tilni tanlang")
	await call.message.edit_text("""Botdan to'g'ri foydalanish:

✅Tilni tanlash bo'limida ikki ustunda tillar berilgan, bular:
1️⃣ - ustunga siz yuboradigan matn tilini belgilaysiz
2️⃣ - ustunga siz yuborgan matnizni tarjima qilish kerak bo'lgan  tilni belgilaysiz


♻️Tilni almashtirish uchun /lang kommondasini yuboring""")
	user_id = call.from_user.id
	changeLangs = InlineKeyboardMarkup(row_width=2)
	check = sql.execute(f"""SELECT * FROM choosLang WHERE user_id = {user_id}""").fetchone()
	buttons = []
	for button in lang_list:
		if check == None:
			buttons.append(InlineKeyboardButton(text=button, callback_data=button))
		else:
			if button in check:
				buttons.append(InlineKeyboardButton(text=f"✅{button}", callback_data=button))
			else:
				buttons.append(InlineKeyboardButton(text=button, callback_data=button))
	changeLangs.add(*buttons)
	await call.message.edit_reply_markup(reply_markup=changeLangs)

@dp.callback_query_handler()
async def choosL(call: types.CallbackQuery):
	user_id = call.from_user.id
	checks = sql.execute(f"""SELECT lang_in FROM choosLang WHERE user_id = {call.from_user.id}""").fetchone()
	if checks == None:
		sql.execute(
			f"""INSERT INTO choosLang (user_id, nums) VALUES ('{user_id}', 'face')""")
		db.commit()
		if call.data in langL1:
			sql.execute(f"UPDATE choosLang SET lang_in = ? WHERE user_id = ?", (f"{call.data}", f"{user_id}"))
			db.commit()
		else:
			sql.execute(f"UPDATE choosLang SET lang_out = ? WHERE user_id = ?", (f"{call.data}", f"{user_id}"))
			db.commit()
	else:
		if call.data in langL1:
			sql.execute(f"UPDATE choosLang SET lang_in = ? WHERE user_id = ?", (f"{call.data}", f"{user_id}"))
			db.commit()
		else:
			sql.execute(f"UPDATE choosLang SET lang_out = ? WHERE user_id = ?", (f"{call.data}", f"{user_id}"))
			db.commit()
	await call.answer("Tanlandi")
	changeLangs = InlineKeyboardMarkup(row_width=2)
	check = sql.execute(f"""SELECT * FROM choosLang WHERE user_id = {user_id}""").fetchone()
	buttons = []
	if check == None:
		for button in lang_list:
			buttons.append(InlineKeyboardButton(text=button, callback_data=button))
		changeLangs.add(*buttons)
	else:
		for button in lang_list:
			if check == None:
				buttons.append(InlineKeyboardButton(text=button, callback_data=button))
			else:
				if button in check:
					buttons.append(InlineKeyboardButton(text=f"✅{button}", callback_data=button))
				else:
					buttons.append(InlineKeyboardButton(text=button, callback_data=button))
		changeLangs.add(*buttons)
	try:
		await call.message.edit_reply_markup(changeLangs)
	except:
		pass

@dp.message_handler(content_types="text")
async def translet(message: types.Message):
	sql.execute("SELECT id FROM channels")
	rows = sql.fetchall()
	join_inline = types.InlineKeyboardMarkup(row_width=1)
	for row in rows:
		all_details = await dp.bot.get_chat(chat_id=row[0])
		title = 1
		url = all_details['invite_link']
		join_inline.insert(InlineKeyboardButton(f"{title} - kanal", url=url))
		title+=1
	join_inline.add(InlineKeyboardButton("🔁 Tekshirish", callback_data='check'))

	if await functions.check_on_start(message.chat.id):
		try:
			user_id = message.from_user.id
			lang_in = sql.execute(f"""SELECT lang_in FROM choosLang WHERE user_id = {user_id}""").fetchone()
			lang_out = sql.execute(f"""SELECT lang_out FROM choosLang WHERE user_id = {user_id}""").fetchone()
			translator = GoogleTranslator(source=lang_inn[lang_in[0]], target=lang_outt[lang_out[0]])
			await message.reply(translator.translate(message.text))
		except:
			await message.reply("Xatolik sodir bo'ldi.\n\nSiz tilni qaytadan tanlang\n\nQaytadan tanlash uchun /lang dan foydalaning")
	else:
		await message.answer("Botimizdan foydalanish uchun kanalimizga azo bo'ling", reply_markup=join_inline)



if __name__=="__main__":
	executor.start_polling(dp)
