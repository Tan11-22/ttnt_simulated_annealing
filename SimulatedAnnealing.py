import copy
import csv
import math
import random
import numpy as np
import pandas as pd

def kiemTraGVTrongTiet(tkb,idGV, listGV,tiet):
    for i in range(len(tkb)):
        if listGV[idGV] == tkb[i][tiet]:
            return False
    return True
def taoTKBNgauNhien(tkb, lopRandom, r, t, c, soGiangVien, listGV):
    # Tính tổng số tiết mà lớp đó phải học và tống số tiết lớp đ

    tongSoTietLopRandom = 0
    tongSoTietCoThe=0
    for i in range(len(r[lopRandom])):
        tongSoTietLopRandom +=r[lopRandom][i]
    if tongSoTietLopRandom == 0: return tkb
    for i in range(len(c[lopRandom])):
        tongSoTietCoThe +=c[lopRandom][i]
    if tongSoTietCoThe < tongSoTietLopRandom:
        print("Số tiết lớp đó có thể học đang ít hơn số tiết nhà trường phân công cho giáo viên")
        exit()
    # Chọn random giáo viên cho các tiết còn lại của lớp
    while tongSoTietLopRandom > 0:
        check = random.randint(1,tongSoTietCoThe)
        tietRandom = 0
        #Chọn ra tiết đó là tiết có thể học
        for i in range(len(c[lopRandom])):
            check -=c[lopRandom][i]
            if check == 0:
                tietRandom = i
                c[lopRandom][i] = 0
                break
        tongSoTietLopRandom -=1
        tongSoTietCoThe -= 1
        tmp = 100
        while (tmp > 0):
            GVRandom = random.randint(0, soGiangVien - 1)
            if r[lopRandom][GVRandom] !=0 and kiemTraGVTrongTiet(tkb,GVRandom,listGV,tietRandom):
                # print(listGV[gvrd], " ", "Có thể dạy vào tiết ",tietRandom," của lớp ", listLop[lopRandom])
                tkb[lopRandom][tietRandom]= listGV[GVRandom]
                #t[GVRandom][tietRandom] = 0
                r[lopRandom][GVRandom] -= 1
                #d[lopRandom][tietRandom] = 0
                break
            tmp -= 1
    return tkb


def costCalculation(tkb, listGV, d, lop):
    f = 0
    # Ràng buộc cứng số tiết bắt buộc phải học của một lớp bàng ma trận d
    w0 = 0
    for i in range(len(d[lop])):
        if d[lop][i] == 1 and tkb[lop][i] == "":
            w0 += 1
    f += w0 * 30
    # Ràng buộc mềm
    w5=0
    w1=0
    for gv in listGV:
        for j in range(len(tkb[lop])//8):
            check = []
            check1 = 0
            for i in range(8):
                if gv == tkb[lop][j*8+i]:
                    check1 += 1
                    check.append(i)
            if check1 > 2 :
                w5+=1
            if check1 ==  2:
                if check[1] - check[0] != 1:
                    w1+=1
    f += w1 * 6
    f += w5 * 5
    return f
# #Thay đổi các tiết học với nhau
def swappingNeighborhoods(tkb, lop, listGV, t, c):

    # Chọn ngẫu nhiên 1 tiết bất kì của lớp x

    chonTiet1 = random.randint(0,47)
    while tkb[lop][chonTiet1] == "":
        chonTiet1 = random.randint(0,47)
    gv = tkb[lop][chonTiet1]
    #Chọn ngẫu nhiên 1 lớp bất kì thứ 2 của lớp X và đổi tiết với tiết đã chọn bất kì lần thứ 1
    while True:
        idGV = listGV.index(gv) #giáo viên thứ 1
        chonTiet2 = random.randint(0, 47)
        if chonTiet2 == chonTiet1:
            continue
        if c[lop][chonTiet2] == 1:
            if t[idGV][chonTiet2] == 1 and kiemTraGVTrongTiet(tkb,idGV,listGV, chonTiet2):
                if tkb[lop][chonTiet2] == "":
                    tkb[lop][chonTiet1], tkb[lop][chonTiet2] = tkb[lop][chonTiet2], tkb[lop][chonTiet1]
                    break
                else:
                    gv2 = tkb[lop][chonTiet2]
                    idGV2 = listGV.index(gv2)
                    #Kiểm tra giáo viên đó không bận và chưa có tiết dạy trong tiết chọn lần 1
                    if t[idGV2][chonTiet1] == 1 and kiemTraGVTrongTiet(tkb,idGV2,listGV,chonTiet1):
                        tkb[lop][chonTiet1], tkb[lop][chonTiet2] = tkb[lop][chonTiet2], tkb[lop][chonTiet1]
                        break
    return tkb
#

def simulated_annealing(T, tkb, lop, listGV, t, c, d):
    demTietHoc = 0
    for i in range(len(tkb[lop])):
        if tkb[lop][i] != "":
            demTietHoc += 1
    if demTietHoc == 0:
        return tkb, costCalculation(tkb,listGV, d, lop)
    # Khởi tạo giải pháp ban đầu
    current_solution = tkb
    current_cost = costCalculation(current_solution,listGV, d, lop)

    # Lưu giữ giải pháp tốt nhất tìm được
    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost
    #t1 = t
    # Bắt đầu giải thuật simulated annealing
    while T > 1:
        # Lặp lại quá trình nhiệt độ cao
        for i in range(100):
            # Tạo giải pháp mới bằng cách hoán đổi vị trí của hai giáo viên
            new_solution = current_solution.copy()
            new_solution = swappingNeighborhoods(new_solution,lop,listGV,t,c)
            new_cost = costCalculation(new_solution,listGV,d,lop)

            delta = new_cost - current_cost
            if delta < 0 :
                p = 1
            else:
                p = math.exp(-delta/T)
            if random.random() < p:
                current_solution = new_solution.copy()
                current_cost = new_cost
                if current_cost < best_cost:
                    del best_solution
                    best_solution = copy.deepcopy(current_solution)
                    best_cost = current_cost
                    #t1 = copy.deepcopy(t)
        T *= 0.9

    return best_solution, best_cost


def xuatTKB(tkb, lop, list):
    tkbLop = [["Tiết/Thứ","Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6","Thứ 7"]]
    for i in range(8):
        tkbLop.append(["Tiết " + str(i+1)])
        for j in range(6):
            tkbLop[i+1].append("")
    for i in range(1,len(tkbLop)):
        for j in range(1,len(tkbLop[i])):
            tkbLop[i][j] = tkb[lop][i-1][j-1]
    # for x in tkbLop:
    #     print(x)
    df = pd.DataFrame(tkbLop)
    df.to_csv(list[lop]+".csv", index=False,header=False, encoding='utf-8-sig')

def xuatTKBTatCa(tkb, listLop):
    tkbLopTong = []

    for l in tkb:
        tkbLopTong.append([listLop[tkb.index(l)],"","","","","",""])
        tkbLop=[["Tiết/Thứ","Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6","Thứ 7"]]
        for i in range(8):
            tkbLop.append(["Tiết " + str(i+1)])
            for j in range(6):
                tkbLop[i+1].append("")
        for i in range(1, len(tkbLop)):
            for j in range(1, len(tkbLop[i])):
                tkbLop[i][j] = l[i-1][j-1]
        for i in range(len(tkbLop)):
            tkbLopTong.append(tkbLop[i])

    # for x in tkbLop:
    #     print(x)
    df = pd.DataFrame(tkbLopTong)
    df.to_csv("Thời Khoa Biểu Tổng.csv", index=False,header=False, encoding='utf-8-sig')


def docFile(ten):
    with open(ten+'.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        data = [row[1:] for row in reader]
    return data

def docTKBTong(ten):
    with open(ten+'.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        data = [row[1:] for row in reader]
    data1 = []
    for i in range(len(data)//10):
        data1.append([])
        for j in range(2,10):
            data1[i].append(data[i*10+j])
    return data1
def checkTrung(listLop, lopRandom):
    for x in listLop:
        if x == lopRandom:
            return 1
    return 0

# def chuyenTKB(tkb, n):
#     if n == 0 :
#         tkb1 = [[] for _ in range(len(tkb))]
#         for i in range(len(tkb1)):
#             tkb1[i] = ["" for _ in range(48)]
#         for i in range(len(tkb)):
#             for j in range(len(tkb[i])):
#                 for k in range(len(tkb[i][j])):
#                     tkb1[i][j+k*8]=tkb[i][j][k]
#         return tkb1
#     return 0
def chuyenTKBLop(tkb, listLop, listGV):
    soGV = len(listGV)
    tkb1 = []
    for i in range(soGV):
        tkb1.append([])
        for j in range(8):
            tkb1[i].append([])
            for k in range(6):
                tkb1[i][j].append("")
    for k in range(len(tkb)):
        for i in range(len(tkb[k])):
            for j in range(len(tkb[k][i])):
                if tkb[k][i][j] != "":

                    tkb1[listGV.index(tkb[k][i][j])][i][j] = listLop[k]
    return tkb1

def chuyenTKB(tkb1):
    tkb = []
    for i in range(len(tkb1)):
        tkb.append([])
        for j in range(8):
            tkb[i].append([])
            for k in range(6):
                tkb[i][j].append("")
    for i in range(len(tkb)):
        for j in range(len(tkb[i])):
            for k in range(len(tkb[i][j])):
                tkb[i][j][k] = tkb1[i][k*8+j]
    return tkb
def luuMaTranDieuKien(mt, ten):
    matrix = np.array(mt)
    #
    np.savetxt(str(ten)+".txt", mt, fmt="%d")
def luuList1Chieu(list, ten):
    with open(str(ten)+".txt", "w",encoding="utf-8") as f:
        f.write(", ".join(list))
    f.close()

