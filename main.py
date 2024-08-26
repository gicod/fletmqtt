import flet as ft
import paho.mqtt.client as mqtt
import datetime

def main(page: ft.Page):
    page.title = 'First'
    page.adaptive = True
    page.scroll = True
    page.window.width= 400
    
    # Настройки MQTT
    broker_address = "localhost"  # Замените на ваш адрес брокера
    port = 1883
    topic_for_publish = "test/topic"  # Топик для отправки сообщений
    topic_for_subscribe = "#"  # Топик для подписки
    
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Получено сообщение: {msg}")
        print(f"Топик: {message.topic}")
        print(f"Время: {timestamp}")

        # Обновляем интерфейс Flet, например, отобразив полученное сообщение в таблице
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
        
    # Создаем клиента MQTT
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address, port=port)
    client.subscribe(topic_for_subscribe)
    client.loop_start()

    def on_button_click(client):
        msg = text_input.value
        topic = topic_input.value
        client.publish(topic, msg)
        print(f"Отправлено сообщение: {msg} в топик {topic}")
        # text_input.value = ""   

    # Создаем интерфейс Flet
    topic_input = ft.TextField(label="Введите топик для отправки", value=topic_for_publish)
    text_input = ft.TextField(label="Введите сообщение")
    button = ft.ElevatedButton(text="Отправить", on_click=lambda e: on_button_click(client))

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Сообщение")),
            ft.DataColumn(ft.Text("Топик")),
            ft.DataColumn(ft.Text("Время"))
        ]
    )
    page.add(topic_input, text_input, button, data_table)

ft.app(target=main)