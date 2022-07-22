# from db_init import Group, Test
# from sqlalchemy.orm import relationship, Session
# from sqlalchemy import create_engine
# import os


# engine = create_engine(os.getenv("DATABASE_URL"), echo=True, future=True)
# sql_session = Session(engine)



# test_group = sql_session.query(Group).filter(Group.id == 3).first()
# tc = Test(test_name = "Creatine", groups = test_group, link_test_api = "https://en.wikipedia.org/wiki/Creatine", username = "huynq", description = "Creatine is an organic compound with the nominal formula (H2N)(HN)CN(CH3)CH2CO2H. It exists in various modifications (tautomers) in solution. Creatine is found in vertebrates where it facilitates recycling of adenosine triphosphate (ATP), primarily in muscle and brain tissue. ")


# sql_session.add(tc)

# sql_session.commit()