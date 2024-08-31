import flet as ft
import paho.mqtt.client as mqtt
import datetime

from cont_publish import ContPublish as cp

def main(page: ft.Page):
    page.title = 'fletmqtt'
    page.adaptive = True
    page.scroll = True
    page.window.width= 400
    
    broker_address = "192.168.10.1"
    # broker_address = "192.168.31.131"
    port = 1883
    # topic_for_publish = "test/topic"
    topic_for_publish = '/er/radar/cmd'
    topic_for_subscribe = "#"
    topic_ignored_for_subscribe = '/er/riddles/info'
    # data = [{'msg','topic','time'}]
    
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

    def btn_on_click_publish(topic, msg):
        
        print(f"Отправлено сообщение: {msg} в топик {topic}")
        client.publish(topic, msg)

    def btn_on_click_clear_history(e):
        print("Очистка истории сообщений")
        data_table.rows.clear()
        page.update()
        
    topic_input = ft.TextField(label="Топик для отправки", value=topic_for_publish)
    topic_ignore = ft.TextField(label="Топик для игнора", value=topic_ignored_for_subscribe)
        
    text_input = ft.TextField(label="Введите сообщение", value='activate', bgcolor=ft.colors.CYAN_900)
    button = ft.ElevatedButton(text="Отправить", on_click=lambda e: btn_on_click_publish(topic = topic_input.value, msg = text_input.value))
    
    text_input_2 = ft.TextField(label="Введите сообщение", value='finish', bgcolor=ft.colors.TEAL_900)
    button_2 = ft.ElevatedButton(text="Отправить", on_click=lambda e: btn_on_click_publish(topic = topic_input.value, msg = text_input_2.value))
    
    btn_clear = ft.ElevatedButton(text="Очистить историю", on_click=btn_on_click_clear_history)

    cont_publish = cp(btn_on_click_publish)
    
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Сообщение")),
            ft.DataColumn(ft.Text("Топик")),
            ft.DataColumn(ft.Text("Время"))
        ]
    )
    
    page.add(
        topic_input, 
        topic_ignore, 
        text_input, button, 
        text_input_2, button_2, 
        cont_publish,
        btn_clear,
        data_table
    )

ft.app(target=main)