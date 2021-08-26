import asyncio
import datetime


# -----------------------------------------------------------------------------
# 小demo
# part 1

async def main():
    """
    part 1 简单介绍一下异步
    :return:
    """
    print('hello')
    await asyncio.sleep(2)
    print('world')


# -----------------------------------------------------------------------------
# part 2
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main2():
    """
    part 2
    创建一个异步程序，需要运行say_after函数4次，怎么运行
    整个过程会运行10秒
    :return:
    """
    start_date = datetime.datetime.now()
    print(f'Start at {start_date:%Y-%m-%d %H:%M:%S}')

    await say_after(delay=1, what='hello')
    await say_after(delay=2, what='world')
    await say_after(delay=3, what='foo')
    await say_after(delay=4, what='bar')

    end_date = datetime.datetime.now()
    print(f'finished at {end_date:%Y-%m-%d %H:%M:%S}')
    print(f'total used time: {(end_date - start_date).seconds} s')


# -----------------------------------------------------------------------------
# part 3
# 因为part 2运行上面4个say_after函数需要10s，我们想要减少运行时间，方法1,
# 这个方法只是需要4s即可运行完4个say_after函数

async def main3():
    """
    # 因为part 2运行上面4个say_after函数需要10s，我们想要减少运行时间，方法1
    :return:
    """
    start_date = datetime.datetime.now()
    print(f'Start at {start_date:%Y-%m-%d %H:%M:%S}')

    task1 = asyncio.create_task(say_after(delay=1, what='hello'))
    task2 = asyncio.create_task(say_after(delay=2, what='world'))
    task3 = asyncio.create_task(say_after(delay=3, what='foo'))
    task4 = asyncio.create_task(say_after(delay=4, what='bar'))

    await task1
    await task2
    await task3
    await task4
    end_date = datetime.datetime.now()
    print(f'finished at {end_date:%Y-%m-%d %H:%M:%S}')
    print(f'total used time: {(end_date - start_date).seconds} s')


# -----------------------------------------------------------------------------
# part 4
# part3 虽然将part2的时间从10s减少到了4s，可是写法实在是不优雅，我不喜欢
# 那么多task1，task2，task3，task4，那我要是有很多task，我要写那么多代码，实在是太难看，
# 那么这个能不能使用列表推导式呢？可以的
async def main4():
    """
    part 4比part 3就是好在了可以使用列表推导式，代码看着更加优雅
    :return:
    """
    start_date = datetime.datetime.now()
    print(f'Start at {start_date:%Y-%m-%d %H:%M:%S}')

    task = [asyncio.create_task(say_after(delay=delay, what=what)) for delay, what in
            zip([1, 2, 3, 4], ['hello', 'world', 'foo', 'bar'])]

    [await task_ for task_ in task]
    end_date = datetime.datetime.now()
    print(f'finished at {end_date:%Y-%m-%d %H:%M:%S}')
    print(f'total used time: {(end_date - start_date).seconds} s')


# -----------------------------------------------------------------------------
# part 5
# part 4 虽然使用列表，这样可以使用列表推导式，但是依然不够优雅：
# 因为我们每次都要创建一个task：create_task部分 来对say_after包装一下
# 那我们直接将这个crate_task拿到这个列表推导式外面应该怎么写
# 于是part 5来了
async def main5():
    """
    将create_task拿到列表外面（变成了gather)
    并且舍去列表推导式展开部分
    :return:
    """
    start_date = datetime.datetime.now()
    print(f'Start at {start_date:%Y-%m-%d %H:%M:%S}')

    await asyncio.gather(*[say_after(delay=delay, what=what) for delay, what in
                           zip([1, 2, 3, 4], ['hello', 'world', 'foo', 'bar'])])

    end_date = datetime.datetime.now()
    print(f'finished at {end_date:%Y-%m-%d %H:%M:%S}')
    print(f'total used time: {(end_date - start_date).seconds} s')


# -----------------------------------------------------------------------------
# part 6
# 虽然现在part 5已经基本上很好了，足够优雅到可以让我们去解决一些比较
# 麻烦、困难的问题，但是现实生活中可不是这样的，比如说：
# 每一个函数运行时间不能过长，都有时间限制，这种情况怎么办？
# 那么part 6就是来解决这个问题的
# 我们这个了假设每一个任务运行时间不能超过3秒，并且如果一个任务超时了，
# 不能出现错误，应该直接忽略，不影响别的任务运行，那这样应该怎么做

async def solove_timeout(func, timeout=1.0, **kargs):
    try:
        await asyncio.wait_for(func(**kargs), timeout=timeout)
    except asyncio.TimeoutError:
        print("Timeout!")


async def main6():
    """
    part 6
    这里加上时间限制，如果时间超过3.2秒，那么子任务就会被取消，但是不影响别的任务
    """
    start_date = datetime.datetime.now()
    print(f'Start at {start_date:%Y-%m-%d %H:%M:%S}')

    await asyncio.gather(*[solove_timeout(say_after, timeout=3.2, delay=delay, what=what) for delay, what in
                           zip([1, 2, 3, 4], ['hello', 'world', 'foo', 'bar'])])

    end_date = datetime.datetime.now()
    print(f'finished at {end_date:%Y-%m-%d %H:%M:%S}')
    print(f'total used time: {(end_date - start_date).seconds} s')

# -----------------------------------------------------------------------------
# part 7
# part 6解决了单个子任务运行超时的问题，还有一个问题，如果限制并发的任务数量？
# 比如我有100个任务需要访问服务器（不管是爬虫还是数据库）
# 如果不作限制，这个100个任务可能会在一瞬间去访问服务器，对服务器造成很大的压力，
# 那我怎么做，可以现在并发的数量呢？
# part 7就可以解决这个问题，可以设置每个时刻，最多只有2个协程运行，
# 上一个运行完了，下一个继续补上，最终全部运行完成。

async def run_limit(func, sem, **kargs):
    async with sem:
        await func(**kargs)


async def main7():
    """
    使用asyncio.semaphore来限制最大的协程数量
    这里运行的时间是6s，因为1运行完，3开始运行，2结束的时候是4运行，最终根据最长时间的来计算，也就是6秒
    """
    start_date = datetime.datetime.now()
    print(f'Start at {start_date:%Y-%m-%d %H:%M:%S}')
    sem = asyncio.Semaphore(2)
    await asyncio.gather(*[run_limit(say_after, sem=sem, delay=delay, what=what) for delay, what in
                           zip([1, 2, 3, 4], ['hello', 'world', 'foo', 'bar'])])

    end_date = datetime.datetime.now()
    print(f'finished at {end_date:%Y-%m-%d %H:%M:%S}')
    print(f'total used time: {(end_date - start_date).seconds} s')




if __name__ == '__main__':
    asyncio.run(main())
    # asyncio.run(main2())
    # asyncio.run(main3())
    # asyncio.run(main4())
    # asyncio.run(main5())
    # asyncio.run(main6())
    # asyncio.run(main7())
