#!/usr/bin/python2
## -*- coding: utf-8 -*-

import MySQLdb
import sys
import calendar
import datetime

s = {
	'light' : 2,
	'humi' : 3,
	'temp' : 4,
	'pressure' : 5,
}

class DBase:
	u'''Odbiór danych z bazy i ich konwersja'''
	def __init__(self, host, user, password, dbase, table):
		u'''Łaczy z bazą'''
		self.host = host
		self.user = user
		self.password = password
		self.dbase = dbase
		self.table = table
		try:
			self.db = MySQLdb.connect(host=host, port=3306, user=user , passwd=password, db=dbase)

		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit (1)
		self.c = self.db.cursor()
		self.c.execute('SELECT * FROM ' + self.table)

	def query_all(self, rows):
		u'''Pobiera wszystkie rekordy dla zadanej kolumny w tabeli'''
		self.rows = rows
		self.c.execute("SELECT " + rows + " FROM " + self.table)
		return self.c.fetchall()

	def query_last(self, rows):
		self.rows = rows
		self.c.execute("SELECT " + rows + " FROM " + self.table + " LIMIT " + str((self.c.rowcount)- 1) + ", " + str(self.c.rowcount))
		return self.c.fetchall()[0][0]

	def query_limit(self, rows, limit):
		u'''Pobiera określoną ilość ostatnich rekordów dla zadanej kolumny w tabeli'''
		self.limit = limit
		self.c.execute('SELECT * FROM ' + self.table)
		self.c.execute("SELECT " + rows + " FROM " + self.table + " LIMIT " + str((self.c.rowcount)-(int(limit)+1)) + ", " + str(self.c.rowcount))
		return self.c.fetchall()

	def json(self, series):
		self.series = series
		u'''Tworzy ciąg danych w formacie JSON'''
		self.data = []
		self.c.execute('SELECT * FROM ' + self.table)
		for self.rec in self.c.fetchall():
			self.data.append("[" + str(calendar.timegm(self.rec[1].timetuple())*1000) + ", " + str(self.rec[int(s[series])]) + "]")
		return ("["+", ".join(map(lambda x: str(x), self.data))+"]")

	def list():
		u'''Tworzy ciąg danych w postaci listy'''
		pass

	def __del__(self):
		u'''Zamyka połaczenie z bazą'''
		self.db.close()
