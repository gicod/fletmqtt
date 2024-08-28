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
    data = [{'msg','topic','time'}]
    
    def on_message(client, userdata, message):
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
        
    topic_input = ft.TextField(label="Введите топик для отправки", value=topic_for_publish)
        
    text_input = ft.TextField(label="Введите сообщение", value='activate', bgcolor=ft.colors.CYAN_900)
    button = ft.ElevatedButton(text="Отправить", on_click=lambda e: on_button_click(msg = text_input.value))
    
    text_input_2 = ft.TextField(label="Введите сообщение", value='finish', bgcolor=ft.colors.TEAL_900)
    button_2 = ft.ElevatedButton(text="Отправить", on_click=lambda e: on_button_click(msg = text_input_2.value))
    
    btn_clear = ft.ElevatedButton(text="Очистить историю", on_click=on_btn_clear)

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Сообщение")),
            ft.DataColumn(ft.Text("Топик")),
            ft.DataColumn(ft.Text("Время"))
        ]
    )
    
    page.add(
        topic_input, 
        text_input, button, 
        text_input_2, button_2, 
        btn_clear,
        data_table
    )

ft.app(target=main)