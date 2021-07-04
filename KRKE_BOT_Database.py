

# Returns from database entries with specific date.
def select_date(cursor, today, alert_status):
    # Get remind entries with specified date and alert status, data ordered by date.
    cursor.execute("SELECT * FROM reminds WHERE Date LIKE ? AND Alert_Status = ? ORDER BY Date", (today, alert_status))
    return cursor.fetchall()


# Insert entry into database
def insert_entry(connect, cursor, name, date, creator, channel_id, author_id, created):
    with connect:
        cursor.execute("INSERT INTO reminds (Name, Date, Creator, Alert_Status, Repeat, Count, Channel_id, Author_id, Created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (name, date, creator, 0, 0, 0, channel_id, author_id, created))


# Update entry after.
def update_entry(connect, cursor, id):
    with connect:
        cursor.execute("UPDATE reminds SET Alert_Status = 1 WHERE ID = :id", {'id': id})
