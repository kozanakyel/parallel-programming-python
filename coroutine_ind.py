import asyncio
from util.delay_functions import delay

async def coroutine_add_one(number: int) -> int:
    return number + 1


def add_one(number: int) -> int:
    return number + 1


# function_result = add_one(1)
# coroutine_result = asyncio.run(coroutine_add_one(1))

# print(f"Function result is {function_result} and the type is {type(function_result)}")
# print(
#     f"Coroutine result is {coroutine_result} and the type is {type(coroutine_result)}"
# )


async def main() -> None:
    one_plus_one = await coroutine_add_one(1)
    two_plus_one = await coroutine_add_one(2)
    print(one_plus_one)
    print(two_plus_one)
    
asyncio.run(main())

async def hello_world_message() -> str:
    await asyncio.sleep(1)
    return "Hello World!"


async def main() -> None:
    message = await hello_world_message()
    print(message)


asyncio.run(main())


import asyncio


async def add_one(number: int) -> int:
    return number + 1


async def hello_world_message() -> str:
    await delay(1)
    return 'Hello World!'


async def main() -> None:
    message = await hello_world_message()
    one_plus_one = await add_one(1)
    print(one_plus_one)
    print(message)


asyncio.run(main())


