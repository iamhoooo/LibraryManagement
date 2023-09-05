import mysql.connector
from tkinter import *

# MySQL 연결 설정
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # MySQL 사용자 이름
    password="1234",  # MySQL 비밀번호
    database="book"  # 데이터베이스 이름
)

cursor = conn.cursor()

# Tkinter 창 생성
root = Tk()
root.title("도서대출 관리 프로그램")

# 검색 결과를 표시할 창
search_result_window = Toplevel(root)

# 로그인 함수
def login():
    username = username_entry.get()
    password = password_entry.get()

    # MySQL에서 로그인 검증
    cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
    user = cursor.fetchone()

    if user:
        login_label.config(text=f"로그인 성공! 사용자 ID: {user[0]}")
        # 로그인한 사용자에 대한 기능 추가
    else:
        login_label.config(text="로그인 실패. 사용자 이름 또는 비밀번호가 올바르지 않습니다.")

# 회원가입 함수
def register():
    username = new_username_entry.get()
    password = new_password_entry.get()

    # MySQL에 새 사용자 추가
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
    conn.commit()
    register_label.config(text="회원가입이 완료되었습니다.")

# 대여 함수
def borrow_book():
    # 대여할 도서 정보를 입력받음
    book_title = input("대여할 도서 제목을 입력하세요: ")

    # 도서 정보를 데이터베이스에서 조회
    cursor.execute("SELECT * FROM books WHERE title = %s", (book_title,))
    book = cursor.fetchone()

    if book:
        if book[2] == 1:
            print("이 도서는 이미 대여 중입니다.")
        else:
            # 도서를 대여 중으로 표시
            cursor.execute("UPDATE books SET available = 1 WHERE title = %s", (book_title,))
            conn.commit()
            print(f"{book_title} 도서가 대여되었습니다.")
    else:
        print("해당 도서가 존재하지 않습니다.")

# 반납 함수
def return_book():
    # 반납할 도서 정보를 입력받음
    book_title = input("반납할 도서 제목을 입력하세요: ")

    # 도서 정보를 데이터베이스에서 조회
    cursor.execute("SELECT * FROM books WHERE title = %s", (book_title,))
    book = cursor.fetchone()

    if book:
        if book[2] == 0:
            print("이 도서는 이미 반납되었습니다.")
        else:
            # 도서를 대여 가능으로 표시
            cursor.execute("UPDATE books SET available = 0 WHERE title = %s", (book_title,))
            conn.commit()
            print(f"{book_title} 도서가 반납되었습니다.")
    else:
        print("해당 도서가 존재하지 않습니다.")

# 도서 추가 함수
def add_book():
    book_title = book_title_entry.get()
    book_author = book_author_entry.get()
    book_publisher = book_publisher_entry.get()

    # 도서 정보를 데이터베이스에 추가
    cursor.execute("""
        INSERT INTO books (title, author, publisher, available)
        VALUES (%s, %s, %s, 0)
    """, (book_title, book_author, book_publisher))
    conn.commit()
    
    add_result_label.config(text=f"{book_title} 도서가 추가되었습니다.")

# 도서 삭제 함수
def delete_book():
    # 삭제할 도서 제목 입력
    book_title = input("삭제할 도서 제목을 입력하세요: ")

    # 도서 정보를 데이터베이스에서 조회
    cursor.execute("SELECT * FROM books WHERE title = %s", (book_title,))
    book = cursor.fetchone()

    if book:
        # 도서를 데이터베이스에서 삭제
        cursor.execute("DELETE FROM books WHERE title = %s", (book_title,))
        conn.commit()
        print(f"{book_title} 도서가 삭제되었습니다.")
    else:
        print("해당 도서가 존재하지 않습니다.")

# 도서 수정 함수
def update_book():
    # 수정할 도서 제목 입력
    book_title = input("수정할 도서 제목을 입력하세요: ")

    # 도서 정보를 데이터베이스에서 조회
    cursor.execute("SELECT * FROM books WHERE title = %s", (book_title,))
    book = cursor.fetchone()

    if book:
        # 수정할 도서의 새 정보 입력
        new_title = input("새로운 도서 제목을 입력하세요 (변경하지 않으려면 엔터): ")
        new_author = input("새로운 도서 저자를 입력하세요 (변경하지 않으려면 엔터): ")
        new_publisher = input("새로운 도서 출판사를 입력하세요 (변경하지 않으려면 엔터): ")

        # 입력한 정보로 도서 정보를 업데이트
        if new_title:
            cursor.execute("UPDATE books SET title = %s WHERE title = %s", (new_title, book_title))
        if new_author:
            cursor.execute("UPDATE books SET author = %s WHERE title = %s", (new_author, book_title))
        if new_publisher:
            cursor.execute("UPDATE books SET publisher = %s WHERE title = %s", (new_publisher, book_title))

        conn.commit()
        print(f"{book_title} 도서 정보가 수정되었습니다.")
    else:
        print("해당 도서가 존재하지 않습니다.")

# 도서 검색 함수
def search_books():
    search_option = search_option_entry.get()
    keyword = keyword_entry.get()

    # 선택한 옵션에 따라 쿼리를 생성
    if search_option == "제목":
        query = "SELECT * FROM books WHERE title LIKE %s"
    elif search_option == "저자":
        query = "SELECT * FROM books WHERE author LIKE %s"
    elif search_option == "출판사":
        query = "SELECT * FROM books WHERE publisher LIKE %s"
    else:
        search_result_label.config(text="올바른 검색 옵션을 선택하세요.")
        return

    # 도서 검색
    cursor.execute(query, ('%' + keyword + '%',))
    books = cursor.fetchall()

    if books:
        search_result_window.title("검색 결과")
        result_label = Label(search_result_window, text="검색 결과:")
        result_label.pack()

        for book in books:
            result_text = f"도서 제목: {book[1]}, 저자: {book[2]}, 출판사: {book[3]}, 대여 가능: {'대여 가능' if book[4] == 0 else '대여 중'}"
            result_label = Label(search_result_window, text=result_text)
            result_label.pack()
    else:
        search_result_label.config(text="검색 결과가 없습니다.")


# 프로그램 종료 함수
def exit_program():
    conn.close()
    root.destroy()

# 로그인 프레임
login_frame = Frame(root)
login_frame.pack()

Label(login_frame, text="로그인").grid(row=0, column=0, columnspan=2)

Label(login_frame, text="사용자 이름:").grid(row=1, column=0)
username_entry = Entry(login_frame)
username_entry.grid(row=1, column=1)

Label(login_frame, text="비밀번호:").grid(row=2, column=0)
password_entry = Entry(login_frame, show="*")
password_entry.grid(row=2, column=1)

login_button = Button(login_frame, text="로그인", command=login)
login_button.grid(row=3, column=0, columnspan=2)

login_label = Label(login_frame, text="")
login_label.grid(row=4, column=0, columnspan=2)

# 회원가입 프레임
register_frame = Frame(root)
register_frame.pack()

Label(register_frame, text="회원가입").grid(row=0, column=0, columnspan=2)

Label(register_frame, text="새 사용자 이름:").grid(row=1, column=0)
new_username_entry = Entry(register_frame)
new_username_entry.grid(row=1, column=1)

Label(register_frame, text="새 비밀번호:").grid(row=2, column=0)
new_password_entry = Entry(register_frame, show="*")
new_password_entry.grid(row=2, column=1)

register_button = Button(register_frame, text="회원가입", command=register)
register_button.grid(row=3, column=0, columnspan=2)

register_label = Label(register_frame, text="")
register_label.grid(row=4, column=0, columnspan=2)

# 메뉴 프레임
menu_frame = Frame(root)
menu_frame.pack()

Label(menu_frame, text="도서대출 관리 프로그램").grid(row=0, column=0, columnspan=3)

borrow_button = Button(menu_frame, text="대여", command=borrow_book)
borrow_button.grid(row=2, column=0)

return_button = Button(menu_frame, text="반납", command=return_book)
return_button.grid(row=2, column=2)

# add_button = Button(menu_frame, text="도서 추가", command=add_book)
# add_button.grid(row=3, column=0)

# delete_button = Button(menu_frame, text="도서 삭제", command=delete_book)
# delete_button.grid(row=3, column=1)

# update_button = Button(menu_frame, text="도서 수정", command=update_book)
# update_button.grid(row=4, column=0)

search_button = Button(menu_frame, text="도서 검색", command=search_books)
search_button.grid(row=3, column=1)

# 도서 검색 프레임
search_option_label = Label(root, text="도서 검색 옵션을 선택하세요 (제목/저자/출판사):")
search_option_label.pack()

search_option_entry = Entry(root)
search_option_entry.pack()

keyword_label = Label(root, text="검색할 키워드를 입력하세요:")
keyword_label.pack()

keyword_entry = Entry(root)
keyword_entry.pack()

search_result_label = Label(root, text="")
search_result_label.pack()

# 도서 추가프레임
book_title_label = Label(root, text="도서 제목을 입력하세요:")
book_title_label.pack()

book_title_entry = Entry(root)
book_title_entry.pack()

book_author_label = Label(root, text="도서 저자를 입력하세요:")
book_author_label.pack()

book_author_entry = Entry(root)
book_author_entry.pack()

book_publisher_label = Label(root, text="도서 출판사를 입력하세요:")
book_publisher_label.pack()

book_publisher_entry = Entry(root)
book_publisher_entry.pack()

add_button = Button(root, text="도서 추가", command=add_book)
add_button.pack()

add_result_label = Label(root, text="")
add_result_label.pack()


# 종료 버튼
exit_button = Button(root, text="종료", command=exit_program)
exit_button.pack()

root.mainloop()
