import math
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


class ImageCanvas(Widget):
    """Tap once for the cue ball, then tap the target ball."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points = []
        self.texture_rect = None
        self.bind(pos=self.redraw, size=self.redraw)

    def redraw(self, *_):
        self.canvas.after.clear()
        with self.canvas.after:
            if len(self.points) >= 1:
                x, y = self.points[0]
                Color(1, 1, 1, 1)
                Ellipse(pos=(x-dp(7), y-dp(7)), size=(dp(14), dp(14)))
            if len(self.points) >= 2:
                x1, y1 = self.points[0]
                x2, y2 = self.points[1]
                Color(1, 0.15, 0.12, 1)
                Line(points=[x1, y1, x2, y2], width=dp(2.5))
                Color(1, 0.85, 0.1, 1)
                Ellipse(pos=(x2-dp(7), y2-dp(7)), size=(dp(14), dp(14)))

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        self.points.append(touch.pos)
        if len(self.points) > 2:
            self.points = [touch.pos]
        self.redraw()
        app = App.get_running_app()
        if len(self.points) == 1:
            app.status.text = "تم تحديد الكرة البيضاء. اضغط على الكرة المستهدفة."
        else:
            x1, y1 = self.points[0]
            x2, y2 = self.points[1]
            dx, dy = x2 - x1, y2 - y1
            angle = math.degrees(math.atan2(-dy, dx)) % 360
            distance = math.hypot(dx, dy)
            app.status.text = f"الزاوية التقريبية: {angle:.1f}°   |   المسافة: {distance:.0f} بكسل"
        return True


class DezelPoolApp(App):
    def build(self):
        self.title = "DEZEL POOL AI"
        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))

        header = Label(
            text="[b]DEZEL POOL AI[/b]\\nمساعد تحليل التصويب",
            markup=True, size_hint_y=None, height=dp(65),
            font_size="20sp", halign="center", valign="middle"
        )
        root.add_widget(header)

        buttons = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        pick = Button(text="اختيار صورة", background_color=(0.1, 0.48, 0.28, 1))
        reset = Button(text="إعادة التحديد", background_color=(0.2, 0.25, 0.32, 1))
        pick.bind(on_release=self.choose_image)
        reset.bind(on_release=self.reset_points)
        buttons.add_widget(pick)
        buttons.add_widget(reset)
        root.add_widget(buttons)

        self.status = Label(
            text="اختر لقطة شاشة، ثم اضغط على الكرة البيضاء والكرة المستهدفة.",
            size_hint_y=None, height=dp(62), halign="center", valign="middle"
        )
        root.add_widget(self.status)

        self.image_area = BoxLayout()
        self.image = Image(source="", allow_stretch=True, keep_ratio=True)
        self.overlay = ImageCanvas()
        # Overlay uses the full area; it is a visual guide and does not alter the source image.
        self.image_area.add_widget(self.image)
        self.image_area.add_widget(self.overlay)
        root.add_widget(self.image_area)

        note = Label(
            text="أداة تعليمية لحساب خط مستقيم تقريبي فقط؛ لا تتنبأ بدقة بتأثير الدوران أو التصادمات.",
            size_hint_y=None, height=dp(48), font_size="12sp",
            halign="center", valign="middle"
        )
        root.add_widget(note)
        return root

    def choose_image(self, *_):
        chooser = FileChooserIconView(
            filters=["*.png", "*.jpg", "*.jpeg", "*.webp"],
            path=os.path.expanduser("~")
        )
        box = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(6))
        box.add_widget(chooser)
        controls = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        cancel = Button(text="إلغاء")
        select = Button(text="فتح الصورة")
        controls.add_widget(cancel)
        controls.add_widget(select)
        box.add_widget(controls)
        popup = Popup(title="اختر لقطة شاشة", content=box, size_hint=(0.95, 0.9))
        cancel.bind(on_release=popup.dismiss)

        def load_selected(*_):
            if chooser.selection:
                path = chooser.selection[0]
                self.image.source = path
                self.image.reload()
                self.overlay.points = []
                self.overlay.redraw()
                self.status.text = "الصورة جاهزة. اضغط على الكرة البيضاء ثم الكرة المستهدفة."
                popup.dismiss()

        select.bind(on_release=load_selected)
        popup.open()

    def reset_points(self, *_):
        self.overlay.points = []
        self.overlay.redraw()
        self.status.text = "تمت إعادة التحديد. اضغط على الكرة البيضاء ثم الكرة المستهدفة."


if __name__ == "__main__":
    DezelPoolApp().run()
