Команда: АТ-01 Подбор Аутфитов

Формат системы: Телеграм-бот

Цель проекта:

  Создание сервиса по подбору аутфитов

Описание:
  Телеграм-бот, в котором у пользователя есть возможность собрать аутфит в соответствии с его бюджетом

Целевая аудитория:
  Молодые люди из СНГ в возрасте с 14 до 30 лет

Основное преимущество:
  Удобное расположение проекта в одном из самых популярных мессенджеров в странах СНГ, и в мире в целом

Стек технологий: Python3, json, telebot

Сценарий использования:

  Пользователь находит бота в поиске телеграма и нажимает на команду /start
  Далее он может выбрать категорию из предложенных
  Пользователь подбирает по своему усмотрению одежду  
  С помощью специальной кнопки на Reply-Клавиатуре может указать свой бюджет, который он может потратить на одежду
  Пользователь может просматривать корзину добавленных товаров, и удалить их оттуда
  Пользователь может сравнить цену указанную им, и цену всей его корзины

Основные требования к ПО для пользования:

  Наличие приложение Телеграм
  
Структура приложения:
  
/telegrambot.py - основной файл, где происходит вся работа с ботом  
/packaging.py - файл в котором совершается вся обработка корзины и товаров в каталоге  
/clothes.py - модель товара одежды  
/parser.py - скрипт, выполняющий загрузку карточек товара одежды (в работе бота он не используется)  
/user_budget.json - json-файл, хранящий стоимость корзины и указанный бюджет пользователя по его id  
/user_data.json - json-файл, хранящий товары корзины пользователя по его id  
/clothes.json - json-файл, хранящий весь каталог товаров бота  
