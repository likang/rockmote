#! /bin/env python
# -*- coding: utf-8 -*-
import web,json
import os
from config import configurator,DBHelper

class index:
  def GET(self):
    return render.index()

class libloader:
  def POST(self):
    if config.paths:
      for path in config.paths:
        if os.path.exists(path):
          pass


class settings:
  def GET(self):
    return render.settings()
  def POST(self):
    user_data = web.input(per_page=config.per_page,
      paths=config.paths,deep_search=config.deep_search)
    config.per_page = int(user_data.per_page)
    valid_paths=[]
    if user_data.paths:
      paths = user_data.paths.splitlines()
      for path in paths:
        if os.path.exists(path):
          if not path in valid_paths:
            valid_paths.append(path)

    config.paths = '\n'.join(valid_paths)
    config.deep_search = int(user_data.deep_search)
    DBHelper().save_settings(config)
    params={
      'per_page':config.per_page,
      'paths':config.paths,
      'deep_search':config.deep_search
    }
    web.header('Content-Type', 'application/json')
    return json.dumps(params)


if __name__ == "__main__":

  urls = (
    '/', 'index',
    '/settings','settings',
    '/reload','libloader'
  )
  global config
  config = configurator()
  app = web.application(urls,globals())
  render = web.template.render('templates/', base='layout', 
    globals={'config':config})

  app.run()
