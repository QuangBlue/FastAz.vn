from kivy.uix.screenmanager import Screen, SlideTransition


class Test123(Screen):
    def testing123(self):
        self.parent.transition = SlideTransition(direction="right")
        self.parent.current = self.parent.current = "Test"
        self.parent.transition = SlideTransition(direction="left")
