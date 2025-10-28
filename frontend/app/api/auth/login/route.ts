import { type NextRequest, NextResponse } from "next/server"

// Mock user database - replace with real database
const MOCK_USERS = [
  {
    id: "1",
    studentId: "STU001",
    password: "password123",
    name: "Иван Петров",
    email: "ivan@example.com",
  },
  {
    id: "2",
    studentId: "STU002",
    password: "password123",
    name: "Мария Иванова",
    email: "maria@example.com",
  },
]

export async function POST(request: NextRequest) {
  try {
    const { studentId, password } = await request.json()

    // Find user
    const user = MOCK_USERS.find((u) => u.studentId === studentId && u.password === password)

    if (!user) {
      return NextResponse.json({ error: "Неверный ID ученика или пароль" }, { status: 401 })
    }

    // Generate mock token
    const token = `token_${user.id}_${Date.now()}`

    // Return user data without password
    const { password: _, ...userWithoutPassword } = user

    return NextResponse.json({
      user: userWithoutPassword,
      token,
    })
  } catch (error) {
    return NextResponse.json({ error: "Ошибка сервера" }, { status: 500 })
  }
}
