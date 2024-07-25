from tkinter.ttk import Combobox, Separator
from PIL import Image, ImageDraw, ImageFont
import PIL
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog as fd
import numpy as np
from matplotlib import font_manager as fm
from tkinter import messagebox

wmark_text = ""
font_color = ""
width_range = []
height_range = []
im1 = None
im2 = None
im1_size = ()
im2_size = ()
text_check = -1

def open_photo():
    global im1, im2, im1_size
    filepath = fd.askopenfilename()
    if im1 is None:
        im1 = PIL.Image.open(filepath).convert('RGBA')
        im1_size = im1.size
        field0.insert(0, filepath)
    else:
        im2 = PIL.Image.open(filepath).convert('RGBA')
        field3.insert(0, filepath)
    w_list = np.arange(0, im1_size[0], 1)
    h_list = np.arange(0, im1_size[1], 1)
    combo4['values'] = list(w_list)
    combo5['values'] = list(h_list)
    combo2['values'] = list(w_list)
    combo3['values'] = list(h_list)
    if im2 is None:
        im1.show()
    else:
        im2.show()


def do_partial_opacity(img, opacity):
    img_array = np.array(img)
    for i in img_array:
        for n in i:
            if n[3] != 0:
                n[3] = opacity
    trans_img = PIL.Image.fromarray(img_array, 'RGBA')
    return trans_img


def imprint_logo():
    global im1, im2
    opacity = int(slider2.get())
    rotation = int(slider3.get())
    trans_logo = do_partial_opacity(im2, opacity)
    rotated_logo = trans_logo.rotate(rotation, expand=True, fillcolor=(0, 0, 0, 0))
    logo_loc = ()
    if img_check.get() == 0:
        logo_loc = (int(combo4.get()), int(combo5.get()))
    else:
        logo_loc = (int(im1.size[0]/2 - rotated_logo.size[0]/2), int(im1.size[1]/2 - rotated_logo.size[1]/2))
    watermarks_logo = PIL.Image.new('RGBA', im1.size, (255, 255, 255, 0))
    watermarks_logo.paste(rotated_logo, logo_loc)
    combined_image = PIL.Image.alpha_composite(im1, watermarks_logo)
    combined_image.show()
    image_reqs = (field0, field3, slider2, slider3, combo4, combo5)
    for widget in image_reqs:
        if str(type(widget)).find('Scale') > -1:
            widget.set(0)
        elif str(type(widget)).find('Combobox') > -1:
            widget.set('')
        else:
            widget.delete(0, END)
    img_check.set(0)
    combined_path = fd.asksaveasfilename()
    field0.delete(0, END)
    field0.insert(0, combined_path)
    combined_image.save(combined_path)
    im1 = combined_image


def imprint_text():
    global im1
    text = field1.get()
    font_size = int(combo1.get())
    font_color = convert_color(field2.get())
    font_name = combo0.get().replace('-', ' ')
    file = fm.findfont(font_name)
    opacity = int(slider0.get())
    rotation = int(slider1.get())
    font = ImageFont.truetype(file, font_size)
    text_size = font.getsize(text)
    # create image for text
    rgba_list = font_color.copy()
    rgba_list.append(0)
    rgba_transparent = tuple(rgba_list)
    text_image = PIL.Image.new('RGBA', text_size, rgba_transparent)
    text_draw = ImageDraw.Draw(text_image)
    # draw text on image
    rgba_list = font_color.copy()
    rgba_list.append(opacity)
    rgba_translucent = tuple(rgba_list)
    print(f"rgba_translucent is {rgba_translucent}")
    text_draw.text((0, 0), text, rgba_translucent, font=font)
    # rotate text image and fill with transparent color
    rotated_text_image = text_image.rotate(rotation, expand=True, fillcolor=(0, 0, 0, 0))
    rotated_text_image_size = rotated_text_image.size
    text_loc = ()
    if text_check.get() == 0:
        text_loc = (int(combo2.get()), int(combo3.get()))
    else:
        half_im1_width = im1.size[0] / 2
        half_rotated_txt_img_width = rotated_text_image_size[0] / 2
        half_im1_height = im1.size[1] / 2
        half_rotated_txt_img_height = rotated_text_image_size[1] / 2
        print(f"im1_width/2 - rotated_txt_img_width/2 is {half_im1_width - half_rotated_txt_img_width}")
        print(f"im1_height/2 in rotated_txt_img_eight/2 is {half_im1_height - half_rotated_txt_img_height}")
        print(f"text_loc should then be ({half_im1_width - half_rotated_txt_img_width}, {half_im1_height - half_rotated_txt_img_height})")
        text_loc = (int(im1.size[0]/2 - rotated_text_image_size[0]/2), int(im1.size[1]/2 - rotated_text_image_size[1]/2))
    watermarks_image = PIL.Image.new('RGBA', im1_size, (255, 255, 255, 0))
    watermarks_image.paste(rotated_text_image, text_loc)
    combined_image = PIL.Image.alpha_composite(im1, watermarks_image)
    text_reqs = (field0, field1, combo0, combo1, combo2, combo3, slider0, slider1)
    for widget in text_reqs:
        if str(type(widget)).find('Scale') > -1:
            widget.set(0)
        elif str(type(widget)).find('Combobox') > -1:
            widget.set('')
        else:
            widget.delete(0, END)
    text_check.set(0)
    combined_path = fd.asksaveasfilename()
    field0.delete(0, END)
    field0.insert(0, combined_path)
    combined_image.save(combined_path)
    im1 = combined_image
    combined_image.show()


def convert_color(hex_string):
    print(f"hex_string is {hex_string}")
    hex_string = hex_string[1:len(hex_string)]
    color = []
    for indx in range(0, 5, 2):
        color_string = hex_string[indx:indx+2]
        a_color = int(color_string, 16)
        color.append(a_color)
    return color


def form_completed():
    text_pass = 8
    image_pass = 6
    text_tally = 0
    image_tally = 0
    text_reqs = (field0, field1, combo0, combo1, combo2, combo3, slider0, slider1)
    image_reqs = (field0, field3, slider2, slider3, combo4, combo5)
    for widget in text_reqs:
        if str(type(widget)).find('Scale') == -1 and len(widget.get()) > 0:
            text_tally += 1
        elif str(type(widget)).find('Scale') > -1 and widget.get() > 0:
            text_tally += 1
    for widget in image_reqs:
        if str(type(widget)).find('Scale') == -1 and len(widget.get()) > 0:
            image_tally += 1
        elif str(type(widget)).find('Scale') > -1:
            image_tally += 1
    print(f"form_completed()--text_tally is {text_tally}, image_tally is {image_tally}")
    if text_tally == text_pass and not image_tally == image_pass:
        return 1, 0
    elif text_tally == text_pass and image_tally == image_pass:
        return 1, 1
    elif text_tally != text_pass and image_tally == image_pass:
        return 0, 1
    else:
        return 0, 0


def do_watermark():
    result = form_completed()
    if result[0] == 1 and result[1] == 1:
        imprint_text()
        imprint_logo()
    if result[0] == 1 and result[1] == 0:
        imprint_text()
    if result[0] == 0 and result[1] == 1:
        imprint_logo()
    if result[0] == 0 and result[1] == 0:
        messagebox.showinfo("Attention!", "You need to set all parameters for either a text watermark, a logo watermark, or both!")


### GUI Stuff ###

# Import module
from tkinter import *


def choose_color():
    color_code = colorchooser.askcolor(title="Choose Color")
    field2.delete(0, END)
    field2.insert(0, str(color_code[1]))


# Create object
window = Tk()

# Adjust size
window.geometry("650x600")

# Add image file
bg = PhotoImage(file="impress_background.png")

img_check = IntVar()
text_check = IntVar()

label0 = Label(window, text="Watermark Maker", fg="blue", font="Junkyard")
label0.grid(row=1, column=1, columnspan=4, pady=12)
button1 = Button(window, text="Select Main Image", command=open_photo)
button1.grid(row=2, column=2, pady=8)
field0 = Entry(window)
field0.grid(row=2, column=3, pady=8)
label1 = Label(window, text="Imprint Text To Your Image")
label1.grid(row=3, column=1, columnspan=4, pady=8)
label1 = Label(window, text="Text ")
label1.grid(row=4, column=1, pady=8)
field1 = Entry(window)
field1.grid(row=4, column=2, pady=8)
button0 = Button(window, text="Text Color", command=choose_color)
button0.grid(row=4, column=3)
field2 = Entry(window)
field2.grid(row=4, column=4)
label2 = Label(window, text="Font:")
label2.grid(row=5, column=1)
available_fonts = fm.get_font_names()
combo0 = Combobox(window, state="readonly", values=available_fonts)
combo0.grid(row=5, column=2, padx=12)
label3 = Label(window, text="Font Size:")
label3.grid(row=5, column=3)
combo1 = Combobox(window, state="readonly", values=[20, 44, 50, 56, 62, 68, 74, 80, 86, 92, 100, 108, 132, 148, 160], width=8)
combo1.grid(row=5, column=4)
label4 = Label(window, text="Text Opacity")
label4.grid(row=6, column=1)
slider0 = Scale(window, from_=0, to=255, orient=HORIZONTAL)
slider0.grid(row=6, column=2)
label5 = Label(window, text="Text Rotation")
label5.grid(row=6, column=3)
slider1 = Scale(window, from_=0, to=360, orient=HORIZONTAL)
slider1.grid(row=6, column=4)
label7 = Label(window, text="Set Text\nCoordinates")
label7.grid(row=7, column=1)
combo2 = Combobox(window, state="readonly",values=width_range)
combo2.grid(row=7, column=2, padx=12)
combo3 = Combobox(window, state="readonly", values=[])
combo3.grid(row=7, column=3)
check0 = Checkbutton(window, text="Center", variable=text_check, onvalue=1, offvalue=0)
check0.grid(row=7, column=4)
label6 = Label(window, text="Imprint A Logo To Your Image")
label6.grid(row=8, column=1, columnspan=4, pady=8)
button3 = Button(text="Select Photo", command=open_photo)
button3.grid(row=9, column=1, columnspan=2)
field3 = Entry(window)
field3.grid(row=9, column=3, columnspan=2)
label4 = Label(window, text="Image Opacity")
label4.grid(row=10, column=1)
slider2 = Scale(window, from_=0, to=255, orient=HORIZONTAL)
slider2.grid(row=10, column=2)
label5 = Label(window, text="Image Rotation")
label5.grid(row=10, column=3)
slider3 = Scale(window, from_=0, to=360, orient=HORIZONTAL)
slider3.grid(row=10, column=4)
label7 = Label(window, text="Set Image\nCoordinates")
label7.grid(row=11, column=1)
combo4 = Combobox(window, state="readonly", values=width_range)
combo4.grid(row=11, column=2)
combo5 = Combobox(window, state="readonly", values=[])
combo5.grid(row=11, column=3)
check1 = Checkbutton(window, text="Center", variable=img_check, onvalue=1, offvalue=0)
check1.grid(row=11, column=4)
button4 = Button(window, text="Create Watermarked Image", command=do_watermark)
button4.grid(row=12, column=1, columnspan=4, pady=12)

for child in window.winfo_children():
    child.grid_configure(pady=6)

window.mainloop()



