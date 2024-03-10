import json

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivymd.uix.list import *
from kivy.clock import Clock

from fusion_brain import fb_requests
from interface import colors
from interface import text
from interface import vars
from img_create import image_create


class MainApp(MDApp):
    def build(self):
        # установка тёмной темы
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.material_style = "M3"

        # TODO переделать на ввод ключей при старте приложения

        # чтение ключей из файла keys.json
        with open("keys.json") as keys_file:
            api_keys = json.load(keys_file)

        # объект взаимодействия с API Fusion Brain
        fb_request = fb_requests.FBRequest(api_keys["api_key"], api_keys["secret_api_key"])
        # получение ID модели нейросети
        # TODO проверка правильности API ключей
        model_id = fb_request.get_model()

        # основной блок
        main_layout = MDBoxLayout(orientation="vertical",  # ориентация блоков внутри
                                  md_bg_color=colors.FB_DARK_GRAY,  # цвет фона
                                  )

        # верхняя панель
        top_toolbar = MDTopAppBar(title=text.TITLE,  # загловок
                                  shadow_color=colors.FB_BLACK,  # цвет тени
                                  specific_text_color=colors.FB_GREEN,  # цвет текста и иконок
                                  left_action_items=[  # кнопки слева
                                      ["home"],
                                      ["dots-vertical"],
                                  ],
                                  right_action_items=[  # кнопки справа
                                      ["android"],
                                      ["phone"]
                                  ],
                                  md_bg_color=colors.FB_BLACK,  # цвет фона
                                  )

        # нижнее меню навигации
        bottom_menu = MDBottomNavigation(panel_color=colors.FB_BLACK,  # цвет панели
                                         selected_color_background=colors.FB_DARK_GRAY,  # цвет кнопки выбранной вкладки
                                         text_color_active=colors.FB_GREEN,  # цвет текста и иконок кнопки выбранной вкладки
                                         )

        # вкладка меню очередь генерации
        menu_left = MDBottomNavigationItem(name="Menu_left",  # атрибут, нужный для обращения
                                           icon="format-list-bulleted",  # иконка
                                           text=text.LEFT_MENU,  # текст
                                           )

        # вкладка генерации
        menu_center = MDBottomNavigationItem(name="Menu_center",  # атрибут, нужный для обращения
                                             icon="motion-play-outline",  # иконка
                                             text=text.CENTER_MENU,  # текст
                                             )

        # вкладка галереи
        menu_right = MDBottomNavigationItem(name="Menu_right",  # атрибут, для обращения
                                            icon="image-multiple-outline",  # иконка
                                            text=text.RIGHT_MENU,  # текст
                                            )

        # убирание значка о завершённых генерациях при нажатии на левую вкладку
        def clear_new_result_icon(self):
            self.badge_icon = ""

        menu_left.bind(on_tab_press=clear_new_result_icon)

        # центральная вкладка - генератор
        page_generator = MDFloatLayout()

        # текстовое поле ввода промпта
        prompt_text_field = MDTextField(size_hint=(0.9, None),  # размер в процентах от размера блока
                                        pos_hint={  # позиция относительно блока
                                            "center_x": 0.5,
                                            "center_y": 0.9
                                        },
                                        mode="rectangle",  # режим текстового поля
                                        hint_text=text.PROMPT_HINT_TEXT,  # текст подписи поля
                                        hint_text_color_normal=colors.FB_GRAY,  # цвет подписи
                                        hint_text_color_focus=colors.FB_WHITE,  # цвет подписи при вводе
                                        text_color_focus=colors.FB_WHITE,  # цвет текста при вводе
                                        max_text_length=1000,  # максимальный размер вводимого текста в символах
                                        active_line=True,  # линия под текстом при вводе
                                        allow_copy=True,  # разрешить копирование
                                        base_direction="ltr",  # направление текста
                                        cursor_blink=True,  # мигание курсора
                                        helper_text=text.PROMPT_HELPER_TEXT,  # текст при срабатывании ошибки
                                        helper_text_mode="on_error",  # когда выводить текст helper
                                        multiline=False,  # многострочный ввод
                                        )

        # текстовое поле ввода ширины
        width_text_field = MDTextField(size_hint=(0.4, None),  # размер в процентах от размера блока
                                       pos_hint={  # позиция относительно блока
                                            "center_x": 0.25,
                                            "center_y": 0.7
                                       },
                                       mode="rectangle",  # режим текстового поля
                                       hint_text=text.WIDTH_HINT_TEXT,  # текст подписи поля
                                       hint_text_color_normal=colors.FB_GRAY,  # цвет подписи
                                       hint_text_color_focus=colors.FB_WHITE,  # цвет подписи при вводе
                                       text_color_focus=colors.FB_WHITE,  # цвет текста при вводе
                                       text="1024",  # текст по умолчанию
                                       active_line=True,  # линия под текстом при вводе
                                       allow_copy=True,  # разрешить копирование
                                       base_direction="ltr",  # направление текста
                                       cursor_blink=True,  # мигание курсора
                                       helper_text=text.WIDTH_HELPER_TEXT,  # текст при срабатывании ошибки
                                       helper_text_mode="on_error",  # когда выводить текст helper
                                       input_filter="int",  # ввод только целых чисел
                                       )

        # текстовое поле ввода высоты
        height_text_field = MDTextField(size_hint=(0.4, None),  # размер в процентах от размера блока
                                        pos_hint={  # позиция относительно блока
                                           "center_x": 0.75,
                                           "center_y": 0.7
                                        },
                                        mode="rectangle",  # режим текстового поля
                                        hint_text=text.HEIGHT_HINT_TEXT,  # текст подписи поля
                                        hint_text_color_normal=colors.FB_GRAY,  # цвет подписи
                                        hint_text_color_focus=colors.FB_WHITE,  # цвет подписи при вводе
                                        text_color_focus=colors.FB_WHITE,  # цвет текста при вводе
                                        text="1024",  # текст по умолчанию
                                        active_line=True,  # линия под текстом при вводе
                                        allow_copy=True,  # разрешить копирование
                                        base_direction="ltr",  # направление текста
                                        cursor_blink=True,  # мигание курсора
                                        helper_text=text.HEIGHT_HELPER_TEXT,  # текст при срабатывании ошибки
                                        helper_text_mode="on_error",  # когда выводить текст helper
                                        input_filter="int",  # ввод только целых чисел
                                        )

        # текстовое поле ввода негативного промпта
        negative_prompt_text_field = MDTextField(size_hint=(0.9, None),  # размер в процентах от размера блока
                                                 pos_hint={  # позиция относительно блока
                                                    "center_x": 0.5,
                                                    "center_y": 0.5
                                                 },
                                                 mode="rectangle",  # режим текстового поля
                                                 hint_text=text.NEGATIVE_PROMPT_HINT_TEXT,  # текст подписи поля
                                                 hint_text_color_normal=colors.FB_GRAY,  # цвет подписи
                                                 hint_text_color_focus=colors.FB_WHITE,  # цвет подписи при вводе
                                                 text_color_focus=colors.FB_WHITE,  # цвет текста при вводе
                                                 max_text_length=200,  # максимальный размер вводимого текста в символах
                                                 active_line=True,  # линия под текстом при вводе
                                                 allow_copy=True,  # разрешить копирование
                                                 base_direction="ltr",  # направление текста
                                                 cursor_blink=True,  # мигание курсора
                                                 multiline=False,  # многострочный ввод
                                                 )

        # сегмент выбора стиля
        style_choose_row = MDSegmentedControl(size_hint=(0.9, None),  # размер в процентах от размера блока
                                              pos_hint={  # позиция относительно блока
                                                    "center_x": 0.5,
                                                    "center_y": 0.3
                                              },
                                              md_bg_color=colors.FB_BLACK,
                                              )

        # получение словаря стилей
        styles_dict = fb_requests.get_styles_dict()
        # формирование сегментов выбора на основе словаря
        for style in styles_dict:
            style_element = MDSegmentedControlItem(text=style,
                                                   )
            style_choose_row.add_widget(style_element)

        # обработка выбора стиля
        choosed_style = "Default"

        # функция записи стиля
        def style_button_active(self, item):
            nonlocal choosed_style
            choosed_style = styles_dict[f'{item.text}']

        style_choose_row.bind(on_active=style_button_active)

        # кнопка генератора
        generate_button = MDRoundFlatIconButton(text=text.GENERATE_BUTTON,
                                                icon="creation",
                                                pos_hint={
                                                    "center_x": 0.5,
                                                    "center_y": 0.1
                                                },
                                                size_hint=(0.6, None),
                                                md_bg_color=colors.FB_GREEN,
                                                theme_icon_color="Custom",
                                                theme_text_color="Custom",
                                                icon_color=colors.FB_BLACK,
                                                text_color=colors.FB_BLACK,
                                                )

        # словарь запросов на генерацию
        uuid_dict = {}

        # словарь обработанных запросов
        result_requests = {}

        # возвращение кнопки генератора в активное состояние
        def enable_generate(self):
            # изменение кнопки на активную
            generate_button.text = text.GENERATE_BUTTON
            generate_button.disabled = False

        # нажатие на кнопку генератора
        def press_generate(self):
            if prompt_text_field.text == "":
                prompt_text_field.error = True

            if int(width_text_field.text) < 1 or int(width_text_field.text) > 1024:
                width_text_field.error = True

            if int(height_text_field.text) < 1 or int(height_text_field.text) > 1024:
                height_text_field.error = True

            is_generate_prompts_ok = (prompt_text_field.error is False) and (negative_prompt_text_field.error is False)
            is_generate_params_ok = (width_text_field.error is False) and (height_text_field.error is False)

            if is_generate_prompts_ok and is_generate_params_ok and len(uuid_dict) < 6:

                # сбор всех параметров для запроса
                prompt = prompt_text_field.text
                negative_prompt = negative_prompt_text_field.text
                width_image = int(width_text_field.text)
                height_image = int(height_text_field.text)

                # изменение кнопки на неактивную на 2 секунды
                self.text = text.GENERATE_BUTTON_PRESSED
                self.disabled = True
                Clock.schedule_once(enable_generate, 2)

                # создание запроса на генерацию
                uuid = fb_request.generate(prompt,
                                           model_id,
                                           width_image,
                                           height_image,
                                           negative_prompt,
                                           choosed_style)

                # добавление полученного uuid в список
                uuid_dict.update({uuid: prompt})
                create_queue_list(page_queue)

                if len(uuid_dict) >= 6:
                    # изменение кнопки на неактивную
                    self.text = text.GENERATE_BUTTON_PRESSED_QUEUE
                    self.disabled = True

        generate_button.bind(on_press=press_generate)

        # левая вкладка - список очереди на генерацию
        page_queue = MDList()

        # проверка статуса генерации
        def check_generate_status(self):
            if len(uuid_dict) != 0:
                for generation_uuid in uuid_dict:

                    result = fb_request.check_generation(generation_uuid)

                    prompt = uuid_dict[generation_uuid]

                    if result["censored"] is True:
                        comment = "Ваш запрос не прошёл цензуру Fusion Brain"
                        status = "ОШИБКА"
                        text_color = colors.FB_ERROR

                    elif result["status"] == "FAIL":
                        comment = f"Возникла ошибка: {result['errorDescription']}"
                        status = "ОШИБКА"
                        text_color = colors.FB_ERROR

                    elif result["status"] == "DONE":
                        status = "Генерация завершена"
                        # сохранение изображения
                        file_name = image_create.create_images(result["images"], prompt, vars.FOLDER_PATH)
                        comment = f"Изображение {file_name} сгенерировано"
                        text_color = colors.FB_SUCCESS

                    else:
                        status = "generation"
                        comment = "generation"
                        text_color = (0, 0, 0, 0)

                    if status != "generation":
                        # добавить в список отработанных запросов
                        result_requests.update({generation_uuid: {
                                                                    "status": status,
                                                                    "comment": comment,
                                                                    "prompt": prompt,
                                                                    "text_color": text_color,
                                                                 }})

                resulted = None
                for result_uuid in result_requests:
                    resulted = uuid_dict.pop(result_uuid, None)

                # отрисовка списка запросов заново
                if resulted is not None:
                    # значок уведомления о новых генерациях
                    menu_left.badge_icon = "alert-circle-outline"
                    create_queue_list(page_queue)
                    Clock.schedule_once(enable_generate, 1)

        # проверка статуса генерации каждые 2 секунды
        Clock.schedule_interval(check_generate_status, 2)

        # формирование элементов списка на основе списка запросов генерации
        def create_queue_list(page_queue):
            page_queue.clear_widgets()
            if len(uuid_dict) == 0:
                queue_element = TwoLineListItem(text="Очередь пуста",
                                                secondary_text="Сформируйте запрос на генерацию")
                page_queue.add_widget(queue_element)
            else:
                for request in uuid_dict:
                    queue_element = TwoLineListItem(text="Генерация ...",
                                                    secondary_text=uuid_dict[request],
                                                    theme_text_color="Custom",
                                                    text_color=colors.FB_INFO,
                                                    secondary_text_color=colors.FB_GRAY)
                    page_queue.add_widget(queue_element)

            if len(result_requests) != 0:
                if len(result_requests) >= 4:
                    result_requests.popitem()

                for uuid in result_requests:
                    queue_element = ThreeLineListItem(text=result_requests[uuid]["status"],
                                                      secondary_text=result_requests[uuid]["prompt"],
                                                      tertiary_text=result_requests[uuid]["comment"],
                                                      theme_text_color="Custom",
                                                      text_color=result_requests[uuid]["text_color"],
                                                      secondary_text_color=colors.FB_GRAY
                                                      )
                    page_queue.add_widget(queue_element)

        create_queue_list(page_queue)

        # периодическое очищение списка завершённых генераций
        def delete_result(self):
            if len(result_requests) != 0:
                result_requests.popitem()
                create_queue_list(page_queue)
        # очистка каждые 15 секунд
        Clock.schedule_interval(delete_result, 20)

        # сборка всех блоков
        page_generator.add_widget(prompt_text_field)
        page_generator.add_widget(width_text_field)
        page_generator.add_widget(height_text_field)
        page_generator.add_widget(negative_prompt_text_field)
        page_generator.add_widget(style_choose_row)
        page_generator.add_widget(generate_button)

        menu_left.add_widget(page_queue)
        menu_center.add_widget(page_generator)

        bottom_menu.add_widget(menu_left)
        bottom_menu.add_widget(menu_center)
        bottom_menu.add_widget(menu_right)

        main_layout.add_widget(top_toolbar)
        main_layout.add_widget(bottom_menu)

        return main_layout


MainApp().run()
