from kivy.app import App
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import mysql.connector

class SearchPopup(Popup):
    def __init__(self, data, **kwargs):
        super(SearchPopup, self).__init__(**kwargs)
        self.data = data

        layout = BoxLayout(orientation='vertical')

        # Adding horizontal layout for search input and button
        search_layout = BoxLayout(size_hint=(1, 0.1))

        # Adding search box
        self.search_input = TextInput(hint_text='Search', multiline=False)
        search_layout.add_widget(self.search_input)

        # Adding search button
        search_button = Button(text='Search', size_hint=(None, 1))
        search_button.bind(on_press=self.search_employee)
        search_layout.add_widget(search_button)

        layout.add_widget(search_layout)

        # Adding title label
        title_label = Label(text="Search Result", font_size=24, size_hint=(1, 0.1))
        layout.add_widget(title_label)

        # Creating table layout for data display
        self.table_layout = BoxLayout(orientation='vertical')
        self.update_table_layout()

        # Adding scroll view for the table layout
        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(self.table_layout)
        layout.add_widget(scroll_view)

        # Adding back button
        back_button = Button(text='Back', size_hint=(None, None), size=(100, 40), pos_hint={'x': 0, 'y': 0})
        back_button.bind(on_press=self.dismiss_search_popup)
        layout.add_widget(back_button)

        self.content = layout

    def dismiss_search_popup(self, instance):
        self.dismiss()

    def update_table_layout(self):
        # Clear previous content
        self.table_layout.clear_widgets()

        if self.data:
            # Adding data to the table layout
            for item in self.data:
                label = Label(text=item['text'])
                self.table_layout.add_widget(label)
        else:
            label = Label(text="No results found.")
            self.table_layout.add_widget(label)

    def search_employee(self, instance):
        search_text = self.search_input.text
        search_result = self.perform_search(search_text)
        self.data = search_result
        self.update_table_layout()

    def perform_search(self, search_text):
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pass@123',
            database='gaurav_connection'
        )

        cursor = connection.cursor(dictionary=True)

        # Execute the search query
        query = "SELECT * FROM employee01 WHERE emp_id = %s OR emp_name = %s"
        cursor.execute(query, (search_text, search_text))

        # Fetch all rows
        search_result = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Convert search result into the expected format
        formatted_result = [{
                                'text': f"ID: {row['Emp_Id']}, Name: {row['Emp_Name']}, Salary: {row['Emp_Salary']}, City: {row['Emp_City']}, Department: {row['Emp_Department']}"}
                            for row in search_result]

        return formatted_result

class TablePopup(Popup):
    def __init__(self, data, **kwargs):
        super(TablePopup, self).__init__(**kwargs)
        self.data = data

        layout = BoxLayout(orientation='vertical')

        # Adding title label
        title_label = Label(text="Your Registration is Successful", font_size=24, size_hint=(1, 0.1))
        layout.add_widget(title_label)

        # Creating table layout for data display
        table_layout = BoxLayout(orientation='vertical')

        # Adding data to the table layout
        for item in self.data:
            label = Label(text=item['text'])
            table_layout.add_widget(label)

        # Adding scroll view for the table layout
        scroll_view = ScrollView(size_hint=(1, 0.3))  # Adjust as needed
        scroll_view.add_widget(table_layout)
        layout.add_widget(scroll_view)

        # Adding input fields for update and delete operations
        input_layout = BoxLayout(orientation='vertical')

        # Emp_Id input
        self.id_input = TextInput(hint_text='Emp_Id', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                  size_hint=(None, None), size=(400, 40))
        input_layout.add_widget(self.id_input)

        # Emp_Name input
        self.name_input = TextInput(hint_text='Emp_Name', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                    size_hint=(None, None), size=(400, 40))
        input_layout.add_widget(self.name_input)

        # Emp_Salary input
        self.salary_input = TextInput(hint_text='Emp_Salary', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                      size_hint=(None, None), size=(400, 40))
        input_layout.add_widget(self.salary_input)

        # Emp_City input
        self.city_input = TextInput(hint_text='Emp_City', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                    size_hint=(None, None), size=(400, 40))
        input_layout.add_widget(self.city_input)

        # Emp_Department input
        self.department_input = TextInput(hint_text='Emp_Department', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                          size_hint=(None, None), size=(400, 40))
        input_layout.add_widget(self.department_input)

        # Update button
        update_button = Button(text='Update in MySQL', size_hint=(None, None),
                               pos_hint={'center_x': 0.5, 'center_y': 0.2}, size=(200, 40))
        update_button.bind(on_press=self.update_in_mysql)
        input_layout.add_widget(update_button)

        # Delete button
        delete_button = Button(text='Delete in MySQL', size_hint=(None, None),
                               pos_hint={'center_x': 0.5, 'center_y': 0.2}, size=(200, 40))
        delete_button.bind(on_press=self.delete_from_mysql)
        input_layout.add_widget(delete_button)

        # Result label
        self.result_label = Label(text='', size_hint=(1, None), height=50)
        input_layout.add_widget(self.result_label)

        layout.add_widget(input_layout)

        move_layout = GridLayout(cols=3, size_hint_y=None, height=40)

        # Close button
        close_button = Button(text='Close', size_hint=(None, None), size=(100, 40), pos_hint={'x': 0, 'y': 0})
        close_button.bind(on_press=self.close_app)
        move_layout.add_widget(close_button)

        # Back button
        back_button = Button(text='Back', size_hint=(None, None), size=(100, 40), pos_hint={'right': 1, 'y': 0})
        back_button.bind(on_press=self.go_back)
        move_layout.add_widget(back_button)

        search_button = Button(text='Search', size_hint=(None, None),
                               pos_hint={'right': 1, 'y': 0}, size=(100, 40))
        search_button.bind(on_press=self.search_employee)
        move_layout.add_widget(search_button)

        layout.add_widget(move_layout)

        self.content = layout

    def go_back(self, instance):
        self.dismiss()

    def close_app(self, instance):
        App.get_running_app().stop()

    def update_in_mysql(self, instance):
        Emp_Id_value = self.id_input.text
        Emp_Name_value = self.name_input.text
        Emp_Salary_value = self.salary_input.text
        Emp_City_value = self.city_input.text
        Emp_Department_value = self.department_input.text

        try:
            # Connect to MySQL
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Pass@123',
                database='gaurav_connection'
            )

            cursor = connection.cursor()

            # Execute the UPDATE query
            query = "UPDATE employee01 SET Emp_Name=%s, Emp_Salary=%s, Emp_City=%s, Emp_Department=%s WHERE Emp_Id=%s"
            values = (Emp_Name_value, Emp_Salary_value, Emp_City_value, Emp_Department_value, Emp_Id_value)
            cursor.execute(query, values)

            connection.commit()
            connection.close()

            self.result_label.text = "Data updated in MySQL successfully!"

        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
            self.show_error_message(f"MySQL Error: {e}")

        except Exception as e:
            print(f"Error: {e}")
            self.show_error_message(f"Error: {e}")

    def delete_from_mysql(self, instance):
        Emp_Id_value = self.id_input.text

        try:
            # Connect to MySQL
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Pass@123',
                database='gaurav_connection'
            )
            cursor = connection.cursor()

            # Execute the DELETE query
            query = "DELETE FROM employee01 WHERE Emp_Id=%s"
            cursor.execute(query, (Emp_Id_value,))
            connection.commit()
            connection.close()

            self.result_label.text = "Data deleted from MySQL successfully!"

        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
            self.show_error_message(f"MySQL Error: {e}")

        except Exception as e:
            print(f"Error: {e}")
            self.show_error_message(f"Error: {e}")

    def search_employee(self, instance):
        # Perform search operation and display the results in another popup
        emp_id = self.id_input.text
        search_result = self.perform_search(emp_id)
        search_popup = SearchPopup(data=search_result)
        search_popup.open()

    def perform_search(self, emp_id):
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pass@123',
            database='gaurav_connection'
        )

        cursor = connection.cursor(dictionary=True)

        # Execute the search query
        query = "SELECT * FROM employee01 WHERE emp_id = %s OR emp_name = %s"
        cursor.execute(query, (emp_id, emp_id))

        # Fetch all rows
        search_result = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Convert search result into the expected format
        formatted_result = [{
                                'text': f"ID: {row['emp_id']}, Name: {row['emp_name']}, Salary: {row['emp_salary']}, City: {row['emp_city']}, Department: {row['emp_department']}"}
                            for row in search_result]

        return formatted_result


class MyApp(App):
    data = ListProperty([])  # Data property for RecycleView
    Window.clearcolor = (0.8, 0.8, 0.8, 1)
    popup = None

    def build(self):
        self.layout = BoxLayout(orientation='horizontal')

        # Left side: Original content
        left_layout = BoxLayout(orientation='vertical')

        left_layout.add_widget(Label(text='Register Here', font_size=30))

        self.id_input = TextInput(hint_text='Emp_Id', size_hint=(None, None), width=400, height=50,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5})
        left_layout.add_widget(self.id_input)

        self.name_input = TextInput(hint_text='Emp_Name', size_hint=(None, None), width=400, height=50,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5})
        left_layout.add_widget(self.name_input)

        self.salary_input = TextInput(hint_text='Emp_Salary', size_hint=(None, None), width=400, height=50,
                                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        left_layout.add_widget(self.salary_input)

        self.city_input = TextInput(hint_text='Emp_City', size_hint=(None, None), width=400, height=50,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5})
        left_layout.add_widget(self.city_input)

        self.department_input = TextInput(hint_text='Emp_Department', size_hint=(None, None), width=400, height=50,
                                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        left_layout.add_widget(self.department_input)

        self.save_button = Button(text='Save to MySQL', on_press=self.save_to_mysql, size_hint=(None, None), width=400,
                                  height=50, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        left_layout.add_widget(self.save_button)

        left_layout.add_widget(Label(text=' '))

        button_grid = GridLayout(cols=6, size_hint_y=None, height=100)

        close_button = Button(text='Close', size_hint=(None, None), size=(100, 40), pos_hint={'x': 0, 'y': 0})
        close_button.bind(on_press=self.close_app)
        button_grid.add_widget(close_button)

        button_grid.add_widget(Label(text=''))
        # Search Window button
        search_button = Button(text='Search Window', on_press=self.open_search_popup, size_hint=(None, None),
                               size=(150, 40))
        button_grid.add_widget(search_button)

        # Update Window button

        update_button = Button(text='Update Window', size_hint=(None, None), height=40, width=150,
                               on_press=self.open_update_popup)
        button_grid.add_widget(update_button)

        left_layout.add_widget(button_grid)
        self.layout.add_widget(left_layout)

        return self.layout

    def close_app(self, instance):
        App.get_running_app().stop()

    def save_to_mysql(self, instance=None):
        Emp_Id_value = self.id_input.text
        Emp_Name_value = self.name_input.text
        Emp_Salary_value = self.salary_input.text
        Emp_City_value = self.city_input.text
        Emp_Department_value = self.department_input.text

        try:
            # Connect to MySQL
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Pass@123',
                database='gaurav_connection'
            )

            cursor = connection.cursor()

            query = "INSERT INTO employee01 (Emp_Id, Emp_Name, Emp_Salary, Emp_City, Emp_Department) VALUES (%s, %s, %s, %s, %s)"
            values = (Emp_Id_value, Emp_Name_value, Emp_Salary_value, Emp_City_value, Emp_Department_value)

            cursor.execute(query, values)

            connection.commit()
            connection.close()

            # self.result_label.text = "Data saved to MySQL successfully!"

            # Update RecycleView data
            new_data = {
                'text': f'ID: {Emp_Id_value}, Name: {Emp_Name_value}, Salary: {Emp_Salary_value}, City: {Emp_City_value}, Department: {Emp_Department_value}'}
            # self.rv.data.append(new_data)

            # Open the pop-up window
            self.popup = TablePopup(data=[new_data])
            self.popup.open()

        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
            # self.result_label.text = f"MySQL Error: {e}"
            self.show_error_message(f"MySQL Error: {e}")

        except Exception as e:
            print(f"Error: {e}")
            # self.result_label.text = f"Error: {e}"
            self.show_error_message(f"Error: {e}")

    def show_error_message(self, message):
        # Determine the height of the error box based on the length of the message
        error_height = max(len(message.split('\n')) * 20, 200)  # Adjust the factor (20) as needed
        error_popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None),
                            size=(800, error_height))
        error_popup.open()

    def open_search_popup(self, instance):
        search_popup = SearchPopup(data=self.data)
        search_popup.open()

    def open_update_popup(self, instance):
        self.popup = TablePopup(data=self.data)
        self.popup.open()

if __name__ == '__main__':
    MyApp().run()
