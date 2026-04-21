from __future__ import annotations

from datetime import date

from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from money_manager.database import CATEGORIES, CURRENCIES, THEMES, Database
from money_manager.services import MoneyManagerService
from money_manager.widgets import Card, PieChartWidget


if Config.has_section("input"):
    Config.remove_section("input")
Config.add_section("input")
Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.set("graphics", "minimum_width", "520")
Config.set("graphics", "minimum_height", "1020")

from kivy.core.window import Window


LIGHT = {
    "window": (0.07, 0.07, 0.09, 1),
    "page": (0.973, 0.976, 0.98, 1),
    "surface": (1, 1, 1, 1),
    "surface_muted": (0.96, 0.97, 0.98, 1),
    "text": (0.12, 0.13, 0.18, 1),
    "muted": (0.45, 0.49, 0.56, 1),
    "border": (0.88, 0.90, 0.93, 1),
    "primary": (0.23, 0.51, 0.96, 1),
    "success": (0.06, 0.72, 0.42, 1),
    "danger": (0.92, 0.27, 0.27, 1),
}

DARK = {
    "window": (0.03, 0.04, 0.06, 1),
    "page": (0.10, 0.11, 0.15, 1),
    "surface": (0.13, 0.14, 0.19, 1),
    "surface_muted": (0.18, 0.19, 0.24, 1),
    "text": (0.95, 0.96, 0.98, 1),
    "muted": (0.70, 0.72, 0.78, 1),
    "border": (0.22, 0.24, 0.30, 1),
    "primary": (0.34, 0.62, 0.98, 1),
    "success": (0.16, 0.80, 0.49, 1),
    "danger": (0.93, 0.36, 0.36, 1),
}

CHART_COLORS = [
    (0.06, 0.72, 0.42, 1),
    (0.23, 0.51, 0.96, 1),
    (0.55, 0.36, 0.96, 1),
    (0.96, 0.62, 0.11, 1),
    (0.93, 0.27, 0.60, 1),
    (0.90, 0.73, 0.13, 1),
    (0.02, 0.72, 0.83, 1),
]


def money_prefix(currency: str) -> str:
    return {
        "USD": "$",
        "EUR": "EUR ",
        "GBP": "GBP ",
        "NPR": "NPR ",
        "JPY": "JPY ",
    }.get(currency, f"{currency} ")


class BasePhoneScreen(Screen):
    def app(self) -> "MoneyManagerApp":
        return App.get_running_app()

    def palette(self) -> dict[str, tuple]:
        return self.app().palette

    def paint_background(self, widget, color_key: str) -> None:
        widget.canvas.before.clear()
        with widget.canvas.before:
            color = Color(*self.palette()[color_key])
            rect = Rectangle(pos=widget.pos, size=widget.size)
        widget.bind(pos=lambda inst, *_: self._sync_rect(inst, color, rect, color_key))
        widget.bind(size=lambda inst, *_: self._sync_rect(inst, color, rect, color_key))

    def _sync_rect(self, widget, color, rect, color_key: str) -> None:
        color.rgba = self.palette()[color_key]
        rect.pos = widget.pos
        rect.size = widget.size

    def styled_label(self, text: str, *, size_hint_y=None, height=None, font_size="16sp", bold=False, color_key="text", halign="left") -> Label:
        label = Label(
            text=text,
            markup=bold,
            color=self.palette()[color_key],
            size_hint_y=size_hint_y,
            height=height,
            font_size=font_size,
            halign=halign,
            valign="middle",
        )
        label.bind(size=lambda inst, *_: setattr(inst, "text_size", inst.size))
        return label

    def button(self, text: str, *, kind="primary", height=48) -> Button:
        bg = self.palette()["primary"]
        fg = (1, 1, 1, 1)
        if kind == "muted":
            bg = self.palette()["surface_muted"]
            fg = self.palette()["text"]
        elif kind == "danger":
            bg = self.palette()["danger"]
        btn = Button(
            text=text,
            size_hint_y=None,
            height=dp(height),
            background_normal="",
            background_color=bg,
            color=fg,
        )
        return btn

    def input_field(self, hint: str, *, password=False, height=48) -> TextInput:
        return TextInput(
            hint_text=hint,
            multiline=False,
            password=password,
            size_hint_y=None,
            height=dp(height),
            background_normal="",
            background_active="",
            padding=(dp(12), dp(12)),
            background_color=self.palette()["surface_muted"],
            foreground_color=self.palette()["text"],
            hint_text_color=self.palette()["muted"],
            cursor_color=self.palette()["text"],
        )

    def phone_page(self, page_bg="page", include_bottom_nav=False, active_nav=None) -> tuple[AnchorLayout, BoxLayout]:
        outer = AnchorLayout(anchor_x="center", anchor_y="center")
        self.paint_background(outer, "window")

        frame = Card(
            bg_color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(dp(454), dp(972)),
            padding=dp(12),
            spacing=0,
        )
        screen = Card(
            bg_color=self.palette()[page_bg],
            size_hint=(1, 1),
            padding=0,
            spacing=0,
        )
        outer.add_widget(frame)
        frame.add_widget(screen)

        island_row = AnchorLayout(size_hint_y=None, height=dp(42))
        island = Card(bg_color=(0, 0, 0, 1), size_hint=(None, None), size=(dp(126), dp(28)), padding=0, spacing=0)
        island_row.add_widget(island)
        screen.add_widget(island_row)

        content_area = BoxLayout(orientation="vertical", spacing=0)
        screen.add_widget(content_area)

        scroll = ScrollView(bar_width=0)
        content_box = BoxLayout(orientation="vertical", spacing=dp(12), padding=(dp(16), dp(10), dp(16), dp(16)), size_hint_y=None)
        content_box.bind(minimum_height=content_box.setter("height"))
        scroll.add_widget(content_box)
        content_area.add_widget(scroll)

        if include_bottom_nav:
            nav = Card(bg_color=self.palette()["surface"], size_hint_y=None, height=dp(72), orientation="horizontal", padding=(dp(8), dp(10), dp(8), dp(10)))
            for key, label_text in [("stats", "Stats"), ("budget", "Budget"), ("profile", "Profile")]:
                btn = Button(
                    text=label_text,
                    background_normal="",
                    background_color=self.palette()["surface"],
                    color=self.palette()["primary"] if active_nav == key else self.palette()["muted"],
                )
                btn.bind(on_release=lambda _btn, name=key: self.app().go_to(name))
                nav.add_widget(btn)
            content_area.add_widget(nav)
        return outer, content_box

    def header(self, title: str, back_target: str | None = None) -> BoxLayout:
        row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(12))
        if back_target:
            back = self.button("<", kind="muted", height=40)
            back.size_hint_x = None
            back.width = dp(40)
            back.bind(on_release=lambda *_: self.app().go_to(back_target))
            row.add_widget(back)
        row.add_widget(self.styled_label(title, font_size="28sp"))
        return row

    def section_card(self) -> Card:
        return Card(bg_color=self.palette()["surface"], spacing=dp(10))

    def divider_label(self, text: str) -> Label:
        return self.styled_label(text, color_key="muted", size_hint_y=None, height=dp(24), font_size="14sp")


class LoginScreen(BasePhoneScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root, content = self.phone_page(page_bg="surface")
        wrapper = BoxLayout(orientation="vertical", size_hint_y=None, padding=(0, dp(110), 0, 0), spacing=dp(18))
        wrapper.bind(minimum_height=wrapper.setter("height"))

        brand = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None, height=dp(120))
        brand.add_widget(self.styled_label("M M", font_size="40sp", size_hint_y=None, height=dp(60), halign="center"))
        brand.add_widget(self.styled_label("Money Managers", color_key="muted", size_hint_y=None, height=dp(28), halign="center"))
        wrapper.add_widget(brand)

        form = BoxLayout(orientation="vertical", spacing=dp(14), size_hint_y=None)
        form.bind(minimum_height=form.setter("height"))
        form.add_widget(self.styled_label("Username", size_hint_y=None, height=dp(24)))
        self.username = self.input_field("Enter your username")
        form.add_widget(self.username)
        form.add_widget(self.styled_label("Password", size_hint_y=None, height=dp(24)))
        self.password = self.input_field("Enter your password", password=True)
        form.add_widget(self.password)
        login_button = self.button("Login")
        login_button.bind(on_release=lambda *_: self.submit())
        form.add_widget(login_button)
        forgot = self.button("Forgot Password?", kind="muted", height=36)
        forgot.bind(on_release=lambda *_: self.show_message("Password reset is not automated in this build. Use Profile after logging in."))
        form.add_widget(forgot)
        register = self.button("Register", kind="muted", height=42)
        register.bind(on_release=lambda *_: self.app().go_to("register"))
        form.add_widget(register)
        self.status = self.styled_label("", color_key="muted", size_hint_y=None, height=dp(40), halign="center")
        form.add_widget(self.status)
        wrapper.add_widget(form)
        content.add_widget(wrapper)
        self.add_widget(root)

    def username_key(self, value: str) -> str:
        cleaned = "".join(ch.lower() for ch in value.strip() if ch.isalnum() or ch in "._-")
        return f"{cleaned}@local.app"

    def show_message(self, message: str) -> None:
        self.status.text = message

    def submit(self) -> None:
        user = self.app().service.login(self.username_key(self.username.text), self.password.text)
        if not user:
            self.show_message("Invalid username or password.")
            return
        self.app().login(user)


class RegisterScreen(BasePhoneScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root, content = self.phone_page(page_bg="surface")
        wrapper = BoxLayout(orientation="vertical", size_hint_y=None, padding=(0, dp(90), 0, 0), spacing=dp(18))
        wrapper.bind(minimum_height=wrapper.setter("height"))

        brand = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None, height=dp(120))
        brand.add_widget(self.styled_label("M M", font_size="40sp", size_hint_y=None, height=dp(60), halign="center"))
        brand.add_widget(self.styled_label("Create your account", color_key="muted", size_hint_y=None, height=dp(28), halign="center"))
        wrapper.add_widget(brand)

        self.name_input = self.input_field("Enter your name")
        self.password = self.input_field("Enter your password", password=True)
        self.confirm = self.input_field("Confirm your password", password=True)
        for title, field in [("Name", self.name_input), ("Password", self.password), ("Confirm Password", self.confirm)]:
            wrapper.add_widget(self.styled_label(title, size_hint_y=None, height=dp(24)))
            wrapper.add_widget(field)

        submit = self.button("Register")
        submit.bind(on_release=lambda *_: self.submit())
        wrapper.add_widget(submit)
        login = self.button("Login", kind="muted", height=42)
        login.bind(on_release=lambda *_: self.app().go_to("login"))
        wrapper.add_widget(login)
        self.status = self.styled_label("", color_key="muted", size_hint_y=None, height=dp(40), halign="center")
        wrapper.add_widget(self.status)
        content.add_widget(wrapper)
        self.add_widget(root)

    def username_key(self, value: str) -> str:
        cleaned = "".join(ch.lower() for ch in value.strip() if ch.isalnum() or ch in "._-")
        return f"{cleaned}@local.app"

    def submit(self) -> None:
        if self.password.text != self.confirm.text:
            self.status.text = "Passwords do not match."
            return
        ok, message = self.app().service.register(
            self.name_input.text,
            self.username_key(self.name_input.text),
            self.password.text,
        )
        self.status.text = message
        if ok:
            self.app().go_to("login")


class DashboardScreen(BasePhoneScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root, self.content = self.phone_page(include_bottom_nav=True)
        self.selected_month = Spinner(
            text=date.today().strftime("%B"),
            values=tuple(
                [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ]
            ),
            size_hint_y=None,
            height=dp(48),
        )
        self.selected_year = Spinner(
            text=str(date.today().year),
            values=tuple(str(year) for year in range(2022, 2027)),
            size_hint_y=None,
            height=dp(48),
        )
        self.selected_month.bind(text=lambda *_: self.refresh())
        self.selected_year.bind(text=lambda *_: self.refresh())
        self.add_widget(self.root)

    def on_pre_enter(self, *_args) -> None:
        self.refresh()

    def month_key(self) -> str:
        month_number = {
            "January": "01",
            "February": "02",
            "March": "03",
            "April": "04",
            "May": "05",
            "June": "06",
            "July": "07",
            "August": "08",
            "September": "09",
            "October": "10",
            "November": "11",
            "December": "12",
        }[self.selected_month.text]
        return f"{self.selected_year.text}-{month_number}"

    def refresh(self) -> None:
        if not self.app().current_user:
            return
        self.content.clear_widgets()
        currency = self.app().currency_symbol()
        data = self.app().db.get_dashboard_data_for_month(self.app().current_user["id"], self.month_key())

        self.content.add_widget(self.styled_label("Dashboard", size_hint_y=None, height=dp(42), font_size="30sp", halign="center"))

        selector = self.section_card()
        row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(12))
        row.add_widget(self.selected_month)
        row.add_widget(self.selected_year)
        selector.add_widget(row)
        self.content.add_widget(selector)

        summary = BoxLayout(size_hint_y=None, height=dp(110), spacing=dp(10))
        summary.add_widget(self.summary_card("Income", f"{currency}{data['income_total']:.2f}", "success"))
        summary.add_widget(self.summary_card("Expense", f"{currency}{data['expense_total']:.2f}", "danger"))
        net_color = "primary" if data["net_total"] >= 0 else "danger"
        summary.add_widget(self.summary_card("Total", f"{currency}{data['net_total']:.2f}", net_color))
        self.content.add_widget(summary)

        transactions_card = self.section_card()
        head = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(8))
        head.add_widget(self.styled_label("Transactions", size_hint_y=None, height=dp(32), font_size="22sp"))
        add_btn = self.button("Add", height=36)
        add_btn.size_hint_x = None
        add_btn.width = dp(92)
        add_btn.bind(on_release=lambda *_: self.app().open_transaction())
        head.add_widget(add_btn)
        transactions_card.add_widget(head)

        if not data["transactions"]:
            transactions_card.add_widget(self.divider_label("No transactions found for the selected month."))
        for record in data["transactions"]:
            item = Button(
                text=f"{record['description']}    {record['transaction_type'].title()}    {'+' if record['transaction_type'] == 'income' else '-'}{currency}{record['amount']:.2f}",
                size_hint_y=None,
                height=dp(58),
                background_normal="",
                background_color=self.palette()["surface"],
                color=self.palette()["success"] if record["transaction_type"] == "income" else self.palette()["danger"],
            )
            item.bind(on_release=lambda _btn, tid=record["id"]: self.app().open_transaction(tid))
            transactions_card.add_widget(item)
        self.content.add_widget(transactions_card)

    def summary_card(self, title: str, value: str, color_key: str) -> Card:
        card = Card(bg_color=self.palette()["surface"], size_hint_x=1)
        card.add_widget(self.styled_label(title, color_key="muted", size_hint_y=None, height=dp(18), font_size="12sp"))
        card.add_widget(self.styled_label(value, color_key=color_key, size_hint_y=None, height=dp(34), font_size="22sp"))
        return card


class TransactionScreen(BasePhoneScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root, self.content = self.phone_page()
        self.amount = self.input_field("0.00")
        self.type_spinner = Spinner(text="Expense", values=("Income", "Expense"), size_hint_y=None, height=dp(48))
        self.category_spinner = Spinner(text=CATEGORIES[0], values=CATEGORIES, size_hint_y=None, height=dp(48))
        self.date_input = self.input_field("YYYY-MM-DD")
        self.note = TextInput(
            hint_text="Add a note...",
            multiline=True,
            size_hint_y=None,
            height=dp(90),
            background_normal="",
            background_active="",
            padding=(dp(12), dp(12)),
            background_color=self.palette()["surface_muted"],
            foreground_color=self.palette()["text"],
            hint_text_color=self.palette()["muted"],
        )
        self.status = self.styled_label("", color_key="muted", size_hint_y=None, height=dp(30))
        self.add_widget(self.root)

    def on_pre_enter(self, *_args) -> None:
        self.refresh()

    def refresh(self) -> None:
        self.content.clear_widgets()
        title = "Update Transaction" if self.app().editing_transaction_id else "Add Transaction"
        self.content.add_widget(self.header(title, "dashboard"))

        card = self.section_card()
        card.add_widget(self.styled_label("Transaction Details", size_hint_y=None, height=dp(30), font_size="22sp"))
        for label_text, widget in [
            ("Amount", self.amount),
            ("Type", self.type_spinner),
            ("Category", self.category_spinner),
            ("Date", self.date_input),
            ("Note", self.note),
        ]:
            card.add_widget(self.styled_label(label_text, size_hint_y=None, height=dp(22)))
            card.add_widget(widget)
        save = self.button("Save")
        save.bind(on_release=lambda *_: self.save())
        card.add_widget(save)
        if self.app().editing_transaction_id:
            delete = self.button("Delete", kind="danger")
            delete.bind(on_release=lambda *_: self.delete())
            card.add_widget(delete)
        card.add_widget(self.status)
        self.content.add_widget(card)

        if self.app().editing_transaction_id:
            record = self.app().db.get_transaction(self.app().current_user["id"], self.app().editing_transaction_id)
            if record:
                self.amount.text = f"{record['amount']:.2f}"
                self.type_spinner.text = record["transaction_type"].title()
                self.category_spinner.text = record["category"]
                self.date_input.text = record["transaction_date"]
                self.note.text = record["description"]
        else:
            self.amount.text = ""
            self.type_spinner.text = "Expense"
            self.category_spinner.text = CATEGORIES[0]
            self.date_input.text = self.app().service.default_transaction_date()
            self.note.text = ""
            self.status.text = ""

    def save(self) -> None:
        ok, message = self.app().service.save_transaction(
            self.app().current_user["id"],
            self.type_spinner.text.lower(),
            self.category_spinner.text,
            self.amount.text,
            self.note.text,
            self.date_input.text,
            self.app().editing_transaction_id,
        )
        self.status.text = message
        if ok:
            self.app().editing_transaction_id = None
            self.app().go_to("dashboard")

    def delete(self) -> None:
        self.app().db.delete_transaction(self.app().current_user["id"], self.app().editing_transaction_id)
        self.app().editing_transaction_id = None
        self.app().go_to("dashboard")


class BudgetScreen(BasePhoneScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root, self.content = self.phone_page()
        self.category_spinner = Spinner(text=CATEGORIES[0], values=CATEGORIES, size_hint_y=None, height=dp(48))
        self.amount_input = self.input_field("Budget limit")
        self.month_input = self.input_field("YYYY-MM")
        self.status = self.styled_label("", color_key="muted", size_hint_y=None, height=dp(30))
        self.add_widget(self.root)

    def on_pre_enter(self, *_args) -> None:
        if not self.month_input.text:
            self.month_input.text = self.app().service.default_budget_month()
        self.refresh()

    def refresh(self) -> None:
        self.content.clear_widgets()
        currency = self.app().currency_symbol()
        self.content.add_widget(self.header("Budget", "dashboard"))
        month_key = self.month_input.text or self.app().service.default_budget_month()
        rows = self.app().db.list_budgets(self.app().current_user["id"], month_key)
        total_budget = sum(row["target_amount"] for row in rows)
        total_planned = total_budget

        total_card = self.section_card()
        total_card.add_widget(self.styled_label("Total Budget", color_key="muted", size_hint_y=None, height=dp(20), halign="center"))
        total_card.add_widget(self.styled_label(f"{currency}{total_budget:.2f}", color_key="primary", size_hint_y=None, height=dp(44), font_size="34sp", halign="center"))
        self.content.add_widget(total_card)

        planned = self.section_card()
        planned.add_widget(self.styled_label("Planned Budget", size_hint_y=None, height=dp(28), font_size="22sp"))
        planned.add_widget(self.divider_label(f"Total Planned: {currency}{total_planned:.2f}"))
        planned.add_widget(self.divider_label(f"Remaining: {currency}{max(total_budget - total_planned, 0):.2f}"))
        self.content.add_widget(planned)

        add_card = self.section_card()
        add_card.add_widget(self.styled_label("Categories", size_hint_y=None, height=dp(28), font_size="22sp"))
        add_card.add_widget(self.category_spinner)
        add_card.add_widget(self.amount_input)
        add_card.add_widget(self.month_input)
        save = self.button("Add")
        save.bind(on_release=lambda *_: self.save_budget())
        add_card.add_widget(save)
        add_card.add_widget(self.status)
        self.content.add_widget(add_card)

        list_card = self.section_card()
        list_card.add_widget(self.styled_label("Saved Categories", size_hint_y=None, height=dp(28), font_size="22sp"))
        if not rows:
            list_card.add_widget(self.divider_label("No category budgets stored for this month."))
        for row in rows:
            pct = 0 if row["target_amount"] <= 0 else (row["spent_amount"] / row["target_amount"]) * 100
            item = Card(bg_color=self.palette()["surface_muted"], size_hint_y=None, height=dp(84))
            item.add_widget(self.styled_label(f"{row['category']}    {currency}{row['target_amount']:.2f}", size_hint_y=None, height=dp(24)))
            item.add_widget(self.divider_label(f"Spent: {currency}{row['spent_amount']:.2f}"))
            item.add_widget(self.divider_label(f"{pct:.0f}% used"))
            list_card.add_widget(item)
        self.content.add_widget(list_card)

    def save_budget(self) -> None:
        ok, message = self.app().service.save_budget(
            self.app().current_user["id"],
            self.category_spinner.text,
            self.amount_input.text,
            self.month_input.text,
        )
        self.status.text = message
        if ok:
            self.amount_input.text = ""
            self.refresh()


class StatsScreen(BasePhoneScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_tab = "income"
        self.root, self.content = self.phone_page()
        self.chart = PieChartWidget(size_hint_y=None, height=dp(300))
        self.add_widget(self.root)

    def on_pre_enter(self, *_args) -> None:
        self.refresh()

    def refresh(self) -> None:
        self.content.clear_widgets()
        self.content.add_widget(self.header("Statistics", "dashboard"))
        card = self.section_card()
        card.add_widget(self.styled_label("Financial Overview", size_hint_y=None, height=dp(28), font_size="22sp"))

        tabs = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        income_btn = self.button("Income", kind="primary" if self.active_tab == "income" else "muted", height=40)
        expense_btn = self.button("Expense", kind="primary" if self.active_tab == "expense" else "muted", height=40)
        income_btn.bind(on_release=lambda *_: self.switch_tab("income"))
        expense_btn.bind(on_release=lambda *_: self.switch_tab("expense"))
        tabs.add_widget(income_btn)
        tabs.add_widget(expense_btn)
        card.add_widget(tabs)

        rows = self.app().db.get_stats_breakdown(self.app().current_user["id"], self.active_tab)
        items = [
            {"name": row["category"], "value": row["total"], "color": CHART_COLORS[index % len(CHART_COLORS)]}
            for index, row in enumerate(rows)
        ]
        self.chart.set_items(items)
        card.add_widget(self.chart)

        currency = self.app().currency_symbol()
        total = sum(item["value"] for item in items)
        if not items:
            card.add_widget(self.divider_label("No data available yet. Add transactions to populate the chart."))
        for item in items:
            pct = 0 if total <= 0 else (item["value"] / total) * 100
            row = Card(bg_color=self.palette()["surface_muted"], size_hint_y=None, height=dp(62), orientation="horizontal")
            swatch = Card(bg_color=item["color"], size_hint=(None, None), size=(dp(18), dp(18)), padding=0, spacing=0)
            row.add_widget(swatch)
            row.add_widget(self.styled_label(item["name"]))
            row.add_widget(self.styled_label(f"{currency}{item['value']:.2f}"))
            row.add_widget(self.styled_label(f"{pct:.1f}%"))
            card.add_widget(row)
        card.add_widget(self.divider_label(f"Total: {currency}{total:.2f}"))
        self.content.add_widget(card)

    def switch_tab(self, tab: str) -> None:
        self.active_tab = tab
        self.refresh()


class ProfileScreen(BasePhoneScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root, self.content = self.phone_page()
        self.name_input = self.input_field("Name")
        self.new_password = self.input_field("New password", password=True)
        self.confirm_password = self.input_field("Confirm password", password=True)
        self.email_toggle = CheckBox(active=False, size_hint=(None, None), size=(dp(34), dp(34)))
        self.notifications_toggle = CheckBox(active=True, size_hint=(None, None), size=(dp(34), dp(34)))
        self.currency_spinner = Spinner(text=CURRENCIES[0], values=CURRENCIES, size_hint_y=None, height=dp(48))
        self.theme_spinner = Spinner(text=THEMES[0], values=THEMES, size_hint_y=None, height=dp(48))
        self.email_address = self.input_field("Alert email address")
        self.status = self.styled_label("", color_key="muted", size_hint_y=None, height=dp(34))
        self.add_widget(self.root)

    def on_pre_enter(self, *_args) -> None:
        self.refresh()

    def refresh(self) -> None:
        self.content.clear_widgets()
        settings = self.app().db.get_settings(self.app().current_user["id"])

        self.content.add_widget(self.header("Profile", "dashboard"))

        profile = self.section_card()
        profile.add_widget(self.styled_label("User Profile", size_hint_y=None, height=dp(28), font_size="22sp", halign="center"))
        profile.add_widget(self.styled_label(self.app().current_user["full_name"], size_hint_y=None, height=dp(28), font_size="24sp", halign="center"))
        self.name_input.text = self.app().current_user["full_name"]
        profile.add_widget(self.name_input)
        save_name = self.button("Edit Name")
        save_name.bind(on_release=lambda *_: self.save_name())
        profile.add_widget(save_name)
        self.content.add_widget(profile)

        password_card = self.section_card()
        password_card.add_widget(self.styled_label("Change Password", size_hint_y=None, height=dp(28), font_size="22sp"))
        password_card.add_widget(self.new_password)
        password_card.add_widget(self.confirm_password)
        change = self.button("Change Password")
        change.bind(on_release=lambda *_: self.change_password())
        password_card.add_widget(change)
        self.content.add_widget(password_card)

        prefs = self.section_card()
        prefs.add_widget(self.styled_label("Preferences", size_hint_y=None, height=dp(28), font_size="22sp"))
        for label_text, widget in [
            ("Enable notifications", self.notifications_toggle),
            ("Enable email reminders", self.email_toggle),
        ]:
            row = BoxLayout(size_hint_y=None, height=dp(42))
            row.add_widget(self.styled_label(label_text))
            row.add_widget(widget)
            prefs.add_widget(row)
        self.notifications_toggle.active = bool(settings["notifications_enabled"])
        self.email_toggle.active = bool(settings["email_alerts_enabled"])
        self.currency_spinner.text = settings["currency"]
        self.theme_spinner.text = settings["theme"]
        self.email_address.text = settings["email_address"] or ""
        prefs.add_widget(self.currency_spinner)
        prefs.add_widget(self.theme_spinner)
        prefs.add_widget(self.email_address)
        save_prefs = self.button("Save Preferences")
        save_prefs.bind(on_release=lambda *_: self.save_preferences())
        prefs.add_widget(save_prefs)
        self.content.add_widget(prefs)

        danger = self.section_card()
        danger.add_widget(self.styled_label("Danger Zone", color_key="danger", size_hint_y=None, height=dp(28), font_size="22sp"))
        delete_btn = self.button("Delete Account", kind="danger")
        delete_btn.bind(on_release=lambda *_: self.delete_account())
        danger.add_widget(delete_btn)
        logout = self.button("Logout", kind="muted")
        logout.bind(on_release=lambda *_: self.app().logout())
        danger.add_widget(logout)
        danger.add_widget(self.status)
        self.content.add_widget(danger)

    def save_name(self) -> None:
        ok, message = self.app().service.update_profile_name(self.app().current_user["id"], self.name_input.text)
        self.status.text = message
        if ok:
            self.app().current_user["full_name"] = self.name_input.text.strip()
            self.refresh()

    def change_password(self) -> None:
        ok, message = self.app().service.change_password(
            self.app().current_user["id"],
            self.new_password.text,
            self.confirm_password.text,
        )
        self.status.text = message
        if ok:
            self.new_password.text = ""
            self.confirm_password.text = ""

    def save_preferences(self) -> None:
        ok, message = self.app().service.save_settings(
            self.app().current_user["id"],
            self.notifications_toggle.active,
            self.email_toggle.active,
            self.email_address.text,
            self.currency_spinner.text,
            self.theme_spinner.text,
        )
        self.status.text = message
        if ok:
            self.app().refresh_theme()

    def delete_account(self) -> None:
        self.app().db.delete_user(self.app().current_user["id"])
        self.app().logout()


class MoneyManagerApp(App):
    title = "Money Manager"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.service = MoneyManagerService(self.db)
        self.current_user = None
        self.palette = LIGHT
        self.screen_manager = ScreenManager()
        self.editing_transaction_id = None

    def build(self):
        Window.size = (540, 1060)
        Window.minimum_width = 520
        Window.minimum_height = 1020
        self.rebuild_screens("login")
        return self.screen_manager

    def rebuild_screens(self, current: str) -> None:
        for screen in list(self.screen_manager.screens):
            self.screen_manager.remove_widget(screen)
        for screen in [
            LoginScreen(name="login"),
            RegisterScreen(name="register"),
            DashboardScreen(name="dashboard"),
            TransactionScreen(name="transaction"),
            BudgetScreen(name="budget"),
            StatsScreen(name="stats"),
            ProfileScreen(name="profile"),
        ]:
            self.screen_manager.add_widget(screen)
        self.screen_manager.current = current

    def currency_symbol(self) -> str:
        if not self.current_user:
            return "$"
        settings = self.db.get_settings(self.current_user["id"])
        return money_prefix(settings["currency"])

    def login(self, user: dict) -> None:
        self.current_user = user
        self.editing_transaction_id = None
        self.refresh_theme(target="dashboard")

    def logout(self) -> None:
        self.current_user = None
        self.editing_transaction_id = None
        self.palette = LIGHT
        Window.clearcolor = self.palette["window"]
        self.rebuild_screens("login")

    def go_to(self, screen_name: str) -> None:
        self.screen_manager.current = screen_name

    def open_transaction(self, transaction_id: int | None = None) -> None:
        self.editing_transaction_id = transaction_id
        self.go_to("transaction")

    def refresh_theme(self, target: str | None = None) -> None:
        theme = "Light"
        if self.current_user:
            theme = self.db.get_settings(self.current_user["id"])["theme"]
        self.palette = DARK if theme == "Dark" else LIGHT
        Window.clearcolor = self.palette["window"]
        self.rebuild_screens(target or self.screen_manager.current or "login")
