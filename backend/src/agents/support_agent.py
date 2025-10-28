"""
AI Agent for Student Support using LangChain + Groq
Automatically detects student problems and suggests solutions
"""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict
from src.agents.tools import TOOLS

load_dotenv()

class StudentSupportAgent:
    def __init__(self, student_id: str = None):
        # Ensure student_id is always a string
        self.student_id = str(student_id) if student_id else "unknown"
        
        # Initialize Groq LLM
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model="qwen/qwen3-32b",  # More capable model for tool use
            temperature=0.7,
            api_key=api_key
        )
        
        # Create system prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — AI-ассистент Master Education для студентов и сотрудников.
Твоя задача: эффективно обрабатывать запросы, следуя точным бизнес-процессам.

📋 КАТЕГОРИИ ЗАПРОСОВ И СЦЕНАРИИ:

1. 🔄 ВОЗВРАТ СРЕДСТВ
   - Спроси: "Укажите, пожалуйста, подробную причину возврата"
   - Заверь: "Мы обязательно рассмотрим Ваш запрос"
   - Инструмент: request_refund()

2. ❄️ ЗАМОРОЗКА ОБУЧЕНИЯ (1-2 месяца)
   - Спроси: "На какой срок хотите заморозку? Точные даты начала и конца?"
   - Информируй: "Уведомим учителей и обновим статус"
   - Инструмент: request_freeze()

3. ☀️ РАЗМОРОЗКА / ПРОДОЛЖЕНИЕ ОБУЧЕНИЯ
   - Спроси: "С какой даты готовы продолжить?"
   - Информируй: "Проверю свободные группы для Вашего уровня"
   - Инструмент: request_unfreeze()

4. 🎁 ИСПОЛЬЗОВАНИЕ БОНУСОВ
   - Спроси: "Какой бонус хотите использовать? (консультация/платформа)"
   - Информируй: "Проверю наличие в системе"
   - Инструмент: use_bonus()

5. 📚 СМЕНА ГРУППЫ / УЧИТЕЛЯ
   - Спроси: "Почему хотите сменить? Желаемое время и дни?"
   - Информируй: "Потребуется одобрение операционного директора"
   - Инструмент: change_group_or_teacher()

6. 🔗 ТЕХНИЧЕСКИЕ ПРОБЛЕМЫ (Ссылки/Платформа/ХБ)
   - СНАЧАЛА предложи решения:
     * Ссылки: "Скопируйте ссылку и вставьте в адресную строку"
     * ХБ: "Включите VPN или подождите 5 минут"
     * Звайд: "Обновите страницу, иногда глючит"
   - Только если не помогло: tech_issue_platform()

7. 📜 СПРАВКА О ПРИСУТСТВИИ
   - Спроси: "Для какой цели нужна справка?"
   - Информируй: "Отправлю шаблон Word для заполнения"
   - Инструмент: request_attendance_certificate()

8. 💰 ПРОДЛЕНИЕ / ДОКУПКА КУРСОВ
   - Уточни: "Продление или докупка? Какой курс и на сколько?"
   - Направь: РОП (допродажа) или Бухгалтер (продление)
   - Инструмент: extend_or_purchase_course()

9. 🤝 ПАРТНЕРСКАЯ ПРОГРАММА
   - Собери: ФИО, Telegram, телефон приглашенного
   - Информируй: "Проверим и начислим бонус при подтверждении"
   - Инструмент: partner_program_request()

10. 🚨 ПРОБЛЕМЫ СОТРУДНИКОВ
    - Узнай суть проблемы детально
    - Определи приоритет
    - Инструмент: staff_issue()

⚠️ ОБЩИЕ ПРАВИЛА:

1. УТОЧНЕНИЕ ПЕРЕД ДЕЙСТВИЕМ:
   - Всегда собирай ВСЕ необходимые детали
   - Задавай вопросы естественно, не как анкета
   - Подтверждай понимание перед созданием тикета

2. ИНФОРМИРОВАНИЕ:
   - Объясняй процесс студенту
   - Сообщай сроки ожидания
   - Указывай кто будет обрабатывать запрос

3. ПРОСТЫЕ ЗАПРОСЫ БЕЗ ТИКЕТОВ:
   - Оценки: check_grades()
   - Расписание: check_schedule()
   - Посещаемость: check_attendance()
   - Материалы: find_learning_materials()
   - Объяснение темы: explain_topic()

4. СТИЛЬ ОБЩЕНИЯ:
   - На русском языке
   - Дружелюбный и профессиональный
   - Показывай заботу о студенте
   - Четко следуй бизнес-процессам

Student ID: {student_id}
"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create agent with tools
        agent = create_tool_calling_agent(self.llm, TOOLS, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=TOOLS,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
    
    def chat(self, message: str, chat_history: List[Dict] = None) -> Dict:
        """
        Process a message from student and return AI response
        
        Args:
            message: Student's message
            chat_history: Previous chat messages
        
        Returns:
            Dictionary with response and optional ticket data
        """
        if chat_history is None:
            chat_history = []
        
        # Convert chat history to LangChain format
        history_messages = []
        for msg in chat_history:
            if msg["role"] == "user":
                history_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                history_messages.append(AIMessage(content=msg["content"]))
        
        try:
            response = self.agent_executor.invoke({
                "input": message,
                "chat_history": history_messages,
                "student_id": str(self.student_id) if self.student_id else "unknown"
            })
            
            output = response["output"]
            
            # Try to extract ticket data from response
            import json
            ticket_data = None
            clean_response = output
            
            try:
                # Check if output contains JSON with ticket info
                if "{" in output and "ticket" in output:
                    # Try to extract JSON from the response
                    start = output.find("{")
                    end = output.rfind("}") + 1
                    if start != -1 and end > start:
                        json_str = output[start:end]
                        parsed = json.loads(json_str)
                        
                        if "ticket" in parsed:
                            ticket_data = parsed["ticket"]
                            clean_response = parsed.get("message", output)
            except json.JSONDecodeError:
                # If parsing fails, return original response
                pass
            
            result = {
                "response": clean_response,
                "ticket": ticket_data
            }
            
            return result
            
        except Exception as e:
            return {
                "response": f"Извините, произошла ошибка: {str(e)}\n\nПопробуйте переформулировать вопрос или обратитесь в поддержку.",
                "ticket": None
            }
    
    async def chat_stream(self, message: str, chat_history: List[Dict] = None):
        """
        Stream response from agent (for real-time UI updates)
        
        Args:
            message: Student's message
            chat_history: Previous chat messages
        
        Yields:
            Chunks of the response
        """
        # For streaming, we'll use the regular chat and yield it in chunks
        # (Full streaming support requires more complex setup with LangChain)
        result = self.chat(message, chat_history)
        response_text = result.get("response", "")
        
        # Simulate streaming by yielding words
        words = response_text.split()
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
