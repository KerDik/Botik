# Тут много импорта, согласен, я можно сказать только начал знакомство с aiogram, так что импортировал всю хуйню что встречал в инструкциях ))))
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import Message
import asyncio
import logging
import config
# Вот с CallbackQuery я пытался разобраться, поскольку инлайн кнопки бывают очень даже полезны (например я бы смог уже реализовать передачу id в другую функцию - строка 124)
from aiogram.handlers import CallbackQueryHandler, callback_query
from database import dbworker
from aiogram.filters import Command , Filter, StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import reply #Это файл с клавиатурой, я начал перемещать все кнопки туда, а вызывать их буду через 'reply_markup='



db = dbworker()
# Так и не ознакомился с роутером(
rt = Router()
bot = Bot(token=config.TOKEN)
# dp = Dispatcher(storage=MemoryStorage())
dp = Dispatcher()

class CreateProfile(StatesGroup):
	name = State()
	sex = State()
	hair = State()
	cloth = State()
	fact = State()
	game = State()


# Через эту функцию запускаю бота
async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",)
    await dp.start_polling(bot)



# Указанные ниже команды сделал для себя - чтоб видеть кто есть , кого нет 
@dp.message(Command("allw"))
async def allw(message:Message, bot:Bot):
	all_woman = db.show_all_woman()
	fin_g = ''
	for el in all_woman:
		fin_g += f'Имя-{el[2]}\nВо что одета-{el[3]}\nМесто-{el[4]}\nИнтересный факт-{el[5]}\nСовпадение-{el[6]}\n\n\n'
	await message.answer(fin_g)

@dp.message(Command("delete_me_pls"))
async def deleter(message: Message, bot:Bot):
	db.delete_profile(message.from_user.id)
	await message.answer("Считай ты выш(-ел/-ла) из системы🙃")


@dp.message(Command("allm"))
async def allm(message:Message, bot:Bot):
	all_man = db.show_all_man()
	fin_m = ''
	for el in all_man:
		fin_m += f'Имя-{el[2]}\nВо что одета-{el[3]}\nМесто-{el[4]}\nИнтересный факт-{el[5]}\nСовпадение-{el[6]}\n\n\n'
	await message.answer(fin_m)

# Для этих двух нужно будет указать отдельные функции в файле БД, иначе он будет маркировать возвращаемые анкеты как совпавшие(match=1)
# Но пока не дошёл до этого, головняк на другом поймал
@dp.message(Command("fing"))
async def fing(message:Message, bot: Bot):
	girl = db.find_girl(message.from_user.id)
	await bot.send_message(727068614, girl)#id мой если что


@dp.message(Command("finm"))
async def finm(message:Message, bot: Bot):
	man = db.find_man(message.from_user.id)
	await bot.send_message(727068614,man )



# Тут начинается основной блок
@dp.message(StateFilter(None),Command("start"))
async def get_start(message:Message, bot: Bot,state:FSMContext):
	# Тут я проверяю не захотел ли кто повторно поискать кого-нибудь (переход в игру)
	if (db.profile_exists(message.from_user.id)):
		await message.answer("Минуточку...\n Ты уже есть в базе!!!! Так не пойдёт)")
		await message.answer("Я ХОЧУ ПОИГРАТЬ!",reply_markup=reply.reply_keyboard)
	else:	
		await message.answer('Привет! Я помогу тебе найти пару на этот вечер, а может и на следующие несколько.\nДля начала тебе нужно заполнить анкету, а после я пришлю тебе такую же анкету рандомно выбранного для тебя партнера.\nТвоя задача  - всего лишь найти его/её в толпе')
		await asyncio.sleep(7)
		await message.answer('Укажи свой пол:', reply_markup=reply.keyboard)
		#Отсюда код уходит в самый низ, хз почему , но бот молчал и останавливался на этом месте пока я не закинул вссё вниз


# Тут подвернулся видос на 15 минут, решил вкинуть интерактивчик для тех кто пытается повторно заполнить анкету, типа Балда-3
# Выиграешь - сможешь снова поискать, иначе удалится переписка(ну до функционала я тоже не дошёл пока...)
@dp.message(F.text == "PLAY A GAME!")
async def user_exists(message:Message):
	await message.answer("Хорошо, сыграем в кости - а там уже посмотрим, что можно сделать)\nПравила простые - сначала кидаю кость я, потом ты - у кого выпадет чило больше, тот и выиграл(Я кидаю кость и за тебя и за себя)")
	await asyncio.sleep(5)
	await bot.send_message(message.chat.id,'Начинаем игру😈')
	await asyncio.sleep(1)
	bot_data = await bot.send_dice(message.from_user.id)
	bot_data = bot_data.dice.value
	await asyncio.sleep(5)
	user_data = await bot.send_dice(message.from_user.id)
	user_data = user_data.dice.value
	await asyncio.sleep(7)
	if bot_data > user_data:
		await message.answer("Не в этот раз, попытайся найти собеседника без помощи интернетов, у тебя БУКВАЛЬНО пространство наполненое людьми😬")
	elif bot_data < user_data:
		await message.answer("😳😳😳")
		await message.answer("Окей, нажми /delete_me_pls, заполни анкету снова и сможешь повторить поиск(только никому не рассказывай, иначе баланс удач/неудач нарушится и всё пойдёт по...)")
	else:
		await message.answer("Ничья, что поделать🤝(удели внимание реальности, а не мне🫥)")



@dp.message(F.text == "Я парень🤠")
async def find_girl(message:Message):
	idi_w = 0
	girl, idi = db.find_woman(idi_w)
	if not girl:
		await message.answer("Погоди, твоя подружка опаздывает (женщины🙄).\nНужно дождаться пока она заполнит анкету.\nЯ напишу тебе через 5 минут и мы вернёмся к поиску)")
		await asyncio.sleep(300)
		if not db.is_user_gotten(message.from_user.id) :
			await message.answer ("Ну давай ещё разок клацкни",reply_markup=reply.which_one)
		else:
			await message.answer("Ну вот и всё)\nБыл рад помочь скрасить вечер)\nНе хулигань, люби родителей и не делай ставки на спорт 😉 ")
	else:
		man_to_girl = db.man_to_wom(message.from_user.id)
		await message.answer("Вот она - Women с большой буквы😏\nДерзай")
		await message.answer(girl)
		await bot.send_message(idi,"А вот и твой кавалер)")
		await bot.send_message(idi,man_to_girl)



@dp.message(F.text =="Я девушка💁‍♀️")
async def find_man(message:Message):
	idi_m = 0
	man, idi = db.find_male(idi_m)
	if not man:
		await message.answer("Твой кавалер опаздывает\nНужно дождаться пока он заполнит анкету.\nЯ напишу тебе через 5 минут, и мы вернёмся к поиску")
		await asyncio.sleep(300)
		if not db.is_user_gotten(message.from_user.id) :
			await message.answer ("Давай ещё раз",reply_markup=reply.which_one)
		else:
			await message.answer("Ну вот и всё)\nБыл рад помочь скрасить вечер)\nНе хулигань, люби родителей и не пользуйся косметикой с теломеразой😉")
	else:
		girl_to_man = db.wom_to_man(message.from_user.id)
		await message.answer("А вот и твой кавалер😉")
		await bot.send_message(message.chat.id, man)
		await bot.send_message(idi,"А вот и тобой заинтересовались))")
		await bot.send_message(idi,girl_to_man)



# тут вносились окончательные данные и уже потом я переходил к функции поиска 
# Кстати очередной забавный факт -  если вставлять функции под этим хэндлером - в очередной раз можно быть посланым нахуй
# (не гнобите шибко, было мало времени разобраться, чтобы в такие малые сроки понять что к чему)
@dp.message(CreateProfile.fact)
async def fill_fact(message:Message, state=FSMContext ):
	if len(message.text) < 2:
		await message.answer("К сожалению, этого мало, расскажи поподробнее")
	else:
		await state.update_data(fact=message.text)
		db.set_fact(message.from_user.id,message.text)
		await message.answer("Анкета заполнена!\nТеперь нужно немного подождать")
		await asyncio.sleep(10)
		if not db.is_user_gotten(message.from_user.id) :
			await state.clear()
			await message.answer('Ну всё, можем приступать к поиску партнёра🕵️', reply_markup=reply.which_one )
			await message.answer('Ах да, я забыл - ТЫ парень или девушка?')
		else:
			await state.clear()
			await message.answer("Ну вот и всё)\nСпасибо что воспользовались нашим ботом, надеюсь напитки вам понравятся также - как моему коню понравилось их делать) ")



# абсолютно идентично нижнему
@dp.message(CreateProfile.hair)
async def fill_hair(message:Message, state=FSMContext ):
	await state.update_data(hair=message.text)
	db.set_hair(message.from_user.id,message.text)
	await state.set_state(CreateProfile.fact)
	await asyncio.sleep(2)
	await message.answer('И последнее:\nЧто ты мне скажешь сразу после привет?)\n\n(Считайте это паролем друг для друга)\nP.S.\nНеобязательно одно короткое слово, прояви фантазию и подумай чем бы ты смог(-ла) зацепить собеседника🥵')

# с одеждой таже фигня
@dp.message(CreateProfile.cloth)
async def fill_cloth(message:Message, state=FSMContext):
	await state.update_data(cloth=message.text)
	db.set_cloth(message.from_user.id,message.text)
	await state.set_state(CreateProfile.hair)
	await asyncio.sleep(2)
	await message.answer('Удиви меня!\nРасскажи необычный факт о себе🤔')
	
# Первый аргумент имя, вызываю функцию через db и сразу вкладываю его в таблицу по id
@dp.message(CreateProfile.name, F.text)
async def fill_name(message:Message, state=FSMContext ):
	await state.update_data(name=message.text)
	db.set_name(message.from_user.id,message.text)
	await state.set_state(CreateProfile.cloth)
	await asyncio.sleep(2)
	await message.answer('Чем ты сегодня выделяешься из толпы?')
	dp.message.register(fill_cloth)



# Вот эти два нижних приёмыша(от слова "принимать") идут после выбора пола, я решил организовать заполнение анкеты через State()
# Но видимо ничегошеньки я не понял, раз заполняю я снизу вверх.....
# А так, тут я сразу вносил пол и id в таблицу - как бы занимая место , все остальные данные вносил через UPDATE по id
# (когда писал на телеботе - такой формат заполнения давал неплохие результаты, пока все не стали заполнять одновременно...)
@dp.message(F.text == 'MAN')
async def begin(message:Message,state = FSMContext):
	sex = 1
	db.create_man(message.from_user.id, sex)
	await state.set_state(CreateProfile.name)
	await asyncio.sleep(2)
	await message.answer('Как тебя зовут?')
	dp.message.register(fill_name)	

@dp.message(F.text == 'WOMAN')
async def fill_woman(message:Message, state= FSMContext):
	sex = 2
	db.create_woman(message.from_user.id, sex)
	await state.set_state(CreateProfile.name)
	await asyncio.sleep(2)
	await message.answer('Как тебя зовут?')
	dp.message.register(fill_name)


@dp.message(F.text)
async def just_chatting(message:Message):
	await message.answer("Привет!\nСлуш, я ещё маленький чтобы работать чисто на смс-очки, так что ты кликай /start если твоя анкета ещё не создана и внимательно следуй инструкциям!\nХорошего вечера😉")


if __name__ == '__main__':
    asyncio.run(start())