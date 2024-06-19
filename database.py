import sqlite3


class dbworker:
	def __init__(self):
		self.connection = sqlite3.connect('database.db')
		self.cursor = self.connection.cursor()

	def add_user(self,telegram_username,telegram_id,full_name):
		'''Добавляем нового юзера'''
		with self.connection:
			return self.cursor.execute("INSERT INTO `users` (`telegram_username`, `telegram_id`,`full_name`) VALUES(?,?,?)", (telegram_username,telegram_id,full_name))
	

	def show_all_woman(self):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM users WHERE sex=2").fetchall()
			return result
	
	def show_all_man(self):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM users WHERE sex=1").fetchall()
			return result
		
	def create_man(self,id,sex):
		with self.connection:
			return self.cursor.execute("INSERT INTO users(id,sex) VALUES(?,?)", (id,sex,))

	def create_woman(self,id,sex):
		with self.connection:
			return self.cursor.execute("INSERT INTO users(id,sex) VALUES(?,?)", (id,sex,))
		
	def set_name(self,id,name):
		with self.connection:
			return self.cursor.execute("UPDATE users SET name = ? WHERE id=?", (name,id,))
	
	def set_cloth(self,id,cloth):
		with self.connection:
			return self.cursor.execute("UPDATE users SET cloth = ? WHERE id=?", (cloth,id,))

	def set_hair(self,id,hair):
		with self.connection:
			return self.cursor.execute("UPDATE users SET hair = ? WHERE id=?", (hair,id,))
		
	def set_fact(self,id,fact):
		with self.connection:
			return self.cursor.execute("UPDATE users SET fact = ?, match=0 WHERE id=?", (fact,id,))

	def profile_exists(self,id):
		'''Проверка есть ли анкета в бд'''
		with self.connection:
			result = self.cursor.execute('SELECT * FROM users WHERE id= ?', (id,)).fetchall()
			return bool(len(result))
		
	def delete_profile(self,user_id):
		'''Удаление анкеты'''
		with self.connection:
			return self.cursor.execute("DELETE FROM users WHERE id = ?",(user_id,))
	
	def is_user_gotten(self,id):
		with self.connection:
			self.cursor.execute("SELECT match FROM users WHERE id = ?",(id,))
			result = self.cursor.fetchone()[0]
			return result



	# ,w_param,idi_m
	def find_woman(self,idi_w):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE sex = 2 AND match = 0 ORDER BY random() LIMIT 1")
		girl = cur.fetchall()
		wom=''
		for el in girl:
			wom +=  f'Имя-{el[2]}\nМои ориентиры-{el[3]}\nЗабавный факт-{el[4]}\nЧто я скажу-{el[5]}\n'
			idi_w = el[0]
		cur.execute("UPDATE users SET match=1 WHERE id = ?",(idi_w,))
		conn.commit()
		cur.close()
		conn.close()
		return wom,idi_w
	

	def find_male(self,idi_m):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE sex = 1 AND match = 0 ORDER BY random() LIMIT 1")
		man = cur.fetchall()
		man_m = ''
		for el in man:
			man_m +=  f'Имя-{el[2]}\nМои ориентиры-{el[3]}\nЗабавный факт-{el[4]}\nЧто я скажу-{el[5]}\n'
			idi_m = el[0]
		cur.execute("UPDATE users SET match=1 WHERE id = ?",(idi_m,))
		conn.commit()
		cur.close()
		conn.close()
		return man_m,idi_m
	
	def man_to_wom(self,m_id):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE id=?",(m_id,))
		man = cur.fetchall()
		m_param = ''
		for el in man:
			m_param += f'Имя-{el[2]}\nМои ориентиры-{el[3]}\nЗабавный факт-{el[4]}\nЧто я скажу-{el[5]}\n'
		cur.execute("UPDATE users SET match = 1 WHERE id= ?",(m_id,))
		conn.commit()
		cur.close()
		conn.close()
		return m_param


	def wom_to_man(self,w_id):
		conn = sqlite3.connect('database.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE id=?",(w_id,))
		wom = cur.fetchall()
		w_param =''
		for el in wom:
			w_param += f'Имя-{el[2]}\nМои ориентиры-{el[3]}\nЗабавный факт-{el[4]}\nЧто я скажу-{el[5]}\n'
		cur.execute("UPDATE users SET match=1 WHERE id=?",(w_id,))
		conn.commit()
		cur.close()
		conn.close()
		return w_param