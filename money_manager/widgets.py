from __future__ import annotations

from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget


class Card(BoxLayout):
    def __init__(self, bg_color: tuple[float, float, float, float], **kwargs):
        super().__init__(orientation="vertical", padding=16, spacing=10, **kwargs)
        self.bg_color = bg_color
        with self.canvas.before:
            self._color = Color(*self.bg_color)
            self._rect = RoundedRectangle(radius=[18])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *_args) -> None:
        self._color.rgba = self.bg_color
        self._rect.pos = self.pos
        self._rect.size = self.size


class MetricCard(Card):
    def __init__(self, title: str, value: str, subtitle: str, palette: dict[str, tuple], **kwargs):
        super().__init__(bg_color=palette["surface"], size_hint_y=None, height=130, **kwargs)
        self.add_widget(Label(text=title, color=palette["muted"], halign="left", valign="middle"))
        self.add_widget(
            Label(
                text=value,
                color=palette["text"],
                font_size="26sp",
                bold=True,
                halign="left",
                valign="middle",
            )
        )
        self.add_widget(Label(text=subtitle, color=palette["muted"], halign="left", valign="middle"))


class ProgressList(Card):
    def __init__(self, title: str, palette: dict[str, tuple], **kwargs):
        super().__init__(bg_color=palette["surface"], **kwargs)
        self.palette = palette
        self.add_widget(
            Label(
                text=title,
                color=palette["text"],
                size_hint_y=None,
                height=28,
                halign="left",
                valign="middle",
            )
        )
        self.content = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height"))
        self.add_widget(self.content)

    def set_items(self, items: list[tuple[str, float, float, str]]) -> None:
        self.content.clear_widgets()
        if not items:
            self.content.add_widget(
                Label(
                    text="No data available yet.",
                    color=self.palette["muted"],
                    size_hint_y=None,
                    height=32,
                )
            )
            return
        for label_text, value, maximum, meta in items:
            row = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None, height=62)
            row.add_widget(
                Label(
                    text=f"{label_text}    {meta}",
                    color=self.palette["text"],
                    size_hint_y=None,
                    height=24,
                    halign="left",
                    valign="middle",
                )
            )
            progress = ProgressBar(max=max(maximum, 1), value=value)
            row.add_widget(progress)
            self.content.add_widget(row)


class PieChartWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []
        self.bind(pos=self.redraw, size=self.redraw)

    def set_items(self, items):
        self.items = items
        self.redraw()

    def redraw(self, *_args):
        self.canvas.clear()
        if not self.items:
            return
        total = sum(item["value"] for item in self.items) or 1
        diameter = min(self.width, self.height) * 0.72
        x = self.center_x - diameter / 2
        y = self.center_y - diameter / 2
        angle = 0
        with self.canvas:
            for item in self.items:
                slice_angle = 360 * (item["value"] / total)
                Color(*item["color"])
                Ellipse(pos=(x, y), size=(diameter, diameter), angle_start=angle, angle_end=angle + slice_angle)
                angle += slice_angle
