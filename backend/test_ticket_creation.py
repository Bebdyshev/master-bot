#!/usr/bin/env python3
"""
Скрипт для тестирования создания тикетов
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.support_agent import StudentSupportAgent
import json


def test_technical_issue():
    """Test technical issue ticket creation"""
    print("=" * 60)
    print("TEST 1: Техническая проблема")
    print("=" * 60)
    
    agent = StudentSupportAgent(student_id="TEST123")
    
    result = agent.chat("Не могу войти в систему, пишет ошибку авторизации")
    
    print("\nОтвет агента:")
    print(result["response"])
    
    if result.get("ticket"):
        print("\n📋 ИНФОРМАЦИЯ О ТИКЕТЕ:")
        print(json.dumps(result["ticket"], indent=2, ensure_ascii=False))
    else:
        print("\n⚠️ Тикет не был создан!")
    
    print("\n")


def test_document_request():
    """Test document request ticket creation"""
    print("=" * 60)
    print("TEST 2: Запрос документа")
    print("=" * 60)
    
    agent = StudentSupportAgent(student_id="TEST456")
    
    result = agent.chat("Мне нужна справка об обучении")
    
    print("\nОтвет агента:")
    print(result["response"])
    
    if result.get("ticket"):
        print("\n📋 ИНФОРМАЦИЯ О ТИКЕТЕ:")
        print(json.dumps(result["ticket"], indent=2, ensure_ascii=False))
    else:
        print("\n⚠️ Тикет не был создан!")
    
    print("\n")


def test_teacher_contact():
    """Test teacher contact ticket creation"""
    print("=" * 60)
    print("TEST 3: Сообщение преподавателю")
    print("=" * 60)
    
    agent = StudentSupportAgent(student_id="TEST789")
    
    result = agent.chat("Хочу связаться с преподавателем Ивановым по математике, у меня вопрос по домашнему заданию")
    
    print("\nОтвет агента:")
    print(result["response"])
    
    if result.get("ticket"):
        print("\n📋 ИНФОРМАЦИЯ О ТИКЕТЕ:")
        print(json.dumps(result["ticket"], indent=2, ensure_ascii=False))
    else:
        print("\n⚠️ Тикет не был создан!")
    
    print("\n")


def test_priority_detection():
    """Test priority detection"""
    print("=" * 60)
    print("TEST 4: Определение приоритета (срочная проблема)")
    print("=" * 60)
    
    agent = StudentSupportAgent(student_id="TEST999")
    
    result = agent.chat("СРОЧНО! Не могу сдать экзамен, система выдает ошибку!")
    
    print("\nОтвет агента:")
    print(result["response"])
    
    if result.get("ticket"):
        print("\n📋 ИНФОРМАЦИЯ О ТИКЕТЕ:")
        print(json.dumps(result["ticket"], indent=2, ensure_ascii=False))
        print(f"\n⚡ Приоритет: {result['ticket'].get('priority', 'unknown').upper()}")
    else:
        print("\n⚠️ Тикет не был создан!")
    
    print("\n")


def test_normal_question():
    """Test normal question (should not create ticket)"""
    print("=" * 60)
    print("TEST 5: Обычный вопрос (не должен создавать тикет)")
    print("=" * 60)
    
    agent = StudentSupportAgent(student_id="TEST000")
    
    result = agent.chat("Какие у меня оценки?")
    
    print("\nОтвет агента:")
    print(result["response"])
    
    if result.get("ticket"):
        print("\n❌ ОШИБКА: Тикет был создан, хотя не должен был!")
        print(json.dumps(result["ticket"], indent=2, ensure_ascii=False))
    else:
        print("\n✅ Правильно: Тикет не создан для обычного вопроса")
    
    print("\n")


if __name__ == "__main__":
    print("\n🚀 ТЕСТИРОВАНИЕ СИСТЕМЫ СОЗДАНИЯ ТИКЕТОВ\n")
    
    try:
        test_technical_issue()
        test_document_request()
        test_teacher_contact()
        test_priority_detection()
        test_normal_question()
        
        print("=" * 60)
        print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ОШИБКА ПРИ ВЫПОЛНЕНИИ ТЕСТОВ:\n{str(e)}")
        import traceback
        traceback.print_exc()
