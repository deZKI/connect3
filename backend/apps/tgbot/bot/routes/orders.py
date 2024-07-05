from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from apps.products.models import Product, Order
from apps.users.models import UserExtended
from ..consts import *
from ..decorators import user_is_payed
from ..keyboards import products_keyboard_reply, confirm_purchase_keyboard, main_keyboard

order_router = Router()


class Purchase(StatesGroup):
    selecting_product = State()
    confirming_purchase = State()


@order_router.message(F.text == TEXT_MY_ORDERS)
@user_is_payed
async def send_my_orders(message: types.Message):
    await message.answer('Ваши заказы', reply_markup=await main_keyboard(message=message))


@order_router.message(F.text == TEXT_PRODUCT_ORDER)
async def show_products(message: types.Message, state: FSMContext):
    await message.answer(TEXT_PRODUCT_CHOOSE, reply_markup=await products_keyboard_reply())
    await state.set_state(Purchase.selecting_product)


@order_router.message(Purchase.selecting_product)
async def select_product(message: types.Message, state: FSMContext):
    if message.text == TEXT_BACK:
        await state.clear()  # Завершаем текущее состояние FSM
        await message.answer("Вы вернулись в главное меню.", reply_markup=await main_keyboard(message=message))
        return

    product_name = message.text.split(" - ")[0]
    try:
        product = await Product.objects.aget(name=product_name)
        await state.update_data(product_id=product.id)
        await message.answer(
            TEXT_PRODUCT_BUY_AGREE.format(product_name, product),
            reply_markup=confirm_purchase_keyboard()
        )
        await state.set_state(Purchase.confirming_purchase)
    except Product.DoesNotExist:
        await message.answer(TEXT_ORDER_SORRY)


@order_router.message(Purchase.confirming_purchase)
async def confirm_purchase(message: types.Message, state: FSMContext):
    if message.text == TEXT_AGREE:
        user_data = await state.get_data()
        product_id = user_data.get("product_id")
        try:
            product = await Product.objects.aget(id=product_id)
            user = await UserExtended.objects.aget(tg_chat_id=message.from_user.id)

            # Проверка на достаточность средств на балансе
            if user.balance < product.price:
                await message.answer(TEXT_NO_MONEY,
                                     reply_markup=await main_keyboard(user=user))
                await state.clear()
                return

            # Уменьшение баланса пользователя
            user.balance -= product.price
            await user.asave(update_fields=['balance'])

            # Создание заказа
            await Order(product=product, user=user).asave()
            await message.answer(
                TEXT_PRODUCT_BUY_SUCCESS.format(product.name, product.price, user.balance),
                reply_markup=await main_keyboard(user=user))
            await state.clear()
        except Product.DoesNotExist:
            await message.answer(TEXT_PRODUCT_NOT_FOUND)
    elif message.text == TEXT_DISAGREE:
        await message.answer(TEXT_PRODUCT_ORDER_CANCEL, reply_markup=await main_keyboard(message=message))
        await state.clear()
    else:
        await message.answer(TEXT_PRODUCT_ORDER_INCORRECT)
