from kivymd.app import MDApp

# ✅ Use Kivy Screen/ScreenManager (more stable on Android builds)
from kivy.uix.screenmanager import Screen, ScreenManager

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

# ✅ Toolbar fallback (some versions)
try:
    from kivymd.uix.toolbar import MDTopAppBar
except Exception:
    from kivymd.uix.toolbar import MDToolbar as MDTopAppBar

from kivymd.uix.pickers import MDDatePicker
from kivymd.toast import toast

import requests
import certifi
from datetime import date, datetime

# ==========================================
# PASTE YOUR GOOGLE SCRIPT URL BELOW
# ==========================================
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbypHp24_ZNQ1GI8x-YpdZfblb9dlFkCKpx7a1mcu5KUeHhH7Ju4842xGo0lswS6VZmP/exec'
# ==========================================

CURRENT_USER = ""


class LoginScreen(Screen):
    pass


class MainAppScreen(Screen):
    pass


class FamilyExpenseApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        # ✅ Some versions may not have accent_palette
        if hasattr(self.theme_cls, "accent_palette"):
            self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        self.sm = ScreenManager()

        # ==================================
        # SCREEN 1: LOGIN
        # ==================================
        login_screen = LoginScreen(name='login')
        layout_login = MDBoxLayout(orientation='vertical', padding="40dp", spacing="20dp")

        layout_login.add_widget(MDLabel(text="", size_hint_y=None, height="50dp"))

        # ✅ Removed bold=True (causes crash). Using markup instead.
        layout_login.add_widget(MDLabel(text="[b]Family Finance[/b]", markup=True,
                                        halign="center", font_style="H4"))
        layout_login.add_widget(MDLabel(text="Secure Login", halign="center",
                                        theme_text_color="Hint", font_style="Caption"))

        self.login_user = MDTextField(hint_text="Username", helper_text="Akshay or Monika", icon_right="account")
        layout_login.add_widget(self.login_user)

        self.login_pass = MDTextField(hint_text="Password", password=True, icon_right="key-variant")
        layout_login.add_widget(self.login_pass)

        btn_login = MDFillRoundFlatIconButton(text="LOGIN", icon="login", size_hint_x=1, padding="15dp")
        btn_login.bind(on_release=self.check_login)
        layout_login.add_widget(btn_login)
        layout_login.add_widget(MDLabel())

        login_screen.add_widget(layout_login)
        self.sm.add_widget(login_screen)

        # ==================================
        # SCREEN 2: MAIN APP
        # ==================================
        self.main_screen = MainAppScreen(name='main')
        main_layout = MDBoxLayout(orientation='vertical')

        # Toolbar
        self.toolbar = MDTopAppBar(title="Home", elevation=4)
        try:
            self.toolbar.md_bg_color = self.theme_cls.primary_color
        except Exception:
            pass

        self.toolbar.right_action_items = [
            ["refresh", lambda x: self.refresh_dashboard(None)],
            ["logout", lambda x: self.logout()]
        ]
        main_layout.add_widget(self.toolbar)

        self.nav_bar = MDBottomNavigation()

        # --- TAB 1: ADD ENTRY ---
        self.screen_add = MDBottomNavigationItem(name='screen1', text='Add', icon='plus-circle')

        scroll_add = MDScrollView()
        layout_add = MDBoxLayout(orientation='vertical', padding="20dp", spacing="15dp", adaptive_height=True)

        # 1. Date Picker
        layout_add.add_widget(MDLabel(text="Select Date:", theme_text_color="Secondary", font_style="Caption"))
        self.selected_date_obj = date.today()
        self.btn_date = MDRectangleFlatIconButton(text=f"Date: {date.today()}",
                                                  icon="calendar", size_hint_x=1, padding="10dp")
        self.btn_date.bind(on_release=self.show_date_picker)
        layout_add.add_widget(self.btn_date)

        # 2. Type
        layout_add.add_widget(MDLabel(text="Transaction Type:", theme_text_color="Secondary", font_style="Caption"))
        type_grid = MDGridLayout(cols=2, spacing="15dp", adaptive_height=True)

        self.btn_expense = MDFillRoundFlatIconButton(text="EXPENSE", icon="arrow-down-bold", size_hint_x=1)
        self.btn_income = MDFillRoundFlatIconButton(text="INCOME", icon="arrow-up-bold", size_hint_x=1)

        self.btn_expense.bind(on_release=self.set_type_expense)
        self.btn_income.bind(on_release=self.set_type_income)

        self.btn_expense.md_bg_color = (1, 0.3, 0.3, 1)
        self.btn_income.md_bg_color = (0.9, 0.9, 0.9, 1)
        self.btn_income.text_color = (0, 0, 0, 0.5)

        type_grid.add_widget(self.btn_expense)
        type_grid.add_widget(self.btn_income)
        layout_add.add_widget(type_grid)

        # 3. Person
        layout_add.add_widget(MDLabel(text="Beneficiary:", theme_text_color="Secondary", font_style="Caption"))
        self.person_grid = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)

        self.btn_akshay = MDFillRoundFlatIconButton(text="Akshay", icon="account", size_hint_x=1)
        self.btn_monika = MDFillRoundFlatIconButton(text="Monika", icon="account-heart", size_hint_x=1)
        self.btn_abhi = MDFillRoundFlatIconButton(text="Abhimanyu", icon="baby-face", size_hint_x=1)
        self.btn_family = MDFillRoundFlatIconButton(text="Family", icon="home-group", size_hint_x=1)

        self.btn_akshay.bind(on_release=lambda x: self.set_person("Akshay"))
        self.btn_monika.bind(on_release=lambda x: self.set_person("Monika"))
        self.btn_abhi.bind(on_release=lambda x: self.set_person("Abhimanyu"))
        self.btn_family.bind(on_release=lambda x: self.set_person("Family"))

        layout_add.add_widget(self.person_grid)  # will be filled after login

        # 4. Inputs
        self.amount_input = MDTextField(hint_text="Amount", icon_right="currency-inr", mode="rectangle", input_filter="int")
        layout_add.add_widget(self.amount_input)

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
        self.screen_dash = MDBottomNavigationItem(name='screen2', text='Analytics', icon='chart-bar')
        self.screen_dash.bind(on_tab_press=self.refresh_dashboard)

        scroll_dash = MDScrollView()
        layout_dash = MDBoxLayout(orientation='vertical', padding="15dp", spacing="15dp", adaptive_height=True)

        # Monthly Cards
        layout_dash.add_widget(MDLabel(text="[b]Monthly Analysis[/b]", markup=True, font_style="H6"))
        month_grid = MDGridLayout(cols=2, spacing="10dp", adaptive_height=True)

        card_m_inc = MDCard(orientation='vertical', padding="10dp", radius=[10],
                            md_bg_color=(0.9, 1, 0.9, 1), size_hint_y=None, height="80dp")
        card_m_inc.add_widget(MDLabel(text="INCOME", font_style="Overline", halign="center"))
        self.lbl_month_inc = MDLabel(text="0", font_style="H6", halign="center",
                                     theme_text_color="Custom", text_color="green")
        card_m_inc.add_widget(self.lbl_month_inc)

        card_m_exp = MDCard(orientation='vertical', padding="10dp", radius=[10],
                            md_bg_color=(1, 0.9, 0.9, 1), size_hint_y=None, height="80dp")
        card_m_exp.add_widget(MDLabel(text="EXPENSE", font_style="Overline", halign="center"))
        self.lbl_month_exp = MDLabel(text="0", font_style="H6", halign="center",
                                     theme_text_color="Custom", text_color="red")
        card_m_exp.add_widget(self.lbl_month_exp)

        month_grid.add_widget(card_m_inc)
        month_grid.add_widget(card_m_exp)
        layout_dash.add_widget(month_grid)

        # Yearly Card
        layout_dash.add_widget(MDLabel(text="[b]Yearly Analysis[/b]", markup=True, font_style="H6"))
        card_y = MDCard(orientation='vertical', padding="15dp", radius=[10],
                        md_bg_color=(0.9, 0.9, 1, 1), size_hint_y=None, height="90dp")
        card_y.add_widget(MDLabel(text="TOTAL SPENT THIS YEAR", font_style="Overline", halign="center"))
        self.lbl_year_exp = MDLabel(text="Rs 0", font_style="H4", halign="center",
                                    theme_text_color="Primary")
        card_y.add_widget(self.lbl_year_exp)
        layout_dash.add_widget(card_y)

        # Charts
        layout_dash.add_widget(MDLabel(text="[b]Who Spent What? (Monthly)[/b]", markup=True, font_style="H6"))
        self.chart_box = MDBoxLayout(orientation='vertical', spacing="8dp", adaptive_height=True)
        layout_dash.add_widget(self.chart_box)

        # History List
        layout_dash.add_widget(MDLabel(text="[b]Recent Transactions[/b]", markup=True, font_style="H6"))
        self.history_list = MDList()
        layout_dash.add_widget(self.history_list)

        scroll_dash.add_widget(layout_dash)
        self.screen_dash.add_widget(scroll_dash)

        self.nav_bar.add_widget(self.screen_add)
        self.nav_bar.add_widget(self.screen_dash)

        main_layout.add_widget(self.nav_bar)
        self.main_screen.add_widget(main_layout)
        self.sm.add_widget(self.main_screen)

        self.selected_type = "Expense"
        self.selected_person = "Family"  # default safe

        return self.sm

    # --- DATE PICKER LOGIC ---
    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.selected_date_obj = value
        self.btn_date.text = f"Date: {value}"

    # --- LOGIN LOGIC ---
    def check_login(self, obj):
        user = self.login_user.text.strip()
        pwd = self.login_pass.text.strip()
        global CURRENT_USER

        if (user == "Akshay" and pwd == "1234") or (user == "Monika" and pwd == "5678"):
            CURRENT_USER = user
            self.toolbar.title = f"Welcome {user}"
            self.setup_ui_for_user(user)
            self.sm.current = 'main'
        else:
            toast("Invalid Credentials")

    def setup_ui_for_user(self, user):
        self.person_grid.clear_widgets()

        if user == "Akshay":
            self.person_grid.add_widget(self.btn_akshay)
            self.person_grid.add_widget(self.btn_abhi)
            self.person_grid.add_widget(self.btn_family)
            self.set_person("Akshay")

        elif user == "Monika":
            self.person_grid.add_widget(self.btn_monika)
            self.person_grid.add_widget(self.btn_abhi)
            self.person_grid.add_widget(self.btn_family)
            self.set_person("Monika")

    def logout(self):
        self.sm.current = 'login'
        self.login_pass.text = ""

    # --- SELECTION LOGIC ---
    def set_type_expense(self, x):
        self.selected_type = "Expense"
        self.btn_expense.md_bg_color = (1, 0.3, 0.3, 1)
        self.btn_expense.text_color = (1, 1, 1, 1)
        self.btn_income.md_bg_color = (0.9, 0.9, 0.9, 1)
        self.btn_income.text_color = (0, 0, 0, 0.5)

    def set_type_income(self, x):
        self.selected_type = "Income"
        self.btn_income.md_bg_color = (0.3, 0.8, 0.3, 1)
        self.btn_income.text_color = (1, 1, 1, 1)
        self.btn_expense.md_bg_color = (0.9, 0.9, 0.9, 1)
        self.btn_expense.text_color = (0, 0, 0, 0.5)

    def set_person(self, name):
        self.selected_person = name
        btns = [self.btn_akshay, self.btn_monika, self.btn_abhi, self.btn_family]
        for btn in btns:
            btn.md_bg_color = (0.95, 0.95, 0.95, 1)
            btn.text_color = (0, 0, 0, 0.7)
            btn.elevation = 0

        target = self.btn_akshay
        if name == "Monika":
            target = self.btn_monika
        elif name == "Abhimanyu":
            target = self.btn_abhi
        elif name == "Family":
            target = self.btn_family

        target.md_bg_color = self.theme_cls.primary_color
        target.text_color = (1, 1, 1, 1)
        target.elevation = 3

    # --- SAVE DATA (✅ fixed) ---
    def send_data(self, obj):
        if not self.amount_input.text or not self.desc_input.text:
            self.status_label.text = "Please fill Amount & Description"
            return

        self.status_label.text = "Saving..."

        try:
            date_to_send = str(self.selected_date_obj)
            payload = {
                'date': date_to_send,
                'amount': self.amount_input.text,
                'desc': self.desc_input.text,
                'user': self.selected_person,
                'type': self.selected_type
            }

            # ✅ Send as form body (Apps Script doPost(e).parameter compatible)
            r = requests.post(
                GOOGLE_SCRIPT_URL,
                data=payload,
                timeout=25,
                verify=certifi.where()
            )
            r.raise_for_status()

            self.status_label.text = "Saved!"
            self.amount_input.text = ""
            self.desc_input.text = ""

        except Exception as e:
            self.status_label.text = f"Error: {type(e).__name__}"
            print("Send Error:", e)

    # --- DASHBOARD LOGIC (✅ fixed) ---
    def refresh_dashboard(self, obj):
        try:
            self.lbl_month_exp.text = "..."
            r = requests.get(GOOGLE_SCRIPT_URL, timeout=25, verify=certifi.where())

            try:
                data = r.json()
            except Exception:
                self.lbl_month_exp.text = "Script not returning JSON"
                print("Response (first 300):", r.text[:300])
                return

            today = date.today()
            curr_month = today.month
            curr_year = today.year

            m_inc = 0
            m_exp = 0
            y_exp = 0
            dist_data = {"Akshay": 0, "Monika": 0, "Abhimanyu": 0, "Family": 0}

            self.history_list.clear_widgets()
            recent_count = 0

            if not isinstance(data, list):
                self.lbl_month_exp.text = "Invalid data format"
                return

            for row in reversed(data):
                if len(row) < 5:
                    continue

                raw_date = str(row[0]).split("T")[0]
                try:
                    row_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                    display_date = row_date.strftime("%d %b")
                except:
                    continue

                amt = float(row[1])
                desc = str(row[2])
                user = str(row[3])
                typ = str(row[4])

                # PRIVACY FILTER
                if CURRENT_USER == "Akshay" and user == "Monika":
                    continue
                if CURRENT_USER == "Monika" and user == "Akshay":
                    continue

                # Year Total
                if row_date.year == curr_year and typ == "Expense":
                    y_exp += amt

                # Month Total
                if row_date.year == curr_year and row_date.month == curr_month:
                    if typ == "Income":
                        m_inc += amt
                    else:
                        m_exp += amt
                        if user in dist_data:
                            dist_data[user] += amt

                # List
                if recent_count < 30:
                    icon = "arrow-up-bold-circle" if typ == "Income" else "arrow-down-bold-circle"
                    color = (0, 0.7, 0, 1) if typ == "Income" else (0.8, 0, 0, 1)

                    item = TwoLineAvatarIconListItem(
                        text=f"Rs {int(amt)} - {desc}",
                        secondary_text=f"{display_date} | {user}"
                    )
                    item.add_widget(IconLeftWidget(icon=icon, theme_text_color="Custom", text_color=color))
                    self.history_list.add_widget(item)
                    recent_count += 1

            self.lbl_month_inc.text = f"Rs {int(m_inc)}"
            self.lbl_month_exp.text = f"Rs {int(m_exp)}"
            self.lbl_year_exp.text = f"Rs {int(y_exp)}"

            self.chart_box.clear_widgets()
            colors = {
                "Akshay": (0.2, 0.2, 1, 1),
                "Monika": (1, 0.4, 0.7, 1),
                "Abhimanyu": (1, 0.6, 0.2, 1),
                "Family": (0, 0.5, 0.5, 1)
            }

            for name, val in dist_data.items():
                if val > 0:
                    percent = (val / m_exp) * 100 if m_exp > 0 else 0
                    self.chart_box.add_widget(
                        MDLabel(
                            text=f"{name}: {int(percent)}% (Rs {int(val)})",
                            font_style="Caption",
                            size_hint_y=None,
                            height="20dp"
                        )
                    )
                    self.chart_box.add_widget(
                        MDProgressBar(
                            value=percent,
                            color=colors.get(name, (0, 0, 1, 1)),
                            size_hint_y=None,
                            height="15dp"
                        )
                    )

        except Exception as e:
            self.lbl_month_exp.text = "Error"
            print("Dashboard Error:", e)


if __name__ == '__main__':
    FamilyExpenseApp().run()
