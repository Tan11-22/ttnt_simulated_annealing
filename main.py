from tkinter import *
from tkinter import ttk, messagebox
from SimulatedAnnealing import *
import numpy as np


#from SimulatedAnnealing import docTKBTong, chuyenTKBLop

currentFrame = None
r = None
t = None
c = None
d = None

listLop = None
listGV = None

checkboxes = []
checkboxes1 = []
checkboxes2 = []

tkb = docTKBTong("Thời Khoa Biểu Tổng")
def inTKB(frame2, tkb, kieu, tmp):

    style = ttk.Style(frame2)

    style.configure("Treeview",
                    rowheight=50,
                    font=('Time New Roman', 10),
                    bordercolor="red",
                    borderwidth=2)


    table = ttk.Treeview(frame2, style="Treeview",
                         columns=("1", "2", "3", "4", "5", "6", "7"),
                         show='headings',
                         selectmode="browse")

    for col in table["columns"]:
        table.column(col, anchor="center", width=150)
    # Thêm tiêu đề cho từng cột
    table.heading("1", text="Tiết/Thứ")
    table.heading("2", text="Thứ 2")
    table.heading("3", text="Thứ 3")
    table.heading("4", text="Thứ 4")
    table.heading("5", text="Thứ 5")
    table.heading("6", text="Thứ 6")
    table.heading("7", text="Thứ 7")
    if kieu == 0:
        for j in range(len(tkb)):
            table.insert("", END, text="",
                         values=["","","",tmp[j]])
            # Thêm dữ liệu vào bảng
            for i in range(0, len(tkb[j])):
                table.insert("", END, text="", values=["Tiết "+str(i+1)]+tkb[j][i])
    elif kieu == 1:
        for i in range(0, len(tkb[tmp])):
            table.insert("", END, text="", values=["Tiết " + str(i + 1)] + tkb[tmp][i])
    elif kieu == 2:
        for i in range(0, len(tkb[tmp])):
            table.insert("", END, text="", values=["Tiết " + str(i + 1)] + tkb[tmp][i])


    table.configure(height=8)
    # Hiển thị bảng
    table.grid(row=1, column=0)


# def evBtn1(checkboxes, frame):
#     global currentFrame
#     if currentFrame != None:
#         currentFrame.grid_remove()
#     print("Nút 1")
#     for i in range(8):
#         for j in range(6):
#             print(f"checkbox {i},{j} = {checkboxes[i][j].get()}")
#     currentFrame = frame

def chonKieuXem(cmbKieu, cmbKieu0,lbKieu0, listLop, listGV):
    if cmbKieu.get() == "Tổng hợp":
        lbKieu0.config(text="Chọn:")
        cmbKieu0['values'] = ["Trống"]
        cmbKieu0.current(0)
    if cmbKieu.get() == "Theo lớp":
        lbKieu0.config(text="Chọn lớp:")
        cmbKieu0['values'] = listLop
        cmbKieu0.current(0)
    elif cmbKieu.get() == "Theo giáo viên":
        lbKieu0.config(text="Chọn giáo viên:")
        cmbKieu0['values'] = listGV
        cmbKieu0.current(0)

def xemTKB(frame2, tkb, cmb1 ,cmb2, listLop, listGV):
    if cmb1.get() == "Tổng hợp":
        inTKB(frame2, tkb, 0 ,listLop)
    if cmb1.get() == "Theo lớp":
        idLop = listLop.index(cmb2.get())
        inTKB(frame2,tkb,1,idLop)
    if cmb1.get() == "Theo giáo viên":
        tkb1 = chuyenTKBLop(tkb,listLop,listGV)
        idGV = listGV.index(cmb2.get())
        inTKB(frame2,tkb1,2,idGV)

def evBtnXuatFile(kieu, kieu0, tkb):
    global listLop, listGV
    if kieu == "Tổng hợp":
        xuatTKBTatCa(tkb, listLop)
        messagebox.showinfo("Thành công!", "Xuất thời khoa biểu tổng hợp thành công!")
        return
    if kieu == "Theo lớp":
        idLop = listLop.index(kieu0)
        xuatTKB(tkb, idLop, listLop)
        messagebox.showinfo("Thành công!", "Xuất thời khoa biểu của lớp "+str(listLop[idLop])+" thành công!")
        return
    if kieu == "Theo giáo viên":
        idGV = listGV.index(kieu0)
        tkb1 = chuyenTKBLop(tkb,listLop,listGV)
        xuatTKB(tkb1,idGV,listGV)
        messagebox.showinfo("Thành công!", "Xuất thời khoa biểu của giáo viên " + str(listGV[idGV]) + " thành công!")
        return

def evBtn1(frame2, tkb, listLop, listGV):
    global  currentFrame
    if currentFrame != None:
        currentFrame.grid_remove()
        frame2.grid()
    framet = Frame(frame2)
    framet.grid(row=0, column=0, sticky="w")
    lbKieu0 = Label(framet, text="Chọn:", width= 20)
    lbKieu0.grid(row=0, column=2)

    cmbKieu0 = ttk.Combobox(framet)
    cmbKieu0['values'] = ["Trống"]
    cmbKieu0.grid(row=0, column=3)

    lbKieu = Label(framet, text="Chọn kiểu xem:")
    lbKieu.grid(row=0, column=0)

    cmbKieu = ttk.Combobox(framet)
    cmbKieu['values'] = ["Tổng hợp","Theo lớp", "Theo giáo viên"]
    cmbKieu.bind("<<ComboboxSelected>>",
                 lambda event: chonKieuXem( cmbKieu, cmbKieu0,lbKieu0, listLop, listGV))
    cmbKieu.grid(row=0, column=1)
    cmbKieu.current(0)
    btnXemTKB = Button(framet, text="Xem",
                          command=lambda: xemTKB(frame2,tkb,cmbKieu,cmbKieu0,listLop,listGV))
    btnXemTKB.grid(row=0, column=4)
    btnXuatTKB = Button(frame2, text="Xuất file",
                        command= lambda : evBtnXuatFile(cmbKieu.get(),cmbKieu0.get(),tkb))
    btnXuatTKB.grid(row=10, column=0,sticky='e',pady= 10)
    inTKB(frame2, tkb, 0, listLop)

    currentFrame = frame2

def inKhungCheckBoxC(frame3,idLop):
    global c, checkboxes1

    lbC = Label(frame3, text="Chọn tiết lớp không thể học:")
    lbC.grid(row=0, column=0,columnspan=2)

    lb = Label(frame3, text="Tiết/Thứ ")
    lb.grid(row=1, column=0, padx=15)
    for i in range(6):
        lb = Label(frame3,text="Thứ " + str(i+2))
        lb.grid(row=1, column=i+1, padx=15)
    for i in range(8):
        lb = Label(frame3,text="Tiết " + str(i+1))
        lb.grid(row=i+2, column=0, pady=(15,15))
    for i in range(8):
        row = []
        for j in range(6):
            var1 = BooleanVar()
            chk1 = Checkbutton(frame3, variable=var1)
            if c[idLop][j*8+i] == 0:
                var1.set(True)


            chk1.grid(row=i+2, column=j+1, padx=15, pady=(15,15))
            row.append(var1)
        checkboxes1.append(row)

    # print(c)
    # print(idLop)
    # for i in range(len(checkboxes1)):
    #     for j in range(len(checkboxes1[i])):
    #         print(checkboxes1[i][j].get(), end=" ")
    #     print()

def inKhungCheckBoxD(frame3,idLop):
    global d, checkboxes2

    lbD = Label(frame3, text="Chọn tiết lớp bắt buộc học:")
    lbD.grid(row=0, column=0,columnspan=2)
    lb = Label(frame3, text="Tiết/Thứ ")
    lb.grid(row=1, column=0, padx=15)
    for i in range(6):
        lb = Label(frame3,text="Thứ " + str(i+2))
        lb.grid(row=1, column=i+1, padx=15)
    for i in range(8):
        lb = Label(frame3,text="Tiết " + str(i+1))
        lb.grid(row=i+2, column=0, pady=(15,15))
    for i in range(8):
        row = []
        for j in range(6):
            var1 = BooleanVar()
            chk1 = Checkbutton(frame3, variable=var1)
            if d[idLop][j*8+i] == 1:
                var1.set(True)


            chk1.grid(row=i+2, column=j+1, padx=15, pady=(15,15))
            row.append(var1)
        checkboxes2.append(row)
def inThongTinLop(frame32, frame33, cmb):
    idLop = listLop.index(cmb.get())
    inKhungCheckBoxC(frame32,idLop)
    inKhungCheckBoxD(frame33, idLop)

def themLop(tb,cmb,frame32,frame33):
    global c,d,r,listLop, listGV ,checkboxes1, checkboxes2
    if tb.get() in listLop:
        messagebox.showerror("Error", "Lớp bạn muốn thêm đã trùng, không thể thêm lớp.")
        return
    else:
        checkboxes1 = []
        checkboxes2 = []
        listLop.append(tb.get())
        tmp = []
        for i in range(len(listGV)):
            tmp.append(0)
        new_row = np.array(tmp)
        r = np.append(r, [new_row], axis=0)

        tmp = []
        for i in range(48):
            tmp.append(1)
        new_row = np.array(tmp)
        c = np.append(c, [new_row], axis=0)  # axis = 0 thêm row
        tmp = []
        for i in range(48):
            tmp.append(0)
        new_row = np.array(tmp)
        d = np.append(d, [new_row], axis=0)
        cmb["values"] = listLop
        cmb.current(len(listLop) - 1)
        luuMaTranDieuKien(r,'R')
        luuMaTranDieuKien(c, 'C')
        luuMaTranDieuKien(d, 'D')
        luuList1Chieu(listLop,'lop')
        inKhungCheckBoxC(frame32,len(listLop) -1)
        inKhungCheckBoxD(frame33, len(listLop) - 1)
        messagebox.showinfo("Thành công!", "Bạn đã thêm lớp thành công.")

def xoaLop(cmb):
    global  r , listLop , c, d
    idLop = listLop.index(cmb.get())
    for i in range(len(r[idLop])):
        if r[idLop][i] > 0 :
            messagebox.showerror("Error", "Lớp đã được phân công giáo viên giáo dạy, không thể xoá.")
            return

    del listLop[idLop]
    r = np.delete(r, idLop, axis= 0 )
    c = np.delete(c, idLop, axis= 0)
    d = np.delete(d,idLop,axis= 0 )
    luuMaTranDieuKien(r, 'R')
    luuMaTranDieuKien(c, 'C')
    luuMaTranDieuKien(d, 'D')
    luuList1Chieu(listLop, 'lop')
    cmb['values'] = listLop
    cmb.grid()
    cmb.current(0)
    messagebox.showinfo("Thành công!", "Bạn đã xoá lớp thành công!")
    #print(listLop)

def luuDieuKienLop(cmb):
    global c, d, listLop, checkboxes1, checkboxes2
    idLop = listLop.index(cmb.get())
    # for i in range(8):
    #     for j in range(6):
    #         #print(checkboxes1[i][j].get())
    for i in range(8):
        for j in range(6):
            if checkboxes1[i][j].get():
                c[idLop][j*8+i] = 0
                #print(c, " ", j*8+i)
    for i in range(8):
        for j in range(6):
            if checkboxes2[i][j].get():
                d[idLop][j*8+i] = 1
    luuMaTranDieuKien(c,'C')
    luuMaTranDieuKien(d, 'D')
    messagebox.showinfo("Thành công!", "Lưu các tiết lớp không thể học và bắt buộc học thành công")

def evBtn2(frame3):
    global currentFrame, listLop, listGV, c, d, r, checkboxes1, checkboxes2
    if currentFrame != None:
        currentFrame.grid_remove()
        frame3.grid()

    frame31 = Frame(frame3)
    frame31.grid(row=0, column=0,columnspan=2)
    frame32 = Frame(frame3)
    frame32.grid(row=2, column=0)

    frame33 = Frame(frame3)
    frame33.grid(row=2, column=1, padx=50)
    cmb = ttk.Combobox(frame31, width=15)
    cmb['values'] = listLop
    cmb.grid(row=1, column=1)
    cmb.current(0)
    cmb.bind("<<ComboboxSelected>>",
             lambda event: inThongTinLop(frame32, frame33, cmb))
    idLop = listLop.index(cmb.get())

    lbThemLop = Label(frame31, text="Nhập lớp: ")
    lbThemLop.grid(row=0, column=0, sticky="w")
    lbThemLop.grid_columnconfigure(0, minsize=20)
    tbThemLop = Entry(frame31, width=18)
    tbThemLop.grid(row=0, column=1, sticky="w")
    btnThemLop = Button(frame31,
                       text="Thêm",
                        command=lambda : themLop(tbThemLop,cmb,frame32,frame33))
    btnThemLop.grid(row=0, column=2)
    lbGV = Label(frame31, text="Lớp: ")
    lbGV.grid(row=1, column=0, sticky="w")

    inKhungCheckBoxC(frame32, idLop)
    inKhungCheckBoxD(frame33, idLop)
    btnCancel = Button(frame33, text="Xoá lớp", width=10, height=2,
                       command=lambda :xoaLop(cmb)
                       )
    btnCancel.grid(row=10, column=5)
    btnSubmit = Button(frame33, text="Lưu thay đổi", width=10, height=2,
                       command=lambda :luuDieuKienLop(cmb)
                       )
    btnSubmit.grid(row=10, column=6)
    currentFrame = frame3


# Bảng thông tin số tiết mà giáo viên phải dạy cho các lớp
def inThongTinSoTiet(frame,cmb, listLop, listGV, tbSoTiet, cmb1,
                     frameTick3):
    global r, t, checkboxes
    gv = cmb.get()
    if gv == "":
        return
    inSoTiet(tbSoTiet, listLop, cmb, cmb1)
    idGV = listGV.index(gv)
    style = ttk.Style(frame)

    style.configure("Treeview",
                    rowheight=40,
                    font=('Time New Roman', 10),
                    #bordercolor="red",
                    borderwidth=2)


    table = ttk.Treeview(frame, style="Treeview",
                         columns=("1", "2"),
                         show='headings',
                         selectmode="browse")

    for col in table["columns"]:
        table.column(col, anchor="center", width=150)
    # Thêm tiêu đề cho từng cột
    table.heading("1", text="Lớp")
    table.heading("2", text="Số tiết")


    # Thêm dữ liệu vào bảng
    for i in range(0, len(r)):
        table.insert("", END, text="", values=[listLop[i],r[i][idGV]])

    table.configure(height=8)
    # Hiển thị bảng
    table.grid(row=0, column=0)
    if frameTick3 != None:
        inKhungCheckBox(frameTick3,checkboxes, idGV)


def inSoTiet(tbSoTiet,listLop,cmb,cmb1):
    global r
    tbSoTiet.delete(0,END)
    idLop = listLop.index(cmb1.get())
    idGV = listGV.index(cmb.get())
    tbSoTiet.insert(0,
                    r[idLop][idGV])

def luuSoTiet(tbSoTiet, cmb1,frameTick4, cmb, listLop, listGV):
    global r, t, c
    idLop = listLop.index(cmb1.get())
    idGV = listGV.index(cmb.get())
    if not tbSoTiet.get().isdigit():
        messagebox.showerror("Error", "Số tiết phải nhập giá trị số.")
        return

    if int(tbSoTiet.get()) > 10 :
        messagebox.showerror("Error", "Số tiết phải là số nhỏ hơn hoặc bằng 10.")
        return
    sumTietTrong = 0
    for i in range(len(t[idGV])):
        sumTietTrong += t[idGV][i]
    if int(tbSoTiet.get()) > sumTietTrong :
        messagebox.showerror("Error", "Số tiết còn trống của giáo viên là " + str(sumTietTrong) +", không thể nhập lớn hơn.")
        return
    sumTietTrong1 = 0
    for i in range(len(c[idLop])):
        sumTietTrong1 += c[idLop][i]
    if int(tbSoTiet.get()) > sumTietTrong1:
        messagebox.showerror("Error",
                             "Số tiết còn trống của lớp "+listLop[idLop]+" là " + str(sumTietTrong1) + ", không thể nhập lớn hơn.")
        return
    if tbSoTiet.get() == r[idLop][idGV]:
        return
    else:
        r[idLop][idGV] = tbSoTiet.get()
        inThongTinSoTiet(frameTick4, cmb, listLop, listGV,tbSoTiet, cmb1,None)
    luuMaTranDieuKien(r, 'R')

def luuGV(idGV):
    global r, t, checkboxes

    for i in range(8):
        for j in range(6):
            if checkboxes[i][j].get():
                t[idGV][j*8+i] = 0
    # for i in range(8):
    #     for j in range(6):
    #         print(checkboxes[i][j].get())
    luuMaTranDieuKien(t, 'T')
    messagebox.showinfo("Thành công!", "Lưu các tiết giáo viên không thể dạy thành công")
    #print(t)
    # for i in range(len(t)):
    #     print(t[i])
    # for i in range(len(r)):
    #     print(r[i])

def inKhungCheckBox(frameTick3,checkboxes,idGV):
    global t
    lbT = Label(frameTick3, text="Chọn tiết lớp không thể học:")
    lbT.grid(row=0, column=0, columnspan=2)
    for i in range(6):
        lb = Label(frameTick3,text="Thứ " + str(i+2))
        lb.grid(row=1, column=i+1, padx=30)
    for i in range(8):
        lb = Label(frameTick3,text="Tiết " + str(i+1))
        lb.grid(row=i+2, column=0, pady=(15,15))
    for i in range(8):
        row = []
        #print("Lần thứ ", i)
        for j in range(6):
            var = BooleanVar()
            chk = Checkbutton(frameTick3, variable=var)
            if t[idGV][j*8+i] == 0:
                var.set(True)
                #print(j*8+i, " ", i, " ", j)

            chk.grid(row=i+2, column=j+1, padx=30, pady=(15,15))
            row.append(var)
        checkboxes.append(row)
def themGiangVien(frameTick4,
                  cmb,
                tbSoTiet,
                cmb1,
                frameTick3,
                tbThemGV):
    global r, t, listGV, listLop, checkboxes
    if tbThemGV.get() in listGV:
        messagebox.showerror("Error", "Giáo viên bạn muốn thêm đã tồn tại, không thể thêm.")
    else:
        checkboxes = []
        listGV.append(tbThemGV.get())
        #print(listGV, "   ", len(listGV))
        tmp = []
        for i in range(len(listLop)):
            tmp.append(0)
        new_column = np.array(tmp).reshape(-1,1)
        r = np.append(r,new_column,axis=1)
        #print(r)
        tmp1 = []
        for i in range(48):
            tmp1.append(1)
        new_row = np.array(tmp1)
        t = np.append(t,[new_row], axis=0) # axis = 0 thêm row
        cmb["values"] = listGV
        cmb.current(len(listGV)-1)
        luuList1Chieu(listGV,'giangvien')
        luuMaTranDieuKien(r,"R")
        luuMaTranDieuKien(t,"T")
        inThongTinSoTiet(frameTick4,
                         cmb,
                         listLop,
                         listGV,
                         tbSoTiet,
                         cmb1,
                         frameTick3
                         )
        messagebox.showinfo("Thành công!", "Thêm giáo viên thành công")

def xoaGV(cmb,
          frameTick4,
                     listLop,
                                tbSoTiet,
                                    cmb1,
                                        frameTick3):
    global r ,t, listGV
    idGV = listGV.index(cmb.get())
    for i in range(len(r)):
        if r[i][idGV] > 0:
            messagebox.showerror("Error","Giáo viên đã được phân công tiết dạy không thể xoá.")
            return
    del listGV[idGV]
    r = np.delete(r,idGV,axis=1)
    t = np.delete(t,idGV,axis=0)
    cmb.current(0)
    luuList1Chieu(listGV, 'giangvien')
    luuMaTranDieuKien(r, "R")
    luuMaTranDieuKien(t, "T")
    inThongTinSoTiet(frameTick4,
                     cmb,
                     listLop,
                     listGV,
                     tbSoTiet,
                     cmb1,
                     frameTick3
                     )
    messagebox.showinfo("Thành công!", "Xoá giáo viên thành công")

def evBtn3(frameTick, listGV, listLop ):
    global currentFrame, checkboxes
    if currentFrame != None:
        currentFrame.grid_remove()
        frameTick.grid()


    global  r, t

    #Frame tiêu đề ở trên
    frameTick2 = Frame(frameTick)
    frameTick2.grid(row=0, column=0)

    #Frame table checkbox thể hiện tiết giáo viên không thể dạy
    frameTick3 = Frame(frameTick)
    frameTick3.grid(row=0, column=1,rowspan=3, padx=10)

    #Frame table thề hiện số tiết và số lớp giáo viên đó phải dạy
    frameTick4 = Frame(frameTick)
    frameTick4.grid(row=1, column=0)

    lbThemGV = Label(frameTick2, text="Nhập tên giáo viên: ")
    lbThemGV.grid(row=0, column=0, sticky="w")
    lbThemGV.grid_columnconfigure(0,minsize=20)
    tbThemGV = Entry(frameTick2, width=18)
    tbThemGV.grid(row=0, column=1, sticky="w")
    btnThemGV = Button(frameTick2,
                          text="Thêm",
                          command=lambda : themGiangVien(frameTick4,
                  cmb,
                tbSoTiet,
                cmb1,
                frameTick3,
                tbThemGV))
    btnThemGV.grid(row=0, column=2)

    lbGV = Label(frameTick2,text="Giáo viên: ")
    lbGV.grid(row=1, column=0, sticky="w")

    # Combobox giáo viên
    cmb = ttk.Combobox(frameTick2, width=15)
    cmb['values'] = listGV
    cmb.grid(row=1, column=1)
    cmb.current(0)

    lbLop = Label(frameTick2, text="Lớp: ")
    lbLop.grid(row=2, column=0, sticky="w")
    cmb1 = ttk.Combobox(frameTick2, width=15)
    cmb1['values'] = listLop
    cmb1.grid(row=2, column=1)
    cmb1.current(0)
    lbSoTiet = Label(frameTick2, text="Số tiết: ")
    lbSoTiet.grid(row=3, column=0,sticky="w")
    tbSoTiet = Entry(frameTick2, width=18)
    tbSoTiet.grid(row=3,column=1,sticky="w")
    tbSoTiet.insert(0,
                    r[listLop.index(cmb1.get())][listGV.index(cmb.get())])
    cmb.bind("<<ComboboxSelected>>",
             lambda event: inThongTinSoTiet(frameTick4,
                                            cmb,
                                            listLop,
                                            listGV,
                                            tbSoTiet,
                                            cmb1,
                                            frameTick3
                                            ))
    cmb1.bind("<<ComboboxSelected>>",
             lambda event: inSoTiet(tbSoTiet,listLop,cmb,cmb1))
    btnLuuSoTiet = Button(frameTick2,
                          text="Cập nhật",
                          command=lambda : luuSoTiet(tbSoTiet, cmb1,frameTick4, cmb, listLop, listGV))
    btnLuuSoTiet.grid(row=4,column=1)
    inThongTinSoTiet(frameTick4, cmb, listLop, listGV,tbSoTiet,cmb1,frameTick3)
    #inKhungCheckBox(frameTick3,checkboxes,listGV.index(cmb.get()))




    btnSubmit = Button(frameTick3, text="Lưu thay đổi", width=10, height=2,
                       command=lambda :luuGV(listGV.index(cmb.get())))
    btnSubmit.grid(row=10,column=7)
    btnCancel = Button(frameTick3, text="Xoá giáo viên", width=10, height=2,
                       command=lambda: xoaGV(cmb,frameTick4,listLop, tbSoTiet, cmb1, frameTick3)
                       )
    btnCancel.grid(row=10, column=6)

    currentFrame = frameTick
def taoLaiTKB( frame2):
    global r, t, c, d, listLop, listGV, tkb
    soLop = len(listLop)
    soGiangVien = len(listGV)
    #MAX = 100
    #print(soLop,len(tkb))
    # Khởi tạo thời khoa biểu trống
    tkb1 = [[] for _ in range(soLop)]
    for i in range(soLop):
        tkb1[i] = ["" for _ in range(48)]
    cTMP = copy.deepcopy(c)
    rTMP = copy.deepcopy(r)
    listCheck = []
    # for i in range(len(tkb)):
    #     listCheck.append(i)
    diemDung = 0
    while diemDung < soLop:
        # Chọn ra 1 lớp bất kì từ danh sách lớp
        lopRandom = random.randint(0, soLop - 1)
        if checkTrung(listCheck, lopRandom):
            continue
        #print(listLop[lopRandom])
        listCheck.append(lopRandom)
        diemDung += 1

        tkb1 = taoTKBNgauNhien(tkb1, lopRandom, rTMP, t, cTMP, soGiangVien, listGV)
        #print(tkb1[5])
        tkb1, best_cost = simulated_annealing(1000, tkb1, lopRandom, listGV, t, c, d)
    tkb = chuyenTKB(tkb1)
    messagebox.showinfo("Thành công!", "Tạo thời khoa biểu cho các lớp thành công")
    xuatTKBTatCa(tkb, listLop)
    evBtn1(frame2, tkb, listLop, listGV)


if __name__ == '__main__':
    with open("lop.txt", "r", encoding="utf-8") as f:
        content = f.read()
    listLop = content.split(", ")
    with open("giangvien.txt", "r", encoding="utf-8") as f:
        content = f.read()
    f.close()
    listGV = content.split(", ")
    r = np.loadtxt("R.txt", delimiter=" ", dtype=int)

    t = np.loadtxt("T.txt", delimiter=" ", dtype=int)
    c = np.loadtxt("C.txt", delimiter=" ", dtype=int)
    d = np.loadtxt("D.txt", delimiter=" ", dtype=int)




    root = Tk()
    # Lấy kích thước màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() - 100

    # Thiết lập kích thước cửa sổ bằng kích thước màn hình
    root.geometry('{}x{}'.format(screen_width, screen_height))
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True)

    
    frame1 = Frame(main_frame, width=50)
    frame1.grid(row=0, column=0, sticky=N + S)
    frame2 = Frame(main_frame)
    frame2.grid(row=0, column=1, sticky=N + S)

    frame3 = Frame(main_frame)
    frame3.grid(row=0, column=1, sticky=N + S)


    frameTick = Frame(main_frame)
    frameTick.grid(row=0, column=1, sticky=N + S)

    frame4 = Frame(main_frame)
    frame4.grid(row=0, column=1, sticky=N + S)



    button1 = Button(frame1, text="Xem thời khoa biểu",
                     width=30,
                     height=2,
                     command=lambda : evBtn1(frame2, tkb,listLop,listGV))
    button2 = Button(frame1, text="Thêm lớp",
                     width=30,
                     height=2,
                     command=lambda : evBtn2(frame3))
    button3 = Button(frame1, text="Thêm giáo viên",
                     width=30, 
                     height=2,
                     command=lambda : evBtn3(frameTick,listGV,listLop))
    button4 = Button(frame1, text="Tạo thời khoa biểu", width=30, height=2,
                     command= lambda : taoLaiTKB(frame2))
    button5 = Button(frame1, text="Thoát", width=30, height=2, command=root.destroy)

    # sử dụng grid để xếp các nút vào khung chứa
    button1.grid(row=0, column=0, padx=10, pady=(25,25))
    button2.grid(row=1, column=0, padx=10, pady=(25,25))
    button3.grid(row=2, column=0, padx=10, pady=(25,25))
    button4.grid(row=3, column=0, padx=10, pady=(25,25))
    button5.grid(row=4, column=0, padx=10, pady=(25,25))


    root.mainloop()
