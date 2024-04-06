from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from plyer import gps

class GPSApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Waiting for GPS coordinates...', size_hint=(1, 0.8))
        self.layout.add_widget(self.label)
        return self.layout

    def on_start(self):
        try:
            # Configure GPS
            gps.configure(on_location=self.on_location)
            gps.start()

            # Schedule updating the location every 1 second
            Clock.schedule_interval(self.update_location, 1)
        except NotImplementedError:
            self.label.text = 'GPS functionality not supported on this platform.'

    def on_location(self, **kwargs):
        latitude = kwargs.get('lat')
        longitude = kwargs.get('lon')
        altitude = kwargs.get('altitude')
        self.label.text = f'Latitude: {latitude}\nLongitude: {longitude}\nAltitude: {altitude}'

    def update_location(self, dt):
        try:
            # Request a single location update
            gps.get_location()
        except NotImplementedError:
            self.label.text = 'GPS functionality not supported on this platform.'

    def on_stop(self):
        # Stop GPS when the app is stopped
        gps.stop()

if __name__ == '__main__':
    GPSApp().run()