from pathlib import Path
import tkinter as tk
from tkinter import simpledialog

class SeeSawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("See-Saw Program")
        
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()
        
        self.left_circles = []
        self.right_circles = []
        self.left_boxes = []
        self.right_boxes = []

        self.circles_weight = "5"
        self.boxes_weight = "20"
        self.circles_weightStringVar = tk.StringVar(value=self.circles_weight)
        self.boxes_weightStringVar = tk.StringVar(value=self.boxes_weight)

        self.WeightLeft = 0
        self.WeightRight = 0

        self.ShowWeightSums = False

        self.create_seesaw()
        self.create_buttons()
        self.create_fields()
        
    def create_seesaw(self):

        # Regn ut vekt på begge sider av vippa
        self.WeightLeft = int(self.circles_weight) * len(self.left_circles) + int(self.boxes_weight) * len(self.left_boxes)
        self.WeightRight = int(self.circles_weight) * len(self.right_circles) + int(self.boxes_weight) * len(self.right_boxes)
    
        # Regn ut forhold mellom vektene
        WeightDiff = self.WeightLeft - self.WeightRight
        
        if WeightDiff > 50:
            WeightDiff = 50
        if WeightDiff < -50:
            WeightDiff = -50


        if self.WeightLeft > self.WeightRight:
            WeightDiff = 50
        elif self.WeightLeft < self.WeightRight:
            WeightDiff = -50

        # Seesaw base
        self.canvas.create_line(188, 525 + WeightDiff , 613, 525 + (WeightDiff * -1), width=5)
        

        OffsetPlateu = 0

        if WeightDiff > 0:
            OffsetPlateu = 50
        if WeightDiff < 0:
            OffsetPlateu = -50

        # Lag platå venstre og høyre side
        self.canvas.create_line(190, 525 + OffsetPlateu, 190, 490 + OffsetPlateu, width=5)  # Strek rett opp
        self.canvas.create_line(100, 490 + OffsetPlateu, 280, 490 + OffsetPlateu, width=5)  # Platå

        self.canvas.create_line(610, 525 + OffsetPlateu * -1, 610, 490 + OffsetPlateu * -1, width=5) # Strek rett opp
        self.canvas.create_line(520, 490 + OffsetPlateu * -1, 700, 490 + OffsetPlateu * -1, width=5) # Platå


        # 'Er-lik' eller 'Er ulik' tegn over vippa
        sign = '='
        if self.WeightLeft != self.WeightRight:
            sign = '≠'
        self.canvas.create_text(400, 480, text=sign, fill="black", font=('Helvetica 100'))

        # Seesaw triangle
        self.canvas.create_polygon(350, 550, 450, 550, 400, 525, fill='brown')
        
        # Left side boxes
        for i in range(len(self.left_boxes)):
            y = 470 - (i * 40)
            
            self.canvas.create_rectangle(100, (y - 20) + OffsetPlateu, 175, (y + 20) + OffsetPlateu, fill='green')
            self.canvas.create_text(137, y + OffsetPlateu, text="X", fill="black", font=('Helvetica 15 bold'))
            
        # Left side circles
        for i in range(len(self.left_circles)):

            offset_y = 40 * (i // 2)
            offset_x = 40 * (i % 2)

            y = 470
            self.canvas.create_oval(200 + offset_x, (y - 20 - offset_y) + OffsetPlateu, 240 + offset_x, (y + 20 - offset_y) + OffsetPlateu, fill='yellow')


        # Right side boxes
        for i in range(len(self.right_boxes)):
            y = 470 - i * 40
            self.canvas.create_rectangle(625, (y - 20) + (OffsetPlateu * -1), 700, (y + 20) + (OffsetPlateu * -1), fill='green')
            self.canvas.create_text(662, y  + (OffsetPlateu * -1), text="X", fill="black", font=('Helvetica 15 bold'))
            
        # Right side circles
        for i in range(len(self.right_circles)):

            offset_y = 40 * (i // 2)
            offset_x = 40 * (i % 2)

            y = 470
            self.canvas.create_oval(525 + offset_x, (y - 20 - offset_y)  + (OffsetPlateu * -1), 565 + offset_x, (y + 20 - offset_y)  + (OffsetPlateu * -1), fill='yellow')

        if self.ShowWeightSums:
            self.canvas.create_text(200, 220, text="Vekt venstre", fill="black", font=('Helvetica 15 bold'), justify=tk.CENTER )
            self.canvas.create_text(600, 220, text="Vekt høyre", fill="black", font=('Helvetica 15 bold'), justify=tk.CENTER )
            self.canvas.create_text(200, 240, text=str(self.WeightLeft), fill="black", font=('Helvetica 15 bold'), justify=tk.CENTER )
            self.canvas.create_text(600, 240, text=str(self.WeightRight), fill="black", font=('Helvetica 15 bold'), justify=tk.CENTER )


    def hide_weight_sums(self):
        self.ShowWeightSums = not self.ShowWeightSums
        self.update_seesaw()

    def create_buttons(self):
        add_circle_left_button = tk.Button(self.root, text="Add Circle (Left)", command=lambda: self.add_shape('circle', 'left'))
        add_circle_left_button.pack(side=tk.LEFT)
        
        add_circle_right_button = tk.Button(self.root, text="Add Circle (Right)", command=lambda: self.add_shape('circle', 'right'))
        add_circle_right_button.pack(side=tk.LEFT)
        
        add_box_left_button = tk.Button(self.root, text="Add Box (Left)", command=lambda: self.add_shape('box', 'left'))
        add_box_left_button.pack(side=tk.LEFT)
        
        add_box_right_button = tk.Button(self.root, text="Add Box (Right)", command=lambda: self.add_shape('box', 'right'))
        add_box_right_button.pack(side=tk.LEFT)
        
        remove_button = tk.Button(self.root, text="Remove Selected", command=self.remove_selected)
        remove_button.pack(side=tk.LEFT)
        
        confirm_button = tk.Button(self.root, text="Confirm", command=self.confirm_removal)
        confirm_button.pack(side=tk.LEFT)

        remove_all_button = tk.Button(self.root, text="Slett alt", command=self.remove_all)
        remove_all_button.pack(side=tk.LEFT)

        hide_weight_button = tk.Button(self.root, text="Skjul vekt input", command=self.hide_weight)
        hide_weight_button.pack(side=tk.LEFT)

        hide_weight_sums_button = tk.Button(self.root, text="Vis/skjul vekter", command=self.hide_weight_sums)
        hide_weight_sums_button.pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.toggle_selection)
        self.canvas.bind("<Button-3>", self.toggle_selection)
        self.canvas.bind_all("<Delete>", self.confirm_removal)

        # Dele-knapp
        btn = tk.Button(self.root, text='Del', bd=5, command=self.Del)
        btn.place(x=650, y=50, width=50)
    
    def Del(self):
        DivideBy = simpledialog.askinteger(title="Del på nummer", prompt='Hvilket nummer vil du dele på?', minvalue=1)
        NumRightCircles = len(self.right_circles) - (len(self.right_circles) // DivideBy)
        NumLeftCircles = len(self.left_circles) - (len(self.left_circles) // DivideBy)

        NumRightBoxes = len(self.right_boxes) - (len(self.right_boxes) // DivideBy)
        NumLeftBoxes = len(self.left_boxes) - (len(self.left_boxes) // DivideBy)

        # Marker bokser og sirkler på hver side. Starter øverst, håper jeg
        self.remove_selected()
        
        allItems = [item for item in self.canvas.find_all()]

        allItems.sort(reverse=True)
        MarkedLeftCircles = 0
        MarkedRightCircles = 0
        MarkedLeftBoxes = 0
        MarkedRightBoxes = 0

        for item in allItems:
            
            ItemCoords = self.canvas.coords(item)

            if self.canvas.type(item) == 'oval':
                if ItemCoords[2] < 350:     # Hvis elemtentet er til venstre for senter av vippa
                    if MarkedLeftCircles != NumLeftCircles:
                        self.canvas.itemconfig(item, fill='red')
                        MarkedLeftCircles += 1

                else:
                    if MarkedRightCircles != NumRightCircles:
                        self.canvas.itemconfig(item, fill='red')
                        MarkedRightCircles += 1

            elif self.canvas.type(item) == 'rectangle':
                if ItemCoords[2] < 350:     # Hvis elemtentet er til venstre for senter av vippa
                    if MarkedLeftBoxes != NumLeftBoxes:
                        self.canvas.itemconfig(item, fill='red')
                        MarkedLeftBoxes += 1
                else:
                    if MarkedRightBoxes != NumRightBoxes:
                        self.canvas.itemconfig(item, fill='red')
                        MarkedRightBoxes += 1

    def remove_all(self):
        self.left_boxes.clear()
        self.left_circles.clear()
        self.right_boxes.clear()
        self.right_circles.clear()
        self.update_seesaw()
        return
    
    def hide_weight(self):
        if self.boxWeightEntry.winfo_x() < 0:
            self.boxWeightEntry.place(x=100)
        else:
            self.boxWeightEntry.place(x=-100)
        self.boxWeightEntry.pack_forget()

    def CheckWeights(self, event) -> bool:
        self.circles_weight = self.circleWeightEntry.get()
        self.boxes_weight = self.boxWeightEntry.get()
        self.update_seesaw()
        return True


    def create_fields(self):
        self.circleWeightLabel = tk.Label(self.root, text="Vekt sirkler:", font=('Helvetica 12 bold'))
        self.boxWeightLabel = tk.Label(self.root, text="Vekt bokser:", font=('Helvetica 12 bold'))

        self.circleWeightEntry = tk.Entry(self.root, textvariable = self.circles_weightStringVar, font=('Helvetica 12 bold'), width=10)
        self.boxWeightEntry = tk.Entry(self.root, textvariable = self.boxes_weightStringVar, font=('Helvetica 12 bold'), width=10, validate='key' )
        self.circleWeightEntry.bind('<Return>', self.CheckWeights)
        self.boxWeightEntry.bind('<Return>', self.CheckWeights)

        self.circleWeightLabel.place(x=0, y= 0)
        self.circleWeightEntry.place(x=100, y= 0)

        self.boxWeightLabel.place(x=0, y= 25)
        self.boxWeightEntry.place(x=100, y= 25)

        
    def add_shape(self, shape, side):
        if shape == 'circle':
            if side == 'left':
                self.left_circles.append('x')
            else:
                self.right_circles.append('x')
        else:
            if side == 'left':
                self.left_boxes.append('x')
            else:
                self.right_boxes.append('x')
        self.update_seesaw()
        
    def toggle_selection(self, event):
        x, y = event.x, event.y
        for item in self.canvas.find_all():
            if self.canvas.type(item) == 'oval' or self.canvas.type(item) == 'rectangle':
                if (self.canvas.coords(item)[1] <= y <= self.canvas.coords(item)[3]) and (self.canvas.coords(item)[0] <= x <= self.canvas.coords(item)[2]):
                    if self.canvas.itemcget(item, 'fill') == 'red':
                        self.canvas.itemconfig(item, fill='yellow' if self.canvas.type(item) == 'oval' else 'green')
                    else:
                        self.canvas.itemconfig(item, fill='red')
                    return  # Gå ut hvis vi har trykket på en eksisterende boks
                
        # Hvis vi kommer hit har vi ikke trykket på en boks og vi vil legge til en
        ShapeToAdd = ''
        SideToAdd = ''

        if event.num == 1: # Venstreklikk
            ShapeToAdd = 'circle'
        else:
            ShapeToAdd = 'box'

        if x < 350: #Til venstre for vippa
            SideToAdd = 'left'
        else:
            SideToAdd = 'right'
            
        self.add_shape(ShapeToAdd, SideToAdd)
        
                        
    def remove_selected(self):
        items_to_remove = [item for item in self.canvas.find_all() if self.canvas.itemcget(item, 'fill') == 'red']
        for item in items_to_remove:
            if self.canvas.type(item) == 'oval':
                if item in self.left_circles:
                    self.left_circles.remove(item)
                elif item in self.right_circles:
                    self.right_circles.remove(item)
            elif self.canvas.type(item) == 'rectangle':
                if item in self.left_boxes:
                    self.left_boxes.remove(item)
                elif item in self.right_boxes:
                    self.right_boxes.remove(item)
        self.update_seesaw()
                    
    def confirm_removal(self, event = None):
        items_to_remove = [item for item in self.canvas.find_all() if self.canvas.itemcget(item, 'fill') == 'red']
        for item in items_to_remove:

            ItemCoords = self.canvas.coords(item)

            if self.canvas.type(item) == 'oval':
                if ItemCoords[2] < 350:     # Hvis elemtentet er til venstre for senter av vippa
                    _ = self.left_circles.pop()
                else:
                    _ = self.right_circles.pop()

            elif self.canvas.type(item) == 'rectangle':
                if ItemCoords[2] < 350:     # Hvis elemtentet er til venstre for senter av vippa
                    _ = self.left_boxes.pop()
                else:
                    _ = self.right_boxes.pop()
        self.update_seesaw()
    
    def update_seesaw(self):
        self.canvas.delete("all")
        self.create_seesaw()
        
root = tk.Tk()
app = SeeSawApp(root)
root.mainloop()
