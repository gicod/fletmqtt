import flet as ft

class ContPublish(ft.UserControl):
    def __init__(self, mqtt_publish) -> None:
        super().__init__()        
        self.mqtt_publish = mqtt_publish
        self.topic = ft.TextField(label="Топик для отправки", value='/er/r/cmd')
        self.msg = ft.TextField(label="Топик для отправки", value='1'),
        self.btn = ft.OutlinedButton(text=f'Активировать', on_click=self.btn_on_click_publish(msg=self.msg.value))
        self.msg2 = ft.TextField(label="Топик для отправки", value='a'),
        self.btn2 = ft.OutlinedButton(text=f'Активировать', on_click=self.btn_on_click_publish(msg=self.msg2.value))
        self.container = ft.Container(
            content=ft.Column([
                ft.Row([
                    self.topic
                ]),
                ft.Row([
                    self.msg,                    
                    self.btn
                ]),
                ft.Row([
                    self.msg2,                    
                    self.btn2
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]),
            padding=10,
            bgcolor=ft.colors.WHITE12,
            border_radius=10,
            width=350,
        )
             
    def btn_on_click_publish(self, e, msg):
        self.mqtt_publish(self.topic.value, msg)
    
    def build(self) -> ft.Row:
        self.line = ft.Row(
            [
                self.container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        return self.line