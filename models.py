import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "Publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.VARCHAR(length=60), unique=True)

    # homeworks = relationship("Homework", back_populates="course")
    def __str__(self):
        return f" Publisher ({self.id},{self.name})"


class Book(Base):
    __tablename__ = "Book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.VARCHAR(length=60), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("Publisher.id"),
                             nullable=False)
    # course = relationship(Course, back_populates="homeworks")
    Publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f"Book {self.id}: ({self.title}, {self.id_publisher})"


class Shop(Base):
    __tablename__ = "Shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.VARCHAR(length=60), nullable=False)

    def __str__(self):
        return f"Shop {self.id}:{self.name}"


class Stock(Base):
    __tablename__ = "Stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("Book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("Shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    Book = relationship(Book, backref="stock")
    Shop = relationship(Shop, backref="stock")

    def __str__(self):
        return f" Stock {self.id}:({self.id_book}, {self.id_shop}," \
               f" {self.count})"


class Sale(Base):
    __tablename__ = "Sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL(5, 2), nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("Stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    Stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f" Sale {self.id}:({self.price}, {self.date_sale}," \
               f" {self.id_stock}, {self.count})"


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
