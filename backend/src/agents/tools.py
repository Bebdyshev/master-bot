"""
AI Agent Tools for MasterEducation Support
Tools for SAT/IELTS preparation platform and university admission support
"""
from langchain.tools import tool
from typing import Optional
import httpx
from src.agents.business_tools import BUSINESS_TOOLS

# Import business-specific tools
from src.agents.business_tools import BUSINESS_TOOLS


@tool
def submit_technical_issue(description: str, student_id: str) -> str:
    """
    Создает тикет для технической проблемы.
    
    ⚠️ ВАЖНО: Используй этот инструмент ТОЛЬКО ПОСЛЕ того, как:
    1. Задал студенту уточняющие вопросы о проблеме
    2. Получил детальное описание (что именно не работает, какие ошибки, когда возникло)
    3. Студент подтвердил, что нужна помощь технической поддержки
    
    НЕ используй сразу при первом упоминании технической проблемы!
    
    Используй когда студент:
    - Детально описал техническую проблему
    - Подтвердил все детали
    - Готов создать тикет на поддержку
    
    Args:
        description: ПОДРОБНОЕ описание проблемы со всеми деталями от студента
        student_id: ID студента
    
    Returns:
        Информация о созданном тикете в JSON формате
    """
    import json
    from datetime import datetime
    
    # Ensure student_id is string
    student_id = str(student_id) if student_id else "unknown"
    
    # Generate ticket ID
    ticket_id = f"TECH-{abs(hash(description + student_id)) % 10000:04d}"
    
    # Determine priority based on keywords
    priority = "medium"
    if any(word in description.lower() for word in ["не могу войти", "срочно", "важно", "критично"]):
        priority = "high"
    elif any(word in description.lower() for word in ["вопрос", "уточнить", "помощь"]):
        priority = "low"
    
    # Create ticket data
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "technical",
        "status": "open",
        "priority": priority,
        "description": description,
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "24 часа" if priority != "high" else "4 часа"
    }
    
    # Return structured response with ticket data
    return json.dumps({
        "success": True,
        "message": f"✅ Тикет #{ticket_id} успешно создан!\n\nВаша заявка принята в работу. Техническая поддержка свяжется с вами в течение {ticket_data['estimated_response']}.\n\nОписание проблемы: {description}\nПриоритет: {priority}",
        "ticket": ticket_data
    }, ensure_ascii=False)


@tool
def request_document(document_type: str, student_id: str) -> str:
    """
    Запрашивает справку или документ.
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ уточнения:
    1. Для какой цели нужен документ
    2. В какие сроки нужен документ
    3. Есть ли особые требования
    
    Используй когда студент:
    - Точно указал тип документа
    - Подтвердил детали запроса
    
    Args:
        document_type: Тип документа (справка, выписка, etc)
        student_id: ID студента
    
    Returns:
        Информация о запросе документа в JSON формате
    """
    import json
    from datetime import datetime
    
    # Ensure student_id is string
    student_id = str(student_id) if student_id else "unknown"
    
    # Generate ticket ID
    ticket_id = f"DOC-{abs(hash(document_type + student_id)) % 10000:04d}"
    
    # Create ticket data
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "document",
        "status": "open",
        "priority": "low",
        "description": f"Запрос на получение документа: {document_type}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "3 рабочих дня"
    }
    
    return json.dumps({
        "success": True,
        "message": f"📄 Запрос на получение документа '{document_type}' принят.\n\nТикет #{ticket_id} создан.\nДокумент будет готов в течение 3 рабочих дней.\nВы получите уведомление на email.",
        "ticket": ticket_data
    }, ensure_ascii=False)
@tool  
def contact_teacher(teacher_name: str, subject: str, message: str, student_id: str) -> str:
    """
    Отправляет сообщение преподавателю.
    
    ⚠️ ВАЖНО: Используй ТОЛЬКО ПОСЛЕ уточнения:
    1. Имя преподавателя и предмет
    2. Суть вопроса или проблемы
    3. Контекст (задание, лекция, тема)
    
    Используй когда студент:
    - Назвал конкретного преподавателя
    - Детально описал вопрос
    - Подтвердил отправку сообщения
    
    Args:
        teacher_name: Имя преподавателя
        subject: Предмет
        message: ПОДРОБНОЕ сообщение с контекстом
        student_id: ID студента
    
    Returns:
        Подтверждение отправки в JSON формате
    """
    import json
    from datetime import datetime
    
    # Ensure student_id is string
    student_id = str(student_id) if student_id else "unknown"
    
    # Generate ticket ID
    ticket_id = f"MSG-{abs(hash(message + student_id)) % 10000:04d}"
    
    # Create ticket data
    ticket_data = {
        "ticket_id": ticket_id,
        "type": "teacher-message",
        "status": "open",
        "priority": "medium",
        "description": f"Сообщение для преподавателя {teacher_name} ({subject}): {message}",
        "student_id": student_id,
        "created_at": datetime.now().isoformat(),
        "estimated_response": "1-2 рабочих дня"
    }
    
    return json.dumps({
        "success": True,
        "message": f"✉️ Сообщение отправлено преподавателю {teacher_name} ({subject}).\n\nТикет #{ticket_id} создан.\nВы получите ответ в течение 1-2 рабочих дней.",
        "ticket": ticket_data
    }, ensure_ascii=False)




# Список всех доступных инструментов
TOOLS = [
    # Общие административные инструменты
    submit_technical_issue,
    request_document,
    contact_teacher,
] + BUSINESS_TOOLS  # Добавляем все бизнес-инструменты

