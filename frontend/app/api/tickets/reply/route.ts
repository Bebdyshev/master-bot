import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { ticketId, message, userId } = body

    // In production, save the reply to the database
    console.log("[v0] Ticket reply:", {
      ticketId,
      userId,
      message,
      timestamp: new Date(),
    })

    // Simulate successful reply
    return NextResponse.json({
      success: true,
      message: "Reply sent successfully",
    })
  } catch (error) {
    console.error("[v0] Error sending reply:", error)
    return NextResponse.json({ error: "Failed to send reply" }, { status: 500 })
  }
}
