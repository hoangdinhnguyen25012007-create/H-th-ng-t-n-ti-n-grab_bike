import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx
from tkinter import *
from tkinter.ttk import Combobox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import folium
import webbrowser


quang_duong = ctrl.Antecedent(np.arange(1, 51, 1), 'quang_duong')
tinh_trang_gt = ctrl.Antecedent(np.arange(0, 101, 1), 'tinh_trang_gt')
muc_cau = ctrl.Antecedent(np.arange(0, 101, 1), 'muc_cau')
thoi_tiet = ctrl.Antecedent(np.arange(0, 101, 1), 'thoi_tiet')
danh_gia = ctrl.Antecedent(np.arange(0, 5.5, 0.5), 'danh_gia')
dung_gio = ctrl.Antecedent(np.arange(0, 101, 1), 'dung_gio')
gia_tien = ctrl.Consequent(np.arange(0, 300.5, 0.5), 'gia_tien', defuzzify_method='mom')
diem_thuong = ctrl.Consequent(np.arange(0, 11, 1), 'diem_thuong', defuzzify_method='mom')


quang_duong['gan'] = fuzz.trimf(quang_duong.universe, [1, 1, 3])
quang_duong['trung_binh'] = fuzz.trimf(quang_duong.universe, [2, 5, 8])
quang_duong['xa'] = fuzz.trimf(quang_duong.universe, [6, 13, 20])
quang_duong['rat_xa'] = fuzz.trimf(quang_duong.universe, [15, 32.5, 50])

tinh_trang_gt['thap'] = fuzz.trimf(tinh_trang_gt.universe, [0, 0, 30])
tinh_trang_gt['trung_binh'] = fuzz.trimf(tinh_trang_gt.universe, [20, 45, 70])
tinh_trang_gt['cao'] = fuzz.trimf(tinh_trang_gt.universe, [60, 80, 100])

muc_cau['thap'] = fuzz.trimf(muc_cau.universe,[0, 0, 30])
muc_cau['trung_binh'] = fuzz.trimf(muc_cau.universe,[20, 45, 70])
muc_cau['cao'] = fuzz.trimf(muc_cau.universe,[60, 80, 100])

thoi_tiet['dep'] = fuzz.trimf(thoi_tiet.universe,[0, 0, 40])
thoi_tiet['hoi_xau'] = fuzz.trimf(thoi_tiet.universe, [20, 45, 70])
thoi_tiet['xau'] = fuzz.trimf(thoi_tiet.universe, [60, 80, 100])

danh_gia['kem'] = fuzz.trimf(danh_gia.universe, [1, 1.5, 2.5])
danh_gia['trung_binh']= fuzz.trimf(danh_gia.universe, [2, 3, 4])
danh_gia['tot'] = fuzz.trimf(danh_gia.universe, [3.5, 4.5, 5])

dung_gio['tre']  = fuzz.trimf(dung_gio.universe, [0, 0, 50])
dung_gio['dung'] = fuzz.trimf(dung_gio.universe, [40, 60, 80])
dung_gio['som']  = fuzz.trimf(dung_gio.universe, [70, 85, 100])

gia_tien['thap'] = fuzz.trimf(gia_tien.universe, [0, 0, 30])
gia_tien['trung_binh'] = fuzz.trimf(gia_tien.universe, [25, 47.5, 70])
gia_tien['cao'] = fuzz.trimf(gia_tien.universe, [50, 100, 150])
gia_tien['rat_cao'] = fuzz.trimf(gia_tien.universe, [150, 225, 300])

diem_thuong['khong'] = fuzz.trimf(diem_thuong.universe, [0, 0, 1])
diem_thuong['it'] = fuzz.trimf(diem_thuong.universe, [1, 2.5, 4])
diem_thuong['bthuong'] = fuzz.trimf(diem_thuong.universe, [5, 6.5, 8])
diem_thuong['nhieu'] = fuzz.trimf(diem_thuong.universe, [7, 10, 10])

rule1  = ctrl.Rule(quang_duong['gan'] & tinh_trang_gt['thap'] & muc_cau['thap'], gia_tien['thap'])
rule2  = ctrl.Rule(quang_duong['gan'] & tinh_trang_gt['trung_binh']& muc_cau['cao'], gia_tien['trung_binh'])
rule3  = ctrl.Rule(quang_duong['trung_binh'] & tinh_trang_gt['cao'] & muc_cau['cao'], gia_tien['cao'])
rule4  = ctrl.Rule(quang_duong['xa'] & tinh_trang_gt['trung_binh']& thoi_tiet['dep'], gia_tien['trung_binh'])
rule5  = ctrl.Rule(quang_duong['xa'] & tinh_trang_gt['cao'] & thoi_tiet['xau'], gia_tien['rat_cao'])
rule6  = ctrl.Rule(quang_duong['rat_xa'] & tinh_trang_gt['cao'] & muc_cau['cao'], gia_tien['rat_cao'])
rule7  = ctrl.Rule(quang_duong['trung_binh'] & tinh_trang_gt['thap'] & muc_cau['thap'], gia_tien['trung_binh'])
rule8  = ctrl.Rule(quang_duong['gan'] & tinh_trang_gt['cao'] & thoi_tiet['xau'], gia_tien['cao'])
rule9  = ctrl.Rule(quang_duong['rat_xa'] & thoi_tiet['xau'], gia_tien['rat_cao'])
rule10 = ctrl.Rule(quang_duong['trung_binh'] & tinh_trang_gt['trung_binh']& thoi_tiet['hoi_xau'], gia_tien['trung_binh'])
rule_default1 = ctrl.Rule(quang_duong['gan'] & quang_duong['trung_binh'] & quang_duong['xa'] & quang_duong['rat_xa'], gia_tien['trung_binh'])

rule11 = ctrl.Rule(danh_gia['tot'] & dung_gio['som'], diem_thuong['nhieu'])
rule12 = ctrl.Rule(danh_gia['trung_binh'] & dung_gio['dung'], diem_thuong['bthuong'])
rule13 = ctrl.Rule(danh_gia['kem'] & dung_gio['tre'], diem_thuong['khong'])
rule14 = ctrl.Rule(quang_duong['xa'] & tinh_trang_gt['cao'] & dung_gio['dung'], diem_thuong['nhieu'])
rule15 = ctrl.Rule(quang_duong['trung_binh'] & tinh_trang_gt['trung_binh']& danh_gia['tot'], diem_thuong['bthuong'])
rule16 = ctrl.Rule(quang_duong['rat_xa'] & thoi_tiet['xau'] & danh_gia['tot'], diem_thuong['nhieu'])
rule17 = ctrl.Rule(quang_duong['gan'] & danh_gia['trung_binh'] & dung_gio['dung'], diem_thuong['it'])
rule18 = ctrl.Rule(quang_duong['xa'] & tinh_trang_gt['cao'] & dung_gio['tre'], diem_thuong['it'])
rule19 = ctrl.Rule(quang_duong['trung_binh'] & thoi_tiet['hoi_xau'] & danh_gia['tot'], diem_thuong['bthuong'])
rule_default2 = ctrl.Rule(dung_gio['tre'] & dung_gio['dung'] & dung_gio['som'], diem_thuong['it'])

mophong_gia  = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule_default1])
mophong_diem = ctrl.ControlSystem([rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule_default2])

root = Tk()
root.title("Hệ thống tín tiền")
root.geometry("1200x750")
tieude = Label(root, text="Hệ thống tín tiền", font=("Times New Roman", 25), fg="blue")
tieude.pack(pady=20)

a = Label(root, text="Nhập điểm đầu: ", font=("Arial", 12))
a.place(x=50, y=100)
a1 = Entry(root, width=50)
a1.place(x=200, y=100)

b = Label(root, text="Nhập điểm cuối: ", font=("Arial", 12))
b.place(x=50, y=150)
b1 = Entry(root, width=50)
b1.place(x=200, y=150)

chonpt = Label(root, text="Chọn phương tiện: ", font=("Arial", 12))
chonpt.place(x=50, y=200)
combobox = Combobox(root, values=["bike", "drive"])
combobox.place(x=200, y=200)

ttgt = Label(root, text="Tình trạng giao thông: ", font=("Arial", 12))
ttgt.place(x=50, y=250)
ttgt1 = Scale(root, from_=0, to=100, orient=HORIZONTAL)
ttgt1.place(x=200, y=250)

mucau = Label(root, text="Mức cầu: ", font=("Arial", 12))
mucau.place(x=50, y=300)
mucau1 = Scale(root, from_=0, to=100, orient=HORIZONTAL)
mucau1.place(x=200, y=300)

thoitiet = Label(root, text="Thời tiết: ", font=("Arial", 12))
thoitiet.place(x=50, y=350)
thoitiet1 = Scale(root, from_=0, to=100, orient=HORIZONTAL)
thoitiet1.place(x=200, y=350)

dunggio = Label(root, text="Đúng giờ: ", font=("Arial", 12))
dunggio.place(x=50, y=400)
dunggio1 = Scale(root, from_=0, to=100, orient=HORIZONTAL)
dunggio1.place(x=200, y=400)

danhgia = Label(root, text="Đánh giá: ", font=("Arial", 12))
danhgia.place(x=50, y=450)
danhgia1 = Combobox(root, values=[1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
danhgia1.place(x=200, y=450)

fr = Frame(root, width=500, height=200, bg="skyblue")
fr.place(x=50, y=500)

tieude= Label(fr, text="Kết quả tính toán :", font=("Arial", 15), bg="skyblue")
tieude.place(x=10 , y=10)


ketqua_label = Label(fr, text="", font=("Arial", 15), bg="skyblue")
ketqua_label.place(relx=0.5, rely=0.5, anchor="center")

def hien_kq():
    diem_dau    = a1.get()
    diem_cuoi   = b1.get()
    phuong_tien = combobox.get()

    geolacator      = Nominatim(user_agent="myGeocoder")
    toado_diem_dau  = geolacator.geocode(diem_dau)
    toado_diem_cuoi = geolacator.geocode(diem_cuoi)

    if toado_diem_dau is None or toado_diem_cuoi is None:

        ketqua_label.config(text="Không tìm thấy địa điểm!")
        return

    toado_dau  = (toado_diem_dau.latitude,  toado_diem_dau.longitude)
    toado_cuoi = (toado_diem_cuoi.latitude, toado_diem_cuoi.longitude)
    center = ((toado_dau[0]+toado_cuoi[0])/2, (toado_dau[1]+toado_cuoi[1])/2)

    G = ox.graph_from_point(center, dist=5000, network_type=phuong_tien)
    orig_node = ox.nearest_nodes(G, toado_dau[1],  toado_dau[0])
    dest_node = ox.nearest_nodes(G, toado_cuoi[1], toado_cuoi[0])
    distance  = nx.shortest_path_length(G, orig_node, dest_node, weight='length')
    so_km = distance / 1000


    tinh_tien = ctrl.ControlSystemSimulation(mophong_gia)
    tinh_diem = ctrl.ControlSystemSimulation(mophong_diem)


    try:
        tinh_tien.input['quang_duong'] = so_km
        tinh_tien.input['tinh_trang_gt'] = ttgt1.get()
        tinh_tien.input['muc_cau'] = mucau1.get()
        tinh_tien.input['thoi_tiet'] = thoitiet1.get()
        tinh_tien.compute()
        gia = tinh_tien.output['gia_tien']
    except KeyError:
        ketqua_label.config(text="Không tính được giá!\nThử thay đổi thông số.")
        return


    try:
        tinh_diem.input['quang_duong'] = so_km
        tinh_diem.input['tinh_trang_gt'] = ttgt1.get()
        tinh_diem.input['thoi_tiet'] = thoitiet1.get()
        tinh_diem.input['danh_gia'] = float(danhgia1.get())
        tinh_diem.input['dung_gio'] = dunggio1.get()
        tinh_diem.compute()
        diem = tinh_diem.output['diem_thuong']
    except KeyError:
        ketqua_label.config(text="Không tính được điểm!\nThử thay đổi thông số.")
        return


    ketqua_label.config(text="")
    qd = Label(fr, text=f"Quãng đường: {round(so_km, 2)} km", font=("Arial", 12), bg="skyblue")
    qd.place(relx=0.5, rely=0.3, anchor="center")

    gt = Label(fr, text=f"Giá tiền: {round(gia, 2)} nghìn đồng", font=("Arial", 12), bg="skyblue")
    gt.place(relx=0.5, rely=0.5, anchor="center")

    dt = Label(fr, text=f"Điểm thưởng: {round(diem, 1)}/10 điểm", font=("Arial", 12), bg="skyblue")
    dt.place(relx=0.5, rely=0.7, anchor="center")

btt = Button(root, text="Tính Toán", bg="lightblue", command=hien_kq, font=("Arial", 20, "bold"))
btt.place(x=400, y=250)

def xem_map():
    diem_dau  = a1.get().strip()
    diem_cuoi = b1.get().strip()

    if diem_dau == "" or diem_cuoi == "":
        ketqua_label.config(text="Vui lòng nhập đầy đủ điểm đầu và điểm cuối!")
        return

    geolocator = Nominatim(user_agent="myGeocoder")
    toado_diem_dau  = geolocator.geocode(diem_dau)
    toado_diem_cuoi = geolocator.geocode(diem_cuoi)

    if toado_diem_dau is None or toado_diem_cuoi is None:
        ketqua_label.config(text="Địa điểm không hợp lệ! Vui lòng nhập lại.")
        return
    diem_dau  = a1.get()
    diem_cuoi = b1.get()
    phuong_tien = combobox.get()

    geolocator = Nominatim(user_agent="myGeocoder")
    toado_diem_dau  = geolocator.geocode(diem_dau)
    toado_diem_cuoi = geolocator.geocode(diem_cuoi)

    if toado_diem_dau is None or toado_diem_cuoi is None:
        ketqua_label.config(text="Không tìm thấy địa điểm!")
        return

    toado_dau  = (toado_diem_dau.latitude,  toado_diem_dau.longitude)
    toado_cuoi = (toado_diem_cuoi.latitude, toado_diem_cuoi.longitude)

    center = ((toado_dau[0]+toado_cuoi[0])/2, (toado_dau[1]+toado_cuoi[1])/2)

    G = ox.graph_from_point(center, dist=5000, network_type=phuong_tien)

    orig_node = ox.nearest_nodes(G, toado_dau[1],  toado_dau[0])
    dest_node = ox.nearest_nodes(G, toado_cuoi[1], toado_cuoi[0])

    route = nx.shortest_path(G, orig_node, dest_node, weight='length')

    m = folium.Map(location=center, zoom_start=13)

    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

    folium.PolyLine(route_coords, color="blue", weight=5).add_to(m)

    folium.Marker(toado_dau, popup="Điểm đầu").add_to(m)
    folium.Marker(toado_cuoi, popup="Điểm cuối").add_to(m)

    m.save("map.html")

    webbrowser.open("map.html")

bbt = Button(root, text="Xem Map", bg="lightblue", command=xem_map, font=("Arial", 20, "bold"))
bbt.place(x=400, y=350)

frame_bieudo1 = Frame(root, width=550, height=300, bg="lightgray")
frame_bieudo1.place(x=600, y=100)

def xem_bd_gia():
    for widget in frame_bieudo1.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(5.5, 3), dpi=100)
    ax = fig.add_subplot(111)

    for term in gia_tien.terms:
        ax.plot(gia_tien.universe, gia_tien[term].mf, label=term)

    ax.set_title("Biểu đồ giá tiền")
    ax.set_xlabel("Giá (nghìn đồng)")
    ax.set_ylabel("Mức độ")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame_bieudo1)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

bbt1 = Button(root, text="Xem Biểu Đồ Giá", bg="lightblue", command=xem_bd_gia, font=("Arial", 15, "bold"))
bbt1.place(x=800, y=80)

frame_bieudo2 = Frame(root, width=550, height=300, bg="lightgray")
frame_bieudo2.place(x=600, y=450)

def xem_bd_diem():
    for widget in frame_bieudo2.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(5.5, 3), dpi=100)
    ax = fig.add_subplot(111)

    for term in diem_thuong.terms:
        ax.plot(diem_thuong.universe, diem_thuong[term].mf, label=term)

    ax.set_title("Biểu đồ điểm thưởng")
    ax.set_xlabel("Điểm")
    ax.set_ylabel("Mức độ")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame_bieudo2)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

bbt2 = Button(root, text="Xem Biểu Đồ Điểm Thưởng", bg="lightblue", command=xem_bd_diem, font=("Arial", 15, "bold"))
bbt2.place(x=750, y=430)
root.mainloop()