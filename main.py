import os
import traceback
from datetime import date, datetime

import requests

from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.toast import toast

# ==========================================
# PASTE YOUR GOOGLE SCRIPT URL BELOW
# ==========================================
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyOlcVfdYgKM6zbPR33IYkrp5EmkMbzKbNNpcrOaDQdNd_pT0tGI8x-YpdZfblb9dlFkCKpx7a1mcu5KUeHhH7Ju4842xGo0lswS6VZmP/exec"
# ==========================================


class LoginScreen(Screen):
    pass


class AddScreen(Screen):
    pass


class AnalyticsScreen(Screen):
    pass


class HistoryScreen(Screen):
    pass


class FamilyExpenseApp(MDApp):
    def build(self):
        self.current_user = ""
        self.error_file = None

        # Theme (keep minimal for compatibility)
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"

        # set crash log path early
        try:
            self.error_file = os.path.join(self.user_data_dir, "crash_log.txt")
        except Exception:
            self.error_file = "crash_log.txt"

        # Wrap UI build to prevent “instant close”
        try:
            return self._build_ui()
        except Exception:
            err = traceback.format_exc()
            self._write_crash(err)
            # Show error on screen instead of closing
            box = MDBoxLayout(orientation="vertical", padding="20dp", spacing="10dp")
            box.add_widget(MDLabel(text="App Error on Start ❌", halign="center", font_style="H6"))
            box.add_widget(MDLabel(text="crash_log.txt file created.", halign="center"))
            box.add_widget(MDLabel(text="(Rebuild after fixing)", halign="center"))
            return box

    def _build_ui(self):
        self.sm = ScreenManager()

        # ---------------- LOGIN ----------------
        login = LoginScreen(name="login")
        login_box = MDBoxLayout(orientation="vertical", padding="30dp", spacing="15dp")

        login_box.add_widget(MDLabel(text="Family Finance Login", halign="center", font_style="H5"))

        self.login_username = MDTextField(
            hint_text="Enter Name (Akshay/Monika/Abhimanyu)",
            mode="rectangle",
        )
        login_box.add_widget(self.login_username)

        btn_login = MDRaisedButton(text="LOGIN")
        btn_login.bind(on_release=self.login_user)
        login_box.add_widget(btn_login)

        login.add_widget(login_box)
        self.sm.add_widget(login)

        # ---------------- MAIN WRAPPER ----------------
        main_wrapper = Screen(name="main")

        root = MDBoxLayout(orientation="vertical")

        # Top title (simple label instead of toolbar to avoid version issues)
        self.title_label = MDLabel(
            text="Family Finance Tracker",
            halign="center",
            font_style="H6",
            size_hint_y=None,
            height="48dp",
        )
        root.add_widget(self.title_label)

        # Content ScreenManager for tabs
        self.content_sm = ScreenManager()

        # ---------- ADD TAB ----------
        add_scr = AddScreen(name="add")
        add_box = MDBoxLayout(orientation="vertical", padding="20dp", spacing="12dp")

        self.amount_input = MDTextField(hint_text="Amount", mode="rectangle", input_filter="int")
        self.category_input = MDTextField(hint_text="Category (Food/Rent/etc.)", mode="rectangle")
        self.desc_input = MDTextField(hint_text="Description (optional)", mode="rectangle")

        add_box.add_widget(self.amount_input)
        add_box.add_widget(self.category_input)
        add_box.add_widget(self.desc_input)

        btn_save = MDRaisedButton(text="SAVE ENTRY")
        btn_save.bind(on_release=self.send_data)
        add_box.add_widget(btn_save)

        self.status_label = MDLabel(text="Ready", halign="center")
        add_box.add_widget(self.status_label)

        add_scr.add_widget(add_box)
        self.content_sm.add_widget(add_scr)

        # ---------- ANALYTICS TAB ----------
        ana_scr = AnalyticsScreen(name="analytics")
        ana_outer = MDBoxLayout(orientation="vertical", padding="20dp", spacing="12dp")

        self.lbl_month_exp = MDLabel(text="Monthly Expense: ₹0", halign="center", font_style="H6")
        self.lbl_savings = MDLabel(text="Savings: ₹0", halign="center", font_style="H6")
        ana_outer.add_widget(self.lbl_month_exp)
        ana_outer.add_widget(self.lbl_savings)

        btn_refresh = MDRaisedButton(text="REFRESH ANALYTICS")
        btn_refresh.bind(on_release=self.refresh_dashboard)
        ana_outer.add_widget(btn_refresh)

        ana_outer.add_widget(MDLabel(text="Distribution:", font_style="Subtitle1"))

        self.dist_list = MDList()
        dist_scroll = MDScrollView()
        dist_scroll.add_widget(self.dist_list)
        ana_outer.add_widget(dist_scroll)

        ana_scr.add_widget(ana_outer)
        self.content_sm.add_widget(ana_scr)

        # ---------- HISTORY TAB ----------
        hist_scr = HistoryScreen(name="history")
        hist_outer = MDBoxLayout(orientation="vertical", padding="20dp", spacing="12dp")

        self.date_input = MDTextField(
            hint_text="Date (YYYY-MM-DD) e.g. 2025-12-14",
            mode="rectangle",
        )
        hist_outer.add_widget(self.date_input)

        btn_filter = MDRaisedButton(text="LOAD HISTORY")
        btn_filter.bind(on_release=self.filter_history)
        hist_outer.add_widget(btn_filter)

        self.history_list = MDList()
        hist_scroll = MDScrollView()
        hist_scroll.add_widget(self.history_list)
        hist_outer.add_widget(hist_scroll)

        hist_scr.add_widget(hist_outer)
        self.content_sm.add_widget(hist_scr)

        root.add_widget(self.content_sm)

        # Bottom buttons (safe)
        bottom = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="56dp", padding="6dp", spacing="6dp")

        btn_add = MDFlatButton(text="ADD")
        btn_add.bind(on_release=lambda x: self.switch_tab("add"))

        btn_ana = MDFlatButton(text="ANALYTICS")
        btn_ana.bind(on_release=lambda x: self.switch_tab("analytics"))

        btn_hist = MDFlatButton(text="HISTORY")
        btn_hist.bind(on_release=lambda x: self.switch_tab("history"))

        bottom.add_widget(btn_add)
        bottom.add_widget(btn_ana)
        bottom.add_widget(btn_hist)

        root.add_widget(bottom)

        main_wrapper.add_widget(root)
        self.sm.add_widget(main_wrapper)

        return self.sm

    def switch_tab(self, name):
        self.content_sm.current = name

    # ==========================
    # LOGIN
    # ==========================
    def login_user(self, instance):
        user = (self.login_username.text or "").strip()
        if user in ["Akshay", "Monika", "Abhimanyu"]:
            self.current_user = user
            toast(f"Welcome {user}")
            self.sm.current = "main"
        else:
            toast("Invalid User")

    # ==========================
    # SEND DATA TO GOOGLE SHEET
    # ==========================
    def send_data(self, instance):
        amount = (self.amount_input.text or "").strip()
        category = (self.category_input.text or "").strip()
        desc = (self.desc_input.text or "").strip()

        if not self.current_user:
            toast("Please login first")
            self.sm.current = "login"
            return

        if not amount or not category:
            toast("Enter amount & category")
            return

        data = {
            "user": self.current_user,
            "amount": amount,
            "category": category,
            "desc": desc,
            "date": str(date.today()),
            "time": datetime.now().strftime("%H:%M:%S"),
        }

        try:
            self.status_label.text = "Saving..."
            r = requests.post(GOOGLE_SCRIPT_URL, json=data, timeout=20)

            if r.status_code == 200:
                toast("Saved ✅")
                self.amount_input.text = ""
                self.category_input.text = ""
                self.desc_input.text = ""
                self.status_label.text = "Saved ✅"
            else:
                toast(f"Save failed ({r.status_code})")
                self.status_label.text = "Error"
        except Exception:
            err = traceback.format_exc()
            self._write_crash(err)
            toast("Network/Server error")
            self.status_label.text = "Network/Server error"

    # ==========================
    # HISTORY
    # ==========================
    def filter_history(self, instance):
        sel_date = (self.date_input.text or "").strip()
        if not sel_date:
            toast("Enter date (YYYY-MM-DD)")
            return

        try:
            self.history_list.clear_widgets()

            r = requests.get(f"{GOOGLE_SCRIPT_URL}?action=history&date={sel_date}", timeout=20)
            data = r.json() if r.status_code == 200 else []

            if not data:
                toast("No entries found")
                return

            for row in data:
                text = f"₹{row.get('amount','')} - {row.get('category','')}"
                sub = f"{row.get('user','')} | {row.get('desc','')}"
                self.history_list.add_widget(TwoLineListItem(text=text, secondary_text=sub))

        except Exception:
            err = traceback.format_exc()
            self._write_crash(err)
            toast("Error loading history")

    # ==========================
    # ANALYTICS
    # ==========================
    def refresh_dashboard(self, instance):
        try:
            self.dist_list.clear_widgets()

            r = requests.get(f"{GOOGLE_SCRIPT_URL}?action=dashboard", timeout=20)
            data = r.json() if r.status_code == 200 else {}

            m_exp = float(data.get("monthly_expense", 0) or 0)
            savings = float(data.get("savings", 0) or 0)
            dist = data.get("distribution", {}) or {}

            self.lbl_month_exp.text = f"Monthly Expense: ₹{m_exp:.0f}"
            self.lbl_savings.text = f"Savings: ₹{savings:.0f}"

            if not dist:
                self.dist_list.add_widget(TwoLineListItem(text="No distribution data", secondary_text=""))
                return

            for name, val in dist.items():
                try:
                    v = float(val or 0)
                except Exception:
                    v = 0
                self.dist_list.add_widget(
                    TwoLineListItem(
                        text=f"{name}: ₹{v:.0f}",
                        secondary_text="",
                    )
                )

        except Exception:
            err = traceback.format_exc()
            self._write_crash(err)
            toast("Analytics error")

    def _write_crash(self, text):
        try:
            with open(self.error_file, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            pass


if __name__ == "__main__":
    FamilyExpenseApp().run()
