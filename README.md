# Игра «Змейка»

Учебное задание по дисциплине «Программирование на Python»:
классы `GameObject`, `Apple`, `Snake` и основной игровой цикл.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python the_snake.py
```

На Python 3.15 используется `pygame-ce` — совместимый форк pygame
с тем же импортом `pygame`. В `requirements.txt` зависимость выбрана
по версии Python: `pygame==2.5.2` для Python < 3.13 и `pygame-ce`
для Python 3.13+.

## Управление

- Стрелки или `WASD` — направление движения.
- `Esc` — выход.
- Яблоко увеличивает счёт и длину змейки.
- При столкновении со стеной или собственным телом игра
  начинается заново.

## Проверки

```bash
pytest
flake8 the_snake.py
```
