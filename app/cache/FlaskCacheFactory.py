from flask_caching import Cache
cache = Cache()

class FlaskCacheFactory:
    
  def __init__(self, timeout = 300, cacheType = "SimpleCache", debug = False):
    self.debug = debug
    self.timeout = timeout
    self.cacheType = cacheType
    pass

  def register(self, app):
    config = {
      "DEBUG": self.debug,
      "CACHE_TYPE": self.cacheType,
      "CACHE_DEFAULT_TIMEOUT": self.timeout,
    }
    # tell Flask to use the above defined config
    app.config.from_mapping(config)
    cache.init_app(app, config = config)
    return cache
