#!/usr/bin/env python3
"""
Тестовый скрипт для проверки процесса уточнения деталей
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.support_agent import StudentSupportAgent
import json


def print_separator():
    print("\n" + "=" * 70 + "\n")


def print_message(role: str, content: str):
    emoji = "👤" if role == "user" else "🤖"
    print(f"{emoji} {role.upper()}: {content}\n")


def test_conversation_flow():
    """
    Тестирует полный диалог с уточнением деталей
    """
    print("🎯 ТЕСТ: Процесс уточнения деталей перед созданием тикета")
    print_separator()
    
    agent = StudentSupportAgent(student_id="TEST123")
    
    # История диалога
    history = []
    
    # Шаг 1: Студент описывает проблему кратко
    print("📝 Сценарий: Студент кратко описывает техническую проблему")
    print_separator()
    
    user_msg_1 = "Не могу войти в систему"
    print_message("Студент", user_msg_1)
    
    result_1 = agent.chat(user_msg_1, chat_history=history)
    print_message("AI", result_1["response"])
    
    # Проверяем, что тикет НЕ создан на первом сообщении
    if result_1.get("ticket"):
        print("❌ ОШИБКА: Тикет создан слишком рано! AI должен сначала уточнить детали.")
    else:
        print("✅ ПРАВИЛЬНО: AI задает уточняющие вопросы вместо немедленного создания тикета")
    
    # Добавляем в историю
    history.append({"role": "user", "content": user_msg_1})
    history.append({"role": "assistant", "content": result_1["response"]})
    
    print_separator()
    
    # Шаг 2: Студент предоставляет детали
    print("📝 Студент предоставляет детальную информацию")
    print_separator()
    
    user_msg_2 = """Пишет ошибку 'Неверный логин или пароль', хотя я точно 
правильно ввожу. Началось сегодня утром после обновления. Пароль не сбрасывал, 
кэш очищал - не помогло."""
    
    print_message("Студент", user_msg_2)
    
    result_2 = agent.chat(user_msg_2, chat_history=history)
    print_message("AI", result_2["response"])
    
    # Добавляем в историю
    history.append({"role": "user", "content": user_msg_2})
    history.append({"role": "assistant", "content": result_2["response"]})
    
    print_separator()
    
    # Шаг 3: Подтверждение создания тикета
    if "создать" in result_2["response"].lower() or "тикет" in result_2["response"].lower():
        print("📝 AI предлагает создать тикет, студент подтверждает")
        print_separator()
        
        user_msg_3 = "Да, создавайте тикет"
        print_message("Студент", user_msg_3)
        
        result_3 = agent.chat(user_msg_3, chat_history=history)
        print_message("AI", result_3["response"])
        
        # Проверяем создание тикета
        if result_3.get("ticket"):
            print("\n✅ УСПЕХ: Тикет создан с полной информацией!")
            print("\n📋 ИНФОРМАЦИЯ О ТИКЕТЕ:")
            print(json.dumps(result_3["ticket"], indent=2, ensure_ascii=False))
            
            # Проверяем детальность описания
            description = result_3["ticket"].get("description", "")
            if len(description) > 50:
                print("\n✅ Описание детальное (больше 50 символов)")
            else:
                print("\n⚠️ Описание слишком короткое")
        else:
            print("\n⚠️ Тикет все еще не создан")
    
    print_separator()


def test_simple_question():
    """
    Тестирует, что простые вопросы не требуют уточнения
    """
    print("🎯 ТЕСТ: Простой вопрос (без создания тикета)")
    print_separator()
    
    agent = StudentSupportAgent(student_id="TEST456")
    
    user_msg = "Какие у меня оценки?"
    print_message("Студент", user_msg)
    
    result = agent.chat(user_msg, chat_history=[])
    print_message("AI", result["response"])
    
    if result.get("ticket"):
        print("\n❌ ОШИБКА: Тикет создан для простого вопроса!")
    else:
        print("\n✅ ПРАВИЛЬНО: Тикет не создан, дан прямой ответ")
    
    print_separator()


def test_document_request_flow():
    """
    Тестирует процесс запроса документа с уточнением
    """
    print("🎯 ТЕСТ: Запрос документа с уточнением деталей")
    print_separator()
    
    agent = StudentSupportAgent(student_id="TEST789")
    history = []
    
    # Шаг 1: Краткий запрос
    user_msg_1 = "Мне нужна справка"
    print_message("Студент", user_msg_1)
    
    result_1 = agent.chat(user_msg_1, chat_history=history)
    print_message("AI", result_1["response"])
    
    if result_1.get("ticket"):
        print("❌ ОШИБКА: Тикет создан без уточнения деталей!")
    else:
        print("✅ ПРАВИЛЬНО: AI запрашивает детали о типе справки")
    
    history.append({"role": "user", "content": user_msg_1})
    history.append({"role": "assistant", "content": result_1["response"]})
    
    print_separator()
    
    # Шаг 2: Детали
    user_msg_2 = "Справка об обучении для работы, нужна срочно"
    print_message("Студент", user_msg_2)
    
    result_2 = agent.chat(user_msg_2, chat_history=history)
    print_message("AI", result_2["response"])
    
    if result_2.get("ticket"):
        print("\n✅ Тикет создан с деталями:")
        print(json.dumps(result_2["ticket"], indent=2, ensure_ascii=False))
    
    print_separator()


def main():
    print("\n" + "🚀 ТЕСТИРОВАНИЕ ПРОЦЕССА УТОЧНЕНИЯ ".center(70, "="))
    print("\n")
    
    try:
        # Тест 1: Полный диалог с уточнением
        test_conversation_flow()
        
        # Тест 2: Простой вопрос
        test_simple_question()
        
        # Тест 3: Запрос документа
        test_document_request_flow()
        
        print("\n" + "✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ ".center(70, "="))
        print("\n")
        
        print("📊 ВЫВОДЫ:")
        print("1. AI должен задавать уточняющие вопросы перед созданием тикета")
        print("2. Простые вопросы должны обрабатываться без создания тикета")
        print("3. Детальные тикеты создаются только после сбора информации")
        print("4. Студент должен подтвердить создание тикета")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА ПРИ ВЫПОЛНЕНИИ ТЕСТОВ:\n{str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
