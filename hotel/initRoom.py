from DBmysql import radMysql

def main():
    rd=radMysql()
    rd.addRooms("r.txt")

if __name__ == '__main__':
    main()
