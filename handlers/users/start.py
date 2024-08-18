import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.scrapping import get_main
from loader import dp, db, bot
from data.config import ADMINS


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    await message.answer("Xush kelibsiz!")

    # ADMINGA xabar beramiz
    count = await db.count_users()
    msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)


categories = {
    'Mobiles, Computers': [
        {
            'active': False,
            'name':'All Mobile Phones'
            , 'url':"https://www.amazon.in/s?bbn=1389401031&rh=n%3A1389401031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723191101&rnid=2665398031&ref=lp_1389401031_nr_p_n_pct-off-with-tax_5"
        },
        {
            'active': False,
            'name':'All Mobile Accessories',
             'url': "https://www.amazon.in/s?bbn=1389402031&rh=n%3A1389402031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723191162&rnid=2665398031&ref=lp_1389402031_nr_p_n_pct-off-with-tax_5"},
        {
            'active': False,
            'name':'Cases & Covers',
             'url': "https://www.amazon.in/s?bbn=1389409031&rh=n%3A1389409031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723191669&rnid=2665398031&ref=lp_1389409031_nr_p_n_pct-off-with-tax_5"},
        {
            'active': False,
            'name':'Screen Protectors',
             'url': "https://www.amazon.in/s?bbn=1389425031&rh=n%3A1389425031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723191692&rnid=2665398031&ref=lp_1389425031_nr_p_n_pct-off-with-tax_5"},
        {
            'active': False,
            'name':'Power Banks',
             'url': "https://www.amazon.in/s?bbn=6612025031&rh=n%3A6612025031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723191714&rnid=2665398031&ref=lp_6612025031_nr_p_n_pct-off-with-tax_5"},
        # {'Refurbished & Open Box': 'url'},
        {
            'active': False,
            'name':'Tablets',
             'url': "https://www.amazon.in/s?bbn=1375458031&rh=n%3A1375458031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723191792&rnid=2665398031&ref=lp_1375458031_nr_p_n_pct-off-with-tax_5"},
        {
            'active': False,
            'name':'Wearable Devices',
             'url': "https://www.amazon.in/s?bbn=11599648031&rh=n%3A11599648031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723191874&rnid=2665398031&ref=lp_11599648031_nr_p_n_pct-off-with-tax_5"},
        {
            'active': False,
            'name':'Electrónica',
             'url': "https://www.amazon.in/s?i=electronics&srs=13773797031&bbn=13773797031&rh=n%3A976419031%2Cp_n_pct-off-with-tax%3A2665402031&dc&ds=v1%3AVUZhOGMhGQNT7c1F1CuPqyz4vI20gWzfXC8Z4IgQbM8&qid=1723192120&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_3"},
        {
            'active': False,
            'name':'Home & Kitchen',
             'url': "https://www.amazon.in/s?i=kitchen&srs=13773797031&bbn=13773797031&rh=n%3A976442031%2Cp_n_pct-off-with-tax%3A2665402031&dc&ds=v1%3AqkS%2FlL9drVpuB3CydUCSuOSWtYCaPEYozIkbCHydby4&qid=1723192150&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_3"},

        {
            'active': False,
            'name':'Office Supplies & Stationery',
             'url': "https://www.amazon.in/s?bbn=2454172031&rh=n%3A2454172031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723192379&rnid=2665398031&ref=lp_2454173031_nr_p_n_pct-off-with-tax_5"},
        {
            'active': False,
            'name':'Drives & Storage',
             'url': "https://www.amazon.in/s?bbn=1375424031&rh=n%3A1375424031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723192483&rnid=2665398031&ref=lp_1375424031_nr_p_n_pct-off-with-tax_5"},
        {
            'active': False,
            'name':'Printers & Ink',
             'url': "https://www.amazon.in/s?i=computers&bbn=1375443031&rh=n%3A15606842031%2Cp_n_pct-off-with-tax%3A2665399031&dc&qid=1723192596&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_1&ds=v1%3AtpMDSBcHVdJNAiAUpS1PQsIm2o9A8HhyOR1PTMXeQWs"},
        {
            'active': False,
            'name':'Networking Devices',
             'url': "https://www.amazon.in/s?bbn=1375427031&rh=n%3A1375427031%2Cp_n_pct-off-with-tax%3A2665399031&dc&qid=1723192629&rnid=2665398031&ref=lp_1375427031_nr_p_n_pct-off-with-tax_0"},
        {
            'active': False,
            'name':'Computer Accessories',
             'url': "https://www.amazon.in/s?i=computers&bbn=1375248031&rh=n%3A1375248031%2Cp_n_pct-off-with-tax%3A2665401031&dc&ds=v1%3A24DjfyBuAHRic0wrlY%2FqS7%2F0Dz%2F0fZMC3q%2BjY2rdaCQ&qid=1723192678&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_4"},
        {
            'active': False,
            'name':'Game Zone',
             'url': "https://www.amazon.in/s?i=computers&bbn=14142561031&rh=n%3A14142561031%2Cp_n_pct-off-with-tax%3A2665399031&dc&qid=1723192729&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_1&ds=v1%3AsQv0jWjRi0telyJ%2BviVl1gyaI3uqqbQo53pejCWgGog"},
        {
            'active': False,
            'name': 'Monitors',
             'url': "https://www.amazon.in/s?i=computers&bbn=1375425031&rh=n%3A1375425031%2Cp_n_pct-off-with-tax%3A2665402031&dc&ds=v1%3AaY158dch2QoU4JFwapH6Wwquhde1Pkj2D5XAPqf7C5c&qid=1723192775&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_3"},
        {
            'active': False,
            'name':'Desktops',
             'url': "https://www.amazon.in/s?i=computers&bbn=1375392031&rh=n%3A1375392031%2Cp_n_pct-off-with-tax%3A2665401031&dc&qid=1723192841&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_4&ds=v1%3A%2FQXvPSI2ScOPkH98dKOYyQdquiuQl98CO7PZzqPqHx8"},
        {
            'active': False,
            'name': 'Components',
             'url': "https://www.amazon.in/s?bbn=1375344031&rh=n%3A1375344031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723192879&rnid=2665398031&ref=lp_1375344031_nr_p_n_pct-off-with-tax_5"},
        {
            'active': False,
            'name':'All Electronics',
             'url': "https://www.amazon.in/s?bbn=976419031&rh=n%3A976419031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723192927&rnid=2665398031&ref=lp_976420031_nr_p_n_pct-off-with-tax_5"},
    ],
    "TV, Appliances": [
        {
            'active': False,
            'name': 'Televisions',
             'url': 'https://www.amazon.in/s?i=electronics&bbn=1389396031&rh=n%3A1389396031%2Cp_n_pct-off-with-tax%3A2665402031&dc&qid=1723196798&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_3&ds=v1%3AmPmhc%2BtAuzb5VsLjERe0q%2B4XlajO%2FIUEUh52xQ4dlVY'},
        {
            'active': False,
            'name': 'Home Entertainment Systems',
             'url': 'https://www.amazon.in/s?bbn=1389375031&rh=n%3A1389375031%2Cp_n_pct-off-with-tax%3A27060456031&dc&qid=1723197162&rnid=2665398031&ref=lp_1389375031_nr_p_n_pct-off-with-tax_4'},
        {
            'active': False,
            'name': 'Headphones',
             'url': 'https://www.amazon.in/s?bbn=1388921031&rh=n%3A1388921031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723197195&rnid=2665398031&ref=lp_1388921031_nr_p_n_pct-off-with-tax_5'},
        {
            'active': False,
            'name': 'Speakers',
             'url': 'https://www.amazon.in/s?i=electronics&bbn=1389365031&rh=n%3A1389365031%2Cp_n_pct-off-with-tax%3A27060456031&dc&ds=v1%3AmOrd3hjSnJ0Dw7QsWnBwn8aK2rzFWBMLKteLjglGAGA&qid=1723197240&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_5'},
        {
            'active': False,
            'name': 'Cameras',
             'url': 'https://www.amazon.in/s?bbn=1388977031&rh=n%3A1388977031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723197301&rnid=2665398031&ref=lp_1388977031_nr_p_n_pct-off-with-tax_5'},
        {
            'active': False,
            'name': 'DSLR Cameras',
             'url': 'https://www.amazon.in/s?i=electronics&bbn=1389177031&rh=n%3A1389177031%2Cp_n_pct-off-with-tax%3A2665399031&dc&qid=1723197334&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_1&ds=v1%3AoYZ91menhluOa6Kd0VizQm%2F9PDYf2YxFU6AK1WzO9KA'},
        {
            'active': False,
            'name':  'Security Cameras',
             'url': 'https://www.amazon.in/s?i=electronics&bbn=1389203031&rh=n%3A1389203031%2Cp_n_pct-off-with-tax%3A2665401031&dc&ds=v1%3A7hOlkEwEOx1d4iwP9Ml0doVes6ev1%2B0bZCqRdduJMrY&qid=1723197430&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_4'},
        {
            'active': False,
            'name': 'Musical Instruments & Professional Audio',
             'url': 'https://www.amazon.in/s?bbn=3677697031&rh=n%3A3677697031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723197463&rnid=2665398031&ref=lp_3677698031_nr_p_n_pct-off-with-tax_5'},

        {
            'active': False,
            'name':  'Air Conditioners',
             'url': 'https://www.amazon.in/s?bbn=3474656031&rh=n%3A3474656031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723197531&rnid=2665398031&ref=lp_3474656031_nr_p_n_pct-off-with-tax_5'},
        {
            'active': False,
            'name':   'Refrigerators',
             'url': 'https://www.amazon.in/s?i=kitchen&bbn=1380365031&rh=n%3A1380365031%2Cp_n_pct-off-with-tax%3A2665400031&dc&qid=1723197581&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_2&ds=v1%3AZLg%2BQVaI7CqCyrCZcAVRVRajIN4yLh4GdRYNEWpevmI'},
        {
            'active': False,
            'name':'Kitchen & Home Appliances',
             'url': 'https://www.amazon.in/s?bbn=4951860031&rh=n%3A4951860031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723197629&rnid=2665398031&ref=lp_4951860031_nr_p_n_pct-off-with-tax_5'},
        {
            'active': False,
            'name': 'Heating & Cooling Appliances',
             'url': 'https://www.amazon.in/s?i=kitchen&bbn=2083423031&rh=n%3A2083423031%2Cp_n_pct-off-with-tax%3A27060456031&dc&ds=v1%3Ag7HUp2wXe4CzU2nb0RFp%2FqtFFVS9ZmGV32HyWubcr2k&qid=1723197658&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_5'}
    ],
    "Men's Fashion": [
        {
            'active': False,
            'name': "Clothing",
            'url': 'https://www.amazon.in/s?bbn=1968024031&rh=n%3A1968024031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723258653&rnid=2665398031&ref=lp_1968024031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "name",
            'url': 'url1'
        },
        {
            'active': False,
            'name': "T-shirts & Polos",
            'url': 'https://www.amazon.in/s?bbn=1968120031&rh=n%3A1968120031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723258756&rnid=2665398031&ref=lp_1968120031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Shirts",
            'url': 'https://www.amazon.in/s?bbn=1968024031&rh=n%3A1968024031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723258796&rnid=2665398031&ref=lp_1968024031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Jeans",
            'url': 'https://www.amazon.in/s?i=apparel&bbn=1968076031&rh=n%3A1968076031%2Cp_n_pct-off-with-tax%3A27060456031&dc&ds=v1%3AdQwT2tOwQit0CaSM3IAGWk9vk%2BO4DQWs8Zm6WKdRbvU&qid=1723258843&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Innerwear",
            'url': 'https://www.amazon.in/s?bbn=1968126031&rh=n%3A1968126031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723258886&rnid=2665398031&ref=lp_1968126031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Watches",
            'url': 'https://www.amazon.in/s?bbn=2563504031&rh=n%3A2563504031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723258924&rnid=2665398031&ref=lp_2563504031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Bags & Luggage",
            'url': 'url1'
        },
        {
            'active': False,
            'name': "Sunglasses",
            'url': 'https://www.amazon.in/s?bbn=1968036031&rh=n%3A1968036031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259062&rnid=2665398031&ref=lp_1968036031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Jewellery",
            'url': 'https://www.amazon.in/s?bbn=7124359031&rh=n%3A7124359031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259087&rnid=2665398031&ref=lp_7124359031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Shoes",
            'url': 'https://www.amazon.in/s?bbn=1983518031&rh=n%3A1983518031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259153&rnid=2665398031&ref=lp_1983518031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Sport wear",
            'url': 'https://www.amazon.in/s?bbn=12456568031&rh=n%3A12456568031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259205&rnid=2665398031&ref=lp_12456568031_nr_p_n_pct-off-with-tax_5'
        },

    ],
    "Women's Fashion": [
        {
            'active': False,
            'name': "Closing",
            'url':'https://www.amazon.in/s?bbn=1953602031&rh=n%3A1953602031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259304&rnid=2665398031&ref=lp_1953602031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Western wear",
            'url':'https://www.amazon.in/s?bbn=11400137031&rh=n%3A11400137031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259376&rnid=2665398031&ref=lp_11400137031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Ethnic Wear",
            'url':'https://www.amazon.in/s?bbn=1968253031&rh=n%3A1968253031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259413&rnid=2665398031&ref=lp_1968253031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
             'name': "Lingerie & Nightwear",
            'url':'https://www.amazon.in/s?bbn=11400136031&rh=n%3A11400136031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259471&rnid=2665398031&ref=lp_11400136031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
             'name': "Watches",
            'url':'https://www.amazon.in/s?bbn=2563505031&rh=n%3A2563505031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259522&rnid=2665398031&ref=lp_2563505031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
             'name': "Handbags & Clutches",
            'url':'https://www.amazon.in/s?bbn=1983338031&rh=n%3A1983338031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259550&rnid=2665398031&ref=lp_1983338031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
             'name': "Gold & Diamond Jewellery",
            'url':'https://www.amazon.in/s?i=jewelry&bbn=5210069031&rh=n%3A5210069031%2Cp_n_pct-off-with-tax%3A27060456031&dc&ds=v1%3Aqn%2ByXorfVsxS3BXnxSdILoSfaU3jH%2FiCDTZr8n0be8M&qid=1723259617&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
             'name': "Sunglasses",
            'url':'https://www.amazon.in/s?bbn=1968401031&rh=n%3A1968401031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259671&rnid=2665398031&ref=lp_1968401031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
             'name': "Shoes",
            'url':'https://www.amazon.in/s?bbn=1983578031&rh=n%3A1983578031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259700&rnid=2665398031&ref=lp_1983578031_nr_p_n_pct-off-with-tax_5'
        },

    ],
    "Home, Kitchen": [
        {
            'active': False,
             'name': "Kitchen Dining",
            'url':'https://www.amazon.in/s?bbn=5925789031&rh=n%3A5925789031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259831&rnid=2665398031&ref=lp_5925789031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Kitchen storage",
            'url': 'https://www.amazon.in/s?bbn=1379989031&rh=n%3A1379989031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259927&rnid=2665398031&ref=lp_1379989031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Furniture",
            'url': 'https://www.amazon.in/s?bbn=1380441031&rh=n%3A1380441031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723259962&rnid=2665398031&ref=lp_1380441031_nr_p_n_pct-off-with-tax_5'
        },

        {
            'active': False,
            'name': "Home Furnishing",
            'url': 'https://www.amazon.in/s?i=kitchen&bbn=1380447031&rh=n%3A1380447031%2Cp_36%3A3444814031%2Cp_n_pct-off-with-tax%3A27060457031&dc&ds=v1%3A1ue%2FVRFX8Q7rtoR5vF0HRkXzXFNk13FA0awqxuCFnCU&qid=1723260014&rnid=2665398031&ref=sr_nr_p_n_pct-off-with-tax_6'
        },
        {
            'active': False,
            'name': "Garden & Outdoors",
            'url': 'https://www.amazon.in/s?bbn=2454175031&rh=n%3A2454175031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260084&rnid=2665398031&ref=lp_2454176031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Indoor Lighting",
            'url': 'https://www.amazon.in/s?bbn=1380485031&rh=n%3A1380485031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260122&rnid=2665398031&ref=lp_1380485031_nr_p_n_pct-off-with-tax_5'
        },

        {
            'active': False,
            'name': "All Home & Kitchen",
            'url': 'https://www.amazon.in/s?bbn=976442031&rh=n%3A976442031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260162&rnid=2665398031&ref=lp_976443031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "All Pets Supplies",
            'url': 'https://www.amazon.in/s?bbn=2454181031&rh=n%3A2454181031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260198&rnid=2665398031&ref=lp_4740420031_nr_p_n_pct-off-with-tax_5'
        },

    ],
    "Beauty, Health, Grocery": [
        {
            'active': False,
             'name': "Beauty & Grooming",
            'url':'url1https://www.amazon.in/s?bbn=1355016031&rh=n%3A1355016031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260426&rnid=2665398031&ref=lp_1355017031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
             'name': "Luxury Beauty",
            'url':'https://www.amazon.in/s?bbn=5311359031&rh=n%3A5311359031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260500&rnid=2665398031&ref=lp_5311359031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
             'name': "Make-up",
            'url':'https://www.amazon.in/s?bbn=1374357031&rh=n%3A1374357031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260537&rnid=2665398031&ref=lp_1374357031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
             'name': "Health & Personal care",
            'url':'https://www.amazon.in/s?bbn=1350384031&rh=n%3A1350384031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260579&rnid=2665398031&ref=lp_1350385031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "All Grocery & Gourment foods",
            'url': 'https://www.amazon.in/s?bbn=2454178031&rh=n%3A2454178031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260617&rnid=2665398031&ref=lp_2454179031_nr_p_n_pct-off-with-tax_5'
        },

    ],
    "Sports, Fitness, Bags, Luggage": [
        {
            'active': False,
            'name': "Cricket",
            'url': 'https://www.amazon.in/s?bbn=3403628031&rh=n%3A3403628031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260762&rnid=2665398031&ref=lp_3403628031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "Badminton",
            'url': 'https://www.amazon.in/s?bbn=3403619031&rh=n%3A3403619031%2Cp_n_pct-off-with-tax%3A27060457031&dc&qid=1723260806&rnid=2665398031&ref=lp_3403619031_nr_p_n_pct-off-with-tax_5'
        },
        {
            'active': False,
            'name': "name",
            'url': 'url1'
        },
        {
            'active': False,
            'name': "name",
            'url': 'url1'
        },
        {
            'active': False,
            'name': "name",
            'url': 'url1'
        },
        {
            'active': False,
            'name': "name",
            'url': 'url1'
        },
        {
            'active': False,
            'name': "name",
            'url': 'url1'
        },
    ],
    "Toys, Baby Products, Kids' Fashion": [
        {
            'active': False,
             'name': "name",
            'url':'url1'
        }
    ],
    "Car, Motorbike, Industrial": [
        {
            'active': False,
             'name': "name",
            'url':'url1'
        }
    ],

}
# A mapping of unique identifiers to categories
categories_mapping = {
    "mc": "Mobiles, Computers",
    "tv": "TV, Appliances",
    "mf": "Men's Fashion",
    "wf": "Women's Fashion",
    "hk": "Home, Kitchen",
    "bh": "Beauty, Health, Grocery",
    "sf": "Sports, Fitness, Bags, Luggage",
    "tb": "Toys, Baby Products, Kids' Fashion",
    "cm": "Car, Motorbike, Industrial"
}


import urllib.parse

@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for identifier, category in categories_mapping.items():
        button = InlineKeyboardButton(text=category, callback_data=identifier)
        keyboard.add(button)

    await message.answer("Choose a category:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in categories_mapping.keys())
async def select_subcategory(callback_query: types.CallbackQuery):
    category_identifier = callback_query.data
    category_name = categories_mapping[category_identifier]

    # Assuming you have a predefined list of subcategories for each category
    subcategories = categories[category_name]

    keyboard = InlineKeyboardMarkup(row_width=1)
    for subcategory in subcategories:
        subcategory_name = subcategory['name']
        is_active = " ✔️" if subcategory['active'] else ""
        button = InlineKeyboardButton(
            text=subcategory_name + is_active,
            callback_data=f"subcategory:{category_identifier}:{subcategory_name}"
        )
        keyboard.add(button)

    keyboard.add(InlineKeyboardButton(text="Back🔙", callback_data="back"))

    await callback_query.message.edit_text(f"Select {category_name} subcategories:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("subcategory:"))
async def toggle_subcategory(callback_query: types.CallbackQuery):
    _, category_identifier, subcategory_name = callback_query.data.split(":")

    category_name = categories_mapping[category_identifier]

    for subcategory in categories[category_name]:
        if subcategory['name'] == subcategory_name:
            subcategory['active'] = not subcategory['active']
            break

    subcategories = categories[category_name]
    keyboard = InlineKeyboardMarkup(row_width=1)
    for subcategory in subcategories:
        is_active = " ✔️" if subcategory['active'] else ""
        button = InlineKeyboardButton(
            text=subcategory['name'] + is_active,
            callback_data=f"subcategory:{category_identifier}:{subcategory['name']}"
        )
        keyboard.add(button)

    keyboard.add(InlineKeyboardButton(text="Back🔙", callback_data="back"))

    await callback_query.message.edit_text(f"Select {category_name} subcategories:", reply_markup=keyboard)




@dp.callback_query_handler(lambda c: c.data == "back")
async def go_back(callback_query: types.CallbackQuery):
    # Create an inline keyboard with categories
    keyboard = InlineKeyboardMarkup(row_width=1)
    for identifier, category in categories_mapping.items():
        button = InlineKeyboardButton(text=category, callback_data=identifier)
        keyboard.add(button)
    # Edit the message to show the main menu
    await callback_query.message.edit_text("Choose a category:", reply_markup=keyboard)


def get_active_subcategories():
    active_subcategories = []

    # Loop through each category in the dictionary
    for category, subcategories in categories.items():
        for subcategory in subcategories:
            if subcategory['active']:  # Check if the subcategory is active
                active_subcategories.append(subcategory)

    return active_subcategories



@dp.message_handler(text="/work", user_id=ADMINS)
async def start_work(message: types.Message):
    active_subcategories = get_active_subcategories()

    if not active_subcategories:
        await message.answer("No active subcategories found.")
        return

    # Start scraping process for each active subcategory URL
    for subcategory in active_subcategories:
        url = subcategory['url']  # Assuming the subcategory dictionary contains a 'url' key
        subcategory_name = subcategory['name']  # Assuming there's a 'name' key as well
        print(subcategory['name'])
        get_main(url)

        await message.answer(f"Finished scraping for {subcategory_name}.")

    await message.answer("Scraping completed for all active subcategories.")
