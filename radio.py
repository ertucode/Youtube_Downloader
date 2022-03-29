import tkinter
import customtkinter



class RadioButton:
    def __init__(self,root,id,groupid,sharedVar,boxes=[],idd = "NumText"):
        self.root = root
        self.id = id
        self.groupid = groupid
        self.sharedVar = sharedVar
        self.boxes = boxes
        self.idd = idd
        self.sharedVar[self.groupid].set(100)
        if self.idd == "NumText": self.idd = self.id
        self.radiobutton = customtkinter.CTkRadioButton(master=self.root, text=self.idd, variable=self.sharedVar[self.groupid], 
                                                    command=self.radiobutton_event, value = self.id)
        if self.groupid == 0:
            if self.id == 0:
                self.radiobutton.pack(side = "left", pady=5, padx = 8)
            else:
                self.radiobutton.pack(side = "left", pady=5, padx = 1)
        elif self.groupid == 1:
            # self.radiobutton.pack(anchor="center", side = "left", padx = 10 ,pady= 10)
            # if self.idd == "Single Track":
            #     self.radiobutton.grid(row=1,column=1,pady=10)
            # else: 
            #     self.radiobutton.grid(row=1,column=0,pady=10)

            if self.idd == "Single Track":
                self.radiobutton.pack(side = "left",padx = 10)
            else: 
                self.radiobutton.pack(side = "left",padx = 10)

    def radiobutton_event(self):
        if self.groupid == 0:
            if self.sharedVar[self.groupid].get() == 100 and self.id == 0: return
            if self.sharedVar[self.groupid].get() == self.id: return
                
            for i, boxes in enumerate(self.boxes):
                if i == self.id:
                    for box in boxes:
                        box.packBox()
                else:
                    for box in boxes:
                        box.hide()