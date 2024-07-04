from aiogram import types, Router, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from apps.products.models import Product, Order
from apps.users.models import UserExtended
from ..consts import TEXT_PRODUCT_ORDER
from ..keyboards import products_keyboard_reply, confirm_purchase_keyboard, main_keyboard

order_router = Router()


class Purchase(StatesGroup):
    selecting_product = State()
    confirming_purchase = State()


@order_router.message(F.text == TEXT_PRODUCT_ORDER)
async def show_products(message: types.Message, state: FSMContext):
    await message.answer("Выберите товар:", reply_markup=await products_keyboard_reply())
    await state.set_state(Purchase.selecting_product)


@order_router.message(Purchase.selecting_product, Text)
async def select_product(message: types.Message, state: FSMContext):
    product_name = message.text.split(" - ")[0]
    try:
        product = await Product.objects.aget(name=product_name)
        await state.update_data(product_id=product.id)
        await message.answer(
            f"Вы хотите купить {product.name} за {product.price} руб.? Подтвердите покупку:",
            reply_markup=confirm_purchase_keyboard()
        )
        await state.set_state(Purchase.confirming_purchase)
    except Product.DoesNotExist:
        await message.answer("Извините, такой товар не найден. Пожалуйста, выберите другой товар.")


@order_router.message(Purchase.confirming_purchase, Text)
async def confirm_purchase(message: types.Message, state: FSMContext):
    if message.text == "Подтвердить покупку":
        user_data = await state.get_data()
        product_id = user_data.get("product_id")
        try:
            product = await Product.objects.aget(id=product_id)
            user = await UserExtended.objects.aget(tg_chat_id=message.from_user.id)

            # Проверка на достаточность средств на балансе
            if user.balance < product.price:
                await message.answer("Недостаточно средств на балансе для совершения покупки.",
                                     reply_markup=await main_keyboard(user=user))
                await state.clear()
                return

            # Уменьшение баланса пользователя
            user.balance -= product.price
            await user.asave(update_fields=['balance'])

            # Создание заказа
            await Order(product=product, user=user).asave()
            await message.answer(
                f"Вы успешно купили {product.name} за {product.price}! Ваш текущий баланс: {user.balance}.",
                reply_markup=await main_keyboard(user=user))
            await state.clear()
        except Product.DoesNotExist:
            await message.answer("Извините, товар не найден.")
    elif message.text == "Отменить":
        await message.answer("Покупка отменена.", reply_markup=await main_keyboard(message=message))
        await state.clear()
    else:
        await message.answer("Пожалуйста, выберите 'Подтвердить покупку' или 'Отменить'.")
