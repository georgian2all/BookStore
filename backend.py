import sqlite3


class Database:
	"""
	Functia init in Python are rolul de a initializa un obiect (baza de date in
	cazul nostru)
	In cazul de fata ne conectam la baza de date si ne asiguram ca exista
	tabela in care stocam informatiile. In situatia in care nu exista, o creez.
	Astfel am initializat obiectul, baza de date.
	"""
	def __init__(self,db):
		self.dbconnection=sqlite3.connect(db)
		self.dbcursor=self.dbconnection.cursor()
		self.dbcursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY,\
						title TEXT,author TEXT,year INTEGER, price REAL)")
		self.dbconnection.commit()


	def insert(self,title,author,year,price):
		self.dbcursor.execute("INSERT INTO books VALUES(NULL,?,?,?,?)",(title,author,year,\
						price))
		self.dbconnection.commit()


	def view(self):
		self.dbcursor.execute("SELECT * FROM books")
		rows=self.dbcursor.fetchall() # este o tupla
		return rows #le vom folosi pt a afisa datele in listboxul din frontend

	def search(self,title="",author="",year="",price=""):
		self.dbcursor.execute("SELECT * FROM books WHERE title=? or author=? or year=? or\
						price=?",(title,author,year,price))
		rows=self.dbcursor.fetchall() # este o tupla
		return rows

	def delete(self,id):
		self.dbcursor.execute("DELETE FROM books WHERE id=?",(id,))
		self.dbconnection.commit()


	def update(self,id,title,author,year,price):
		self.dbcursor.execute("UPDATE books SET title=?,author=?,year=?,price=? WHERE id=?"\
		,(title,author,year,price,id))
		self.dbconnection.commit()

	def __del__(self):
		self.dbconnection.close()




#insert("The Moon","Little Smith",1995,369889)
#update(4,"The Morning","Jhon Sprinter",2015,6985)
#delete(2)
#print(view())
