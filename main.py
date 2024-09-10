import flet as ft
import paho.mqtt.client as mqtt
import datetime

def main(page: ft.Page):
    page.title = 'fletmqtt'
    page.adaptive = True
    page.scroll = True
    page.window.width= 400
    
    broker_address = "192.168.31.131"
    port = 1883
    # topic_for_publish = "test/topic"
    topic_for_publish = '/er/radar/cmd'
    topic_for_subscribe = "#"
    topic_ignored_for_subscribe = '/er/riddles/info'
    data = [{'msg','topic','time'}]
    
    def on_message(client, userdata, message):
        if message.topic.startswith(topic_ignore.value):
            return
    
        msg = str(message.payload.decode("utf-8"))
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Получено сообщение:\t{msg} Топик:\t{message.topic}\tВремя: {timestamp}")
        
        data_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(msg)),
                    ft.DataCell(ft.Text(message.topic)),
                    ft.DataCell(ft.Text(timestamp))
                ]
            )
        )
        page.update()
        
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address, port=port)
    client.subscribe(topic_for_subscribe)
    client.loop_start()

    def on_button_click(msg):
        topic = topic_input.value
        client.publish(topic, msg)
        print(f"Отправлено сообщение: {msg} в топик {topic}")

    def on_btn_clear(e):
        print("Очистка истории сообщений")
        data_table.rows.clear()
        page.update()
        
    topic_input = ft.TextField(label="Топик отправки", value=topic_for_publish, width=180)
    topic_ignore = ft.TextField(label="Топик игнора", value=topic_ignored_for_subscribe, width=180)
        
    text_input = ft.TextField(label="Введите сообщение", value='activate', bgcolor=ft.colors.CYAN_900, width=220)
    button = ft.ElevatedButton(text="Отправить", on_click=lambda e: on_button_click(msg = text_input.value))
    
    text_input_2 = ft.TextField(label="Введите сообщение", value='finish', bgcolor=ft.colors.TEAL_900, width=220)
    button_2 = ft.ElevatedButton(text="Отправить", on_click=lambda e: on_button_click(msg = text_input_2.value))
    
    btn_clear = ft.ElevatedButton(text="Очистить историю", on_click=on_btn_clear, color=ft.colors.GREEN, bgcolor=ft.colors.WHITE24)

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Сообщение")),
            ft.DataColumn(ft.Text("Топик")),
            ft.DataColumn(ft.Text("Время"))
        ]
    )
            
    bnts_publish = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.ElevatedButton(text='0', on_click=lambda e: on_button_click(msg = '0')),
                ft.ElevatedButton(text='1', on_click=lambda e: on_button_click(msg = '1')),
                ft.ElevatedButton(text='2', on_click=lambda e: on_button_click(msg = '2')),
                ft.ElevatedButton(text='3', on_click=lambda e: on_button_click(msg = '3')),
                ft.ElevatedButton(text='4', on_click=lambda e: on_button_click(msg = '4'))
            ])
        ]),
        padding=10,
        bgcolor=ft.colors.WHITE12,
        border_radius=10
    )
        
    page.add(
        ft.Row([topic_input, topic_ignore], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([text_input, button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([text_input_2, button_2], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([bnts_publish], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([btn_clear], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([data_table], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)