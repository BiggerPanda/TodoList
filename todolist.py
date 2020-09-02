# Write your code here

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()
today = datetime.today()
day_after_week = today - timedelta(days=7)


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(VARCHAR, default="default value")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def str_weekday(date):
    day_number = date % 7
    if day_number == 0:
        return 'Monday'
    elif day_number == 1:
        return 'Tuesday'
    elif day_number == 2:
        return 'Wednesday'
    elif day_number == 3:
        return 'Thursday'
    elif day_number == 4:
        return 'Friday'
    elif day_number == 5:
        return 'Saturday'
    elif day_number == 6:
        return 'Sunday'


def add():
    print("Enter task")
    task_in = input(">")
    print("Enter deadline")
    deadline_in = datetime.strptime(input('>'), '%Y-%m-%d')
    new_row = Table(task=task_in, deadline=deadline_in.date())
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def task_printer(date=datetime.today()):
    rows = session.query(Table).filter(Table.deadline == date.date()).all()
    if len(rows) < 1:
        print('Nothing to do! \n')
    else:
        for row in rows:
            print(f'{row.id}. {row} \n')




def all_rows_today():
    print("Today {0} {1}:".format(str_weekday(today.day), today.strftime('%#d %b')))
    task_printer(today)



def all_rows_week():
    rows = session.query(Table).filter(today.date() < day_after_week.date()).all()
    for i in range(0, 7):
        week_day = today+timedelta(i)
        print("{0} {1}:".format(str_weekday(week_day.day), week_day.strftime('%#d %b')))
        task_printer(week_day)


def all_rows_all():
    rows = session.query(Table).order_by(Table.deadline).all()
    if not rows:
        print("Nothing to do!")
    else:
        for main_row in rows:
            print("{0}.{1}. {2}".format(main_row.id, main_row, main_row.deadline.strftime('%#d %b')))


def delete():
    id_task = int(input("Choose the number of the task you want to delete:\n> "))
    rows = session.query(Table).order_by(Table.deadline).all()
    specific_row = rows[id_task-1]
    session.delete(specific_row)
    session.commit()


def missed_task():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    if not rows:
        print("Nothing to do!")
    else:
        for main_row in rows:
            print("{0}.{1}. {2}".format(main_row.id, main_row, main_row.deadline.strftime('%#d %b')))


def simple_menu():

    print("""
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
    """)
    menu_input = int(input(">"))
    while menu_input != 0:

        if menu_input == 1:
            all_rows_today()
        elif menu_input == 2:
            all_rows_week()
        elif menu_input == 0:
            return 0
        elif menu_input == 3:
            all_rows_all()
        elif menu_input == 5:
            add()
        elif menu_input == 4:
            missed_task()
        elif menu_input == 6:
            delete()
        else:
            print("wrong value")

        print("""
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
            """)
        menu_input = int(input(">"))

    print("Bye!")


simple_menu()






