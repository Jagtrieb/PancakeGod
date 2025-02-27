# Описание боевой системы игры

## Общее описание и ход игры
### Команды
В бою участвуют две команды. Одна находится под управлением пользователя, вторая подчиняется игровому ИИ и выступает против первой.
В команде игрока может находится до **4** персонажей, у противника - до **6**. Варианты построения команды противника будут предопределены заранее, в самом бою случайно будет выбираться один из них. Построение своего отряда игрок делает самостоятельно. В нём обязательно должен находиться первый игрок.

### Ходы
В начале боя определяется порядок ходов всех персонажей на поле сражения. Данный процесс происходит в два этапа:
1. **Выбор команды, ходящей первой**: С помощью рандома определяется первая ходящая команда.  
Шансы исходов:  
**Игрок - 75%**  
**Противник - 25%**
2. **Определение последовательности внутри команды**: В команде игрока персонажи ходят по выбранной игроком последовательности _(Когда игрок собирает отряд)_, а в случае противника последовательность определяется с помощью рандома.

### Действия во время хода
Каждый персонаж может совершать разные действия во время наступления его хода.  
Союзные и вражеские персонажи могут:
* **Наносить физические атаки**: использование холодного оружия персонажа для атаки
* **Использовать способности**: использование одной из доступных персонажу способностей, расходуя заряд кристалла или здоровье персонажа 

Помимо этого, члены отряда игрока могут **защищаться** и **использовать предметы из инвентаря**. Главному герою доступен ряд дополнительный действий:
* **Смена кристалла**: смена активного кристалла главного героя для получения доступа к другим способностям. _Недоступно при наличии одного кристалла_.
* **Инициация попытки побега**: главный герой тратит свой ход на попытку побега. Его успешность зависит от рандома и шанса побега, который рассчитывается по следующей формуле:  

        {Сумма значений показателя ловкости всех союзников}/{Количество союзников}

    В случае успеха отряд игрока покинет бой, получив награду за убитых противников. При другом исходе бой продолжается, и ход переходит к следующему персонажу.

### Условия для завершения боя
* **Побег**: игра продолжается с места, где был запущен бой
* **Смерть всей команды врага**: Игрок может выйти из игры или загрузить последнее сохранение
* **Смерть главного героя**: игра продолжается с места, где был запущен бой

## Нанесение и получение урона

### Атака оружием
Обыкновенная физическаяя атака, доступная всем персонажам. Урон данной атаки расчитывается по следущей формуле: 

    sqrt(0.5 * {Сила оружия} * {Сила персонажа})
Оружие имеет показатель точности, и при выборе физической атаки происходит проверка на попадание, исход которой завист от точности оружия. Если проверка не пройдена, урон будет обнулён _(Персонаж промахнулся)_.
#### Критический удар
Преимущество атаки оружия. Наности удвоенный физический урон. Шанс критического удар считается по формуле:

    {Удача персонажа} / 3 + 10

### Урон от атакующей способности
Урон способности зависит от соответствующей характеристики персонажа: физической - от **Силы**, магической - от **Магии**.
Сам урон рассчитывается по следующей формуле:

    sqrt({Стандартный урон способности} * {Показатель характеристики})

### Итоговый наносимый урон
Высчитываются тип и значение урона, которые будут переданы цели для расчёта **Итогового получаемого урона**, учитывающего характеристики, Слабости/Сопротивления цели, её текущее состояние и шансы на уклонение. Расчиытвается по следующей формуле:

    {Бонус к атаке} * {Урон атаки оружием/способностью}

    *Бонус к атаке - параметр, который меняется в зависимости от состояния персонажа, наложенных на него эффектов

### Защита 
Когда персонаж защищается, **бонус к защите увеличивается в 2 раза**_(Бонус к защите применяется при расчёте получаемого урона)_

### Слабости/Соротивления
У кждого персонажа есть свои **слабости** и **сопротивления** к определённым типам атаки. При получении урона соответствующего типа,
он будет **увеличен или уменьшен** в зависимости от Слабостей/Сопротивлений персонажа. Коэффициентом данной механики выступает **Бонус слабости**. Если персонаж слаб к типу получаемого урона, **урон увеличивается в 1.5 раза**_(К.слабости = 1.5)_. В обратном случае, **урон снижается в 5 раз**._(К.слабости = 0.2)_

### Итоговый получаемый урон
Урон, который будет нанесён персонажу в ходе атаки его противника. Расчиытвается по следующей формуле:

    ({Итоговый наносимый урон} * {Бонус слабости}) / ({Бонус к защите} * sqrt({Стойкость персонажа} + {Защита брони}))
Если Итоговый получаемый урон после расчёта будет равен 0 _(Урон является целым числом)_, его значение будет заменено на 1.

### Уклонение
Механика, позволяющая избежать получение урона. Реализована через проверку, шанс успешного исхода в которой считается по формуле:

    {Бонус к уклонению} * {Ловкость персонажа} / 2
Также имеется шанс уклонения от наложения негативных эффектов: он постоянно равен 65%

## Способности поддержки
### Исцеляющие способности
Восстанавливают здоровье союзника. Объём исцеления расчитывается по следующей формуле:

    {Стандартное значение} * sqrt(0.5 * {Магия персонажа})

### Воскрешающие способности
Воскрешают выведенного из строя союзника с определённым запасом здоровья

### Восстанавливающие способности
Снимают негативные эффекты с союзников

### Усиливающие способности
Повышают **Атаку/Защиту/Ловкость** _(в зависимости от способности)_ в 1.4 раза на 3 хода

### Ослабляющие способности
Снижают показатели характеристик противников или накладывают эффекты, мешающие им в бою. Все эффекты действуют 3 хода
Список эффектов:
* **Снижение атаки**
* **Снижение защиты**
* **Снижение уклонения**
* **Сон**: цель не может выполнять действия, однако, при наступлении очереди её хода, Здоровье и Мана цели несного восполнятся. Также, получаемый урон цели возрастёт в 1.25
* **Страх**: цель с шансом 60% пропустит свой ход
* **Запутанность**: цель не сможет использовать способности
* **Возгорание**: в начале хода цель будет получать небольшой урон
* **Шок**: цель пропускает ход, атака оружием по цели с данным эффектом гарантированно будет критической
* **Замерзани**: цель пропускает ход, входящий урон снижен на 10%

### Способности влияющие на шкалу азарта
Данные способности способны повышать или понижать значение **шкалы азарта** _([Подробнее](#командная-атака))_, позволяя игроку манипулировать её значеним у союзников. Использование этиъ атак не требует ни маны, ни здоровья. В зависимости от выбранного эффекта, персонаж "отдаёт" или "забирает" очки азарта

## Особые механики

### Нокаут
Когда персонаж попадает по слабости противника или наносит критический урон, цель сбивается с ног и входит в состояние нокаута, 
её ход считается сделанным. В нокауте персонаж не может выполнять действия и ждёт своей очереди, чтобы восстановиться. Тот, кто нокаутировал противника, получает дополнительный ход. Нокаутированного нельзя нокаутировать дваджды так же, как и получить дополнительный ход при нанесении урона по слабости уже сбитого с ног противника.

### Командная атака
Когда отряд игрока нокаутирует все цели на поле боя, появится возможность провести **командную атаку**. Она наносит массивный урон по всем противникам, **игнорируя все их сопротивления**. Урон такой атаки равен сумме показателей силы атаки оружия каждого члена отряда. Если же игрок откажется от проведения атаки, бой продолжится как обычно, начиная с дополнительного хода персонажа, совершившего последний нокаут. Проведение командной атаки увеличит количество выпадаемых денег и единиц опыта в 1.3 раза.

### Шкала боевого азарта
Механика, влияющая на показатели атаки/защиты в зависимости от поведения игрока. Диапазон шкалы: **0-100** очков. При использовании атаки, атакующих способностей и специальных предметов значение будет возрастать. При защите, использовании способностей поддержки, а также соответствующих предсетов значнение шкалы будет снижаться.  
Влияние на характеристики в зависимости от значения шкалы боевого азарта приведено ниже:
* **0%-20%** - АТК: -10%; ЗЩТ: +15%
* **21%-40%** - АТК: -5%; ЗЩТ: +5%
* **41%-60%** - АТК: 0%; ЗЩТ: 0%
* **61%-80%** - АТК: +5%; ЗЩТ: -5%
* **81%-100%** - АТК: +15%; ЗЩТ: -10%

Помимо всего прочего, у каждого персонажа будет предпочтительный диапазон значения шкалы размером в **40 очков**. Когда значение находится в этом диапазоне, на персонаже будет срабатывать его особый эффект, помогающий в бою, будь то небольшое восстановлене здоровья/маны или увеличение некоторых характеристик.