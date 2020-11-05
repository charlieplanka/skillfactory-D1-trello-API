Приложение работает с Trello API.  
  
**Для работы используйте свои token, key и board_id, полученные на https://trello.com/. Обратите внимание, что board_id должен быть полным, не коротким.**   
  
Праметры находятся в начале файла `board.py`:
```
AUTH_PARAMS = {
    "key": "..",
    "token": ".."
}
BOARD_ID = ".."
```
  
Приложение запускается из командной строки.
  
Вывести все колонки, что есть на доске, вместе с количеством карточек и содержимым карточек:  
```python board.py```

Создать на доске колонку с названием Waiting:  
`python board.py create_column "Waiting"`  
  
Создать карточку Buy a milk в колонке To Do:  
`python board.py create_card "Buy a milk" "To Do"`  
  
Переместить карточку Buy a milk в колонку Doing:  
`python board.py move_card "Buy a milk" "Doing"`  

При попытке переместить карточку, название которой совпадает с другими карточками, появится список карточек с предложением выбрать одну из них, например:  
```
There are several cards named 'Buy a milk':
1: Buy a milk, column: To Do, id: 5fa3b39fdb8e072d2ace9fd9
2: Buy a milk, column: Doing, id: 5fa3b38d86ed757bb8d3b973
Choose a card you want to move to the 'Done' column and type its number (for example, 1):
```
Для продолжения достаточно ввести порядковый номер карточки.
