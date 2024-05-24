import pygame

from scripts.game import game_scene

pygame.init()

font_rus = pygame.font.SysFont('Comic Sans MS', 72)  # шрифт для текста меню


class Menu:  # класс отвечающий за кнопки в меню
    def __init__(self):
        self.option_surflaces: list[str] = list()  # список с поверхностями текста
        self.option_callback = list()  # список с функциями которые принадлежат кнопкам
        self.current_option_index = 0  # текущий элемент
        self.is_action_menu = True  # говорит активно ли сейчас меню, что бы блокировать его в некоторые моменты

    def append_option(self, option: str, callback) -> None:  # метод для дабавление разделов в menu
        self.option_surflaces.append(option)
        self.option_callback.append(callback)

    def switch(self, direction: int) -> None:  # переключение текущего элемента
        if self.is_action_menu:
            self.current_option_index = (self.current_option_index + direction) % len(self.option_callback)

    def select(self):  # вызывает функцию, привязанную к выбранному элеметну и возвращает результат вызова функции
        if self.is_action_menu:
            return self.option_callback[self.current_option_index]()

    def draw(self, surface: pygame.Surface, option_y_padding: int) -> None:
        # метод отрисовки всех элементов
        x, y = surface.get_width() * 0.35, surface.get_height() * 0.35

        font = font_rus

        for i, option in enumerate(self.option_surflaces):  # проходимся по всем повехностям
            # создаём прямоугольник описывающий текст2
            option = font.render(option, True, pygame.Color((255, 255, 255)))
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if self.is_action_menu:
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    # проверяем на пересечение с мышкой
                    # и меняем текущий выбранный элемент на тот, на который указывает мышь
                    self.current_option_index = i
            if i == self.current_option_index:  # если текущий элемент выбранн, создаём подчёркивание для него
                underline = pygame.Surface((option.get_width(), 4))
                underline.fill(pygame.Color((235, 235, 235)))
                underline_pos = (option_rect.x, option_rect.bottom - option_y_padding // 5)
            surface.blit(option, option_rect)  # отрисовываем текст
        surface.blit(underline, underline_pos)  # отрисовываем подчёркивание

    def check_mouse_event(self, option_y_padding, screen):
        # метод находящий элемент на который указывает мышь
        x, y = screen.get_width() * 0.35, screen.get_height() * 0.35
        font = font_rus

        for i, option in enumerate(self.option_surflaces):  # проходимся по всем повехностям
            # создаём прямоугольник описывающий текст2
            option = font.render(option, True, pygame.Color((255, 255, 255)))
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if self.is_action_menu:
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    return self.option_callback[i]()


def menu_scene(screen: pygame.Surface, switch_scene):
    menu = Menu()  # создание меню
    running = True

    def play() -> None:
        nonlocal running
        running = False
        switch_scene(game_scene)


    def exit_game() -> str:
        nonlocal running
        running = False
        switch_scene(None)
        return "Exit"

    menu.append_option("Играть", play)
    menu.append_option("Выйти", exit_game)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu.check_mouse_event(100, screen)
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                # изменение выбранного элеметна меню с помощью стрелочек
                if key[pygame.K_UP]:
                    menu.switch(-1)
                elif key[pygame.K_DOWN]:
                    menu.switch(1)
                elif key[pygame.K_RETURN]:
                    if menu.select() == 'Exit':  # если функция вернула Exit - закрываем игру
                        running = False
                        switch_scene(None)
        screen.fill((0, 0, 0))
        menu.draw(screen, 100)
        pygame.display.flip()
