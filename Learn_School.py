from pymysql import connect

class School(object):
    def __init__(self):
        self.conn=connect(host='localhost',port=3306,user='root',password='ICPC2021spring.',database='School',charset='utf8')
        self.cr = self.conn.cursor()

    def __del__(self):
        self.cr.close()
        self.conn.close()

    def execute_sql(self, sql):
        """执行查询语句"""
        self.cr.execute(sql)
        result = self.cr.fetchall()
        for temp in result:
            print(temp)

    def reg(self):
        """注册"""
        flag = False
        while True:
            username = input("请输入账号或'Q'退出：")
            if username == 'Q':
                return False
            parms_1 = [username]
            sql = 'select * from admin where username=%s;'
            self.cr.execute(sql, parms_1)
            flag = self.cr.fetchone()
            if not flag:
                while True:
                    password = input("请输入密码：")
                    password_1 = input("请再次输入密码：")
                    if password == password_1:
                        break
                subject = input("请输入执教科目：")
                parms_2 = [username,password,subject]
                sql = 'insert into admin values(0,%s,%s,%s);'
                self.cr.execute(sql, parms_2)
                self.conn.commit()
                sql="create table if not exists HLG_" + username + """(
                                    id INT NOT NULL AUTO_INCREMENT,
                                    name VARCHAR(50) NOT NULL,
                                    gander VARCHAR(50) NOT NULL,
                                    student_id VARCHAR(50) NOT NULL,
                                    number VARCHAR(50) NOT NULL,
                                    PRIMARY KEY ( id )
                                    )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
                self.cr.execute(sql)
                print("注册成功！")
                return False
            else:
                print("账号已存在，请重新输入！")
        
    def login(self):
        """登录"""
        flag = False
        while True:
            user = input("请输入账号或'Q'退出：")
            if user == 'Q':
                return False
            psw = input("请输入密码：")
            parms = [user]+[psw]
            sql = 'select * from admin where username=%s and password=%s;'
            self.cr.execute(sql, parms)
            flag = self.cr.fetchone()
            if flag:
                self.Tea_name = user
                self.Stu_name = user
                self.Tea_subject = flag[3]
                print("登录成功！")
                if flag[3] == '学生':
                    print("欢迎"+user+"学生！")
                    return 2
                else:
                    print("欢迎"+user+"老师！")
                    return 1
            else:
                print("账号或者密码输入错误，请重新输入！")

    def show_all_students(self):
        """显示所有学生信息"""
        sql = "select * from HLG_{name};".format(name=self.Tea_name)
        self.execute_sql(sql)

    def show_all_subject(self):
        """显示所有科目成绩"""
        sql = "select * from student_{name};".format(name=self.Stu_name)
        self.execute_sql(sql)

    def add_student(self):
        """添加学生信息"""
        name = input("请输入学生姓名：")
        gander = input("请输入学生性别：")
        student_id = input("请出入学生学号：")
        number = input("请输入学生成绩：")
        parms = [name,gander,student_id,number]
        sql = "insert into HLG_{name} values(0,%s,%s,%s,%s);".format(name=self.Tea_name)
        self.cr.execute(sql, parms)
        self.conn.commit()

        flag = False
        parms_1 = [student_id]
        sql = 'select * from admin where username=%s;'
        self.cr.execute(sql, parms_1)
        flag = self.cr.fetchone()
        if not flag:
            parms_2 = [student_id,'123456','学生']
            sql = 'insert into admin values(0,%s,%s,%s);'
            self.cr.execute(sql, parms_2)
            self.conn.commit()
            sql="create table if not exists student_" + student_id + """(
                                    id INT NOT NULL AUTO_INCREMENT,
                                    subject VARCHAR(50) NOT NULL,
                                    number VARCHAR(50) NOT NULL,
                                    PRIMARY KEY ( id )
                                    )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
            self.cr.execute(sql)

        parms_3 = [self.Tea_subject,number]
        sql = "insert into student_{name} values(0,%s,%s);".format(name=student_id)
        self.cr.execute(sql, parms_3)
        self.conn.commit()

        print("添加成功！")
        
    def delete_student(self):
        """删除学生信息"""
        student_id = input("请输入需要删除学生信息的学号：")
        sql = "delete from HLG_{name} where student_id = %s;".format(name=self.Tea_name)
        parms = [student_id]
        self.cr.execute(sql,parms)
        self.conn.commit()

        parms_1 = [self.Tea_subject]
        sql = "delete from student_{name} where subject = %s;".format(name=student_id)
        self.cr.execute(sql,parms_1)
        self.conn.commit()

        print("删除成功！")

    def update_password(self):
        while True:
            password = input("请输入修改后的密码：")
            password_1 = input("请再次输入修改后密码：")
            if password == password_1:
                break
        sql='update admin set password = %s where username = %s;'
        parms=[password,self.Tea_name]
        self.cr.execute(sql, parms)
        self.conn.commit()
        print("修改成功！")

    def print_teacher(self):
        """老师功能选择"""
        print("0.修改密码")
        print("1.显示所有学生信息")
        print("2.添加学生信息")
        print("3.删除学生信息")
        print("4.退出")
        return input("请选择：")

    def print_student(self):
        """学生功能选择"""
        print("0.修改密码")
        print("1.显示所有科目成绩")
        print("2.退出")
        return input("请选择：")

    def print_main(self):    
        """主页面功能选择"""
        print("1.登录")
        print("2.注册")
        print("3.退出")
        return input("请选择：")

    def run(self):
        login = self.login()
        if login == 1:
            while True:
                num = self.print_teacher()
                if num == '0':
                    self.update_password()
                elif num == '1':
                    self.show_all_students()
                elif num == '2':
                    self.add_student()
                elif num == '3':
                    self.delete_student()
                elif num == '4':
                    return False
                else:
                    print("输入错误，请重新选择！")
        elif login == 2:
            while True:
                num = self.print_student()
                if num == '0':
                    self.update_password()
                elif num == '1':
                    self.show_all_subject()
                elif num == '2':
                    return False
                else:
                    print("输入错误，请重新选择！")

    def all_main(self):
        while True:
            num = self.print_main()
            if num == '1':
                self.run()
            elif num == '2':
                self.reg()
            elif num == '3':
                exit()
            else:
                print("输入错误，请重新选择！")

def main_init():
    Gobase = connect(host='localhost',port=3306,user='root',password='ICPC2021spring.',charset='utf8')
    Gocr = Gobase.cursor()
    Gocr.execute("create database if not exists School;")
    Gocr.execute("use School;")
    Gocr.execute("""create table if not exists admin(
                    admin_id INT NOT NULL AUTO_INCREMENT,
                    username VARCHAR(50) NOT NULL,
                    password VARCHAR(50) NOT NULL,
                    subject VARCHAR(50) NOT NULL,
                    PRIMARY KEY ( admin_id )
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8;""")
    Gocr.close()
    Gobase.close()
    
def main():
    main_init()
    SCH = School()
    SCH.all_main()

main()
