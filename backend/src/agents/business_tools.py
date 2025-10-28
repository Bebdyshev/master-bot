"""
Specialized Business Tools for Master Education
Each tool handles specific business process according to admin workflows
"""
from langchain.tools import tool
from typing import Optional
import json
from datetime import datetime


# ========================================
# 1. 🔄 ВОЗВРАТ СРЕДСТВ
# ========================================

@tool
def request_refund(reason: str, student_id: str) -> str:
    """
    Обрабатывает запрос студента на возврат средств.
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ того, как:
    1. Узнал ПОДРОБНУЮ причину возврата
    2. Заверил клиента, что проблему обязательно решим
    3. Собрал все детали ситуации
    
    Процесс (согласно схеме):
    - Узнать причины возврата
    - Заверить клиента, что проблему решим
    - Отправить данные опер. диру и сервис диру
    
    Args:
        reason: ПОДРОБНАЯ причина возврата с деталями
        student_id: ID студента
    
    Returns:
        JSON с тикетом для операционного и сервисного директора
    """
    student_id = str(student_id) if student_id else "unknown"
    ticket_id = f"REFUND-{abs(hash(reason + student_id)) % 10000:04d}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "refund",
        "status": "open",
        "priority": "high",  # Возвраты всегда высокий приоритет
        "description": f"Запрос на возврат средств. Причина: {reason}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "24 часа",
        "assigned_to": "Операционный и Сервисный Директор",
        "category": "Возврат средств"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✅ Спасибо за информацию. Мы обязательно рассмотрим Ваш запрос.\n\n"
                   f"Тикет #{ticket_id} передан операционному и сервисному директору.\n"
                   f"Ваш запрос будет обработан в течение 24 часов.\n\n"
                   f"Вы можете отслеживать статус в разделе 'Мои Заявки'.",
        "ticket": ticket_data
    }, ensure_ascii=False)


# ========================================
# 2. ❄️ ЗАМОРОЗКА ОБУЧЕНИЯ
# ========================================

@tool
def request_freeze(duration_start: str, duration_end: str, reason: str, student_id: str) -> str:
    """
    Обрабатывает запрос студента на заморозку обучения (от 1 до 2 месяцев).
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ того, как:
    1. Уточнил точный срок заморозки (дата начала и конца, от 1 до 2 месяцев)
    2. Узнал причину заморозки
    
    Процесс (согласно схеме):
    - Дать заморозку от 1 до 2 месяцев
    - Оповестить учителей и кураторов о заморозке
    - Поменять статус клиента на ЗАМОРОЗИТ в АльфаСРМ
    - Поменять значение группы в фикс. таблице
    
    Args:
        duration_start: Дата начала заморозки (формат: YYYY-MM-DD)
        duration_end: Дата конца заморозки (формат: YYYY-MM-DD)
        reason: Причина заморозки (опционально)
        student_id: ID студента
    
    Returns:
        JSON с тикетом для администратора
    """
    student_id = str(student_id) if student_id else "unknown"
    ticket_id = f"FREEZE-{abs(hash(duration_start + student_id)) % 10000:04d}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "freeze",
        "status": "open",
        "priority": "medium",
        "description": f"Запрос на заморозку обучения с {duration_start} по {duration_end}. Причина: {reason}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "24 часа",
        "freeze_start": duration_start,
        "freeze_end": duration_end,
        "actions_required": [
            "Оповестить учителей и кураторов",
            "Изменить статус на ЗАМОРОЗИТ в АльфаСРМ",
            "Обновить фикс. таблицу"
        ],
        "category": "Заморозка обучения"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✅ Запрос на заморозку обучения с {duration_start} по {duration_end} зарегистрирован.\n\n"
                   f"Тикет #{ticket_id} создан.\n\n"
                   f"Администратор выполнит необходимые действия:\n"
                   f"• Уведомит учителей и кураторов\n"
                   f"• Изменит статус в системе на 'ЗАМОРОЗИТ'\n"
                   f"• Обновит все необходимые таблицы\n\n"
                   f"Вы получите уведомление об активации заморозки.",
        "ticket": ticket_data
    }, ensure_ascii=False)


# ========================================
# 3. ☀️ РАЗМОРОЗКА (ПРОДОЛЖЕНИЕ ОБУЧЕНИЯ)
# ========================================

@tool
def request_unfreeze(preferred_date: str, student_id: str) -> str:
    """
    Обрабатывает запрос студента на разморозку и продолжение обучения.
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ того, как:
    1. Уточнил желаемую дату продолжения обучения
    2. Проинформировал о необходимости проверки свободных групп
    
    Процесс (согласно схеме):
    - Предложить клиенту свободные группы
    - Количество уроков = остаток уроков в Альфа СРМ
    - Оповестить куратора и учителя о новом студенте
    - Поменять статус на активный, добавить в группу
    - Обновить фикс. таблицу
    
    Args:
        preferred_date: Желаемая дата продолжения обучения (формат: YYYY-MM-DD)
        student_id: ID студента
    
    Returns:
        JSON с тикетом для администратора
    """
    student_id = str(student_id) if student_id else "unknown"
    ticket_id = f"UNFREEZE-{abs(hash(preferred_date + student_id)) % 10000:04d}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "unfreeze",
        "status": "open",
        "priority": "medium",
        "description": f"Запрос на разморозку обучения с {preferred_date}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "24 часа",
        "unfreeze_date": preferred_date,
        "actions_required": [
            "Проверить свободные группы для уровня студента",
            "Проверить остаток уроков в Альфа СРМ",
            "Уведомить куратора и учителя",
            "Изменить статус на Активный",
            "Добавить в группу в CRM",
            "Обновить фикс. таблицу"
        ],
        "category": "Разморозка обучения"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✅ Запрос на разморозку и продолжение обучения с {preferred_date} зарегистрирован.\n\n"
                   f"Тикет #{ticket_id} создан.\n\n"
                   f"Администратор:\n"
                   f"• Проверит наличие свободных групп для Вашего уровня\n"
                   f"• Подтвердит количество оставшихся уроков\n"
                   f"• Свяжется с Вами с вариантами групп\n\n"
                   f"⚠️ Обратите внимание: Вы продолжите обучение с количеством уроков, "
                   f"согласно данным в CRM.",
        "ticket": ticket_data
    }, ensure_ascii=False)


# ========================================
# 4. 🎁 ИСПОЛЬЗОВАНИЕ БОНУСОВ
# ========================================

@tool
def use_bonus(bonus_type: str, details: str, student_id: str) -> str:
    """
    Обрабатывает запрос студента на использование бонусов.
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ того, как:
    1. Уточнил какой именно бонус хочет использовать студент
    2. Собрал детали (консультация, доступ к платформе и т.д.)
    
    Процесс (согласно схеме):
    - Проверить наличие Бонуса в ФИХ таблице
    - Если нет - "Я с Вами свяжусь"
    - Предоставить бонус:
      a) Консультация - добавить в консультационную группу
      б) Айтс - дать доступ к платформе/добавить в группу
    
    Args:
        bonus_type: Тип бонуса (консультация, доступ к платформе, другое)
        details: Детали запроса
        student_id: ID студента
    
    Returns:
        JSON с тикетом для администратора
    """
    student_id = str(student_id) if student_id else "unknown"
    ticket_id = f"BONUS-{abs(hash(bonus_type + student_id)) % 10000:04d}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "bonus",
        "status": "open",
        "priority": "low",
        "description": f"Запрос на использование бонуса: {bonus_type}. Детали: {details}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "24 часа",
        "bonus_type": bonus_type,
        "actions_required": [
            "Проверить наличие бонуса в ФИХ таблице",
            "Предоставить бонус согласно типу",
            "Обновить статус бонуса"
        ],
        "category": "Использование бонусов"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✅ Заявка на активацию бонуса '{bonus_type}' зарегистрирована.\n\n"
                   f"Тикет #{ticket_id} создан.\n\n"
                   f"Администратор:\n"
                   f"• Проверит наличие Вашего бонуса в системе\n"
                   f"• Активирует бонус согласно типу\n"
                   f"• Свяжется с Вами для подтверждения\n\n"
                   f"Ожидайте ответа в течение 24 часов.",
        "ticket": ticket_data
    }, ensure_ascii=False)


# ========================================
# 5. 📚 СМЕНА ГРУППЫ / УЧИТЕЛЯ
# ========================================

@tool
def change_group_or_teacher(reason: str, preferences: str, student_id: str) -> str:
    """
    Обрабатывает запрос студента на смену группы или учителя.
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ того, как:
    1. Узнал причину смены группы/учителя
    2. Уточнил желаемое время и дни недели
    3. Собрал все пожелания студента
    
    Процесс (согласно схеме):
    - Предложить СВОБОДНЫЕ группы, которые стартовали
    - В новые группы добавляем с разрешения опер. дира
    - Количество уроков должно +/- совпадать
    - Поменять значение в альфа/фикс. таблице
    - Оповестить учителей и кураторов
    
    Args:
        reason: Причина смены группы/учителя
        preferences: Пожелания (время, дни недели и т.д.)
        student_id: ID студента
    
    Returns:
        JSON с тикетом для операционного директора
    """
    student_id = str(student_id) if student_id else "unknown"
    ticket_id = f"CHANGE-{abs(hash(reason + student_id)) % 10000:04d}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "group_change",
        "status": "open",
        "priority": "medium",
        "description": f"Запрос на смену группы/учителя. Причина: {reason}. Пожелания: {preferences}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "48 часов",
        "reason": reason,
        "preferences": preferences,
        "actions_required": [
            "Получить разрешение операционного директора",
            "Предложить свободные группы",
            "Проверить совпадение количества уроков",
            "Обновить CRM и фикс. таблицу",
            "Уведомить учителей и кураторов"
        ],
        "assigned_to": "Операционный директор",
        "category": "Смена группы/учителя"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✅ Заявка на смену группы/учителя зарегистрирована.\n\n"
                   f"Тикет #{ticket_id} создан.\n\n"
                   f"Ваш запрос будет обработан операционным директором.\n\n"
                   f"Администратор:\n"
                   f"• Получит необходимое разрешение\n"
                   f"• Подберет подходящие варианты групп\n"
                   f"• Свяжется с Вами с предложениями\n\n"
                   f"Ожидайте ответа в течение 48 часов.",
        "ticket": ticket_data
    }, ensure_ascii=False)


# ========================================
# 6. 🔗 ТЕХНИЧЕСКИЕ ПРОБЛЕМЫ (ССЫЛКИ/ПЛАТФОРМА)
# ========================================

@tool
def tech_issue_platform(issue_type: str, description: str, student_id: str) -> str:
    """
    Обрабатывает технические проблемы со ссылками, платформой, ХБ.
    
    ⚠️ ВАЖНО: Сначала попробуй базовые решения:
    1. Предложи скопировать ссылку и вставить в адресную строку
    2. Если ХБ не работает - предложи VPN или подождать
    3. Только если не помогло - создавай тикет
    
    Процесс (согласно схеме):
    - Переслать ссылки отдельно
    - Если ХБ - включить VPN или подождать
    - Пароли от платформы предоставит куратор
    - Звайд иногда глючит - вежливо сказать
    - Убедиться, что проблема решена
    
    Args:
        issue_type: Тип проблемы (ссылки, платформа, ХБ, пароли)
        description: Описание проблемы
        student_id: ID студента
    
    Returns:
        JSON с тикетом для куратора/техподдержки
    """
    student_id = str(student_id) if student_id else "unknown"
    ticket_id = f"TECH-{abs(hash(description + student_id)) % 10000:04d}"
    
    # Определяем приоритет
    priority = "high" if "не могу войти" in description.lower() or "доступ" in description.lower() else "medium"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "technical_platform",
        "status": "open",
        "priority": priority,
        "description": f"Техническая проблема ({issue_type}): {description}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "4 часа" if priority == "high" else "12 часов",
        "issue_type": issue_type,
        "actions_required": [
            "Проверить доступ студента",
            "Предоставить рабочие ссылки",
            "Проверить/предоставить пароли при необходимости",
            "Убедиться, что проблема решена"
        ],
        "assigned_to": "Куратор",
        "category": "Технические проблемы"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✅ Тикет #{ticket_id} создан для решения технической проблемы.\n\n"
                   f"Ваш куратор:\n"
                   f"• Проверит Ваш доступ к платформе\n"
                   f"• Предоставит рабочие ссылки\n"
                   f"• Проверит правильность паролей\n"
                   f"• Убедится, что всё работает\n\n"
                   f"Ожидайте ответа в ближайшее время.",
        "ticket": ticket_data
    }, ensure_ascii=False)


# ========================================
# 7. 📜 СПРАВКА О ПРИСУТСТВИИ
# ========================================

@tool
def request_attendance_certificate(purpose: str, student_id: str) -> str:
    """
    Обрабатывает запрос студента на справку о присутствии на курсах.
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ того, как:
    1. Уточнил цель получения справки
    2. Объяснил процесс (заполнение шаблона)
    
    Процесс (согласно схеме):
    - Попросить заполнить шаблон в word формате
    - Отправить шаблон бухгалтеру
    - Отправить подписанную справку клиенту
    
    Args:
        purpose: Цель получения справки (работа, виза и т.д.)
        student_id: ID студента
    
    Returns:
        JSON с тикетом для бухгалтера
    """
    student_id = str(student_id) if student_id else "unknown"
    ticket_id = f"CERT-{abs(hash(purpose + student_id)) % 10000:04d}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "certificate",
        "status": "open",
        "priority": "medium",
        "description": f"Запрос на справку о присутствии на курсах. Цель: {purpose}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "3 рабочих дня",
        "purpose": purpose,
        "actions_required": [
            "Отправить студенту шаблон в Word",
            "Получить заполненный шаблон",
            "Передать бухгалтеру для подписания",
            "Отправить подписанную справку студенту"
        ],
        "assigned_to": "Бухгалтер",
        "category": "Справка о присутствии"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✅ Запрос на справку о присутствии зарегистрирован.\n\n"
                   f"Тикет #{ticket_id} создан.\n\n"
                   f"Процесс оформления:\n"
                   f"1. Вы получите шаблон справки в Word формате\n"
                   f"2. Заполните необходимые данные\n"
                   f"3. Отправьте заполненный шаблон обратно\n"
                   f"4. Бухгалтер подпишет справку\n"
                   f"5. Вы получите готовую справку\n\n"
                   f"Ожидаемый срок: 3 рабочих дня.",
        "ticket": ticket_data
    }, ensure_ascii=False)


# ========================================
# 8. 💰 ПРОДЛЕНИЕ / ДОКУПКА КУРСОВ
# ========================================

@tool
def extend_or_purchase_course(request_type: str, details: str, student_id: str) -> str:
    """
    Обрабатывает запрос студента на продление или докупку курсов.
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ того, как:
    1. Уточнил тип запроса (продление или допродажа)
    2. Собрал детали (какой курс, на сколько и т.д.)
    
    Процесс (согласно схеме):
    - Если допродажа → отправить данные РОП-у по шаблону
    - Если продление → отправить данные бухгалтеру по шаблону
    - Сказать клиенту, что данные отправлены
    - Удостовериться, что с клиентом связались
    
    Args:
        request_type: Тип запроса (продление или допродажа)
        details: Детали запроса (какой курс, срок и т.д.)
        student_id: ID студента
    
    Returns:
        JSON с тикетом для РОП или бухгалтера
    """
    student_id = str(student_id) if student_id else "unknown"
    ticket_id = f"EXTEND-{abs(hash(details + student_id)) % 10000:04d}"
    
    # Определяем кому назначить
    assigned_to = "РОП (Руководитель отдела продаж)" if request_type == "допродажа" else "Бухгалтер"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "extension",
        "status": "open",
        "priority": "medium",
        "description": f"Запрос на {request_type} курсов. Детали: {details}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "24 часа",
        "request_type": request_type,
        "details": details,
        "actions_required": [
            f"Отправить данные {assigned_to} по шаблону",
            "Связаться с клиентом для уточнения деталей",
            "Подтвердить оплату",
            "Обновить данные в CRM"
        ],
        "assigned_to": assigned_to,
        "category": "Продление/Докупка курсов"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✅ Запрос на {request_type} курсов зарегистрирован.\n\n"
                   f"Тикет #{ticket_id} создан.\n\n"
                   f"Ваши данные отправлены {assigned_to}.\n\n"
                   f"С Вами свяжутся для:\n"
                   f"• Уточнения деталей запроса\n"
                   f"• Предоставления информации об оплате\n"
                   f"• Подтверждения изменений\n\n"
                   f"Ожидайте звонка в течение 24 часов.",
        "ticket": ticket_data
    }, ensure_ascii=False)


# ========================================
# 9. 🤝 ПАРТНЕРСКАЯ ПРОГРАММА
# ========================================

@tool
def partner_program_request(invitee_name: str, invitee_telegram: str, invitee_phone: str, student_id: str) -> str:
    """
    Обрабатывает запрос студента по партнерской программе.
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ того, как:
    1. Собрал ФИО приглашенного
    2. Получил Telegram приглашенного
    3. Получил номер телефона приглашенного
    
    Процесс (согласно схеме):
    - Спросить ФИО, Телеграм, номер приглашенного
    - Написать приглашенному и спросить от кого пришел
    - Проверить статус в Альфа СРМ (откуда узнал)
    
    Args:
        invitee_name: ФИО приглашенного человека
        invitee_telegram: Telegram приглашенного
        invitee_phone: Номер телефона приглашенного
        student_id: ID студента-партнера
    
    Returns:
        JSON с тикетом для администратора
    """
    student_id = str(student_id) if student_id else "unknown"
    ticket_id = f"PARTNER-{abs(hash(invitee_name + student_id)) % 10000:04d}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "partner_program",
        "status": "open",
        "priority": "low",
        "description": f"Запрос по партнерской программе. Приглашенный: {invitee_name}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "48 часов",
        "invitee_name": invitee_name,
        "invitee_telegram": invitee_telegram,
        "invitee_phone": invitee_phone,
        "actions_required": [
            "Связаться с приглашенным",
            "Подтвердить источник (от кого пришел)",
            "Проверить статус в Альфа СРМ",
            "Начислить бонус партнеру при подтверждении"
        ],
        "category": "Партнерская программа"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✅ Запрос по партнерской программе зарегистрирован.\n\n"
                   f"Тикет #{ticket_id} создан.\n\n"
                   f"Данные приглашенного:\n"
                   f"• ФИО: {invitee_name}\n"
                   f"• Telegram: {invitee_telegram}\n"
                   f"• Телефон: {invitee_phone}\n\n"
                   f"Администратор:\n"
                   f"• Свяжется с приглашенным для подтверждения\n"
                   f"• Проверит данные в CRM\n"
                   f"• Начислит Вам бонус при успешном подтверждении\n\n"
                   f"Результат проверки будет отправлен в течение 48 часов.",
        "ticket": ticket_data
    }, ensure_ascii=False)


# ========================================
# 10. 🚨 ПРОБЛЕМЫ СОТРУДНИКОВ (ОБЩИЙ ТИП)
# ========================================

@tool
def staff_issue(issue_description: str, staff_id: str) -> str:
    """
    Обрабатывает различные проблемы от сотрудников.
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ того, как:
    1. Узнал суть проблемы детально
    2. Собрал всю необходимую информацию
    
    Процесс (согласно схеме):
    - Узнать суть проблемы
    - Решить проблему
    
    Args:
        issue_description: Подробное описание проблемы
        staff_id: ID сотрудника
    
    Returns:
        JSON с тикетом для администратора/руководителя
    """
    staff_id = str(staff_id) if staff_id else "unknown"
    ticket_id = f"STAFF-{abs(hash(issue_description + staff_id)) % 10000:04d}"
    
    # Определяем приоритет по ключевым словам
    priority = "high"
    if any(word in issue_description.lower() for word in ["срочно", "критично", "не работает"]):
        priority = "high"
    elif any(word in issue_description.lower() for word in ["вопрос", "уточнить"]):
        priority = "low"
    else:
        priority = "medium"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "staff_issue",
        "status": "open",
        "priority": priority,
        "description": f"Проблема сотрудника: {issue_description}",
        "staff_id": staff_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "4 часа" if priority == "high" else "24 часа",
        "actions_required": [
            "Изучить суть проблемы",
            "Определить ответственного",
            "Решить проблему",
            "Подтвердить решение"
        ],
        "assigned_to": "Администратор/Руководитель",
        "category": "Проблемы сотрудников"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✅ Тикет #{ticket_id} создан для решения Вашей проблемы.\n\n"
                   f"Приоритет: {priority.upper()}\n\n"
                   f"Ваша проблема будет рассмотрена администратором.\n"
                   f"Ожидайте ответа в ближайшее время.\n\n"
                   f"Вы можете отслеживать статус в системе.",
        "ticket": ticket_data
    }, ensure_ascii=False)


# Список всех бизнес-инструментов
BUSINESS_TOOLS = [
    request_refund,
    request_freeze,
    request_unfreeze,
    use_bonus,
    change_group_or_teacher,
    tech_issue_platform,
    request_attendance_certificate,
    extend_or_purchase_course,
    partner_program_request,
    staff_issue,
]
