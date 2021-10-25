from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="127.0.0.1",
        user=input("enter username"),
        password=getpass("enter password "),
    ) as connection:
        print(connection)
        show_db_query = "SHOW DATABASES"
        with connection.cursor() as cursor:
            cursor.execute(show_db_query)
            for db in cursor:
                print(db)
        # create_db_query = "CREATE DATABASE online_movie_rating"
        # with connection.cursor() as cursor:
        #     cursor.execute(create_db_query)
        #     print("its execcuted")
except Error as e:
    print(e,"error")
