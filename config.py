class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:glamrock@localhost/bes_ecom'
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True
    
# I had to change my root password and forgot our CORE one,
# so for reference my new one is "glamrock". I hope that is alright.
# (It was a complicated issue.)