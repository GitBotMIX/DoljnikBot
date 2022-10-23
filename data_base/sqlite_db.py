import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('doljnik.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS debtors(name TEXT, long TEXT, user_id TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS longs(name TEXT, long TEXT, user_id TEXT)')

    base.commit()

async def sql_add_command(state, table, message):
    async with state.proxy() as data:
        tupleData = tuple(data.values()) + (str(message.from_user.id),)
        for i in tupleData:
            if '-' in i:
                return False
        cur.execute(f'INSERT INTO {table} VALUES (?, ?, ?)', tupleData)
        base.commit()
        return True



async def sql_read(table, message):
    readList = []
    s = 'Я должен'
    if table == 'debtors':
        s = 'Должен'
    for ret in cur.execute(f'SELECT name, long FROM {table} WHERE user_id == ?', (str(message.from_user.id),)).fetchall():
        readList.append(f'\nИмя: `{ret[0]}`\n{s}: {ret[1]}')
    if readList == []:
        return False
    return '\n\n'.join(readList)


async def sql_name_check_message(message, table):
    check = cur.execute(f'SELECT name FROM {table} WHERE name == ?', (message.text,)).fetchone()
    if check == None:
        return False
    return True


async def sql_name_check_state(state):
    async with state.proxy() as data:
        tupleData = tuple(data.values())
        check = cur.execute('SELECT name FROM debtors WHERE name == ?', (tupleData[0],)).fetchone()
        if check == None:
            return False
        return True


async def sql_delete(message, table):
    cur.execute(f'DELETE FROM {table} WHERE name == ?', (message.text,))
    base.commit()


async def sql_update(state, table):
    async with state.proxy() as data:
        tupleData = tuple(data.values())
        cur.execute(f'UPDATE {table} SET long == ? WHERE name == ?', (tupleData[1], tupleData[0]))
        base.commit()