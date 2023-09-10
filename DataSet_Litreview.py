import sqlite3
import datetime

conn = sqlite3.connect('litreview/db.sqlite3')
cursor = conn.cursor()

#cursor.execute('DELETE FROM reviews_ticket')
#cursor.execute('DELETE FROM reviews_review')
#conn.commit()

data_tickets = [
    ('ticket1', 'description1', 'image1.jpeg', datetime.datetime.now(), 10),
    ('ticket2', 'description2', 'image2.jpeg', datetime.datetime.now(), 11),
    ('ticket3', 'description3', 'image3.jpeg', datetime.datetime.now(), 11),
    ('ticket4', 'description4', 'image4.jpeg', datetime.datetime.now(), 12),
]

cursor.executemany('INSERT INTO reviews_ticket (title, description, image, time_created, user_id) VALUES(?, ?, ?, ?, ?)', data_tickets)

data_reviews = [
    (0, 'HeadlineReview1', 'Review1', datetime.datetime.now(), 10, 7),
    (1, 'HeadlineReview2', 'Review2', datetime.datetime.now(), 10, 8),
    (5, 'HeadlineReview3', 'Review3', datetime.datetime.now(), 11, 9),
    (3, 'HeadlineReview4', 'Review4', datetime.datetime.now(), 12, 9),
]
cursor.executemany('INSERT INTO reviews_review (rating, headline, body, time_created, ticket_id, user_id) VALUES(?, ?, ?, ?, ?, ?)', data_reviews)

conn.commit()
conn.close()

print("Upload dataset test ok")
