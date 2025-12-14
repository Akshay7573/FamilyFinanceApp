from kivymd.app import MDApp

# Screens/ScreenManager: keep compatible across KivyMD versions
try:
    from kivymd.uix.screen import MDScreen as Screen
except Exception:
    from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRectangleFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.pickers import MDDatePicker
from kivymd.toast import toast

import requests
from datetime import date, datetime

# ==========================================
# PASTE YOUR GOOGLE SCRIPT URL BELOW
# ==========================================
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyOlcVfdYgKM6zbPR33IYkrp5EmkMbzKbNNpcrOaDQdNd_pT0tGI8x-YpdZfblb9dlFkCKpx7a1mcu5KUeHhH7Ju4842xGo0lswS6VZmP/exec'
# ==========================================

CURRENT_USER = ""


class LoginScreen(Screen):
    pass


class MainAppScreen(Screen):
    pass


class FamilyExpenseApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        # Some KivyMD versions removed accent_palette; keep app compatible.
        if hasattr(self.theme_cls, "accent_palette"):
            self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        self.sm = ScreenManager()

        # ==================================
        # SCREEN 1: LOGIN
        # ==================================
        login_screen = LoginScreen(name='login')
        layout_login = MDBoxLayout(orientation='vertical', padding="40dp", spacing="20dp")

        layout_login.add_widget(MDLabel(text="Family Finance Login", halign="center", font_style="H5"))

        self.login_username = MDTextField(hint_text="Enter Name (Akshay/Monika/Abhimanyu)", mode="rectangle")
        layout_login.add_widget(self.login_username)

        btn_login = MDFillRoundFlatIconButton(text="LOGIN", icon="login", size_hint_x=1)
        btn_login.md_bg_color = self.theme_cls.primary_color
        btn_login.bind(on_release=self.login_user)
        layout_login.add_widget(btn_login)

        login_screen.add_widget(layout_login)
        self.sm.add_widget(login_screen)

        # ==================================
        # SCREEN 2: MAIN APP (NAVIGATION)
        # ==================================
        main_screen = MainAppScreen(name='main')

        root_layout = MDBoxLayout(orientation='vertical')

        toolbar = MDTopAppBar(title="Family Finance Tracker")
        toolbar.elevation = 10
        root_layout.add_widget(toolbar)

        nav = MDBottomNavigation()

        # --- TAB 1: ADD ENTRY ---
        self.screen_add = MDBottomNavigationItem(name='screen_add', text='Add', icon='plus-circle')
        scroll_add = MDScrollView()
        layout_add = MDBoxLayout(orientation='vertical', padding="20dp", spacing="15dp", size_hint_y=None)
        layout_add.bind(minimum_height=layout_add.setter('height'))

        self.amount_input = MDTextField(hint_text="Amount", icon_right="currency-inr", mode="rectangle", input_filter="int")
        layout_add.add_widget(self.amount_input)

        self.category_input = MDTextField(hint_text="Category (Food/Rent/etc.)", icon_right="tag", mode="rectangle")
        layout_add.add_widget(self.category_input)

        self.desc_input = MDTextField(hint_text="Description", icon_right="notebook-edit", mode="rectangle")
        layout_add.add_widget(self.desc_input)

        btn_save = MDFillRoundFlatIconButton(text="SAVE ENTRY", icon="content-save", size_hint_x=1, padding="15dp")
        btn_save.md_bg_color = self.theme_cls.primary_color
        btn_save.bind(on_release=self.send_data)
        layout_add.add_widget(btn_save)

        self.status_label = MDLabel(text="Ready", halign="center", theme_text_color="Hint", font_style="Caption")
        layout_add.add_widget(self.status_label)

        scroll_add.add_widget(layout_add)
        self.screen_add.add_widget(scroll_add)

        # --- TAB 2: DASHBOARD ---
        self.screen_dash = MDBottomNavigationItem(name='screen_analytics', text='Analytics', icon='chart-bar',
                                                  on_tab_press=self.refresh_dashboard)

        scroll_dash = MDScrollView()
        dash_layout = MDBoxLayout(orientation='vertical', padding="20dp", spacing="15dp", size_hint_y=None)
        dash_layout.bind(minimum_height=dash_layout.setter('height'))

        self.lbl_month_exp = MDLabel(text="Monthly Expense: ₹0", font_style="H6", halign="center")
        dash_layout.add_widget(self.lbl_month_exp)

        self.lbl_savings = MDLabel(text="Savings: ₹0", font_style="H6", halign="center")
        dash_layout.add_widget(self.lbl_savings)

        dash_layout.add_widget(MDLabel(text="Expense Distribution", font_style="Subtitle1"))
        self.chart_box = MDBoxLayout(orientation='vertical', spacing="10dp", size_hint_y=None)
        self.chart_box.bind(minimum_height=self.chart_box.setter('height'))
        dash_layout.add_widget(self.chart_box)

        scroll_dash.add_widget(dash_layout)
        self.screen_dash.add_widget(scroll_dash)

        # --- TAB 3: HISTORY ---
        self.screen_history = MDBottomNavigationItem(name='screen_history', text='History', icon='history')

        scroll_hist = MDScrollView()
        hist_layout = MDBoxLayout(orientation='vertical', padding="20dp", spacing="15dp", size_hint_y=None)
        hist_layout.bind(minimum_height=hist_layout.setter('height'))

        # Filter Row
        filter_row = MDBoxLayout(orientation='horizontal', spacing="10dp", size_hint_y=None, height="60dp")

        self.date_input = MDTextField(hint_text="Select Date", mode="rectangle", readonly=True)
        self.date_input.bind(on_focus=self.show_date_picker)
        filter_row.add_widget(self.date_input)

        btn_filter = MDRectangleFlatIconButton(text="Filter", icon="filter", size_hint_x=None, width="120dp")
        btn_filter.bind(on_release=self.filter_history)
        filter_row.add_widget(btn_filter)

        hist_layout.add_widget(filter_row)

        # History list
        self.history_list = MDList()
        scroll_hist.add_widget(self.history_list)

        self.screen_history.add_widget(scroll_hist)

        # Add all tabs
        nav.add_widget(self.screen_add)
        nav.add_widget(self.screen_dash)
        nav.add_widget(self.screen_history)

        root_layout.add_widget(nav)
        main_screen.add_widget(root_layout)

        self.sm.add_widget(main_screen)

        return self.sm

    # ==========================
    # LOGIN
    # ==========================
    def login_user(self, instance):
        global CURRENT_USER
        user = self.login_username.text.strip()
        if user in ["Akshay", "Monika", "Abhimanyu"]:
            CURRENT_USER = user
            toast(f"Welcome {user}")
            self.sm.current = "main"
        else:
            toast("Invalid User")

    # ==========================
    # SEND DATA TO GOOGLE SHEET
    # ==========================
    def send_data(self, instance):
        global CURRENT_USER

        amount = self.amount_input.text.strip()
        category = self.category_input.text.strip()
        desc = self.desc_input.text.strip()

        if not amount or not category:
            toast("Enter amount & category")
            return

        data = {
            "user": CURRENT_USER,
            "amount": amount,
            "category": category,
            "desc": desc,
            "date": str(date.today()),
            "time": datetime.now().strftime("%H:%M:%S"),
        }

        try:
            self.status_label.text = "Saving..."
            response = requests.post(GOOGLE_SCRIPT_URL, json=data, timeout=15)

            if response.status_code == 200:
                toast("Saved Successfully ✅")
                self.amount_input.text = ""
                self.category_input.text = ""
                self.desc_input.text = ""
                self.status_label.text = "Saved ✅"
            else:
                toast("Error Saving ❌")
                self.status_label.text = "Error"

        except Exception as e:
            toast("Network Error")
            self.status_label.text = "Network Error"
            print("Send Error:", e)

    # ==========================
    # DATE PICKER
    # ==========================
    def show_date_picker(self, instance, value):
        if value:
            picker = MDDatePicker()
            picker.bind(on_save=self.set_date)
            picker.open()

    def set_date(self, instance, value, date_range):
        self.date_input.text = str(value)

    # ==========================
    # FILTER HISTORY
    # ==========================
    def filter_history(self, instance):
        sel_date = self.date_input.text.strip()
        if not sel_date:
            toast("Select date first")
            return

        try:
            self.history_list.clear_widgets()
            response = requests.get(GOOGLE_SCRIPT_URL + f"?action=history&date={sel_date}", timeout=15)
            data = response.json()

            if len(data) == 0:
                toast("No entries found")
                return

            for row in data:
                item = TwoLineAvatarIconListItem(
                    text=f"₹{row['amount']} - {row['category']}",
                    secondary_text=f"{row['user']} | {row['desc']}"
                )
                item.add_widget(IconLeftWidget(icon="cash"))
                self.history_list.add_widget(item)

        except Exception as e:
            toast("Error loading history")
            print("History Error:", e)

    # ==========================
    # DASHBOARD
    # ==========================
    def refresh_dashboard(self, *args):
        try:
            response = requests.get(GOOGLE_SCRIPT_URL + "?action=dashboard", timeout=15)
            data = response.json()

            m_exp = float(data.get("monthly_expense", 0))
            savings = float(data.get("savings", 0))
            dist_data = data.get("distribution", {})

            self.lbl_month_exp.text = f"Monthly Expense: ₹{m_exp}"
            self.lbl_savings.text = f"Savings: ₹{savings}"

            self.chart_box.clear_widgets()
            colors = {
                "Akshay": (0.2, 0.2, 1, 1),
                "Monika": (1, 0.4, 0.7, 1),
                "Abhimanyu": (1, 0.6, 0.2, 1),
                "Family": (0, 0.5, 0.5, 1),
            }

            for name, val in dist_data.items():
                if val > 0:
                    percent = (val / m_exp) * 100 if m_exp > 0 else 0
                    self.chart_box.add_widget(
                        MDLabel(
                            text=f"{name}: ₹{val} ({percent:.1f}%)",
                            font_style="Caption",
                            size_hint_y=None,
                            height="20dp",
                        )
                    )
                    self.chart_box.add_widget(
                        MDProgressBar(
                            value=percent,
                            color=colors.get(name, (0, 0, 1, 1)),
                            size_hint_y=None,
                            height="15dp",
                        )
                    )

        except Exception as e:
            self.lbl_month_exp.text = "Error"
            print("Dashboard Error:", e)


if __name__ == '__main__':
    FamilyExpenseApp().run()
