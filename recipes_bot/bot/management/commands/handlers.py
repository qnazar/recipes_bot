import os

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from django.conf import settings

from ...models import User, Recipe


def get_current_state(user_id):
    user = User.objects.get(user_id=user_id)
    return user.state


bot = TeleBot(token=settings.TOKEN)


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
    user = User.objects.get(user_id=message.from_user.id)
    user.state = 'gender'
    user.name = message.text
    user.save()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Чоловіча')
    btn2 = KeyboardButton('Жіноча')
    keyboard.add(btn1, btn2)

    bot.send_message(message.from_user.id, 'Вибери стать', reply_markup=keyboard)


@bot.message_handler(func=lambda message: get_current_state(message.from_user.id) == 'gender')
def menu(message: Message):
    user = User.objects.get(user_id=message.from_user.id)
    user.state = 'menu'
    user.gender = message.text
    user.save()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Про мене')
    keyboard.add('Рецепти')

    bot.send_message(message.from_user.id, 'Реєстрація пройшла успішно', reply_markup=keyboard)


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


@bot.message_handler(func=lambda message: get_current_state(message.from_user.id) == 'recipe')
def recipe_info(message: Message):
    recipe = Recipe.objects.get(name=message.text)
    if recipe.photo:
        photo = os.path.join(settings.MEDIA_ROOT, str(recipe.photo))
        with open(photo, 'rb') as photo:
            bot.send_photo(message.from_user.id, photo=photo)
    bot.send_message(message.from_user.id, f'<strong>{recipe.name}</strong>\n{recipe.description}', parse_mode='HTML')
