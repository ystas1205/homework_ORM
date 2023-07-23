import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
from config import DSN

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


def store_sampling_request(publisher):
    if publisher.isnumeric():
        subq = session.query(Book.title, Shop.name, Sale.price, Sale.count,
                             Sale.date_sale).join(Publisher).join(
            Stock).join(Sale).join(Shop).filter(Publisher.id == publisher)
    else:
        subq = session.query(Book.title, Shop.name, Sale.price, Sale.count,
                             Sale.date_sale).join(Publisher).join(
            Stock).join(Sale).join(Shop).filter(Publisher.name == publisher)

    for book, shop, sale_price, sale_count, sale_date in subq:
        print(f'{book:<39} | {shop:<8} | {sale_price * sale_count:<7} | '
              f'{sale_date.strftime("%d-%m-%Y")}')


if __name__ == "__main__":
    store_sampling_request(input("Введите имя или идентификатор издателя: "))
    session.close()
    