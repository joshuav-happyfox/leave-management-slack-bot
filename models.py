from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Date, Column, Integer, String

Base = declarative_base()


class Leave(Base):
    __tablename__ = 'leave'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)

    def __repr__(self):
        return (f"<Leave(id={self.id}, name={self.name}, email={self.email}, "
                f"start_date={self.start_date}, end_date={self.end_date}, "
                f"month={self.month}, duration={self.duration}, reason={self.reason})>")
        
        
class ManagerMap(Base):
    __tablename__ = 'manager_map'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    manager_id = Column(String, nullable=False)
    employee_id = Column(String, nullable=False)
    
    def __repr__(self):
        return (f"<ManagerMap(id={self.id}, manager_id={self.manager_id}, "
                f"employee_id={self.employee_id})>")
    
class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    slack_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="employee")
    is_admin = Column(Boolean, default=False)
    avatar = Column(String, nullable=False)    
    def __repr__(self):
        return (f"<Users(id={self.id}, slack_id={self.slack_id}, is_admin={self.is_admin}, avatar={self.avatar}, name={self.name})>")