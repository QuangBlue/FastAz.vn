from kivy.uix.screenmanager import Screen, SlideTransition


class PushProductsScreen(Screen):
    def testing123(self):
        self.parent.transition = SlideTransition(direction="right")
        self.parent.current = self.parent.current = "sign_in_screen"
        self.parent.transition = SlideTransition(direction="left")
