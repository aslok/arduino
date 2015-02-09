USB контроллер умного дома
http://homes-smart.ru/index.php/oborudovanie/uroki-i-primery/41-usb-kontroller-umnogo-doma

Доступные команды:
gpio-usb on <номер GPIO> -Включает высокий уровень на соотвествующем порте.
gpio-usb off <номер GPIO> -Выключает высокий уровень на соотвествующем порте.
gpio-usb status - Чтение статуса GPIO на вывод.
gpio-usb statusin  -Чтение статуса GPIO на ввод.
gpio-usb mode -Управление режимом порта.Для того,чтобы например назначить 7 порт на ввод необходимо ввести gpio-usb mode 7 1  .Режимы записываются в энергонезависимую память.
gpio-usb rcsend <key> -Отправить ключ RCremote.
gpio-usb dhtread -Чтение датчика DHT11 или DHT22,подключенного на GPIO 5.
gpio-usb dhtsetup -Запрос статуса и вкл/выкл опроса датчика DHT.Опрос происходит раз в минуту.Статус записывается в энергонезависимую память.
gpio-usb pwm3 <level> -Управление ШИМ на 3 GPIO.
gpio-usb pwm4 <level> -Управление ШИМ на 4 GPIO.