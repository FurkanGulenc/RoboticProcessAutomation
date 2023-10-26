import tkinter
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import requests
import pandas as pd

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

ICON_PATH = ""

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Hotel Process Automation System")
        self.geometry(f'{1100}x{580}')
        self.iconbitmap(ICON_PATH)

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        # 4. sütun için ağırlık 1 olarak ayarlanıyor.
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=3, rowspan=4, sticky="nsew", padx=(20,0))
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="DBT by Hilton Moda", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="Audit Editor")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="Kur Gönderim Ayarları")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))




        # create operations frame

        self.operations_frame = customtkinter.CTkFrame(self, corner_radius=0)

        self.operations_frame.grid(row=0, column=0, padx=(20,0), rowspan=3, sticky="nsew", columnspan=3)

        self.operations_frame.columnconfigure(2, weight=1)

        self.operations_frame.rowconfigure(5, weight=1)

        self.file_button = customtkinter.CTkButton(self.operations_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Dosya Seç", command=self.select_file_and_upload)
        self.file_button.grid(row=1, column=0, sticky="w", padx=20, pady=20, columnspan=4)

        self.entry = customtkinter.CTkEntry(self.operations_frame, placeholder_text="Excel Files *.xlsx", width=550)
        self.entry.grid(row=1, column=0, padx=(20, 20), pady=(0, 0), sticky="e", columnspan=4)

        self.treeview = ttk.Treeview(self.operations_frame, columns=("Info"), show="headings")
        self.treeview.heading("Info", text="Bilgi")
        self.treeview.tag_configure("odd", background="lightgray")
        self.treeview.tag_configure("even", background="white")
        self.treeview.grid(row=2, column=0, padx=(20, 20), pady=(0,20), sticky="nsew", rowspan=4, columnspan=4)
        style = ttk.Style()
        style.configure("Treeview",
                        foreground="black",  # Yazı rengi
                        background="white",  # Arka plan rengi
                        rowheight=25)  # Satır yüksekliği

        style.configure("Treeview.Heading",
                        foreground="white",  # Başlık yazı rengi
                        background="gray",  # Başlık arka plan rengi
                        font=('Arial', 12, 'bold'))  # Başlık fontu


        self.send_button = customtkinter.CTkButton(self.operations_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Gönder")
        self.send_button.grid(row=6, column=3, padx=20, pady=(20,40), sticky="w")

        self.edit_button = customtkinter.CTkButton(self.operations_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Excel Olarak Kaydet", command= self.save_excel)
        self.edit_button.grid(row=6, column=1, padx=20, pady=(20,40))



        # set default valuess
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        self.treeview.bind('<Button-1>', self.on_treeview_click)


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def save_excel(self):
        # Treeview'deki bilgileri al
        items = self.treeview.get_children()
        data = []
        for item in items:
            data.append(self.treeview.item(item, 'values'))

        # Bilgileri pandas DataFrame'ine dönüştür
        df = pd.DataFrame(data, columns=[col for col in self.treeview['columns']])

        # DataFrame'i .xlsx formatında kaydet
        save_path = tkinter.filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            df.to_excel(save_path, index=False)
            tkinter.messagebox.showinfo("Success", "Excel file has been saved!")
        else:
            tkinter.messagebox.showinfo("Cancelled", "Excel file save was cancelled.")

    """def save_excel(self):
        url = "http://127.0.0.1:8003/show-excel"

        # Send GET request to fetch the Excel
        response = requests.post(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Choose a save path for the Excel file
            save_path = tkinter.filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

            # If a save path is chosen, write the content to the file
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                tkinter.messagebox.showinfo("Success", "Excel file has been saved!")
            else:
                tkinter.messagebox.showinfo("Cancelled", "Excel file download was cancelled.")
        else:
            tkinter.messagebox.showerror("Error", f"Failed to download Excel. Error: {response.text}")"""

    def select_file_and_upload(self):
        file_path = tkinter.filedialog.askopenfilename(title="Dosya Seç")
        if file_path:
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, file_path)

        url="http://127.0.0.1:8003/upload-and-process-excel"

        with open(file_path, "rb") as f:
            response = requests.post(url, files={"files": f})

            if response.status_code == 200:
                df = pd.read_json(response.text)
            
                self.treeview['columns'] = list(df.columns)
                for col in df.columns:
                    self.treeview.heading(col, text=col)
                
                # DataFrame'deki her satırı treeview'e ekleyin ve renkleri ayarlayın
                for index, (_, row) in enumerate(df.iterrows()):
                    if index % 2 == 0:
                        tag = "even"
                    else:
                        tag = "odd"
                    self.treeview.insert("", "end", values=tuple(row), tags=(tag,))
                    
            else:
                self.treeview.insert("", "end", values=(f"{file_path} yüklenirken hata oluştu! Hata: {response.text}"))

    def on_treeview_click(self, event):
        # Tıklanan satır ve sütunu bul
        row_id = self.treeview.identify_row(event.y)
        col = self.treeview.identify_column(event.x)
        
        # Eğer tıklanan sütun 'Hesap Kodu' ise
        if col == "#3":  # X, 'Hesap Kodu' sütununun indexi olmalıdır. Örnek: 3. sütun için "#3" olarak ayarlayın.
            x, y, width, height = self.treeview.bbox(row_id, col)
            value = self.treeview.item(row_id, 'values')[3-1]  # X-1, 'Hesap Kodu' sütununun indexidir.

            # Entry widgetini oluştur ve değeri ile doldur
            self.editable_entry = tkinter.Entry(self.treeview, width=width)
            self.editable_entry.place(x=x, y=y, anchor='w', width=width, height=height)
            self.editable_entry.insert(0, value)
            self.editable_entry.focus_set()

            # Entry'den odak kaybolduğunda ya da Enter tuşuna basıldığında on_entry_confirm fonksiyonunu çağır
            self.editable_entry.bind('<FocusOut>', lambda _ : self.on_entry_confirm(row_id))
            self.editable_entry.bind('<Return>', lambda _ : self.on_entry_confirm(row_id))

    def on_entry_confirm(self, row_id):
        # Değişikliği al ve Treeview'ı güncelle
        new_value = self.editable_entry.get()
        values = list(self.treeview.item(row_id, 'values'))
        values[3-1] = new_value  # X-1, 'Hesap Kodu' sütununun indexidir.
        self.treeview.item(row_id, values=values)

        # Entry widgetini kaldır
        self.editable_entry.destroy()
        

    



if __name__ == "__main__":
    app = App()
    app.mainloop()