"use client"

import { ProtectedRoute } from "@/components/protected-route"
import { useAuth } from "@/lib/auth-context"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { MessageSquare, FileText, LogOut } from "lucide-react"
import Link from "next/link"

function DashboardContent() {
  const { user, logout } = useAuth()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <header className="bg-white border-b border-blue-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">Support Portal</h1>
              <p className="text-sm text-muted-foreground">Welcome, {user?.name}</p>
            </div>
          </div>
          <Button variant="outline" onClick={logout} className="gap-2 bg-transparent">
            <LogOut className="w-4 h-4" />
            Log Out
          </Button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-2 text-balance">How can we help you?</h2>
          <p className="text-muted-foreground text-balance">
            Start a consultation with our AI bot or view your tickets
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <Link href="/chat">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-blue-100 h-full">
              <CardHeader>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <MessageSquare className="w-6 h-6 text-blue-600" />
                </div>
                <CardTitle className="text-balance">Start Consultation</CardTitle>
                <CardDescription className="text-balance">
                  Ask our AI consultant a question and get instant help
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full bg-blue-600 hover:bg-blue-700">Open Chat</Button>
              </CardContent>
            </Card>
          </Link>

          <Link href="/tickets">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-blue-100 h-full">
              <CardHeader>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <FileText className="w-6 h-6 text-blue-600" />
                </div>
                <CardTitle className="text-balance">My Tickets</CardTitle>
                <CardDescription className="text-balance">
                  View the history of your requests and their status
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" className="w-full border-blue-200 bg-transparent">
                  View Tickets
                </Button>
              </CardContent>
            </Card>
          </Link>
        </div>
      </main>
    </div>
  )
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  )
}
