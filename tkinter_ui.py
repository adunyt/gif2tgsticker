import os
import tkinter as tk
import tkinterdnd2 as tkd

import convert
import const

root = tkd.TkinterDnD.Tk()
root.withdraw()
root.title('gif2tgsticker')
root.grid_columnconfigure(0, minsize=600)

fps_var = tk.IntVar()
fps_var.set(const.DEFAULT_FPS)

speed_adjust_mode_var = tk.StringVar()
speed_adjust_mode_var.set(const.DEFAULT_SPEED_ADJUST_MODE)

smart_limit_duration_var = tk.StringVar()
smart_limit_duration_var.set(const.DEFAULT_SMART_DURATION_LIMIT)

fallback_pts_var = tk.StringVar()
fallback_pts_var.set(const.DEFAULT_FALLBACK_PTS)

resize_mode_var = tk.StringVar()
resize_mode_var.set(const.DEFAULT_RESIZE_MODE)

crf_var = tk.IntVar()
crf_var.set(const.DEFAULT_CRF)

apng_delay_var = tk.StringVar()
apng_delay_var.set(const.DEFAULT_APNG_DELAY)

option_box = tk.Frame(root)
option_box.grid(row=0, column=0)

row = 0

tk.Label(option_box, text="FPS:")\
  .grid(row=row, column=0)
tk.Entry(option_box, textvariable=fps_var)\
  .grid(row=row, column=1)

row += 1

tk.Label(option_box, text="Resize mode:")\
  .grid(row=row, column=0)

radio_box = tk.Frame(option_box)
radio_box.grid(row=row, column=1)

tk.Radiobutton(radio_box, text='Scale', value='scale', variable=resize_mode_var)\
  .grid(row=0, column=0)
tk.Radiobutton(radio_box, text='Pad', value='pad', variable=resize_mode_var)\
  .grid(row=0, column=1)

row += 1

tk.Label(option_box, text="Smart speed adjust duration limit\n(when video is longer than 3 seconds):")\
  .grid(row=row, column=0)
tk.Entry(option_box, textvariable=smart_limit_duration_var)\
  .grid(row=row, column=1)

row += 1

tk.Label(option_box, text="Smart speed adjust fallback PTS modifier\n(Used when unable to get duration from video)\n(0.5 = 2x speed):")\
  .grid(row=row, column=0)
tk.Entry(option_box, textvariable=fallback_pts_var)\
  .grid(row=row, column=1)

row += 1

tk.Label(option_box, text="CRF Value(0-51, higher means lower quality, -1=unset):")\
  .grid(row=row, column=0)
tk.Entry(option_box, textvariable=crf_var)\
  .grid(row=row, column=1)

row += 1

tk.Label(option_box, text="WebP to APNG delay(lower means faster playback, -1=unset):")\
  .grid(row=row, column=0)
tk.Entry(option_box, textvariable=apng_delay_var)\
  .grid(row=row, column=1)

row += 1

tk.Label(root, text='Drag and drop files here:')\
  .grid(row=row, column=0, padx=10, pady=5)

row += 1

listbox = tk.Listbox(root, width=1, height=20)
listbox.grid(row=row, column=0, padx=5, pady=5, sticky='news')


row += 1

def drop(event):
    if event.data:
        print('Dropped data:\n', event.data)

        if event.widget == listbox:
            # event.data is a list of filenames as one string;
            # if one of these filenames contains whitespace characters
            # it is rather difficult to reliably tell where one filename
            # ends and the next begins; the best bet appears to be
            # to count on tkdnd's and tkinter's internal magic to handle
            # such cases correctly; the following seems to work well
            # at least with Windows and Gtk/X11
            files = listbox.tk.splitlist(event.data)

            for f in files:
                if os.path.exists(f):
                    out_path = convert.process_file(f, fps_var.get(), resize_mode_var.get(), smart_limit_duration_var.get(), fallback_pts_var.get(), crf_var.get(), apng_delay_var.get())
                    listbox.insert(0, out_path)
                    print('Dropped file: "%s"' % f)
                else:
                    print('Not dropping file "%s": file does not exist.' % f)

    return event.action

listbox.drop_target_register(tkd.DND_FILES, tkd.DND_ALL)
listbox.dnd_bind('<<Drop>>', drop)

root.update_idletasks()
root.deiconify()
root.mainloop()
