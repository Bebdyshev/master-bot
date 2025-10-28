"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { ProtectedRoute } from "@/components/protected-route"
import { useAuth } from "@/lib/auth-context"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { ArrowLeft, Send, Loader2 } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"

type Message = {
  id: string
  role: "user" | "assistant" | "system"
  content: string
  timestamp: Date
  ticket?: {
    ticket_id: string
    type: string
    status: string
    priority: string
    description: string
    student_id?: string
    created_at: string
    estimated_response: string
  }
}

function ChatContent() {
  const { user } = useAuth()
  const router = useRouter()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Initial greeting
    const greeting: Message = {
      id: "1",
      role: "assistant",
      content: `Привет! Я ваш AI-ассистент. Чем могу помочь? 

Я могу:
🔧 Решать технические проблемы
📊 Проверять оценки и успеваемость  
📅 Показывать расписание
📚 Находить учебные материалы
📄 Оформлять документы и справки
✉️ Связывать с преподавателями
📈 Проверять посещаемость

💡 Совет: Опишите вашу проблему подробно - это поможет мне лучше вам помочь. Я могу задать уточняющие вопросы перед тем, как создать тикет на поддержку.`,
      timestamp: new Date(),
    }
    setMessages([greeting])
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
      
      // Get chat history for context
      const history = messages.map(msg => ({
        role: msg.role === "system" ? "assistant" : msg.role,
        content: msg.content
      }))

      const response = await fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: input,
          history: history,
          student_id: user?.studentId || user?.id,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to get response")
      }

      const data = await response.json()

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response || "Извините, не смог обработать ваш запрос. Попробуйте еще раз.",
        timestamp: new Date(),
        ticket: data.ticket || undefined,
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error("Error sending message:", error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Извините, произошла ошибка при обработке запроса. Попробуйте еще раз.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="h-screen bg-gradient-to-br from-blue-50 to-white flex flex-col">
      <header className="flex-shrink-0 bg-white border-b border-blue-100 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center gap-4">
          <Link href="/dashboard">
            <Button variant="ghost" size="icon" className="hover:bg-blue-50">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <div>
            <h1 className="text-xl font-bold text-foreground">AI Поддержка</h1>
            <p className="text-sm text-muted-foreground">Получите мгновенную помощь от AI-ассистента</p>
          </div>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto">
        <main className="max-w-4xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
              <Card
                className={`max-w-[80%] p-4 ${
                  message.role === "user"
                    ? "bg-blue-600 text-white border-blue-600"
                    : message.role === "system"
                      ? "bg-green-50 border-green-200"
                      : "bg-white border-blue-100"
                }`}
              >
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                
                {/* Ticket Card UI - Enhanced with Business Categories */}
                {message.ticket && (
                  <div className={`mt-4 p-5 rounded-xl shadow-lg border-2 ${
                    message.ticket.type === 'technical' || message.ticket.type === 'technical_platform'
                      ? 'bg-gradient-to-br from-emerald-50 to-blue-50 border-emerald-300'
                      : message.ticket.type === 'document' || message.ticket.type === 'certificate'
                      ? 'bg-gradient-to-br from-purple-50 to-pink-50 border-purple-300'
                      : message.ticket.type === 'teacher-message'
                      ? 'bg-gradient-to-br from-orange-50 to-yellow-50 border-orange-300'
                      : message.ticket.type === 'refund'
                      ? 'bg-gradient-to-br from-red-50 to-orange-50 border-red-300'
                      : message.ticket.type === 'freeze' || message.ticket.type === 'unfreeze'
                      ? 'bg-gradient-to-br from-cyan-50 to-blue-50 border-cyan-300'
                      : message.ticket.type === 'bonus'
                      ? 'bg-gradient-to-br from-yellow-50 to-amber-50 border-yellow-300'
                      : message.ticket.type === 'group_change'
                      ? 'bg-gradient-to-br from-indigo-50 to-purple-50 border-indigo-300'
                      : message.ticket.type === 'extension'
                      ? 'bg-gradient-to-br from-green-50 to-emerald-50 border-green-300'
                      : message.ticket.type === 'partner_program'
                      ? 'bg-gradient-to-br from-pink-50 to-rose-50 border-pink-300'
                      : message.ticket.type === 'staff_issue'
                      ? 'bg-gradient-to-br from-slate-50 to-gray-50 border-slate-300'
                      : 'bg-gradient-to-br from-gray-50 to-slate-50 border-gray-300'
                  }`}>
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-2xl">
                            {message.ticket.type === 'technical' || message.ticket.type === 'technical_platform' ? '🔧' :
                             message.ticket.type === 'document' || message.ticket.type === 'certificate' ? '📄' :
                             message.ticket.type === 'teacher-message' ? '✉️' :
                             message.ticket.type === 'refund' ? '🔄' :
                             message.ticket.type === 'freeze' ? '❄️' :
                             message.ticket.type === 'unfreeze' ? '☀️' :
                             message.ticket.type === 'bonus' ? '�' :
                             message.ticket.type === 'group_change' ? '📚' :
                             message.ticket.type === 'extension' ? '💰' :
                             message.ticket.type === 'partner_program' ? '🤝' :
                             message.ticket.type === 'staff_issue' ? '🚨' :
                             '�🎫'}
                          </span>
                          <h3 className={`font-bold text-lg ${
                            message.ticket.type === 'technical' || message.ticket.type === 'technical_platform' ? 'text-emerald-900' :
                            message.ticket.type === 'document' || message.ticket.type === 'certificate' ? 'text-purple-900' :
                            message.ticket.type === 'teacher-message' ? 'text-orange-900' :
                            message.ticket.type === 'refund' ? 'text-red-900' :
                            message.ticket.type === 'freeze' || message.ticket.type === 'unfreeze' ? 'text-cyan-900' :
                            message.ticket.type === 'bonus' ? 'text-yellow-900' :
                            message.ticket.type === 'group_change' ? 'text-indigo-900' :
                            message.ticket.type === 'extension' ? 'text-green-900' :
                            message.ticket.type === 'partner_program' ? 'text-pink-900' :
                            message.ticket.type === 'staff_issue' ? 'text-slate-900' :
                            'text-gray-900'
                          }`}>
                            {message.ticket.type === 'technical' || message.ticket.type === 'technical_platform' ? 'Техническая проблема' :
                             message.ticket.type === 'document' ? 'Запрос документа' :
                             message.ticket.type === 'certificate' ? 'Справка о присутствии' :
                             message.ticket.type === 'teacher-message' ? 'Сообщение преподавателю' :
                             message.ticket.type === 'refund' ? 'Возврат средств' :
                             message.ticket.type === 'freeze' ? 'Заморозка обучения' :
                             message.ticket.type === 'unfreeze' ? 'Разморозка обучения' :
                             message.ticket.type === 'bonus' ? 'Использование бонуса' :
                             message.ticket.type === 'group_change' ? 'Смена группы/учителя' :
                             message.ticket.type === 'extension' ? 'Продление/Докупка' :
                             message.ticket.type === 'partner_program' ? 'Партнерская программа' :
                             message.ticket.type === 'staff_issue' ? 'Проблема сотрудника' :
                             'Тикет создан'}
                          </h3>
                        </div>
                        <p className={`text-sm mt-1 font-mono ${
                          message.ticket.type === 'technical' || message.ticket.type === 'technical_platform' ? 'text-emerald-700' :
                          message.ticket.type === 'document' || message.ticket.type === 'certificate' ? 'text-purple-700' :
                          message.ticket.type === 'teacher-message' ? 'text-orange-700' :
                          message.ticket.type === 'refund' ? 'text-red-700' :
                          message.ticket.type === 'freeze' || message.ticket.type === 'unfreeze' ? 'text-cyan-700' :
                          message.ticket.type === 'bonus' ? 'text-yellow-700' :
                          message.ticket.type === 'group_change' ? 'text-indigo-700' :
                          message.ticket.type === 'extension' ? 'text-green-700' :
                          message.ticket.type === 'partner_program' ? 'text-pink-700' :
                          message.ticket.type === 'staff_issue' ? 'text-slate-700' :
                          'text-gray-700'
                        }`}>
                          #{message.ticket.ticket_id}
                        </p>
                      </div>
                      <span className={`px-3 py-1.5 text-xs font-bold rounded-full border-2 ${
                        message.ticket.status === 'open' 
                          ? 'bg-amber-100 text-amber-800 border-amber-300'
                          : message.ticket.status === 'in-progress'
                          ? 'bg-blue-100 text-blue-800 border-blue-300'
                          : 'bg-green-100 text-green-800 border-green-300'
                      }`}>
                        {message.ticket.status === 'open' ? '🟡 ОТКРЫТ' : 
                         message.ticket.status === 'in-progress' ? '🔵 В РАБОТЕ' : 
                         '🟢 ЗАКРЫТ'}
                      </span>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="bg-white/60 rounded-lg p-3 border border-gray-200">
                        <div className="grid grid-cols-2 gap-3 text-sm">
                          <div>
                            <span className="text-gray-600 font-medium block mb-1">📋 Тип:</span>
                            <span className="text-gray-900 font-semibold capitalize">
                              {message.ticket.type === 'technical' ? 'Техническая' : 
                               message.ticket.type === 'document' ? 'Документ' :
                               message.ticket.type === 'teacher-message' ? 'Преподаватель' :
                               message.ticket.type}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-600 font-medium block mb-1">⚡ Приоритет:</span>
                            <span className={`inline-block px-2.5 py-1 rounded-md text-xs font-bold ${
                              message.ticket.priority === 'high' ? 'bg-red-100 text-red-700 border border-red-300' :
                              message.ticket.priority === 'medium' ? 'bg-orange-100 text-orange-700 border border-orange-300' :
                              'bg-green-100 text-green-700 border border-green-300'
                            }`}>
                              {message.ticket.priority === 'high' ? '🔴 ВЫСОКИЙ' :
                               message.ticket.priority === 'medium' ? '🟠 СРЕДНИЙ' :
                               '🟢 НИЗКИЙ'}
                            </span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="bg-white/60 rounded-lg p-3 border border-gray-200">
                        <span className="text-gray-600 font-medium text-sm block mb-2">📝 Описание:</span>
                        <p className="text-gray-900 text-sm leading-relaxed">{message.ticket.description}</p>
                      </div>
                      
                      <div className="bg-white/60 rounded-lg p-3 border border-gray-200">
                        <div className="flex items-center justify-between text-sm">
                          <div>
                            <span className="text-gray-600 font-medium">⏱️ Время ответа:</span>
                            <span className="text-gray-900 font-semibold ml-2">{message.ticket.estimated_response}</span>
                          </div>
                          <div className="text-xs text-gray-500">
                            {new Date(message.ticket.created_at).toLocaleString('ru-RU', {
                              day: '2-digit',
                              month: '2-digit',
                              year: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className={`mt-4 pt-4 border-t-2 ${
                      message.ticket.type === 'technical' ? 'border-emerald-200' :
                      message.ticket.type === 'document' ? 'border-purple-200' :
                      message.ticket.type === 'teacher-message' ? 'border-orange-200' :
                      'border-gray-200'
                    }`}>
                      <div className="flex items-center gap-2 text-sm">
                        <span className="text-lg">✅</span>
                        <p className={`font-semibold ${
                          message.ticket.type === 'technical' ? 'text-emerald-700' :
                          message.ticket.type === 'document' ? 'text-purple-700' :
                          message.ticket.type === 'teacher-message' ? 'text-orange-700' :
                          'text-gray-700'
                        }`}>
                          {message.ticket.type === 'technical' 
                            ? 'Техническая поддержка свяжется с вами в ближайшее время'
                            : message.ticket.type === 'document'
                            ? 'Документ будет подготовлен в указанный срок'
                            : message.ticket.type === 'teacher-message'
                            ? 'Преподаватель получит ваше сообщение'
                            : 'Ваш запрос обрабатывается'}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
                
                <p className="text-xs mt-2 opacity-70">
                  {message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </p>
              </Card>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <Card className="max-w-[80%] p-4 bg-white border-blue-100">
                <div className="flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                  <p className="text-sm text-muted-foreground">AI думает...</p>
                </div>
              </Card>
            </div>
          )}
          <div ref={messagesEndRef} />
        </main>
      </div>

      <div className="flex-shrink-0 max-w-4xl w-full mx-auto px-4 sm:px-6 lg:px-8 pb-4">
        <form onSubmit={handleSendMessage} className="flex gap-2 py-4">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Введите ваше сообщение..."
            disabled={isLoading}
            className="flex-1 border-blue-200 focus:border-blue-500"
          />
          <Button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700"
          >
            <Send className="w-4 h-4" />
          </Button>
        </form>
      </div>
    </div>
  )
}

export default function ChatPage() {
  return (
    <ProtectedRoute>
      <ChatContent />
    </ProtectedRoute>
  )
}
