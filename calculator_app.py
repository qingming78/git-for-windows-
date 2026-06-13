import tkinter as tk
from tkinter import font
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("计算器")
        root.resizable(False, False)
        root.configure(bg="#1a1a2e")

        self.current = "0"
        self.prev = ""
        self.op = None
        self.reset_screen = False
        self.just_evaluated = False

        # Center window
        root.update_idletasks()
        w, h = 340, 480
        x = (root.winfo_screenwidth() - w) // 2
        y = (root.winfo_screenheight() - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")

        self.normal_font = font.Font(family="Segoe UI", size=40, weight="bold")
        self.small_font = font.Font(family="Segoe UI", size=28, weight="bold")
        self.btn_font = font.Font(family="Segoe UI", size=18, weight="bold")
        self.op_font = font.Font(family="Segoe UI", size=20, weight="bold")
        self.fn_font = font.Font(family="Segoe UI", size=14, weight="bold")

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # Display
        display_frame = tk.Frame(self.root, bg="#0f3460", bd=0, highlightthickness=0)
        display_frame.pack(fill="x", padx=16, pady=(20, 8))

        self.expr_label = tk.Label(display_frame, text="", anchor="e",
                                   bg="#0f3460", fg="#8899bb",
                                   font=("Segoe UI", 14), height=1)
        self.expr_label.pack(fill="x", padx=(16, 16), pady=(16, 0))

        self.result_label = tk.Label(display_frame, text="0", anchor="e",
                                     bg="#0f3460", fg="#ffffff",
                                     font=self.normal_font, height=1)
        self.result_label.pack(fill="x", padx=(16, 16), pady=(0, 12))

        # Error label
        self.error_label = tk.Label(self.root, text="", fg="#e94560",
                                    bg="#1a1a2e", font=("Segoe UI", 12),
                                    anchor="e")
        self.error_label.pack(fill="x", padx=16, pady=(0, 4))

        # Button grid
        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(fill="both", expand=True, padx=12, pady=(0, 16))
        btn_frame.grid_rowconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)
        for i in range(5):
            btn_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1)

        buttons = [
            ("AC", 0, 0, "fn"), ("±", 0, 1, "fn"), ("%", 0, 2, "fn"), ("÷", 0, 3, "op"),
            ("7", 1, 0, "num"), ("8", 1, 1, "num"), ("9", 1, 2, "num"), ("×", 1, 3, "op"),
            ("4", 2, 0, "num"), ("5", 2, 1, "num"), ("6", 2, 2, "num"), ("−", 2, 3, "op"),
            ("1", 3, 0, "num"), ("2", 3, 1, "num"), ("3", 3, 2, "num"), ("+", 3, 3, "op"),
            ("0", 4, 0, "num", 2), (".", 4, 2, "num"), ("=", 4, 3, "eq"),
        ]

        self.op_buttons = {}
        for btn in buttons:
            text, r, c = btn[0], btn[1], btn[2]
            kind = btn[3]
            colspan = btn[4] if len(btn) > 4 else 1

            b = tk.Button(btn_frame, text=text, font=self._btn_font(kind),
                          bg=self._btn_color(kind),
                          fg=self._btn_text_color(kind),
                          bd=0, highlightthickness=0,
                          activebackground=self._btn_active_color(kind),
                          activeforeground="#ffffff",
                          cursor="hand2",
                          command=lambda t=text: self._on_click(t))
            b.grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=4, pady=4)

            if kind == "op":
                self.op_buttons[text] = b

    def _btn_font(self, kind):
        if kind in ("op", "eq"):
            return self.op_font
        elif kind == "fn":
            return self.fn_font
        return self.btn_font

    def _btn_color(self, kind):
        if kind == "eq":
            return "#e94560"
        elif kind == "op":
            return "#1a4a7a"
        elif kind == "fn":
            return "#0a2540"
        return "#0f3460"

    def _btn_text_color(self, kind):
        if kind == "eq":
            return "#ffffff"
        elif kind == "fn":
            return "#667799"
        return "#d0e0ff"

    def _btn_active_color(self, kind):
        if kind == "eq":
            return "#ff5a75"
        elif kind == "op":
            return "#e94560"
        elif kind == "fn":
            return "#1a4a7a"
        return "#1a4a7a"

    def _update_display(self):
        text = self.current
        if len(text) > 12:
            self.result_label.config(text=text, font=self.small_font)
        else:
            self.result_label.config(text=text, font=self.normal_font)

    def _set_error(self, msg):
        self.error_label.config(text=msg)

    def _clear_error(self):
        self.error_label.config(text="")

    def _format_num(self, n):
        s = str(n)
        if len(s) > 15:
            return f"{n:.6e}"
        return s

    def _on_click(self, text):
        if text.isdigit():
            self._input_digit(text)
        elif text == ".":
            self._input_decimal()
        elif text == "AC":
            self._clear()
        elif text == "±":
            self._toggle_sign()
        elif text == "%":
            self._percent()
        elif text == "=":
            self._evaluate()
        elif text in ("+", "−", "×", "÷"):
            self._set_op(text)

    def _input_digit(self, d):
        self._clear_error()
        if self.just_evaluated and not self.op:
            self.current = "0"
            self.just_evaluated = False
        if self.reset_screen:
            self.current = "0"
            self.reset_screen = False
        if self.current == "0" and d != "0":
            self.current = d
        elif len(self.current) < 16:
            self.current += d
        self._update_display()

    def _input_decimal(self):
        self._clear_error()
        if self.reset_screen:
            self.current = "0"
            self.reset_screen = False
        if self.just_evaluated and not self.op:
            self.current = "0"
            self.just_evaluated = False
        if "." not in self.current:
            self.current += "."
        self._update_display()

    def _set_op(self, op):
        self._clear_error()
        self.just_evaluated = False
        if self.op and not self.reset_screen:
            self._evaluate()
        self.prev = self.current
        self.op = op
        self.reset_screen = True
        self.expr_label.config(text=f"{self.prev} {op}")
        for b in self.op_buttons.values():
            b.config(bg=self._btn_color("op"), fg=self._btn_text_color("op"))
        if op in self.op_buttons:
            self.op_buttons[op].config(bg="#e94560", fg="#ffffff")

    def _evaluate(self):
        if not self.op:
            return
        try:
            a = float(self.prev)
            b = float(self.current)
            if self.op == "+":
                r = a + b
            elif self.op == "−":
                r = a - b
            elif self.op == "×":
                r = a * b
            elif self.op == "÷":
                if b == 0:
                    self._set_error("不能除以零")
                    self.current = "0"
                    self.prev = ""
                    self.op = None
                    self.reset_screen = True
                    for b in self.op_buttons.values():
                        b.config(bg=self._btn_color("op"), fg=self._btn_text_color("op"))
                    self._update_display()
                    self.expr_label.config(text="")
                    return
                r = a / b

            if not math.isfinite(r):
                self._set_error("结果无效")
                r = 0

            r = round(r, 12)
            self.current = self._format_num(r)
            self.prev = ""
            self.op = None
            self.reset_screen = True
            self.just_evaluated = True
            for b in self.op_buttons.values():
                b.config(bg=self._btn_color("op"), fg=self._btn_text_color("op"))
            self._update_display()
            self.expr_label.config(text="")
        except Exception:
            self._set_error("计算错误")

    def _clear(self):
        self.current = "0"
        self.prev = ""
        self.op = None
        self.reset_screen = False
        self.just_evaluated = False
        self._clear_error()
        for b in self.op_buttons.values():
            b.config(bg=self._btn_color("op"), fg=self._btn_text_color("op"))
        self.expr_label.config(text="")
        self._update_display()

    def _toggle_sign(self):
        self._clear_error()
        if self.current != "0":
            self.current = self.current[1:] if self.current.startswith("-") else "-" + self.current
        self._update_display()

    def _percent(self):
        self._clear_error()
        v = float(self.current)
        self.current = self._format_num(v / 100)
        self._update_display()

    def _bind_keys(self):
        def key_handler(e):
            k = e.keysym
            if k in ("0","1","2","3","4","5","6","7","8","9"):
                self._input_digit(k)
            elif k == "period":
                self._input_decimal()
            elif k in ("Return", "KP_Enter", "equal"):
                self._evaluate()
            elif k in ("Escape", "c", "C"):
                self._clear()
            elif k == "BackSpace":
                self._clear_error()
                if len(self.current) > 1:
                    self.current = self.current[:-1]
                else:
                    self.current = "0"
                self._update_display()
            elif k == "plus":
                self._set_op("+")
            elif k == "minus":
                self._set_op("−")
            elif k == "asterisk":
                self._set_op("×")
            elif k == "slash":
                self._set_op("÷")
                return "break"
            elif k == "percent":
                self._percent()
        self.root.bind("<Key>", key_handler)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
