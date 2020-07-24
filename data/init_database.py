import pymysql
import config


def init_database():
    connection = get_connection().cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS group_list ('
                       'group_id INTEGER NOT NULL '
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS player_list ('
                       'group_id INTEGER NOT NULL,'
                       'qq_id INTEGER NOT NULL,'
                       'qq_name TEXT,'
                       'player_name TEXT '
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS record ('
                       'group_id INTEGER NOT NULL,'
                       'username TEXT NOT NULL,'
                       'target TEXT NOT NULL,'
                       'damage INTEGER DEFAULT 0,'
                       'date INTEGER NOT NULL '
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS picture_list ('
                       'file_name TEXT,'
                       'sub_directory TEXT,'
                       'origin TEXT '
                       ');')
    connection.execute('CREATE TABLE IF NOT EXISTS picture_quota ('
                       'qq_id integer UNIQUE PRIMARY KEY,'
                       'count integer '
                       ');')
    # connection.execute('CREATE TABLE IF NOT EXISTS message_record ('
    #                    'qq_id integer,'
    #                    'date date'
    #                    ');')
    connection.execute('CREATE TABLE IF NOT EXISTS rank_record ('
                       'group_id INTEGER NOT NULL,'
                       'date INTEGER,'
                       'ranking INTEGER '
                       ');')
    connection.close()


def get_connection():
    return pymysql.connect(config.DATABASE_PATH,
                           config.DATABASE_USERNAME,
                           config.DATABASE_PASSWORD,
                           config.DATABASE_NAME)


if __name__ == '__main__':
    init_database()
