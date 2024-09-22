import sqlite3


# Function to connect to the SQLite database
def connect_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn


# Function to add a URL to the wight_list table
def add_url(conn, url):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO wight_list (url) VALUES (?)", (url,))
    conn.commit()
    print(f'URL "{url}" added to wight_list.')


# Function to retrieve a urls
def retrieve_wight_list(conn):
    query = f"SELECT url FROM wight_list"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return [row[0] for row in rows]


# Function to update the flag value
def update_flag(conn, new_value):
    cursor = conn.cursor()
    cursor.execute("UPDATE flag_table SET flag = ? WHERE id = 1", (new_value,))
    conn.commit()
    print(f"Flag updated to {new_value}.")


# Function to retrieve the current flag value
def retrieve_flag(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT flag FROM flag_table WHERE id = 1")
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        print("No flag found.")
        return None


# Main function
def main():
    # db_name = "urls.db"
    # urls = [
    #     "https://www.facebook.com/",
    #     "https://www.youtube.com/",
    #     "https://www.google.com/",
    # ]

    # # Connect to the database
    # conn = connect_db(db_name)

    # # Add the URL to the database
    # # for url in urls:
    # #     add_url(conn, url)

    # update_flag(conn, False)

    # print(retrieve_flag(conn))

    # # Close the connection
    # conn.close()
    pass


if __name__ == "__main__":
    main()
