import asyncio
from asyncio import CancelledError
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
    
# asyncio.run(main())

async def hello_world_message() -> str:
    await asyncio.sleep(1)
    return "Hello World!"


async def main() -> None:
    message = await hello_world_message()
    print(message)


# asyncio.run(main())


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


# asyncio.run(main())

async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    result = await sleep_for_three
    print(result)

# asyncio.run(main())

async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))

    await sleep_for_three
    await sleep_again
    await sleep_once_more


# asyncio.run(main())

async def hello_every_second():
    for i in range(4):
        await asyncio.sleep(1)
        print("I'm running other code while I'm waiting!")


async def main():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    await hello_every_second()
    await first_delay
    await second_delay

# asyncio.run(main())

async def main():
    long_task = asyncio.create_task(delay(10))

    seconds_elapsed = 0

    while not long_task.done():
        print('Task not finished, checking again in a second.')
        await asyncio.sleep(1)
        seconds_elapsed = seconds_elapsed + 1
        if seconds_elapsed == 5:
            long_task.cancel()

    try:
        await long_task
    except CancelledError:
        print('Our task was cancelled')

# asyncio.run(main())


async def main():
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('Got a timeout!')
        print(f'Was the task cancelled? {delay_task.cancelled()}')


# asyncio.run(main())


async def main():
    task = asyncio.create_task(delay(10))

    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except asyncio.TimeoutError:
        print("Task took longer than five seconds!")
        result = await task
        print(result)


# asyncio.run(main())












