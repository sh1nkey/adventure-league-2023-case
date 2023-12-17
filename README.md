<p align="center">
  <img src="https://sun9-21.userapi.com/impg/cPGcvTz3BIhOEKkqmCY6n4TRp_QucnlHUjO9pw/1iAQfH79NqI.jpg?size=552x347&quality=96&sign=4279860d4e6141679593966c2ad3f2ae&type=album" alt="logo">
</p>

<h1 align="center">Кейс: корпоративный университет Совкомбанка (от команды GEMS)</h1>


Стек технологий бэкенда: DRF, PostgreSQL, Docker🐳, docker-compose, Linux, nginx, gunicorn
##  :speech_balloon: TL:DR 

Демо-версия, нужная для кейс-чемпионата "Лига Приключений: Москва" в 2023 году. 
Сайт разрабатывали:
-Алексей Куделько (Backend Developer)
-Артём Иванов (Frontend Developer)
-Мария Пилипец (UI-UX Designer)

Веб-версия: https://univer-gems.ru


## Готовый функционал

Мини-приложение "users"
* Авторизация (JWT)
* Вывод профиля студента (статистика посещений, статистика успеваемости, отображение прочей информации о студенте)
* Управление таблицами: "направления", "группа", "профиль студента", "учебные группы"

Мини-приложение "conent"
* Вкладка "моё обучение" (подсчёт успеваемости по каждому из предметов, вывод учебных материалов и тестов по каждому)
* Просмотр содержимого выбранного задания или выбранного учебного материала
* Прохождение тестов, проверка результатов, и сохранение их в БД для просмотра преподавателя
* Возможность составления тестов и учебных материалов для студентов

Мини-приложение "timetable"
* Отображение расписания для группы студента
* Возможность отметки присутствующих на паре
* Возможность редактирования расписания для разных групп со стороны куратора

Мини-приложение "applications"
* Возможность отправки заявки со стороны незарегистрированного пользователя
* Функционал для проверки, фильтрации, удаления заявок со стороны абитуриентов
 
 Помимо этого данное веб-приложение содержит базвую документацию в swagger.

## Функционал для будущей доработки

Во время разработки нам пришлось отложить некоторые наши масштабные идеи, чтобы максимально отточить проект. Вот некоторые из них:
1) Добавление ассинхронного распараллеливания запросов в БД при помощи Celery.
2) Любые функции (в том числе цикличные), связанные со временем, как пример: функции связанные с "просрочкой" тестов, которые можно было бы реализовать с помощью Celery-Beat.
3) Кэширование отображения данных (например, информации студента в профиле) при помощи Redis.
4) Подробная статистика посещения студентов: из-за этого на БД пошла бы большая нагрузка, которая могла бы помешать функционированию приложения на ранних этапах.
5) Весь функционал, реализованный с помощью админ-панели, хотелось бы перенести из неё в самодельные эндпоинты, а саму модель - кастомизировать.
6) К сожалению, эффективностью запросов в некоторых случаях пришлось пожертвовать ради того, чтобы успеть всё в срок.
7) В будущем мы хотели бы добавить юнит-тесты для большинства эндпоинтов для экономии времени при разработке
