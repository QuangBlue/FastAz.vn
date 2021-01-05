from function import *
from menu import *

def main():
    for i in menu:
        print (str(i) + " : " + menu[i][0])
    while True:
        try:
            func_c = input("Chọn tính năng muốn sử dụng. Hoặc 'exit' để thoát: ")
            if func_c == 'exit':
                print ('Cảm ơn bạn đã sử dụng ứng dụng Tool Shopee')
                exit()
            if int(func_c) > len(menu):
                print ('Vui lòng nhập đúng lựa chọn tính năng 1')
                continue
            if int(func_c) not in range(len(menu)+1):
                print ('Vui lòng nhập đúng lựa chọn tính năng 2')
                continue
            break
        except ValueError:
            print ('Vui lòng nhập đúng lựa chọn tính năng 3')


    if len(tk_sp) == 0:
        print ('Bạn chưa thêm tài khoản. Tiến hành thêm tài khoản')
        menu[1][1]("Demo")
    print (f'Bạn đang có {len(tk_sp)} tài khoản là:')
    for x in range (len(tk_sp)) :
        print (f'Tài khoản số {x+1} : {list(tk_sp.keys())[x]}')
    while True:
        acc_list = []
        acc_c= list(set(map(str, input('Nhập số tài khoản bạn muốn thao tác. Nhập 0 để chọn tất cả. Nhập "exit" để thoát: ').strip().split())))
        try:
            if len(acc_c) == 1 and ( acc_c[0] == 'exit' or int(acc_c[0]) == 0) :
                if acc_c[0] == 'exit':
                    print ('Cảm ơn bạn đã sử dụng ứng dụng Tool Shopee')
                    exit()
                elif int(acc_c[0]) == 0 :
                    acc_list = list(tk_sp.keys())
                    break
        except:
            print ('Bạn nhập sai cú pháp.')
            continue
        if acc_c == []:
            print ('Không được để trống vui lòng chọn acc cần thao tác')   
            continue       
        else:
            try:             
                for i in acc_c:
                    acc_list.append(list(tk_sp)[int(i)-1])              
                break
            except:
                print ('Bạn nhập sai cú pháp.')
                continue
        break
    print (f"Bạn đã chọn tính năng {menu[int(func_c)][0]} cho các tài khoản {acc_list}\nTiến hành thực hiên {menu[int(func_c)][0]}")

    for acc in acc_list:
        menu[int(func_c)][1](acc)
        print(f'Đã thực hiện {menu[int(func_c)][0]} cho tài khoản {acc}')
        print ('...\n'*2)
    

if __name__ == "__main__":
    main()