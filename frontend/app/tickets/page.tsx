"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { ProtectedRoute } from "@/components/protected-route"
import { useAuth } from "@/lib/auth-context"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { ArrowLeft, Clock, CheckCircle, AlertCircle, MessageSquare } from "lucide-react"
import Link from "next/link"

type Ticket = {
  id: string
  category: string
  message: string
  status: "open" | "in-progress" | "resolved"
  createdAt: Date
  responses: {
    role: "user" | "admin"
    message: string
    timestamp: Date
  }[]
}

function TicketsContent() {
  const { user } = useAuth()
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null)
  const [replyMessage, setReplyMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    // Fetch tickets from API
    fetchTickets()
  }, [])

  const fetchTickets = async () => {
    try {
      const response = await fetch(`/api/tickets?userId=${user?.id}`)
      const data = await response.json()
      setTickets(data.tickets)
    } catch (error) {
      console.error("[v0] Error fetching tickets:", error)
    }
  }

  const handleReply = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!replyMessage.trim() || !selectedTicket) return

    setIsLoading(true)
    try {
      const response = await fetch("/api/tickets/reply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticketId: selectedTicket.id,
          message: replyMessage,
          userId: user?.id,
        }),
      })

      if (response.ok) {
        setReplyMessage("")
        fetchTickets()
        // Update selected ticket
        const updatedTicket = tickets.find((t) => t.id === selectedTicket.id)
        if (updatedTicket) {
          setSelectedTicket(updatedTicket)
        }
      }
    } catch (error) {
      console.error("[v0] Error sending reply:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "open":
        return <Clock className="w-4 h-4" />
      case "in-progress":
        return <AlertCircle className="w-4 h-4" />
      case "resolved":
        return <CheckCircle className="w-4 h-4" />
      default:
        return null
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "open":
        return "bg-blue-100 text-blue-700 border-blue-200"
      case "in-progress":
        return "bg-yellow-100 text-yellow-700 border-yellow-200"
      case "resolved":
        return "bg-green-100 text-green-700 border-green-200"
      default:
        return "bg-gray-100 text-gray-700 border-gray-200"
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <header className="bg-white border-b border-blue-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center gap-4">
          <Link href="/dashboard">
            <Button variant="ghost" size="icon" className="hover:bg-blue-50">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <div>
            <h1 className="text-xl font-bold text-foreground">My Tickets</h1>
            <p className="text-sm text-muted-foreground">View and manage your support requests</p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Tickets List */}
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-foreground">All Tickets</h2>
            {tickets.length === 0 ? (
              <Card className="border-blue-100">
                <CardContent className="py-12 text-center">
                  <MessageSquare className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">No tickets yet</p>
                  <p className="text-sm text-muted-foreground mt-2">
                    Start a chat consultation to create your first ticket
                  </p>
                  <Link href="/chat">
                    <Button className="mt-4 bg-blue-600 hover:bg-blue-700">Start Chat</Button>
                  </Link>
                </CardContent>
              </Card>
            ) : (
              tickets.map((ticket) => (
                <Card
                  key={ticket.id}
                  className={`cursor-pointer transition-all border-blue-100 hover:shadow-md ${
                    selectedTicket?.id === ticket.id ? "ring-2 ring-blue-500" : ""
                  }`}
                  onClick={() => setSelectedTicket(ticket)}
                >
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-base text-balance">{ticket.category}</CardTitle>
                        <CardDescription className="text-sm mt-1">Ticket #{ticket.id}</CardDescription>
                      </div>
                      <Badge variant="outline" className={`gap-1 ${getStatusColor(ticket.status)}`}>
                        {getStatusIcon(ticket.status)}
                        {ticket.status}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground line-clamp-2">{ticket.message}</p>
                    <p className="text-xs text-muted-foreground mt-2">
                      {new Date(ticket.createdAt).toLocaleDateString()} at{" "}
                      {new Date(ticket.createdAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    </p>
                  </CardContent>
                </Card>
              ))
            )}
          </div>

          {/* Ticket Details */}
          <div className="lg:sticky lg:top-6 lg:h-fit">
            {selectedTicket ? (
              <Card className="border-blue-100">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-balance">{selectedTicket.category}</CardTitle>
                      <CardDescription>Ticket #{selectedTicket.id}</CardDescription>
                    </div>
                    <Badge variant="outline" className={`gap-1 ${getStatusColor(selectedTicket.status)}`}>
                      {getStatusIcon(selectedTicket.status)}
                      {selectedTicket.status}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Original Message */}
                  <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                    <p className="text-sm font-medium text-foreground mb-2">Original Request</p>
                    <p className="text-sm text-muted-foreground">{selectedTicket.message}</p>
                    <p className="text-xs text-muted-foreground mt-2">
                      {new Date(selectedTicket.createdAt).toLocaleDateString()} at{" "}
                      {new Date(selectedTicket.createdAt).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>

                  {/* Responses */}
                  {selectedTicket.responses.length > 0 && (
                    <div className="space-y-3">
                      <p className="text-sm font-medium text-foreground">Conversation</p>
                      {selectedTicket.responses.map((response, index) => (
                        <div
                          key={index}
                          className={`p-3 rounded-lg ${
                            response.role === "admin"
                              ? "bg-white border border-blue-100"
                              : "bg-blue-600 text-white ml-8"
                          }`}
                        >
                          <p className="text-xs font-medium mb-1">
                            {response.role === "admin" ? "Support Team" : "You"}
                          </p>
                          <p className="text-sm">{response.message}</p>
                          <p
                            className={`text-xs mt-1 ${response.role === "admin" ? "text-muted-foreground" : "text-blue-100"}`}
                          >
                            {new Date(response.timestamp).toLocaleTimeString([], {
                              hour: "2-digit",
                              minute: "2-digit",
                            })}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Reply Form */}
                  {selectedTicket.status !== "resolved" && (
                    <form onSubmit={handleReply} className="space-y-3">
                      <Textarea
                        value={replyMessage}
                        onChange={(e) => setReplyMessage(e.target.value)}
                        placeholder="Type your reply..."
                        className="border-blue-200 focus:border-blue-500"
                        rows={3}
                      />
                      <Button
                        type="submit"
                        disabled={isLoading || !replyMessage.trim()}
                        className="w-full bg-blue-600 hover:bg-blue-700"
                      >
                        {isLoading ? "Sending..." : "Send Reply"}
                      </Button>
                    </form>
                  )}

                  {selectedTicket.status === "resolved" && (
                    <div className="bg-green-50 p-4 rounded-lg border border-green-200 text-center">
                      <CheckCircle className="w-8 h-8 text-green-600 mx-auto mb-2" />
                      <p className="text-sm font-medium text-green-700">This ticket has been resolved</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Card className="border-blue-100">
                <CardContent className="py-12 text-center">
                  <MessageSquare className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">Select a ticket to view details</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default function TicketsPage() {
  return (
    <ProtectedRoute>
      <TicketsContent />
    </ProtectedRoute>
  )
}
