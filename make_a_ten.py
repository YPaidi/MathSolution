import tkinter as tk
from tkinter import ttk, messagebox

class MakeATenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Learn Subtraction: Make a Ten Strategy!")
        self.root.geometry("900x600") 
        self.root.configure(bg="#f0f8ff") 

        self.is_animating = False

        # --- Top Controls Frame ---
        self.ctrl_frame = tk.Frame(self.root, bg="#f0f8ff", pady=10)
        self.ctrl_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(self.ctrl_frame, text="Start Number:", font=("Arial", 14), bg="#f0f8ff").pack(side=tk.LEFT, padx=(20, 5))
        self.entry_minuend = tk.Entry(self.ctrl_frame, font=("Arial", 14), width=4, justify="center")
        self.entry_minuend.insert(0, "39") 
        self.entry_minuend.pack(side=tk.LEFT)

        tk.Label(self.ctrl_frame, text="−", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(side=tk.LEFT, padx=10)

        tk.Label(self.ctrl_frame, text="Subtract:", font=("Arial", 14), bg="#f0f8ff").pack(side=tk.LEFT, padx=5)
        self.entry_subtrahend = tk.Entry(self.ctrl_frame, font=("Arial", 14), width=4, justify="center")
        self.entry_subtrahend.insert(0, "17") 
        self.entry_subtrahend.pack(side=tk.LEFT)

        self.btn_start = tk.Button(self.ctrl_frame, text="Start Animation", font=("Arial", 12, "bold"), bg="#32cd32", fg="white", command=self.start_animation)
        self.btn_start.pack(side=tk.LEFT, padx=20)

        self.btn_reset = tk.Button(self.ctrl_frame, text="Reset", font=("Arial", 12, "bold"), bg="#ff6347", fg="white", command=self.reset_ui)
        self.btn_reset.pack(side=tk.LEFT, padx=5)

        tk.Label(self.ctrl_frame, text="Speed:", font=("Arial", 12), bg="#f0f8ff").pack(side=tk.LEFT, padx=(20, 5))
        self.slider_speed = ttk.Scale(self.ctrl_frame, from_=1, to=10, orient=tk.HORIZONTAL, value=5)
        self.slider_speed.pack(side=tk.LEFT)

        # --- Main Canvas (Smart Whiteboard) ---
        self.canvas = tk.Canvas(self.root, width=860, height=480, bg="white", highlightthickness=2, highlightbackground="#ccc")
        self.canvas.pack(pady=10)

        # Narrator Text
        self.narrator = self.canvas.create_text(430, 60, text="", font=("Arial", 18, "bold"), fill="#333", width=800, justify=tk.CENTER)
        
        # Final Answer Text
        self.final_answer_text = self.canvas.create_text(430, 420, text="", font=("Arial", 32, "bold"), fill="#2e8b57")

        self.reset_ui()

    def update_narrator(self, text):
        if self.is_animating:
            self.canvas.itemconfig(self.narrator, text=text)

    def reset_ui(self):
        if self.is_animating: return 
        self.canvas.delete("all")
        self.narrator = self.canvas.create_text(430, 60, text="", font=("Arial", 18, "bold"), fill="#333", width=800, justify=tk.CENTER)
        self.final_answer_text = self.canvas.create_text(430, 420, text="", font=("Arial", 32, "bold"), fill="#2e8b57")

    def start_animation(self):
        if self.is_animating: return

        try:
            self.m = int(self.entry_minuend.get())
            self.s = int(self.entry_subtrahend.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid whole numbers.")
            return

        if self.s >= self.m:
            messagebox.showerror("Math Error", "The Start Number must be larger than the Subtract number.")
            return

        self.next_ten = ((self.s // 10) + 1) * 10
        if self.next_ten >= self.m:
            messagebox.showinfo("Notice", "This problem doesn't cross a ten boundary! Try 39 - 17.")
            return

        jump_1 = self.next_ten - self.s
        jump_2 = self.m - self.next_ten
        answer = jump_1 + jump_2

        self.is_animating = True
        self.reset_ui()

        self.draw_number_line(self.s, self.m)
        self.init_canvas_items()
        
        speed_val = self.slider_speed.get()
        hop_delay = int(10 + (11 - speed_val) * 8)     
        frames_per_hop = int(15 + (11 - speed_val) * 8) 
        
        txt_step1 = f"Step 1: Start at {self.s} and jump forward by {jump_1} to reach the next ten ({self.next_ten})."
        
        self.root.after(500, lambda: [
            self.update_narrator(txt_step1),
            self.big_hop_and_draw_arc(
                self.s, self.next_ten, self.arc_orange, self.arrow_orange, self.lbl_orange, self.rect_orange, f"+{jump_1}", "#ff8c00", frames_per_hop, hop_delay,
                on_complete=lambda: [
                    
                    self.root.after(1500, lambda: [
                        # Using the shorter sentence option!
                        self.update_narrator(f"Step 2: It's a jump of {jump_2} from {self.next_ten} to {self.m}."),
                        self.big_hop_and_draw_arc(
                            self.next_ten, self.m, self.arc_blue, self.arrow_blue, self.lbl_blue, self.rect_blue, f"+{jump_2}", "#1e90ff", frames_per_hop, hop_delay,
                            on_complete=lambda: self.root.after(2000, lambda: self.handle_addition_phase(jump_2, jump_1, answer, hop_delay, frames_per_hop))
                        )
                    ])
                ]
            )
        ])

    def handle_addition_phase(self, blue_jump, orange_jump, answer, hop_delay, frames_per_hop):
        next_ten_for_blue = ((blue_jump // 10) + 1) * 10
        dist_to_ten = next_ten_for_blue - blue_jump

        if dist_to_ten < orange_jump and (blue_jump % 10 != 0):
            rem = orange_jump - dist_to_ten
            split_1 = self.next_ten - dist_to_ten 
            
            txt_step3 = f"Step 3: Start at {blue_jump} and add {dist_to_ten} to make a ten ({next_ten_for_blue})."
            txt_step4 = f"Step 4: Continue counting by adding the rest {rem}."
            
            self.update_narrator("Now, watch how the blue line eats the orange line...")
            
            self.morph_arcs(
                self.next_ten, split_1, f"+{next_ten_for_blue}", f"+{rem}", frames_per_hop, hop_delay,
                on_complete=lambda: [
                    self.update_narrator(txt_step3),
                    
                    self.root.after(3000, lambda: [
                        self.morph_arcs(
                            split_1, self.s, f"+{answer}", "", frames_per_hop, hop_delay,
                            on_complete=lambda: [
                                self.update_narrator(txt_step4),
                                self.root.after(2500, lambda: self.show_final_answer(answer))
                            ]
                        )
                    ])
                ]
            )
        else:
            txt_combine = f"Step 3: Combine the jumps directly to get {answer}."
            
            self.update_narrator("Now, watch how the blue line eats the orange line...")
            
            self.morph_arcs(
                self.next_ten, self.s, f"+{answer}", "", frames_per_hop, hop_delay,
                on_complete=lambda: [
                    self.update_narrator(txt_combine),
                    self.root.after(2500, lambda: self.show_final_answer(answer))
                ]
            )

    def show_final_answer(self, answer):
        self.canvas.itemconfig(self.final_answer_text, text=f"Therefore: {self.m} − {self.s} = {answer}")
        self.canvas.itemconfig(self.rabbit, text="🐰🎉")
        self.is_animating = False

    def get_x_coord(self, val):
        return 50 + (val - self.start_val) * self.pixels_per_unit

    def draw_number_line(self, s, m):
        self.start_val = s - 1
        self.end_val = m + 1
        total_units = self.end_val - self.start_val
        self.pixels_per_unit = (860 - 100) / max(total_units, 1) 
        self.base_y = 280 

        self.canvas.create_line(30, self.base_y, 830, self.base_y, width=4, fill="black", arrow=tk.BOTH)

        for i in range(self.start_val, self.end_val + 1):
            x = self.get_x_coord(i)
            is_ten = (i % 10 == 0)
            tick_length = 15 if is_ten else 8
            font_weight = "bold" if is_ten else "normal"
            color = "#cc0000" if is_ten else "black"

            self.canvas.create_line(x, self.base_y - tick_length, x, self.base_y + tick_length, width=2)
            
            if total_units > 40:
                if is_ten or i == s or i == m:
                    self.canvas.create_text(x, self.base_y + 25, text=str(i), font=("Arial", 12, font_weight), fill=color)
            else:
                self.canvas.create_text(x, self.base_y + 25, text=str(i), font=("Arial", 14, font_weight), fill=color)

    def init_canvas_items(self):
        start_x = self.get_x_coord(self.s)
        self.rabbit = self.canvas.create_text(start_x, self.base_y - 15, text="🐰", font=("Arial", 36), fill="#FF1493")

        self.arc_orange = self.canvas.create_arc(0,0,0,0, start=180, extent=0, style=tk.ARC, outline="#ff8c00", width=4, state=tk.HIDDEN)
        self.arrow_orange = self.canvas.create_polygon(0,0,0,0,0,0, fill="#ff8c00", state=tk.HIDDEN)
        self.rect_orange = self.canvas.create_rectangle(0,0,0,0, fill="#e0b0ff", outline="black", state=tk.HIDDEN)
        self.lbl_orange = self.canvas.create_text(0,0, text="", font=("Arial", 16, "bold"), fill="black", state=tk.HIDDEN)

        self.arc_blue = self.canvas.create_arc(0,0,0,0, start=180, extent=0, style=tk.ARC, outline="#1e90ff", width=4, state=tk.HIDDEN)
        self.arrow_blue = self.canvas.create_polygon(0,0,0,0,0,0, fill="#1e90ff", state=tk.HIDDEN)
        self.rect_blue = self.canvas.create_rectangle(0,0,0,0, fill="#add8e6", outline="black", state=tk.HIDDEN)
        self.lbl_blue = self.canvas.create_text(0,0, text="", font=("Arial", 16, "bold"), fill="black", state=tk.HIDDEN)

    def big_hop_and_draw_arc(self, start_val, end_val, arc_id, arrow_id, lbl_id, rect_id, final_label, color, frames_per_hop, hop_delay, on_complete):
        x0 = self.get_x_coord(start_val)
        x1 = self.get_x_coord(end_val)
        h = min((x1 - x0) * 0.5, 130)
        
        self.canvas.coords(arc_id, x0, self.base_y - h, x1, self.base_y + h)
        self.canvas.itemconfig(arc_id, state=tk.NORMAL, extent=0)

        def frame(f):
            if not self.is_animating: return
            progress = f / frames_per_hop
            
            x = x0 + (x1 - x0) * progress
            y = self.base_y - 15 - h * (1 - (progress * 2 - 1)**2)
            self.canvas.coords(self.rabbit, x, y)
            
            current_extent = -180 * progress
            self.canvas.itemconfig(arc_id, extent=current_extent)
            
            if f < frames_per_hop:
                self.root.after(hop_delay, lambda: frame(f + 1))
            else:
                self.canvas.itemconfig(arc_id, extent=-180)
                
                points = [x1, self.base_y, x1 - 12, self.base_y - 8, x1 - 12, self.base_y + 8]
                self.canvas.coords(arrow_id, *points)
                self.canvas.itemconfig(arrow_id, state=tk.NORMAL)
                
                lbl_x = (x0 + x1)/2
                lbl_y = self.base_y - h - 15
                self.canvas.coords(lbl_id, lbl_x, lbl_y)
                self.canvas.itemconfig(lbl_id, text=final_label, state=tk.NORMAL)
                
                bbox = self.canvas.bbox(lbl_id)
                pad = 4
                self.canvas.coords(rect_id, bbox[0]-pad, bbox[1]-pad, bbox[2]+pad, bbox[3]+pad)
                self.canvas.itemconfig(rect_id, state=tk.NORMAL)
                self.canvas.tag_lower(rect_id, lbl_id) 
                
                self.canvas.tag_raise(self.rabbit)
                on_complete()

        frame(1)

    def morph_arcs(self, start_split, end_split, target_blue_label, target_orange_label, frames, delay_ms, on_complete):
        current_frame = 0
        x_s = self.get_x_coord(self.s)
        x_m = self.get_x_coord(self.m)

        def update():
            if not self.is_animating: return
            nonlocal current_frame
            current_frame += 1
            progress = current_frame / frames
            current_split = start_split + (end_split - start_split) * progress
            x_split = self.get_x_coord(current_split)

            if current_split > self.s + 0.05: 
                h_o = min((x_split - x_s) * 0.5, 130)
                self.canvas.coords(self.arc_orange, x_s, self.base_y - h_o, x_split, self.base_y + h_o)
                
                points_o = [x_split, self.base_y, x_split - 12, self.base_y - 8, x_split - 12, self.base_y + 8]
                self.canvas.coords(self.arrow_orange, *points_o)
                
                lbl_x_o = (x_s + x_split)/2
                lbl_y_o = self.base_y - h_o - 15
                self.canvas.coords(self.lbl_orange, lbl_x_o, lbl_y_o)
                
                # Update box position but keep old text while moving
                bbox_o = self.canvas.bbox(self.lbl_orange)
                if bbox_o:
                    self.canvas.coords(self.rect_orange, bbox_o[0]-4, bbox_o[1]-4, bbox_o[2]+4, bbox_o[3]+4)
                    
            else:
                self.canvas.itemconfig(self.arc_orange, state=tk.HIDDEN)
                self.canvas.itemconfig(self.arrow_orange, state=tk.HIDDEN)
                self.canvas.itemconfig(self.lbl_orange, state=tk.HIDDEN)
                self.canvas.itemconfig(self.rect_orange, state=tk.HIDDEN)

            h_b = min((x_m - x_split) * 0.5, 130)
            self.canvas.coords(self.arc_blue, x_split, self.base_y - h_b, x_m, self.base_y + h_b)
            
            lbl_x_b = (x_split + x_m)/2
            lbl_y_b = self.base_y - h_b - 15
            self.canvas.coords(self.lbl_blue, lbl_x_b, lbl_y_b)
            
            # Update box position but keep old text while moving
            bbox_b = self.canvas.bbox(self.lbl_blue)
            if bbox_b:
                self.canvas.coords(self.rect_blue, bbox_b[0]-4, bbox_b[1]-4, bbox_b[2]+4, bbox_b[3]+4)

            if current_frame < frames:
                self.root.after(delay_ms, update)
            else:
                # Text changes ONLY when the movement is fully complete
                self.canvas.itemconfig(self.lbl_blue, text=target_blue_label)
                bbox_b_final = self.canvas.bbox(self.lbl_blue)
                if bbox_b_final:
                    self.canvas.coords(self.rect_blue, bbox_b_final[0]-4, bbox_b_final[1]-4, bbox_b_final[2]+4, bbox_b_final[3]+4)

                if current_split > self.s + 0.05:
                    self.canvas.itemconfig(self.lbl_orange, text=target_orange_label)
                    bbox_o_final = self.canvas.bbox(self.lbl_orange)
                    if bbox_o_final:
                        self.canvas.coords(self.rect_orange, bbox_o_final[0]-4, bbox_o_final[1]-4, bbox_o_final[2]+4, bbox_o_final[3]+4)
                
                on_complete()

        update()

if __name__ == "__main__":
    root = tk.Tk()
    app = MakeATenApp(root)
    root.mainloop()