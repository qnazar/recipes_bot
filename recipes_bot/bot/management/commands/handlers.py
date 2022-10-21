import os

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from django.conf import settings

from ...models import User, Recipe


def get_current_state(user_id):
    user = User.objects.get(user_id=user_id)
    return user.state


bot = TeleBot(token=settings.TOKEN)
bot.set_my_commands([
    BotCommand('/start', 'Старт'),
    BotCommand('/refresh', 'Оновити рецепти')
])


@bot.message_handler(commands=['start'])
def start(message: Message):
    user, created = User.objects.get_or_create(user_id=message.from_user.id)
    if created:
        user.first_name = message.from_user.first_name
        user.last_name = message.from_user.last_name
        user.username = message.from_user.username
        user.state = 'name'
        user.save()
        bot.send_message(message.from_user.id, f'Привіт! Давай познайомися.\nВведи своє ім’я')
    else:
        bot.send_message(message.from_user.id, 'Ти вже зареєстований.')


@bot.message_handler(func=lambda message: get_current_state(message.from_user.id) == 'name')
def gender(message: Message):
    if message.text.isalpha():
        user = User.objects.get(user_id=message.from_user.id)
        user.state = 'gender'
        user.name = message.text
        user.save()

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = KeyboardButton('Чоловіча')
        btn2 = KeyboardButton('Жіноча')
        keyboard.add(btn1, btn2)

        bot.send_message(message.from_user.id, 'Вибери стать', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Ім’я може складатися лише з літер.')


@bot.message_handler(func=lambda message: get_current_state(message.from_user.id) == 'gender')
def menu(message: Message):
    user = User.objects.get(user_id=message.from_user.id)
    if message.text in ('Чоловіча', 'Жіноча'):
        user.gender = message.text
        user.state = 'menu'
        user.save()

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Про мене')
        keyboard.add('Рецепти')

        bot.send_message(message.from_user.id, 'Реєстрація пройшла успішно.', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Вибери стать з клавіатури нижче.')


@bot.message_handler(func=lambda message: message.text == 'Про мене')
def about(message: Message):
    user = User.objects.get(user_id=message.from_user.id)
    bot.send_message(user.user_id, f'Ім’я: {user.name}\nСтать: {user.gender}')


@bot.message_handler(func=lambda message: message.text == 'Рецепти')
def recipes(message: Message):
    user = User.objects.get(user_id=message.from_user.id)
    user.state = 'recipe'
    user.save()
    all_recipes = Recipe.objects.all()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for recipe in all_recipes:
        keyboard.add(recipe.name)
    bot.send_message(message.from_user.id, 'Обери потрібний рецепт', reply_markup=keyboard)


@bot.message_handler(commands=['refresh'])
def reload_recipes(message: Message):
    user = User.objects.get(user_id=message.from_user.id)
    if user.state == 'recipe':
        recipes = Recipe.objects.all()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for recipe in recipes:
            keyboard.add(recipe.name)
        bot.send_message(message.from_user.id, 'Рецепти оновлено', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Спочатку потрібно зайти в розділ "Рецепти"')


@bot.message_handler(func=lambda message: get_current_state(message.from_user.id) == 'recipe')
def recipe_info(message: Message):
    recipe = Recipe.objects.filter(name=message.text).first()
    if not recipe:
        bot.send_message(message.from_user.id, 'Обери рецепт зі списку нижче')
    else:
        if recipe.photo:
            photo = os.path.join(settings.MEDIA_ROOT, str(recipe.photo))
            with open(photo, 'rb') as photo:
                bot.send_photo(message.from_user.id, photo=photo)
        bot.send_message(message.from_user.id,
                         f'<strong>{recipe.name}</strong>\n{recipe.description}',
                         parse_mode='HTML')
