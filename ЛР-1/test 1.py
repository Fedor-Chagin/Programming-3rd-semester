import os

def comprehensive_test():
    """Полные тесты с учетом всех пар"""
    test_cases = [
        # Верные тесты (должны проходить ✅)
        ("2 7 11 15", "9", "0 1", True),
        ("3 2 4", "6", "1 2", True),
        ("3 3", "6", "0 1", True),
        ("1 2 3 4 5 6", "7", "0 5\n1 4\n2 3", True),  # ВСЕ пары!
        ("-1 10 2 5", "9", "0 1", True),    # -1+10=9
        
        # Неверные тесты (должны НЕ проходить ❌)
        ("2 7 11 15", "9", "1 2", False),   # неправильные индексы
        ("3 2 4", "6", "0 1", False),       # должно быть 1 2, а не 0 1
        ("3 3", "6", "1 0", False),         # индексы в неправильном порядке
        ("1 2 3", "10", "0 1", False),      # нет пар, но ожидаем вывод
        ("4 5 6", "9", "", False),          # 4+5=9, но ожидаем пустой вывод
        ("1 2 3 4 5 6", "7", "0 5", False), # ожидаем только первую пару, но программа выводит все
    ]
    
    print("~ ПОЛНЫЙ ТЕСТИНГ: верные и неверные тесты ~")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for nums, target, expected, should_pass in test_cases:
        print(f"\n Тест: nums={nums}, target={target}")
        print(f"Ожидаем: '{expected}' ({'результат должен совпасть' if should_pass else 'результат не должен совпасть'})")
        
        # Создание входного файла
        with open("input.txt", "w") as f:
            f.write(nums + "\n")
            f.write(target + "\n")
        
        # Запуск программы
        output = os.popen('python3 №1.py < input.txt').read().strip()
        
        print(f"Результат:  '{output}'")
        
        # Проверяем соответствует ли результат ожиданию
        result_matches = (output == expected)
        
        # Тест проходит если:
        # - should_pass=True и результат совпадает, ИЛИ
        # - should_pass=False и результат НЕ совпадает
        test_passed = (should_pass and result_matches) or (not should_pass and not result_matches)
        
        if test_passed:
            print("✅ ТЕСТ ПРОЙДЕН")
            passed += 1
        else:
            print("❌ ТЕСТ НЕ ПРОЙДЕН. ОШИБКА")
            failed += 1
        
        # Удаляем временный файл
        os.remove("input.txt")
    
    print("\n" + "=" * 50)
    print(f"📊 РЕЗУЛЬТАТ: {passed} пройдено, {failed} не пройдено")
    if failed == 0:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print(" Есть ошибки!")

if __name__ == "__main__":
    comprehensive_test()