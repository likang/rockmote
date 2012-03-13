#! /bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os

class configurator:
  def __init__(self):
    self.per_page = 20
    self.deep_search = 1
    self.paths = None
    if not os.path.exists('db.sqlite'):
      self.freshman = 1
    else:
      self.freshman = 0
    self.save_attrs = ('per_page','deep_search','paths')

    dbhelper= DBHelper()
    dbhelper.check_db()
    dbhelper.read_settings(self)


class DBHelper:
  def __init__(self):
    self.db_name = 'db.sqlite'

  def read_settings(self, config):
    db = sqlite3.connect(self.db_name)
    c = db.cursor()
    c.execute("select name,value from conf")
    conf = c.fetchall()
    for cf in conf:
      value = cf[1]
      if type(getattr(config,cf[0])) == type(1):
        value = int(value) 
      setattr(config,cf[0], value)
    c.close()
    db.close()

  def save_settings(self, config):
    db = sqlite3.connect(self.db_name)
    c = db.cursor()
    c.execute("delete from conf")
    for attr in config.save_attrs:
      c.execute("insert into conf(name,value) values('%s','%s')" %
        (attr,getattr(config,attr)))
    c.close()
    db.commit()
    db.close()

  def check_db(self):
    db = sqlite3.connect(self.db_name)
    c = db.cursor()
    c.execute("""select count(*) from sqlite_master 
                 where type='table' and name='conf'""")
    r = c.fetchone()
    if r[0] == 0:
      c.execute("create table conf(name text, value text)")
      db.commit()

    c.execute("""select count(*) from sqlite_master 
                 where type='table' and name='lib'""")
    r = c.fetchone()
    if r[0] == 0:
      c.execute("""create table lib(id integer primary key, name text, 
                   path text, duration text, created_at datetime default 
                   current_timestamp)""")
      db.commit()

    c.execute("""select count(*) from sqlite_master 
                 where type='table' and name='playlist_lib'""")
    r = c.fetchone()
    if r[0] == 0:
      c.execute("""create table playlist_lib(id integer primary key, 
                   playlist integer, name text, 
                   path text, duration text, created_at datetime default 
                   current_timestamp)""")
      db.commit()

    c.execute("""select count(*) from sqlite_master 
                 where type='table' and name='playlist'""")
    r = c.fetchone()
    if r[0] == 0:
      c.execute("create table playlist(id integer primary key, name text)")
      db.commit()
    c.close()
    db.close()
