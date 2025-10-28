import { type NextRequest, NextResponse } from "next/server"

type ChatRequest = {
  message: string
  category: string | null
  conversationState: string
  userId: string
}

// Simple keyword-based response system
const getAIResponse = (message: string, category: string | null): { message: string; shouldCreateTicket: boolean } => {
  const lowerMessage = message.toLowerCase()

  // Technical Issues
  if (category === "Technical Issues") {
    if (lowerMessage.includes("login") || lowerMessage.includes("password")) {
      return {
        message:
          "For login issues, try resetting your password using the 'Forgot Password' link on the login page. If that doesn't work, I'll create a ticket for our technical team to assist you.",
        shouldCreateTicket: lowerMessage.includes("reset") || lowerMessage.includes("doesn't work"),
      }
    }
    if (lowerMessage.includes("slow") || lowerMessage.includes("loading")) {
      return {
        message:
          "Try clearing your browser cache and cookies. If the issue persists, I'll escalate this to our technical team.",
        shouldCreateTicket: true,
      }
    }
  }

  // Account Problems
  if (category === "Account Problems") {
    if (lowerMessage.includes("email") || lowerMessage.includes("contact")) {
      return {
        message:
          "You can update your contact information in your profile settings. Would you like me to create a ticket for account verification?",
        shouldCreateTicket: lowerMessage.includes("can't") || lowerMessage.includes("unable"),
      }
    }
  }

  // Course Questions
  if (category === "Course Questions") {
    if (lowerMessage.includes("schedule") || lowerMessage.includes("timetable")) {
      return {
        message:
          "You can view your course schedule in the 'My Courses' section. If you need to make changes, I'll create a ticket for the academic team.",
        shouldCreateTicket: lowerMessage.includes("change") || lowerMessage.includes("modify"),
      }
    }
  }

  // Payment Issues
  if (category === "Payment Issues") {
    return {
      message:
        "Payment issues require verification from our finance team. I'm creating a ticket for you now, and they'll contact you within 24 hours.",
      shouldCreateTicket: true,
    }
  }

  // Default response - create ticket for complex issues
  if (lowerMessage.length > 100 || lowerMessage.includes("help") || lowerMessage.includes("urgent")) {
    return {
      message:
        "I understand this is a complex issue. Let me create a support ticket so our team can provide you with detailed assistance.",
      shouldCreateTicket: true,
    }
  }

  return {
    message:
      "I've noted your concern. Could you provide more details so I can better assist you? If this is urgent, I can create a support ticket for immediate attention.",
    shouldCreateTicket: false,
  }
}

export async function POST(request: NextRequest) {
  try {
    const body: ChatRequest = await request.json()
    const { message, category, userId } = body

    // Get AI response
    const { message: aiMessage, shouldCreateTicket } = getAIResponse(message, category)

    let ticketId = null
    if (shouldCreateTicket) {
      // Generate a ticket ID (in production, this would be stored in a database)
      ticketId = `TKT-${Date.now()}`

      // Here you would typically save the ticket to a database
      console.log("[v0] Creating ticket:", {
        ticketId,
        userId,
        category,
        message,
        status: "open",
        createdAt: new Date(),
      })
    }

    return NextResponse.json({
      message: aiMessage,
      ticketCreated: shouldCreateTicket,
      ticketId,
    })
  } catch (error) {
    console.error("[v0] Error in chat API:", error)
    return NextResponse.json({ error: "Failed to process message" }, { status: 500 })
  }
}
