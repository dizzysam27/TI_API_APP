from urllib.parse import urlparse
from urllib.parse import parse_qs
import customtkinter
import os
from PIL import Image, ImageTk
import Retrieve_Product_Info, Retrieve_Token, Retrieve_Product_Order_Info, Retrieve_Mouser_Info, Retrieve_DigiKey_Info
import tkinter as tk                
from tkinter import font as tkfont  
import pandas as pd
import webbrowser
from CTkTable import *
from CTkMessagebox import CTkMessagebox
import pyperclip


# SETS THE LOCATION OF THE IMAGE FOLDER WHEN THE IMAGES USED WITHIN THE PROGRAM ARE STORED
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")

# THE CLASS APP CREATES THE WINDOW AND THE CONTROLLER FOR SWITCHING BETWEEN FRAMES
class App(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # THIS IS WHERE THE WINDOW IS CREATED WHICH WILL CONTAIN THE FRAMES
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Texas Instruments API")
        self.geometry(f"{800}x{500}")
        
        # HIDE WINDOW TO CHANGE ICON AND BACKGROUND -- PREVENTS WINDOW FLASHING
        self.withdraw()
        
        # CREATE TI ICON FOR WINDOW
        icon_ti = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "icon.ico")))
        self.iconphoto(False, icon_ti)
        
        # THE CONTAINER IS CREATED WHERE ALL THE FRAMES ARE STACKED ON TOP OF EACH OTHER AND WHEN A FRAME IS REQUIRED
        # IT WILL BE RAISED ABOVE THE OTHERS
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # DATA SHARED ACROSS ALL FRAMES, IMPORTANT DICTIONARY 
        self.shared_data = {
                # REFERENCES STORED DATA ARRAY OF WHAT PART NUMBER TO SHOW ON SAVED FRAME
                    "current_number": 0,
                    "number_of_parts": 0,
                    "saved_part_info": [],
                    "saved_part_button": [],
                    "mouser_var": tk.IntVar(),
                    "digikey_var": tk.IntVar()
                }
            
        # CYCLE THROUGH THE AVAILABLE PAGES AND CREATE A LIST OF FRAMES
        self.frames = {}
        for F in (LoginPage, MouserLoginPage, DigiKeyLoginPage, SearchPage, SavedFrame):

            # PUT ALL THE PAGES IN THE SAME LOCATION AND THE ONE ON TOP OF THE STACKING ORDER WILL BE THE ONE THAT IS
            # VISIBLE
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        # DEFINE THE FIRST FRAME AS THE LOGIN FRAME
        self.show_frame("LoginPage")
          
        # SHOW FIRST FRAME WHEN WINDOW IS FULLY SETUP
        self.deiconify()

    # CREATE A FUNCTION WHICH SHOWS THE FRAME BASED UPON THE THE PAGE NAME PASSED INTO THE FUNCTION
    def show_frame(self, page_name):
        
        frame = self.frames[page_name]
        frame.tkraise()
        
    def get_page(self, page_class):
        return self.frames[page_class]

class LoginPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        # ACCESS THE BACKGROUND IMAGE AND PLACE
        image = Image.open((os.path.join(image_path, "bgTI.jpg")))
        self.img_copy= image.copy()
        background_image = ImageTk.PhotoImage(image)
        self.background = customtkinter.CTkLabel(self, image=background_image, text="")
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        self.background.bind('<Configure>', self.Resize)
        
        # ACCESS AND PLACE THE LOGO IMAGE
        logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "ti_logo.png")), size=(400, 120))
        login_frame_logo = customtkinter.CTkLabel(self, text="", image=logo_image, bg_color="white")
        login_frame_logo.place(relx=0.5, rely=0.08, anchor='n')

        # CREATE ENTRY BOXES FOR THE CLIENT ID AND CLIENT SECRET. ALSO CREATE A BUTTON WHICH RETRIEVES AN ACCESS TOKEN WHEN PRESSED
        self.username_entry = customtkinter.CTkEntry(self, width=200, placeholder_text="Client ID", corner_radius=50)
        self.username_entry.place(relx=0.5, rely=0.35, anchor='n')
        self.password_entry = customtkinter.CTkEntry(self, width=200, show="*", placeholder_text="Client Secret", corner_radius=50)
        self.password_entry.place(relx=0.5, rely=0.43, anchor='n')
        login_button = customtkinter.CTkButton(self, text="Login", command = self.login_event, width=200, fg_color="#CC0000",corner_radius=50, hover_color="#80200B")
        login_button.place(relx=0.5, rely=0.55, anchor='n')
        
        self.login_with_mouser = customtkinter.CTkCheckBox(self, text =' Login with Mouser', onvalue=1, offvalue=0, variable = self.controller.shared_data['mouser_var'], text_color='black',fg_color='#004a86',hover_color='#14375e',bg_color='white')
        self.login_with_mouser.place(relx=0.5, rely=0.65, anchor='n')
        self.login_with_mouser = customtkinter.CTkCheckBox(self, text =' Login with Digikey', onvalue=1, offvalue=0, variable = self.controller.shared_data['digikey_var'], text_color='black',fg_color='#CC0000',hover_color='#5e1420', bg_color='white')
        self.login_with_mouser.place(relx=0.5, rely=0.73, anchor='n')

    # THIS FUNCTION CHANGES THE SIZE OF THE BACKGROUND IMAGE ALLOWING THE WINDOW TO BE RESIZED  
    def Resize(self,event):

        new_width = event.width
        new_height = event.height
        image = self.img_copy.resize((new_width, new_height))
        background_image = ImageTk.PhotoImage(image)
        self.background.configure(image = background_image)
    
    # THIS FUNCTION IS CALLED WHEN THE LOGIN BUTTON IS PRESSED. A VALID ACCESS TOKEN WILL BE RETURNED IF CREDENTIALS 
    # ARE VALID. A 0 WILL BE RETRUNED IF THE CREDENTIALS ARE NOT VALID AND THE USER WILL BE PROMPTED TO ENTER THEIR
    # DETAILS AGAIN
    def login_event(self):

        #user = Retrieve_Token.Authenticate(self.username_entry.get(), self.password_entry.get())
        user = Retrieve_Token.Authenticate('l8g9S577exxtpmCSGC56mnBsT2REZN7a', 'CROP7wM4aXq3A6Oz')

        # SETS THE TOKEN VARIABLE AS GLOBAL SO THE TOKEN CAN BE ACCESSED BY ANY CLASS TO MAKE INFORMATION REQUESTS
        global token
        token = user.authenticate_token()

        # IF THE TOKEN IS VALID THEN WE MOVE TO THE PAGEONE
        if token == 0:
            invalid_label = customtkinter.CTkLabel(self.background, text="Invalid Login", width=200, corner_radius=5, bg_color='yellow')
            invalid_label.place(relx = 0.5, rely=0.65, anchor='n')
            
        else:
            
            if self.controller.shared_data['mouser_var'].get() == 1:
                self.controller.show_frame("MouserLoginPage")
                
            elif self.controller.shared_data['digikey_var'].get() == 1:
                self.controller.show_frame("DigiKeyLoginPage")
                
            else:
                self.controller.show_frame("SearchPage")
        


# THIS IS A CLASS WHICH CONTAINS EVERYTHING WITHIN THE LOGIN FRAME
class MouserLoginPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        # ACCESS THE BACKGROUND IMAGE AND PLACE
        image = Image.open((os.path.join(image_path, "bgMOUSER.jpg")))
        self.img_copy= image.copy()
        background_image = ImageTk.PhotoImage(image)
        self.background = customtkinter.CTkLabel(self, image=background_image, text="")
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        self.background.bind('<Configure>', self.Resize)
        
        # CREATE ENTRY BOXES FOR THE CLIENT ID AND CLIENT SECRET. ALSO CREATE A BUTTON WHICH RETRIEVES AN ACCESS TOKEN WHEN PRESSED
        self.username_entry = customtkinter.CTkEntry(self, width=200, placeholder_text="Mouser Client ID",bg_color='#90A0E2', corner_radius=50)
        self.username_entry.place(relx=0.5, rely=0.43, anchor='n')
        login_button = customtkinter.CTkButton(self, text="Login", command = self.login_event, width=200, fg_color="#1E45E5", corner_radius=50, bg_color='#90A0E2')
        login_button.place(relx=0.5, rely=0.55, anchor='n')

    # THIS FUNCTION CHANGES THE SIZE OF THE BACKGROUND IMAGE ALLOWING THE WINDOW TO BE RESIZED  
    def Resize(self,event):

        new_width = event.width
        new_height = event.height
        image = self.img_copy.resize((new_width, new_height))
        background_image = ImageTk.PhotoImage(image)
        self.background.configure(image =  background_image)
    
    # THIS FUNCTION IS CALLED WHEN THE LOGIN BUTTON IS PRESSED. A VALID ACCESS TOKEN WILL BE RETURNED IF CREDENTIALS 
    # ARE VALID. A 0 WILL BE RETRUNED IF THE CREDENTIALS ARE NOT VALID AND THE USER WILL BE PROMPTED TO ENTER THEIR
    # DETAILS AGAIN
    def login_event(self):

        #user = Retrieve_Token.Authenticate(self.username_entry.get(), self.password_entry.get())
        user = Retrieve_Mouser_Info.MouserInfo(self.username_entry.get())

        
        # SETS THE TOKEN VARIABLE AS GLOBAL SO THE TOKEN CAN BE ACCESSED BY ANY CLASS TO MAKE INFORMATION REQUESTS

        # IF THE TOKEN IS VALID THEN WE MOVE TO THE PAGEONE
        if token == 0:
            invalid_label = customtkinter.CTkLabel(self.background, text="Invalid Login", width=200, corner_radius=5, bg_color='yellow')
            invalid_label.place(relx = 0.5, rely=0.65, anchor='n')
            
        else:
            
            if self.controller.shared_data['digikey_var'].get() == 1:
                self.controller.show_frame("DigiKeyLoginPage")
                
            else:
                self.controller.show_frame("SearchPage")
                

# THIS IS A CLASS WHICH CONTAINS EVERYTHING WITHIN THE LOGIN FRAME
class DigiKeyLoginPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        # ACCESS THE BACKGROUND IMAGE AND PLACE
        # # image = Image.open((os.path.join(image_path, "digikey.jpg")))
        # self.img_copy= image.copy()
        self.background = customtkinter.CTkLabel(self, fg_color="#222222", text="")
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        self.background.bind('<Configure>', self.Resize)
        
        # ACCESS AND PLACE THE LOGO IMAGE
        logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "DigiKey_New_Logo.jpg")), size=(400, 120))
        login_frame_logo = customtkinter.CTkLabel(self, text="", image=logo_image)
        login_frame_logo.place(relx=0.5, rely=0.08, anchor='n')

        # CREATE ENTRY BOXES FOR THE CLIENT ID AND CLIENT SECRET. ALSO CREATE A BUTTON WHICH RETRIEVES AN ACCESS TOKEN WHEN PRESSED

        login_button = customtkinter.CTkButton(self, text="Login to Digikey", command = self.login_event, width=200, fg_color="#CC0000", corner_radius=50, bg_color='#222222')
        login_button.place(relx=0.5, rely=0.5, anchor='n')

    # THIS FUNCTION CHANGES THE SIZE OF THE BACKGROUND IMAGE ALLOWING THE WINDOW TO BE RESIZED  
    def Resize(self,event):

        new_width = event.width
        new_height = event.height

    # THIS FUNCTION IS CALLED WHEN THE LOGIN BUTTON IS PRESSED. A VALID ACCESS TOKEN WILL BE RETURNED IF CREDENTIALS 
    # ARE VALID. A 0 WILL BE RETRUNED IF THE CREDENTIALS ARE NOT VALID AND THE USER WILL BE PROMPTED TO ENTER THEIR
    # DETAILS AGAIN
    def login_event(self):

        webbrowser.open('https://api.digikey.com/v1/oauth2/authorize?response_type=code&client_id=ljXW2AAvWc3EbORa841OhnrBTTgF0h22&redirect_uri=https%3A%2F%2Fwww.ti.com%2Fdigikey_callback%2F')

        signed_in_button = customtkinter.CTkButton(self, text="Signed In?", command = self.signed_in_event, width=200, fg_color="#CC0000", corner_radius=50, bg_color='#222222')
        signed_in_button.place(relx=0.5, rely=0.6, anchor='n')

    def signed_in_event(self):

        import pywinauto
        desktop = pywinauto.Desktop(backend="uia")
        window = desktop.windows(title_re=".* Google Chrome$", control_type="Pane")[0]

        wrapper_list = window.descendants(control_type="TabItem")
        for wrapper in wrapper_list:
            wrapper.click_input()
            wrapper_url = window.descendants(title="Address and search bar", control_type="Edit")[0]
            print(wrapper_url.get_value())

            try:
                url = wrapper_url.get_value()
                parsed_url = urlparse(url)
                captured_value = parse_qs(parsed_url.query)['code'][0]
                print(captured_value)
            except:
                pass
        
        
        digikey_client_id = "ljXW2AAvWc3EbORa841OhnrBTTgF0h22"
        digikey_client_secret = "jTECZeL0nkf0a4Tj"

        b = Retrieve_DigiKey_Info.Get_Digikey_Authentication_Token()
        idk = b.Get_Authentication_Token_First(digikey_client_id,digikey_client_secret,captured_value)
        print(idk)

        # a = Retrieve_DigiKey_Info.Get_Digikey_Authentication_Token(digikey_client_id,digikey_client_secret,captured_value)


        # Retrieve_DigiKey_Info.Renew_Digikey_Authentication_Token(digikey_client_id,digikey_client_secret,refreshtoken)


        
                # IF THE TOKEN IS VALID THEN WE MOVE TO THE PAGEONE
        if token == 0:
            invalid_label = customtkinter.CTkLabel(self.background, text="Invalid Login", width=200, corner_radius=5, bg_color='yellow')
            invalid_label.place(relx = 0.5, rely=0.65, anchor='n')
            
        else:
            self.controller.show_frame("SearchPage")


# CLASS WHICH CREATES NAVIGATION BAR, WHICH WILL BE VISIBLE ON EVERY PAGE
# ALSO CREATES BLANK FRAME WHICH WILL DISPLAY DATA BASED ON CHILD CLASSES
# THIS IS MAIN LAYOUT AND CHILD CLASSES WILL CHANGE THE INFORMATION DISPLAYED
class navigation_side_bar(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # IMPORT THE ICONS FOR THE LOGO AND NAVIGATION FRAME BUTTONS
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "b.png")), size=(250, 125))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_light_red.png")))
        self.save_logo = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "save_logo.png")))
        self.export_to_csv_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "csv_icon_red.png")))
        
        # CONFIGURE THE FRAME TO HAVE 1 ROW AND 2 COLUMNS 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # SET UP THE NAVIGATION FRAME WITH A LOGO, SEARCH BUTTON AND CSV BUTTON
        actual_navigation_frame = customtkinter.CTkFrame(self, fg_color="white", corner_radius=0)
        actual_navigation_frame.grid(row=0, column=0, sticky="nsew")
        actual_navigation_frame.grid_rowconfigure(3, weight=1)
        actual_navigation_frame.grid_columnconfigure(0, weight =1)

        self.navigation_frame = customtkinter.CTkScrollableFrame(actual_navigation_frame,fg_color="#CC0000", corner_radius=0,
                                                                 scrollbar_button_color = "#912f2c", scrollbar_fg_color = "transparent")

        self.navigation_frame.grid(row=3, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(100, weight=1)
        self.navigation_frame.grid_columnconfigure(0, weight =1)
        navigation_frame_label = customtkinter.CTkLabel(actual_navigation_frame, text="", image=self.logo_image, bg_color="white",corner_radius=10,compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        navigation_frame_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        search_frame_button = customtkinter.CTkButton(actual_navigation_frame, height=40, border_spacing=10, text="Search",command=self.search_frame_button_event, fg_color="white", text_color="black", corner_radius = 0, 
                                                           image=self.chat_image, anchor="w")
        search_frame_button.grid(row=1, column=0, sticky="nsew")

        export_to_csv_button = customtkinter.CTkButton(actual_navigation_frame, height=40, border_spacing=10, text="Export to CSV",command=self.export_to_csv_button_event, fg_color="white", text_color="black", corner_radius = 0, 
                                                           image=self.export_to_csv_image, anchor="w")
        export_to_csv_button.grid(row=2, column=0, sticky="new")
        
        #CREATE BLANK FRAME WHERE INFORMATION WILL BE DISPLAYED
        self.blank_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white")
        self.blank_frame.grid(row=0, column=1, sticky='nsew')
        self.blank_frame.grid_columnconfigure(0, weight=1)
        self.blank_frame.grid_rowconfigure(1, weight= 1)
    
    # CREATE ARRAYS WHERE THE SAVED PRODUCT INFORMATION IS STORED 
    saved_parts = []
    all_saved_parts_product_info = []
    
    # THIS ARRAY IS USED AS LABELS FOR THE PRODUCT INFORMATION IN THE PRODUCT INFORMAION FRAME
    info_types = ["Id","Description","Generic Product Id","Url","Family Description","Datasheet","Life Cycle Status","Price","Lead Time","Inventory Status","Full Box Quantity","Min Order Quantity","Next Increment Quantity",
                           "Standard Pack Quantity","Ok to Order", "Stop Ship","Obsolete","Lifetime Buy","Change Order Window","Extended Shelf Life","Export Control Classification No.","Hts Code","Military Goods","Pin","Package Type",
                           "Package Group","Industry Package Type","Jedec Code","Package Carrier","Width","Length","Thickness","Pitch","Max Height","Quality Estimator Url","Material Content URL"]
        
    # THIS ARRAY IS USED TO INDEX THE DICTIONARY RETURNED BY THE PRODUCT INFORMATION API. THE STRINGS WITHIN PERFECTLY MATCH WITH THOSE WITHIN THE PRODUCT INFORMATION API DICTIONARY
    info_get = ["Identifier","Description","GenericProductIdentifier","Url","ProductFamilyDescription","DatasheetUrl","LifeCycleStatus","Price","LeadTimeWeeks","InventoryStatus","FullBoxQty","MinOrderQty","NextIncrementQty",
                           "StandardPackQty","OkayToOrder", "StopShip","Obsolete","LifetimeBuy","ChangeOrderWindow","ExtendedShelfLife","ExportControlClassificationNumber","HtsCode","MilitaryGoods","Pin","PackageType",
                           "PackageGroup","IndustryPackageType","JedecCode","PackageCarrier","Width","Length","Thickness","Pitch","MaxHeight","QualityEstimatorUrl","MaterialContentUrl"]
        
    # THIS ARRAY IS USED TO INDEX THE DICTIONARY RETURNED BY THE ORDER INFORMATION API. THE STRINGS WITHIN PERFECTLY MATCH WITH THOSE WITHIN THE ORDER INFORMATION API DICTIONARY
    ordering_info = ["tiPartNumber","genericPartNumber","buyNowUrl","quantity","pricing","futureInventory","description","minimumOrderQuantity","standardPackQuantity","exportControlClassificationNumber","htsCode","pinCount",
                              "packageType","packageCarrier","customReel","lifeCycle"]
    
        
    #FUNCTIONS ASSOCIATED WITH SIDEBAR BUTTONS
        
    def search_frame_button_event(self):
        self.controller.show_frame("SearchPage")
        
    def export_to_csv_button_event(self):
        
        selected_product_info_for_part = []
        selected_product_info_for_all_parts = []
        selected_product_info_columns = []

        for j in range(len(self.saved_parts)):
            selected_product_info_columns = []
            for i in range(len(self.switch_state)):
                if self.switch_state[i] == 1:
                    selected_product_info_columns.append(self.info_get[i])
                    try:
                        selected_product_info_for_part.append(self.all_saved_parts_product_info[j][self.info_get[i]])
                        
                    except KeyError:
                        selected_product_info_for_part.append("Information Not Available")


            selected_product_info_for_all_parts.append(selected_product_info_for_part)
            selected_product_info_for_part = []

        df = pd.DataFrame(selected_product_info_for_all_parts)
        df.columns = selected_product_info_columns
        
        df.to_csv("parts.csv")
        
    def place_saved_part(self):
        
        # PLACE DOWN ALL BUTTONS CREATED
        for i in range(self.controller.shared_data["number_of_parts"]):
            self.controller.shared_data['saved_part_button'][i].grid(row = i, sticky ='snew')
            
            print('h')
        
    
        
class SearchPage(navigation_side_bar):
    
    def __init__(self, parent, controller):
        
        # ARRAY FOR CHECKBOXS
        self.product_information_frame_switches = []
        self.switch_state = [1]*30
    
        # ARRAY TO SAVE CURRENT SEARCH
        self.saved_info = [0]*36
        
        # INHERIT THE SIDE BAR
        super().__init__(parent, controller)
        
        # SET UP THE SEARCH FRAME WITH AN ENTRY BOX, SEARCH BUTTON AND NEW_PART_BUTTON
        search_frame = customtkinter.CTkFrame(self.blank_frame, corner_radius=0, fg_color="white")
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_rowconfigure(1, weight= 1)
        self.search_frame_search_entry = customtkinter.CTkEntry(self.blank_frame, width=300, placeholder_text="Part Number")
        self.search_frame_search_entry.grid(row=1, column=0, padx=5, pady=10, sticky="new")
        self.search_frame_search_button = customtkinter.CTkButton(self.blank_frame, text="Search",command=self.search_event, compound="top", fg_color="#CC0000",  hover_color="#80200B")
        self.search_frame_search_button.grid(row=1, column=1, padx=5, pady=10, sticky='new')
        search_frame_new_part_button = customtkinter.CTkButton(self.blank_frame, text="Save", command= self.new_part, compound="top", fg_color="#CC0000",  hover_color="#80200B")
        search_frame_new_part_button.grid(row=1, column=2, padx=5, pady=10, sticky='new')
        
         # FIRST SCROLLABLE WIDGET: CONTAINS THE PRODUCT INFORMATION
        self.part_product_information_frame = customtkinter.CTkScrollableFrame(self.blank_frame, label_text="Product Information", label_fg_color = "#80200B", label_text_color = 'white')
        self.part_product_information_frame.grid(row=1, columnspan=2, rowspan=2, padx=(5,0), pady = (50, 5), sticky="nsew")
        self.part_product_information_frame.grid_columnconfigure(0, weight =1)
        self.part_product_information_frame.grid_rowconfigure(0, weight=1)
        
        # SECOND SCROLLABLE WIDGET: CONTAINS THE FILTERS WHICH CAN BE USED TO SHOW OR HIDE SPECIFIC INFORMATION ABOUT A PRODUCT
        product_information_frame = customtkinter.CTkScrollableFrame(self.blank_frame, label_text="Filters", label_fg_color = "#80200B", label_text_color = 'white')
        product_information_frame.grid(row=1, column=2, padx=5, rowspan =2, pady = (50, 5), sticky="nsew")
        product_information_frame.grid_columnconfigure(0, weight =1)
        product_information_frame.grid_rowconfigure(3, weight=1)
        
         # SET UP 3 BUTTONS WHICH LINK TO URLS 
         # FIRST BUTTON OPENS LINK TO VIEW WEBSITE, SECOND BUTTON OPENS DATASHEET AND THIRD BUTTON OPENS QUALITY ESTIMATOR URL
        search_frame_tiwebsite_button = customtkinter.CTkButton(self.blank_frame, text="View on TI.com",command=self.tiwebsite_event, compound="top", fg_color="#CC0000", hover_color="#80200B")
        search_frame_tiwebsite_button.grid(row=3, column=0, padx=5, pady=5, sticky='new')
        search_frame_datasheet_button = customtkinter.CTkButton(self.blank_frame, text="Datasheet",command=self.datasheet_event, compound="top", fg_color="#CC0000", hover_color="#80200B")
        search_frame_datasheet_button.grid(row=3, column=1, padx=5, pady=5, sticky='new')
        quality_estimator_button = customtkinter.CTkButton(self.blank_frame, text="Quality Estimator",command=self.quailty_estimator_event, compound="top", fg_color="#CC0000", hover_color="#80200B")
        quality_estimator_button.grid(row=3, column =2, padx=5, pady=5, sticky='new' )
       
        self.part_description = customtkinter.CTkLabel(self.part_product_information_frame,  text ='', text_color = "#CC0000")
        self.part_description.grid(row=0, pady = (0, 10))
        
        # MASTER CHECKBOX WHICH TURNS ALL CHECKBOXS ON OR OFF
        self.master_var= tk.IntVar()
        self.switch_master = customtkinter.CTkCheckBox(master=product_information_frame, text ='All', command= self.enable_all_filters, variable=self.master_var, onvalue=1, offvalue=0, fg_color="#CC0000", hover_color="#80200B")
        self.switch_master.grid(row=0, column =0, sticky='n', padx = (50,0), pady=(0,20))
        self.switch_master.select()
        
        
        # SET UP 30 SWITCHES, AS THAT IS HOW MUCH DATA IS SHOWN
        # ITERATION VARIABLE IS USED AS POSITION INDEX IN TABLE
        iteration = 0
        self.not_checkboxes_list=["Url", "Datasheet", "Quality Estimator Url", "Id", "Description", "Material Content URL"]
        for i in range(len(navigation_side_bar.info_types)):
            
            # IGNORES URLs
            if navigation_side_bar.info_types[i] in self.not_checkboxes_list:
                pass
            else:
                # SET UP PRODUCT INFORMATION CHECKBOXES TO CONTROL WHICH DATA IS DISPLAYED
                switch = customtkinter.CTkCheckBox(master=product_information_frame, text=self.info_types[i], command=lambda f=iteration: self.switchable_button_press(f), fg_color="#CC0000", hover_color="#80200B")
                switch.select()
                switch.grid(row=iteration+1, column=0, pady=(0, 20),sticky="w")
                self.product_information_frame_switches.append(switch)
                
                iteration +=1
                
    def make_table(self, rows):
        try:
            self.info_table.grid_forget()
        except:
            pass
        
        info_table = CTkTable(master=self.part_product_information_frame, row = rows , column=2 ,values = '', wraplength = '200', command = self.command, corner_radius=0)

        return info_table
    
    def command(self, position):
        
        try:
            self.info_table.deselect(self.pos_row, self.pos_col)
        except:
            pass
        # GET ROW AND COLUMN OF SELECTED CELL
        self.pos_row = position['row']
        self.pos_col = position['column']
        
        # GET VALUE IN CELL (HAVE TO DO LIKE THIS OTHERWISE RETURNS WHOLE TABLE FOR SOME CELLS)
        self.info_table.select(self.pos_row, self.pos_col)
        cell_list = self.info_table.get()
        
        pyperclip.copy(cell_list[self.pos_row][self.pos_col])
        # CTkMessagebox(master= self, title = None, message = "Copied to clipboard", width = 10, height =10)
        tk.messagebox.showinfo(title=None, message="Copied to clipboard")
        
    # FUNCTION FOR WHEN THE SEARCH BUTTON IS PRESSED   
    def search_event(self):
        
        # RETRIEVE THE PRODUCT INFO FROM THE PRODUCT INFO API
        self.part = Retrieve_Product_Info.Info(self.search_frame_search_entry.get(), token)
        
        # STORE INFO IN ARRAY CALLED_INFO
        self.called_info= self.part.call_info()
        self.switch_master.select()

        # DISPLAYS NAME OF PRODUCT AS TITLE OF SCROLLABLE FRAME
        self.part_product_information_frame.configure(label_text = self.called_info[navigation_side_bar.info_get[0]])
        # DISPLAYS DISCRIPTION OF PRODUCT
        self.part_description.configure(text = self.called_info[navigation_side_bar.info_get[1]])
        
        # CHECKS TO SEE IF PRODUCT INFORMATION IS AVAILABLE ABOUT THE PART AND DISPLAYS THE DATA ACCORDINGLY
        count = 0
        self.info_table=self.make_table(30)
        self.info_table.grid(row = 1, column = 0, sticky='nsew')
        for i in range(len(navigation_side_bar.info_types)):
            
            # DISPLAY TITLE OF DATA 
            info_text = navigation_side_bar.info_types[i]
            # IGNORES URLs AS THEY HAVE SEPERATE BUTTON
            if info_text in self.not_checkboxes_list:
                pass
            
            # DISPLAYS DATA IN TABLE
            else:
                # SELECTS FILTER SWITCHES
                self.product_information_frame_switches[count].select()
                self.switch_state[count]=1
                

                # TRIES FINDING INFO IN DICTIONARY
                try:
                    self.info_table.insert(count, 0, info_text, text_color = 'black')
                    textDisplay = str( self.called_info[navigation_side_bar.info_get[i]] )
                    self.info_table.insert(count, 1, textDisplay, text_color = 'black')
                    
                # IF NO INFO IN DICTIONARY, PRINT N/A IN DIFFERENT COLOUR
                except KeyError:
                    # DOESN'T WORK ATM AS DOESN'T SHOW NO INFORMATION
                    # try:
                    #         gpns = Retrieve_Product_Order_Info.Search_by_GPN(token, self.search_frame_search_entry.get())
                    #         print(gpns.find_all_opns_from_gpn())
                    
                        self.info_table.insert(count, 0, info_text, text_color = '#ad9d05')
                        textNothing = "Information not available"
                        self.info_table.insert(count, 1, textNothing, text_color = '#ad9d05')
                count +=1
        
    # SETS ALL THE FILTERS TO ACTIVE. DISPLAY ALL DATA WHEN THE ALL CHECKBOX IS SELECTED
    def enable_all_filters(self):
        
        if (self.master_var.get() == 1):
            self.info_table=self.make_table(30)
            self.info_table.grid(row = 1, column = 0, sticky='nsew')
            # CHECKS TO SEE IF PRODUCT INFORMATION IS AVAILABLE ABOUT THE PART AND DISPLAYS THE DATA ACCORDINGLY
            count = 0
            for i in range(len(navigation_side_bar.info_types)):
                
                # DISPLAY TITLE OF DATA 
                info_text = navigation_side_bar.info_types[i]
                # IGNORES URLs AS THEY HAVE SEPERATE BUTTON
                if info_text in self.not_checkboxes_list:
                    pass
                
                # DISPLAYS DATA IN TABLE
                else:
                    # SELECTS FILTER SWITCHES
                    self.product_information_frame_switches[count].select()
                    self.switch_state[count]=1
                    
                    # TRIES FINDING INFO IN DICTIONARY
                    try:
                        self.info_table.insert(count, 0, info_text, text_color = 'black')
                        textDisplay = str( self.called_info[navigation_side_bar.info_get[i]] )
                        self.info_table.insert(count, 1, textDisplay, text_color = 'black')
                        
                    # IF NO INFO IN DICTIONARY, PRINT N/A IN DIFFERENT COLOUR
                    except KeyError:
                            self.info_table.insert(count, 0, info_text, text_color = '#ad9d05')
                            textNothing = "Information not available"
                            self.info_table.insert(count,1, textNothing, text_color = '#ad9d05')
                    count +=1
    
        elif (self.master_var.get()==0):
            self.info_table=self.make_table(0)
            self.info_table.grid(row = 1, column = 0, sticky='nsew')
            for i in range(30):
                self.product_information_frame_switches[i].deselect()
                self.switch_state[i]=0
                
                
    # DISPLAYS INFORMATION IF THE CORRESPONDING CHECKBOX IS ENABLED
    def switchable_button_press(self, number):
        
        # XOR TO TOGGLE BETWEEN 1 OR 0
        self.switch_state[number] ^= 1
        buttons_on=0
       
        for i in range(len(self.switch_state)):
            if self.switch_state[i]==1:
                buttons_on+=1
        
        position = 0
        tick_box=0
        try:
            self.info_table.delete_columns(0, 1)
        except:
            pass
        self.info_table=self.make_table(buttons_on)
        self.info_table.grid(row = 1, column = 0, sticky='new')
        for i in range(len(navigation_side_bar.info_types)):
            # TITLE OF DATA 
            info_text = navigation_side_bar.info_types[i]
            # IGNORES URLs AND DESCRIPTIONS
            if info_text in self.not_checkboxes_list:
                pass
            
            else:
                if self.switch_state[tick_box] == 1:
                    try:
                        self.info_table.insert(position, 0, info_text, text_color = 'black')
                        textDisplay = str(self.called_info[navigation_side_bar.info_get[i]])
                        self.info_table.insert(position, 1, textDisplay, text_color = 'black')
                    except KeyError:
                        self.info_table.insert(position, 0, info_text, text_color = '#ad9d05')
                        textNothing = "Information not available"
                        self.info_table.insert(position,1, textNothing, text_color = '#ad9d05')
                    position+=1
                tick_box+=1
      
    # FUNCTION IS CALLED EVERY TIME THE SAVE BUTTON IS PRESSED
    def new_part(self):
        
        # STORE INFO IN DATA ARRAY
        self.controller.shared_data['saved_part_info'].append(self.called_info)
        
        # CREATE A LOCAL VARIABLE FOR THIS FUNCTION
        # MISLEADING AS STARTS FROM ZERO
        number_of_parts_saved = self.controller.shared_data["number_of_parts"]
        
        # CREATE NEW BUTTON OF SAVED PART
        part_button = customtkinter.CTkButton(self.navigation_frame, height=40, border_spacing=10, text = self.called_info["Identifier"], fg_color ="transparent", command = lambda n=number_of_parts_saved: self.navigation_frame_saved_part_button_event(n), text_color='white', image=self.save_logo, corner_radius=0, hover_color="#80200B")
        self.controller.shared_data['saved_part_button'].append(part_button)
        
        # INCREASE NUMBER OF SAVED PARTS AND TEMP VARIABLE BY ONE
        self.controller.shared_data["number_of_parts"] = (number_of_parts_saved+1)
        number_of_parts_saved +=1
        
        self.place_saved_part()
        # for i in range(self.controller.shared_data["number_of_parts"]):
        #     self.controller.shared_data['saved_part_button'][i].grid(row = i, sticky ='new')
        
    def navigation_frame_saved_part_button_event(self, number):
        
        # SETS SHARED VARIABLE TO CURRENT PART NUMBER, THEN CALL NEXT FRAME
        self.controller.shared_data["current_number"] = number
        self.controller.show_frame("SavedFrame")
        
        # CALL FUNCTION IN SAVED FRAME, WHICH DISPLAYS SAVED DATA IMMEDIATELY ---IMPORTANT
        save_page = self.controller.get_page("SavedFrame")
        save_page.display_saved_info()
        
    def tiwebsite_event(self):
        webbrowser.open(self.called_info['Url'])
        
        gpns = Retrieve_Product_Order_Info.Search_by_GPN(token, self.search_frame_search_entry.get())
        #print(gpns.find_all_opns_from_gpn())
                
    def datasheet_event(self):
        webbrowser.open(self.called_info['DatasheetUrl'])
        
    def quailty_estimator_event(self):
        webbrowser.open(self.called_info['QualityEstimatorUrl'])
        
    def material_content_event(self):
        webbrowser.open(self.called_info['MaterialContentUrl'])

class SavedFrame(navigation_side_bar):
    
    def __init__(self, parent, controller):
        
         # INHERIT THE SIDE BAR
        super().__init__(parent, controller)
        
        self.part_product_information_frame = customtkinter.CTkScrollableFrame(self.blank_frame, label_text='Product Information', label_fg_color = "#80200B", label_text_color = 'white', scrollbar_button_color = "#912f2c")
        self.part_product_information_frame.grid(row=1, columnspan=2, rowspan=2, padx=(5,5), pady = (50, 5), sticky="nsew")
        
        # SCROLLABLE FRAME EXPANDS WHEN WINDOW EXPANDS
        self.part_product_information_frame.rowconfigure(0, weight =1)
        self.part_product_information_frame.columnconfigure(0, weight =1)
        
        self.part_description = customtkinter.CTkLabel(self.part_product_information_frame, text = '',  text_color = "#CC0000")
        self.part_description.grid(row=0, pady = (0, 10))
        
        self.not_checkboxes_list=["Url", "Datasheet", "Quality Estimator Url", "Id", "Description", "Material Content URL"]
        
    def make_table(self, rows):
        try:
            self.saved_info_table.grid_forget()
        except:
            pass
        
        info_table = CTkTable(master=self.part_product_information_frame, row = rows , column=2 ,values = '', wraplength = '200', corner_radius=0, command = self.command)

        return info_table
        
    def display_saved_info(self):
        
        
        count = 0
    
        self.saved_info_table=self.make_table(30)
        self.saved_info_table.grid(row = 1, column = 0,  sticky='new')
        
        current_info = self.controller.shared_data["saved_part_info"][self.controller.shared_data["current_number"]]
        
        # DISPLAYS NAME OF PRODUCT AS TITLE OF SCROLLABLE FRAME
        self.part_product_information_frame.configure(label_text = current_info[navigation_side_bar.info_get[0]])
        # DISPLAYS DISCRIPTION OF PRODUCT
        self.part_description.configure(text = current_info[navigation_side_bar.info_get[1]])
        
        for i in range(len(current_info)):
            
            # DISPLAY TITLE OF DATA 
            info_text = navigation_side_bar.info_types[i]

            # IGNORES URLs AS THEY HAVE SEPERATE BUTTON
            if info_text in self.not_checkboxes_list:
                pass
            
            # DISPLAYS DATA IN TABLE
            else:

                # TRIES FINDING INFO IN DICTIONARY
                try:
                    self.saved_info_table.insert(count, 0, info_text, text_color = 'black')
                    textDisplay = str( current_info[navigation_side_bar.info_get[i]] )
                    self.saved_info_table.insert(count, 1, textDisplay, text_color = 'black')
                    
                # IF NO INFO IN DICTIONARY, PRINT N/A IN DIFFERENT COLOUR
                except KeyError:
                    
                        self.saved_info_table.insert(count, 0, info_text, text_color = '#ad9d05')
                        textNothing = "Information not available"
                        self.saved_info_table.insert(count, 1, textNothing, text_color = '#ad9d05')
                count +=1
            
        self.place_saved_part()
    
    def command(self, position):
        
        try:
            self.saved_info_table.deselect(self.pos_row, self.pos_col)
        except:
            pass
        # GET ROW AND COLUMN OF SELECTED CELL
        self.pos_row = position['row']
        self.pos_col = position['column']
        
        # GET VALUE IN CELL (HAVE TO DO LIKE THIS OTHERWISE RETURNS WHOLE TABLE FOR SOME CELLS)
        self.saved_info_table.select(self.pos_row, self.pos_col)
        cell_list = self.saved_info_table.get()
        
        self.cell_info = cell_list[self.pos_row][self.pos_col]
        
        # COPY TO CLIPBOARD AND DISPLAY MESSAGE
        pyperclip.copy(cell_list[self.pos_row][self.pos_col])
        tk.messagebox.showinfo(title=None, message="Copied to clipboard")
        
# RUN THE APP
if __name__ == "__main__":
    app = App()
    app.mainloop()
    
        