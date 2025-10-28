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
  options?: string[]
}

type ConversationState = "greeting" | "category-selection" | "problem-solving" | "ticket-created"

function ChatContent() {
  const { user } = useAuth()
  const router = useRouter()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [conversationState, setConversationState] = useState<ConversationState>("greeting")
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const categories = ["Technical Issues", "Account Problems", "Course Questions", "Payment Issues", "Other"]

  useEffect(() => {
    // Initial greeting
    const greeting: Message = {
      id: "1",
      role: "assistant",
      content: `Hello ${user?.name}! I'm your AI support assistant. I'm here to help you with any questions or issues you may have. Please select a category to get started:`,
      timestamp: new Date(),
      options: categories,
    }
    setMessages([greeting])
  }, [user?.name])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleCategorySelect = async (category: string) => {
    setSelectedCategory(category)
    setConversationState("problem-solving")

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: category,
      timestamp: new Date(),
    }

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: "assistant",
      content: `Great! You've selected "${category}". Please describe your issue in detail, and I'll do my best to help you resolve it.`,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage, assistantMessage])
  }

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
      // Call the API to process the message
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: input,
          category: selectedCategory,
          conversationState,
          userId: user?.id,
        }),
      })

      const data = await response.json()

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.message,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])

      // Check if a ticket was created
      if (data.ticketCreated) {
        setConversationState("ticket-created")
        const ticketMessage: Message = {
          id: (Date.now() + 2).toString(),
          role: "system",
          content: `A support ticket (#${data.ticketId}) has been created for you. Our team will review it and get back to you soon. You can view your tickets in the "My Tickets" section.`,
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, ticketMessage])
      }
    } catch (error) {
      console.error("[v0] Error sending message:", error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "I'm sorry, I encountered an error processing your request. Please try again.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex flex-col">
      <header className="bg-white border-b border-blue-100 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center gap-4">
          <Link href="/dashboard">
            <Button variant="ghost" size="icon" className="hover:bg-blue-50">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <div>
            <h1 className="text-xl font-bold text-foreground">AI Support Chat</h1>
            <p className="text-sm text-muted-foreground">Get instant help from our AI assistant</p>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col">
        <div className="flex-1 overflow-y-auto mb-4 space-y-4">
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
                <p className="text-sm leading-relaxed">{message.content}</p>
                {message.options && (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {message.options.map((option) => (
                      <Button
                        key={option}
                        variant="outline"
                        size="sm"
                        onClick={() => handleCategorySelect(option)}
                        className="bg-white hover:bg-blue-50 border-blue-200"
                      >
                        {option}
                      </Button>
                    ))}
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
                  <p className="text-sm text-muted-foreground">AI is thinking...</p>
                </div>
              </Card>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSendMessage} className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading || conversationState === "greeting"}
            className="flex-1 border-blue-200 focus:border-blue-500"
          />
          <Button
            type="submit"
            disabled={isLoading || !input.trim() || conversationState === "greeting"}
            className="bg-blue-600 hover:bg-blue-700"
          >
            <Send className="w-4 h-4" />
          </Button>
        </form>
      </main>
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
