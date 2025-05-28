from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import requests
import json
import os
from datetime import datetime

THINGSBOARD_TOKEN = os.getenv('THINGSBOARD_TOKEN', 'pCNDucPvl95tmuzPzNzE')
THINGSBOARD_URL = f"https://thingsboard.cloud/api/v1/{THINGSBOARD_TOKEN}/telemetry"


class IoTDashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 10

        # Área de visualización de datos
        self.data_display = TextInput(
            text='Presione "Obtener Datos" para comenzar...\n',
            size_hint=(1, 0.6),
            readonly=True,
            background_color='#333333',
            foreground_color='white'
        )
        self.add_widget(self.data_display)

        # Botones de control
        btn_layout = BoxLayout(size_hint=(1, 0.2))
        self.get_btn = Button(
            text="Obtener Datos",
            background_color='#4CAF50',
            on_press=self.get_json_data
        )
        self.send_btn = Button(
            text="Enviar a ThingsBoard",
            background_color='#2196F3',
            on_press=self.send_to_tb
        )
        btn_layout.add_widget(self.get_btn)
        btn_layout.add_widget(self.send_btn)
        self.add_widget(btn_layout)

    def update_display(self, message):
        self.data_display.text += f"\n{message}"

    def get_json_data(self, instance):
        self.update_display("[+] Solicitando datos al dispositivo...")
        Clock.schedule_once(lambda dt: self.fetch_data())

    def fetch_data(self):
        try:
            response = requests.get("http://192.168.4.1/METER", timeout=10)
            response.raise_for_status()
            self.meter_data = json.loads(response.content.decode())

            self.update_display("\n[✔] Datos obtenidos correctamente:")
            self.update_display(f"- Horas: {self.meter_data.get('horas', 'N/A')}")
            self.update_display(f"- Días: {self.meter_data.get('dias', 'N/A')}")
            self.update_display(f"- Meses: {self.meter_data.get('meses', 'N/A')}")

            if 'ultima_actualizacion' in self.meter_data:
                timestamp = datetime.fromtimestamp(self.meter_data['ultima_actualizacion'])
                self.update_display(f"- Última actualización: {timestamp.strftime('%d/%m/%Y %H:%M')}")

            self.send_btn.disabled = False

        except Exception as e:
            self.update_display(f"\n[!] Error: {str(e)}")

    def send_to_tb(self, instance):
        self.update_display("\n[↑] Enviando datos a ThingsBoard...")
        Clock.schedule_once(lambda dt: self.upload_data())

    def upload_data(self):
        try:
            response = requests.post(THINGSBOARD_URL, json=self.meter_data)
            response.raise_for_status()
            self.update_display(f"[✔] Envío exitoso (Código: {response.status_code})")
        except Exception as e:
            self.update_display(f"[!] Error de envío: {str(e)}")


class MainApp(App):
    def build(self):
        self.title = "Dashboard IoT Integrado"
        return IoTDashboard()


if __name__ == "__main__":
    MainApp().run()