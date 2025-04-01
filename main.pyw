import json
import socket
import threading

if __name__ == '__main__':
    import tkinter as tk
    from tkinter import ttk, messagebox, PhotoImage

    deviceList = {}


    def device_list_populate():
        global deviceList
        try:
            with open('Device_list.json', 'r') as f:
                deviceList = json.load(f)
                comboBox_devices.config(values=list(deviceList.keys()))
                comboBox_IPs.config(values=list(deviceList.values()))
                comboBox_devices.current(0)
                comboBox_IPs.current(0)
        except Exception as e:
            print(e)


    def write_device_list():
        global deviceList
        device = comboBox_devices.get()
        ip = comboBox_IPs.get()

        if ip.strip() == '' or device.strip() == '':
            messagebox.showerror('ERROR', 'Device and IP fields cannot be empty!')
        else:
            deviceList.update({device: ip})
            deviceList = dict(sorted(deviceList.items()))
            comboBox_devices.config(values=list(deviceList.keys()))
            comboBox_IPs.config(values=list(deviceList.values()))

        try:
            with open('Device_list.json', 'w', encoding='utf-8') as f:
                json.dump(deviceList, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(e)


    def delete_device():
        confirm_delete = messagebox.askyesno('Confirmation',
                                             'Are you sure you want to delete the selected device?')
        if confirm_delete:
            deviceList.pop(comboBox_devices.get())
            comboBox_devices.config(values=list(deviceList.keys()))
            comboBox_IPs.config(values=list(deviceList.values()))
            comboBox_devices.current(0)
            comboBox_IPs.current(0)
        else:
            pass

        try:
            with open('Device_list.json', 'w', encoding='utf-8') as f:
                json.dump(deviceList, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(e)


    def change_ip_combobox(device):
        comboBox_IPs.current(comboBox_devices.current())


    def change_devices_combobox(ip):
        comboBox_devices.current(comboBox_IPs.current())


    def populate_timeline_list(sock):
        command = 'getAuxTimelines\r'
        sock.sendall(command.encode('utf-8'))
        response = sock.recv(1024)
        print(response)
        label_last_reply.config(text=response)
        response = response.decode('utf-8')[6:]
        json_data = json.loads(response)
        json_data = [item['Name'] for item in json_data['ItemList']]
        comboBox_timeline_list.config(values=json_data)
        comboBox_timeline_list.current(0)


    def get_status(sock):
        command = 'getStatus 1\r'
        sock.sendall(command.encode('UTF-8'))
        response = sock.recv(1024)
        label_last_reply.config(text=response)
        response = response.decode('UTF-8')[11:]
        status = response.split('"')
        temp_list = status[1].split()
        status.pop(1, )
        for x in temp_list:
            status.append(x)
        label_current_show.config(text=status[0])


    def run_selected(sock):
        command = f'run "{comboBox_timeline_list.get()}"\r'
        sock.sendall(command.encode('UTF-8'))
        response = sock.recv(1024)
        label_last_reply.config(text=response)


    def halt_selected(sock):
        command = f'halt "{comboBox_timeline_list.get()}"\r'
        sock.sendall(command.encode('UTF-8'))
        response = sock.recv(1024)
        label_last_reply.config(text=response)


    def kill_selected(sock):
        command = f'kill "{comboBox_timeline_list.get()}"\r'
        sock.sendall(command.encode('UTF-8'))
        response = sock.recv(1024)
        label_last_reply.config(text=response)


    def send_custom_command(sock):
        command = f'{custom_command_string.get()}\r'
        sock.sendall(command.encode('UTF-8'))
        response = sock.recv(1024)
        label_last_reply.config(text=response)


    def load_show(sock):
        command = f'load {load_show_string.get()}\r'
        print(command)
        sock.sendall(command.encode('UTF-8'))
        response = sock.recv(1024)
        label_last_reply.config(text=response)


    def connection(index):
        host = comboBox_IPs.get()
        port = 3039

        with (socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock):
            sock.connect((host, port))
            print(f'connected to server {host}:{port}')
            label_connected_to.config(text=host)

            sock.sendall('authenticate 1\r'.encode('utf-8'))
            print(sock.recv(1024))

            if index == 1:
                populate_timeline_list(sock)
                get_status(sock)
            elif index == 2:
                run_selected(sock)
            elif index == 3:
                halt_selected(sock)
            elif index == 4:
                kill_selected(sock)
            elif index == 5:
                send_custom_command(sock)
            elif index == 6:
                load_show(sock)


    def connection_thread(index):
        conn_thread = threading.Thread(target=connection, args=(index,), daemon=True)
        conn_thread.start()


    def show_info():
        messagebox.showinfo('Info', 'By:Tharinda Lakshan\r@MotionGate-DPR(2025 Mar)')


    root = tk.Tk()
    root.resizable(False, False)
    root.grid_columnconfigure(0, weight=1)
    root.title('WatchOut Controller')
    root.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='logo.png'))
    #root.geometry('320x400')

    buttonStyle = ttk.Style()
    buttonStyle.configure('my.TButton', font=('', 10))

    custom_command_string = tk.StringVar(root)
    load_show_string = tk.StringVar(root)
    info_icon = PhotoImage(file='info.png')
    save_icon = PhotoImage(file='save.png')
    delete_icon = tk.PhotoImage(file='delete.png')
    run_icon = tk.PhotoImage(file='run.png')
    halt_icon = tk.PhotoImage(file='halt.png')
    kill_icon = tk.PhotoImage(file='kill.png')

    main_frame = ttk.LabelFrame(root)
    frame1 = ttk.LabelFrame(main_frame, text='Connection')
    frame2 = ttk.LabelFrame(main_frame, text='Info')
    frame3 = ttk.LabelFrame(main_frame, text='Timelines')
    frame4 = ttk.LabelFrame(main_frame, text='Custom Commands')
    frame5 = ttk.LabelFrame(main_frame, text='Response')

    frame1.grid_columnconfigure(0, weight=1)
    frame1.grid_columnconfigure(1, weight=1)
    frame3.grid_columnconfigure(0, weight=1)
    frame3.grid_columnconfigure(1, weight=1)
    frame3.grid_columnconfigure(2, weight=1)
    frame4.grid_columnconfigure(0, weight=2)
    frame4.grid_columnconfigure(1, weight=1)

    button_info = ttk.Button(root, command=show_info, image=info_icon)
    comboBox_devices = ttk.Combobox(frame1, values=list(deviceList.keys()), state='normal')
    comboBox_IPs = ttk.Combobox(frame1, values=list(deviceList.values()), state='normal')
    button_save_device = ttk.Button(frame1, command=write_device_list, image=save_icon)
    button_delete_device = ttk.Button(frame1, command=delete_device, image=delete_icon)
    button_connect = ttk.Button(frame1, text='Connect', command=lambda: connection_thread(1), style='my.TButton')
    label_connected_to_label = ttk.Label(frame2, text='Connected To : ')
    label_connected_to = ttk.Label(frame2)
    label_current_show_label = ttk.Label(frame2, text='Current Show  : ')
    label_current_show = ttk.Label(frame2, width=35)
    #label_timeline_list = ttk.Label(frame3, text='Timelines : ')
    comboBox_timeline_list = ttk.Combobox(frame3, state='normal')
    button_run_selected = ttk.Button(frame3, command=lambda: connection_thread(2), image=run_icon)
    button_halt_selected = ttk.Button(frame3, command=lambda: connection_thread(3), image=halt_icon)
    button_kill_selected = ttk.Button(frame3, command=lambda: connection_thread(4), image=kill_icon)
    entry_custom_command = ttk.Entry(frame4, textvariable=custom_command_string)
    button_send_command = ttk.Button(frame4, text='Send', command=lambda: connection_thread(5), style='my.TButton')
    entry_load_show = ttk.Entry(frame4, textvariable=load_show_string)
    button_load_show = ttk.Button(frame4, text='Load Show', command=lambda: connection_thread(6), style='my.TButton')
    label_last_reply = tk.Label(frame5, wraplength=280, justify='left', height=7)

    button_info.grid(column=0, row=0, sticky='ew', padx=5, pady=(5, 0))
    main_frame.grid(column=0, row=1, padx=5, pady=(0, 5))
    frame1.grid(column=0, row=1, sticky='ew', padx=5, pady=(0, 5))
    frame2.grid(column=0, row=2, sticky='ew', padx=5, pady=5)
    frame3.grid(column=0, row=3, sticky='ew', padx=5, pady=5)
    frame4.grid(column=0, row=4, sticky='ew', padx=5, pady=5)
    frame5.grid(column=0, row=5, sticky='ew', padx=5, pady=5)
    comboBox_devices.grid(column=0, row=0, sticky='ew', padx=2, pady=2)
    comboBox_IPs.grid(column=1, row=0, sticky='ew', padx=2, pady=2)
    button_save_device.grid(column=0, row=1, sticky='ew', ipady=2, padx=2, pady=2)
    button_delete_device.grid(column=1, row=1, sticky='ew', ipady=2, padx=2, pady=2)
    button_connect.grid(column=0, row=2, sticky='ew', columnspan=2, ipady=10, padx=2, pady=(2, 4))
    label_connected_to_label.grid(column=0, row=0, sticky='ew', padx=2, pady=2)
    label_connected_to.grid(column=1, row=0, sticky='ew', padx=2, pady=2)
    label_current_show_label.grid(column=0, row=1, sticky='ew', padx=2, pady=(2, 4))
    label_current_show.grid(column=1, row=1, sticky='ew', padx=2, pady=(2, 4))
    #label_timeline_list.grid(column=0, row=0, sticky='ew')
    comboBox_timeline_list.grid(column=0, row=0, sticky='ew', columnspan=3, padx=2, pady=2)
    button_run_selected.grid(column=0, row=1, sticky='ew', ipady=3, padx=2, pady=(2, 4))
    button_halt_selected.grid(column=1, row=1, sticky='ew', ipady=3, padx=2, pady=(2, 4))
    button_kill_selected.grid(column=2, row=1, sticky='ew', ipady=3, padx=2, pady=(2, 4))
    entry_custom_command.grid(column=0, row=0, sticky='ew', ipady=5, padx=2, pady=2)
    button_send_command.grid(column=1, row=0, sticky='ew', ipady=4, padx=2, pady=2)
    entry_load_show.grid(column=0, row=1, sticky='ew', ipady=5, padx=2, pady=(2, 4))
    button_load_show.grid(column=1, row=1, sticky='ew', ipady=4, padx=2, pady=(2, 4))
    label_last_reply.grid(column=0, row=0, sticky='ew', padx=2, pady=(2, 4))

    comboBox_devices.bind("<<ComboboxSelected>>", change_ip_combobox)
    comboBox_IPs.bind("<<ComboboxSelected>>", change_devices_combobox)

    device_list_populate()

    root.mainloop()
