Приложение работает с Trello API. Доска: https://trello.com/b/AXPZWOVS/created-via-api  
Приложение запускается из командной строки.
  
Вывести все колонки, что есть на доске, вместе с количеством карточек и содержимым карточек:  
```python board.py```

Создать на доске колонку с названием Waiting:  
`python board.py create_column "Waiting"`  
  
Создать карточку Buy a milk в колонке To Do:  
`python board.py create_card "Buy a milk" "To Do"`  
  
Переместить карточку Buy a milk в колонку Doing:  
`python board.py move_card "Buy a milk" "Doing"`  
