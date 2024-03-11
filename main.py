import os
import pickle

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.list import *
from kivy.clock import Clock
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivy import platform

from fusion_brain import fb_requests
from interface import colors
from interface import text
from interface import vars
from img_create import image_create
# from plyer import storagepath

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])


class MainApp(MDApp):

    # сборка элементов
    def build(self):
        # установка тёмной темы
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.material_style = "M3"

        # переменная, сохранены ли API ключи, по умолчанию нет
        global is_keys_success
        is_keys_success = False

        # словарь api ключей
        global api_keys
        api_keys = {}

        # FOLDER_PATH = "/storage/emulated/0/"
        FOLDER_PATH = "./"


        # экраны
        main_layout = MDScreenManager()

        # приветственный экран
        welcome_screen = MDScreen(name="welcome_screen",)

        # экран ввода API ключей
        keys_screen = MDScreen(name="keys_screen")

        # основной экран
        generator_screen = MDScreen(name="generator_screen")

        # сборка экранов
        main_layout.add_widget(welcome_screen)
        main_layout.add_widget(keys_screen)
        main_layout.add_widget(generator_screen)
        # начальный экран
        main_layout.current = "welcome_screen"

        global fb_request
        global model_id

        fb_request = fb_requests.FBRequest("placeholder", "placeholder")
        model_id = fb_request.get_model()

        # пропуск начального экрана
        def skip_welcome_screen(self):
            global fb_request
            global api_keys
            global model_id
            if is_keys_success:
                # объект взаимодействия с API Fusion Brain
                fb_request = fb_requests.FBRequest(api_keys["api_key"], api_keys["secret_api_key"])
                # получение ID модели нейросети
                model_id = fb_request.get_model()
                main_layout.current = "generator_screen"
            else:
                main_layout.current = "keys_screen"

        # блок приветственного экрана
        welcome_layout = MDFloatLayout(MDLabel(text="Welcome to",
                                               pos_hint={
                                                   "center_x": 0.5,
                                                   "center_y": 0.7
                                               },
                                               font_style="Body1",
                                               halign="center",
                                               theme_text_color="Custom",
                                               text_color=colors.FB_WHITE),
                                       MDLabel(text="FUSION BRAIN",
                                               pos_hint={
                                                   "center_x": 0.5,
                                                   "center_y": 0.6
                                               },
                                               font_style="H4",
                                               halign="center",
                                               theme_text_color="Custom",
                                               text_color=colors.FB_GREEN),
                                       MDLabel(text="Text2Image generator",
                                               pos_hint={
                                                   "center_x": 0.5,
                                                   "center_y": 0.52
                                               },
                                               font_style="H5",
                                               halign="center",
                                               theme_text_color="Custom",
                                               text_color=colors.FB_WHITE),
                                       MDRaisedButton(text="Старт",
                                                      font_style="Button",
                                                      theme_text_color="Custom",
                                                      size_hint=(0.4, 0.08),
                                                      pos_hint={
                                                          "center_x": 0.5,
                                                          "center_y": 0.4
                                                      },
                                                      text_color=colors.FB_BLACK,
                                                      shadow_color=colors.FB_BLACK,
                                                      md_bg_color=colors.FB_GREEN,
                                                      on_release=skip_welcome_screen,
                                                      ),
                                       MDLabel(text="Автор: https://github.com/some-kind",
                                               pos_hint={
                                                   "center_x": 0.5,
                                                   "center_y": 0.2
                                               },
                                               font_style="Body2",
                                               halign="center",
                                               theme_text_color="Custom",
                                               text_color=colors.FB_GRAY),
                                       MDLabel(text="Fusion Brain: https://fusionbrain.ai",
                                               pos_hint={
                                                   "center_x": 0.5,
                                                   "center_y": 0.25
                                               },
                                               font_style="Body2",
                                               halign="center",
                                               theme_text_color="Custom",
                                               text_color=colors.FB_WHITE),
                                       md_bg_color=colors.FB_DARK_GRAY,
                                       )
        welcome_screen.add_widget(welcome_layout)

        # блок экрана ввода API ключей
        keys_layout = MDFloatLayout(MDLabel(text="Для работы приложения неоходимо ввести API ключи",
                                            pos_hint={
                                                "center_x": 0.5,
                                                "center_y": 0.8
                                            },
                                            font_style="H5",
                                            halign="center",
                                            theme_text_color="Custom",
                                            text_color=colors.FB_WHITE,
                                            ),
                                    MDLabel(text="Для получения своих ключей посетите https://fusionbrain.ai/docs/doc/poshagovaya-instrukciya-po-upravleniu-api-kluchami/",
                                            pos_hint={
                                                "center_x": 0.5,
                                                "center_y": 0.2
                                            },
                                            font_style="Body2",
                                            halign="center",
                                            theme_text_color="Custom",
                                            text_color=colors.FB_GRAY,
                                            ),
                                    md_bg_color=colors.FB_DARK_GRAY,
                                    )
        # блок API ключа
        field_api_key = MDTextField(size_hint=(0.9, 0.1),  # размер в процентах от размера блока
                                    pos_hint={  # позиция относительно блока
                                        "center_x": 0.5,
                                        "center_y": 0.6
                                    },
                                    mode="rectangle",  # режим текстового поля
                                    hint_text="API ключ",  # текст подписи поля
                                    hint_text_color_normal=colors.FB_GRAY,  # цвет подписи
                                    hint_text_color_focus=colors.FB_WHITE,  # цвет подписи при вводе
                                    text_color_focus=colors.FB_WHITE,  # цвет текста при вводе
                                    font_size=45,
                                    active_line=True,  # линия под текстом при вводе
                                    allow_copy=True,  # разрешить копирование
                                    base_direction="ltr",  # направление текста
                                    cursor_blink=True,  # мигание курсора
                                    multiline=False,  # многострочный ввод
                                    )

        # блок secret API ключа
        field_secret_api_key = MDTextField(size_hint=(0.9, 0.1),  # размер в процентах от размера блока
                                           pos_hint={  # позиция относительно блока
                                               "center_x": 0.5,
                                               "center_y": 0.5
                                           },
                                           mode="rectangle",  # режим текстового поля
                                           hint_text="Secret API ключ",  # текст подписи поля
                                           hint_text_color_normal=colors.FB_GRAY,  # цвет подписи
                                           hint_text_color_focus=colors.FB_WHITE,  # цвет подписи при вводе
                                           text_color_focus=colors.FB_WHITE,  # цвет текста при вводе
                                           font_size=45,
                                           active_line=True,  # линия под текстом при вводе
                                           allow_copy=True,  # разрешить копирование
                                           base_direction="ltr",  # направление текста
                                           cursor_blink=True,  # мигание курсора
                                           multiline=False,  # многострочный ввод
                                           password=True,
                                           password_mask="*",
                                           )
        
        # кнопка проверки API ключей
        check_keys_button = MDRaisedButton(text="Проверить ключи",
                                           font_style="Button",
                                           theme_text_color="Custom",
                                           size_hint=(0.4, 0.08),
                                           pos_hint={
                                               "center_x": 0.5,
                                               "center_y": 0.35
                                           },
                                           text_color=colors.FB_BLACK,
                                           shadow_color=colors.FB_BLACK,
                                           md_bg_color=colors.FB_GREEN,
                                           )

        # нажатие кнопки проверки API ключей
        def release_check_keys(self):
            # получение ключей из полей ввода
            api_key = field_api_key.text
            secret_api_key = field_secret_api_key.text
            api_test = fb_requests.FBRequest(api_key, secret_api_key)

            # смена кнопки
            check_keys_button.disabled = True
            check_keys_button.text = "Идёт проверка ..."
            # проверочный запрос
            check_result = api_test.check_keys()
            if check_result is True:
                # смена кнопки
                check_keys_button.disabled = True
                check_keys_button.text = "Успешно"
                check_keys_button.text_disabled_color = colors.FB_SUCCESS
                api_keys["api_key"] = api_key
                api_keys["secret_api_key"] = secret_api_key
                # запись ключей в кэш
                global is_keys_success
                is_keys_success = True
                api_keys_info = {"is_keys_success": True,
                                 "api_key": api_key,
                                 "secret_api_key": secret_api_key}
                with open("cache.pickle", "wb") as cache_file:
                    cache_file.write(pickle.dumps(api_keys_info))

                global fb_request
                global model_id
                # объект взаимодействия с API Fusion Brain
                fb_request = fb_requests.FBRequest(api_keys["api_key"], api_keys["secret_api_key"])
                # получение ID модели нейросети
                model_id = fb_request.get_model()

                main_layout.current = "generator_screen"
            else:
                # смена кнопки
                check_keys_button.disabled = True
                check_keys_button.text = "Неверные ключи"
                check_keys_button.text_disabled_color = colors.FB_ERROR
                Clock.schedule_once(enable_check_keys, 2)

        # возврат кнопки проверки ключей в активной состояние
        def enable_check_keys(self):
            check_keys_button.disabled = False
            check_keys_button.text = "Проверить ключи"

        check_keys_button.bind(on_release=release_check_keys)
        keys_layout.add_widget(field_api_key)
        keys_layout.add_widget(field_secret_api_key)
        keys_layout.add_widget(check_keys_button)
        keys_screen.add_widget(keys_layout)



        # основной блок
        generator_layout = MDBoxLayout(orientation="vertical",  # ориентация блоков внутри
                                       md_bg_color=colors.FB_DARK_GRAY,  # цвет фона
                                       )
        generator_screen.add_widget(generator_layout)

        # верхняя панель
        top_toolbar = MDTopAppBar(title=text.TITLE,  # загловок
                                  shadow_color=colors.FB_BLACK,  # цвет тени
                                  specific_text_color=colors.FB_GREEN,  # цвет текста и иконок
                                  # left_action_items=[  # кнопки слева
                                  #     ["home"],
                                  #     ["dots-vertical"],
                                  # ],
                                  # right_action_items=[  # кнопки справа
                                  #     ["android"],
                                  #     ["phone"]
                                  # ],
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
            menu_left.badge_icon = ""

        menu_left.bind(on_tab_press=clear_new_result_icon)

        # центральная вкладка - генератор
        page_generator = MDFloatLayout()

        # текстовое поле ввода промпта
        prompt_text_field = MDTextField(size_hint=(0.9, 0.1),  # размер в процентах от размера блока
                                        pos_hint={  # позиция относительно блока
                                            "center_x": 0.5,
                                            "center_y": 0.9
                                        },
                                        mode="rectangle",  # режим текстового поля
                                        hint_text=text.PROMPT_HINT_TEXT,  # текст подписи поля
                                        hint_text_color_normal=colors.FB_GRAY,  # цвет подписи
                                        hint_text_color_focus=colors.FB_WHITE,  # цвет подписи при вводе
                                        text_color_focus=colors.FB_WHITE,  # цвет текста при вводе
                                        font_size=45,
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
                                       font_size=45,
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
                                        font_size=45,
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
                                                 font_size=45,
                                                 base_direction="ltr",  # направление текста
                                                 cursor_blink=True,  # мигание курсора
                                                 multiline=False,  # многострочный ввод
                                                 )

        # сегмент выбора стиля
        style_choose_row = MDGridLayout(size_hint=(0.9, None),  # размер в процентах от размера блока
                                        pos_hint={  # позиция относительно блока
                                            "center_x": 0.5,
                                            "center_y": 0.3
                                        },
                                        md_bg_color=colors.FB_BLACK,
                                        radius=10,
                                        cols=4,
                                        )

        # получение словаря стилей
        styles_dict = fb_requests.get_styles_dict()
        # формирование сегментов выбора на основе словаря
        for style in styles_dict:
            style_element = MDCheckbox(id=styles_dict[style],
                                       size_hint=(0.3, 0.3),
                                       pos_hint={
                                           "center_y": 0.5,
                                           "center_x": 0.5
                                       },
                                       checkbox_icon_down="radiobox-marked",
                                       checkbox_icon_normal="radiobox-blank",
                                       radio_icon_down="radiobox-marked",
                                       radio_icon_normal="radiobox-blank",
                                       group="style"
                                       )
            style_element.color_active = colors.FB_WHITE
            style_element.color_inactive = colors.FB_GRAY
            style_choose_row.add_widget(style_element)

            style_text = MDLabel(text=style,
                                 pos_hint={
                                     "center_x": 0.5,
                                     "center_y": 0.5,
                                 },
                                 font_style="Body2",
                                 theme_text_color="Custom",
                                 text_color=colors.FB_WHITE,
                                 )
            style_choose_row.add_widget(style_text)

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
                                                font_style="Button"
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

                choosed_style = "Default"
                # выбор стиля
                for checkbox in style_choose_row.children:
                    if isinstance(checkbox, MDCheckbox) and checkbox.state == "down":
                        choosed_style = checkbox.id

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
                        file_name = image_create.create_images(result["images"], prompt, vars.FOLDER)
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
                                                secondary_text="Сформируйте запрос на генерацию",
                                                font_style="Button")
                page_queue.add_widget(queue_element)
            else:
                for request in uuid_dict:
                    queue_element = TwoLineListItem(text="Генерация ...",
                                                    secondary_text=uuid_dict[request],
                                                    theme_text_color="Custom",
                                                    text_color=colors.FB_INFO,
                                                    secondary_text_color=colors.FB_GRAY,
                                                    font_style="Button")
                    page_queue.add_widget(queue_element)

            if len(result_requests) != 0:

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
                first_key = next(iter(result_requests))
                result_requests.pop(first_key)
                create_queue_list(page_queue)
        # очистка каждые 30 секунд
        Clock.schedule_interval(delete_result, 30)

        # проверка папки изображений и сборка свайпера при переходе на вкладку
        def create_image_list(self):
            self.clear_widgets()

            page_images = MDSwiper(bar_width=10,  # ширина полосы прокрутки
                                   bar_color=colors.FB_GRAY,  # цвет полосы прокрутки при прокрутке
                                   bar_inactive_color=colors.FB_DARK_GRAY,  # цветка полосы прокрутки
                                   bar_margin=10,  # отступ полосы прокрутки от края блока
                                   bar_pos_x="bottom",  # положение полосы прокрутки
                                   swipe_on_scroll=False,  # прокуртка колесом мыши
                                   items_spacing=25,  # расстояние между слайдами в пикселях
                                   transition_duration=1,  # длительность перехода между слайдами в секундах

                                   )

            # сборка данных о файлах
            files_list = []
            for root, dirs, files in os.walk(vars.FOLDER):
                for file_name in files:
                    files_list.append(file_name)
            # если файлов нет
            if not files_list:
                image_element = MDSwiperItem(MDLabel(text="Изображений пока нет",
                                                     pos_hint={
                                                         "center_x": 0.5,
                                                         "center_y": 0.5
                                                     },

                                                     ))
                page_images.add_widget(image_element)
            else:

                for image_file in reversed(files_list):
                    image_element = MDSwiperItem(MDSmartTile(MDLabel(text=image_file,
                                                                     theme_text_color="Custom",
                                                                     text_color=colors.FB_WHITE,
                                                                     font_style="Body2",
                                                                     ),
                                                             source=vars.FOLDER + image_file,
                                                             radius=10,
                                                             box_radius=(0, 0, 10, 10),
                                                             box_color=(0, 0, 0, 0.6),
                                                             size_hint=(0.9, 0.9),
                                                             pos_hint={
                                                                 "center_x": 0.5,
                                                                 "center_y": 0.5
                                                             },
                                                             box_position="footer",
                                                             disabled=True,

                                                             ))

                    page_images.add_widget(image_element)

            menu_right.add_widget(page_images)

        # привязка к переходу на страницу изображений
        menu_right.bind(on_tab_press=create_image_list)

        # create_image_list(page_images)

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

        generator_layout.add_widget(top_toolbar)
        generator_layout.add_widget(bottom_menu)

        return main_layout

    # старт приложения и проверка кэша
    def on_start(self):
        global is_keys_success
        global api_keys
        try:
            with open("cache.pickle", "rb") as cache_file:
                api_keys_data = pickle.loads(cache_file.read())
                is_keys_success = api_keys_data["is_keys_success"]
                api_keys = {"api_key": api_keys_data["api_key"],
                            "secret_api_key": api_keys_data["secret_api_key"]}
        except FileNotFoundError:
            pass


MainApp().run()
