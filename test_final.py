from eve_escalation_watcher import parse

near = {'WRZ1001': 2, 'M-4KDB': 3, 'H6-EYX': 1, '0-VG7A': 0}

print('=== ФИНАЛЬНЫЕ ТЕСТЫ ===\n')

print('Покупки (должны игнорироваться):')
tests_buy = [
    'WRZ1001 M-4KDB x',
    '0-VG7A х',
    '0-VG7A* х'
]
for t in tests_buy:
    result = parse(f"[20:27] > {t}", near)
    status = "ИГНОР ✓" if not result else "АЛЕРТ! ✗"
    print(f'  {t:30} -> {status}')

print('\nПродажи (должны алертить):')
tests_sell = [
    ('H6-EYX 23h 150mil excalation', near),
    ('0-VG7A angel 150m', near),
    ('WRZ1001 M-4KDB escalation', {'WRZ1001': 2, 'M-4KDB': 3})
]
for t, n in tests_sell:
    result = parse(f"[20:27] > {t}", n)
    status = f"{len(result)} систем ✓" if result else "НЕТ ✗"
    print(f'  {t:30} -> {status}')
