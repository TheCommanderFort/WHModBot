import re
import praw
from praw import reddit
import sqlite3
from sqlite3 import Error

import process_comment

def create_connection(path):
	connection = None
	try:
		connection = sqlite3.connect(path)
		print("Connected to the posts database in process_removal")
	except Error as e:
		print(f"The error '{e}' occurred")

	return connection


conn = create_connection('posts.db')
c = conn.cursor()


def process_removal(removal_action, reddit: reddit):
	print('Removal detected. Updating database...')
	c.execute('DELETE FROM posts WHERE url=?', (removal_action.target_permalink,))
	conn.commit()
	process_comment.update_wiki(reddit)