from Users import Base, engine
#from Questions import Base, engine

# Barcha model(l)ar asosida jadval(lar) yaratadi
Base.metadata.create_all(bind=engine)