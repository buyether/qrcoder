from aiogram import Bot, Dispatcher, executor, types
import qrcode
import os
from pyzbar.pyzbar import decode
from PIL import Image as PILImage


bot = Bot('6924160060:AAEWPh0nzy9uICy-RysOYBG8atYErnO1YZQ')
dp = Dispatcher(bot)


async def create_qr(user_id, data):
    directory = f"users_data/{user_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,)

    qr.make(fit=True)
    qr.add_data(data)

    filename = f"{directory}/qr.png"
    img = qr.make_image(fill_color=(28, 32, 40), back_color=(207, 222, 255))
    img.save(filename)
    return filename


@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    with open('source/main.png', 'rb') as photo:
        await bot.send_photo(message.from_user.id, photo, caption='<b>Привет!</b>\nЭтот бот поможет создать и расшифровать QR-код.', parse_mode='html')


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def decode_image(message: types.Message):
    user_id = message.from_user.id

    photo = message.photo[-1]
    photo_path = f"users_data/{user_id}/input_image.jpg"
    await photo.download(destination_file=photo_path)

    decoded_objects = decode(PILImage.open(photo_path))
    if decoded_objects:
        decoded_data = decoded_objects[0].data.decode('utf-8')
        await bot.send_message(user_id, text=decoded_data)
    else:
        await bot.send_message(user_id, 'QR-код не обнаружен на изображении')


@dp.message_handler()
async def create_from_text(message: types.Message):
    user_id = message.from_user.id
    data = message.text

    qr_filename = await create_qr(user_id, data)
    with open(qr_filename, 'rb') as photo:
        await bot.send_photo(message.from_user.id, photo, caption=data)

if __name__ == "__main__":
    executor.start_polling(dp)
