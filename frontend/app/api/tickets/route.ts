import { type NextRequest, NextResponse } from "next/server"

// Mock data - in production, this would come from a database
const mockTickets = [
  {
    id: "TKT-1234567890",
    category: "Technical Issues",
    message: "I'm having trouble logging into my account. The password reset link doesn't seem to work.",
    status: "in-progress" as const,
    createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
    responses: [
      {
        role: "admin" as const,
        message:
          "Thank you for contacting us. We've identified the issue with the password reset system and are working on a fix. In the meantime, I can manually reset your password. Please check your email.",
        timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
      },
      {
        role: "user" as const,
        message: "Thank you! I received the email and was able to reset my password successfully.",
        timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000),
      },
    ],
  },
  {
    id: "TKT-1234567891",
    category: "Course Questions",
    message: "I need to change my course schedule for next semester. How can I do that?",
    status: "open" as const,
    createdAt: new Date(Date.now() - 5 * 60 * 60 * 1000), // 5 hours ago
    responses: [],
  },
  {
    id: "TKT-1234567892",
    category: "Payment Issues",
    message: "My payment was processed but I haven't received confirmation. Transaction ID: PAY-12345",
    status: "resolved" as const,
    createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 7 days ago
    responses: [
      {
        role: "admin" as const,
        message:
          "We've located your payment. There was a delay in our system. Your payment has been confirmed and you should receive a confirmation email shortly.",
        timestamp: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000),
      },
      {
        role: "user" as const,
        message: "Perfect! I received the confirmation. Thank you for your help!",
        timestamp: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000),
      },
    ],
  },
]

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const userId = searchParams.get("userId")

    // In production, filter tickets by userId from database
    // For now, return mock data
    return NextResponse.json({ tickets: mockTickets })
  } catch (error) {
    console.error("[v0] Error fetching tickets:", error)
    return NextResponse.json({ error: "Failed to fetch tickets" }, { status: 500 })
  }
}
