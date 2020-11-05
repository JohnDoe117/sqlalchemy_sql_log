import datetime
from sqlalchemy import Column, String, create_engine, DateTime, Integer
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:123456789@localhost:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

from sqlalchemy import event



# 创建对象的基类:
Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db_session.query_property()

@event.listens_for(engine, "before_cursor_execute")
def comment_sql_calls(conn, cursor, statement, parameters, context, executemany):
    raw_sql = statement%parameters
    print(raw_sql)


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    passwd = Column(String(20))
    insert_time = Column(DateTime, default=datetime.datetime.now, comment='插入时间')

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            passwd=self.passwd
        )

    @staticmethod
    def add(analysis_dict):
        instance = User(
            name=analysis_dict.get("name"),
            passwd=analysis_dict.get("passwd"),
        )

        db_session.add(instance)

        try:
            db_session.commit()

            return True
        except Exception as e:
            db_session.rollback()
            print(e)

        return False


    @staticmethod
    def get_pw(name):

        instance = User.query.filter_by(name=name).first()
        # res = str(User.query.filter_by(name=name))
        # print(res)

        if instance:
            return instance.to_dict()
        return None



if __name__ == '__main__':

    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

    # res = User.get_pw('1')
    User.add({"name":'john', "passwd":"111"})
    # print(res)


