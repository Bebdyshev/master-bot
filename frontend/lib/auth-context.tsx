"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import { useRouter } from "next/navigation"

interface User {
  id: string
  studentId: string
  name: string
  email: string
}

interface AuthContextType {
  user: User | null
  login: (studentId: string, password: string) => Promise<void>
  logout: () => void
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Check for existing session
    const storedUser = localStorage.getItem("user")
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
    setIsLoading(false)
  }, [])

  const login = async (studentId: string, password: string) => {
    try {
      // POST directly to the external Students/login endpoint as requested
      const response = await fetch("https://api.mastereducation.kz/api/Students/login", {
        method: "POST",
        headers: {
          "Accept": "application/json, text/plain, */*",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ studentId, password }),
      })

      if (!response.ok) {
        // Try to surface an error message from the response when possible
        let message = "Неверный ID ученика или пароль"
        try {
          const errJson = await response.json()
          if (errJson && (errJson.message || errJson.error)) {
            message = errJson.message || errJson.error
          }
        } catch (e) {
          // ignore parse errors and keep default message
        }
        throw new Error(message)
      }

      const data = await response.json()

      // Normalize possible response shapes. Many APIs return { token, user } or { accessToken, student }
      const token = data?.token || data?.accessToken || null
      const user = data?.user || data?.student || (token ? null : data)

      if (user) {
        setUser(user)
        localStorage.setItem("user", JSON.stringify(user))
      }

      if (token) {
        localStorage.setItem("token", token)
      }

      router.push("/dashboard")
    } catch (error) {
      throw error instanceof Error ? error : new Error("Ошибка при входе")
    }
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem("user")
    localStorage.removeItem("token")
    router.push("/login")
  }

  return <AuthContext.Provider value={{ user, login, logout, isLoading }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
