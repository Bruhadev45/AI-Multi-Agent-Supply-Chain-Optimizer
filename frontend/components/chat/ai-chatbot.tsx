"use client"

import { useState, useRef, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { MessageCircle, X, Send, Bot, User } from "lucide-react"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: Date
}

export function AIChatbot() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello! I'm your AI logistics assistant. I can help you with route optimization, vendor selection, demand forecasting, and supply chain queries. How can I assist you today?",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsTyping(true)

    // Simulate AI response with relevant logistics content
    setTimeout(() => {
      const response = generateLogisticsResponse(input)
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
      setIsTyping(false)
    }, 1000)
  }

  const generateLogisticsResponse = (query: string): string => {
    const lowerQuery = query.toLowerCase()

    // Route optimization queries
    if (lowerQuery.includes("route") || lowerQuery.includes("optimize")) {
      return "To optimize your route, I recommend: 1) Use the route optimization tool on the Optimizer page 2) Select origin and destination cities 3) Choose a scenario (normal, high demand, etc.) 4) Our AI agents will analyze the best path considering cost, time, and risks."
    }

    // Vendor queries
    if (lowerQuery.includes("vendor") || lowerQuery.includes("supplier")) {
      return "For vendor selection, our system evaluates: • Cost efficiency • Reliability score (on-time delivery) • Sustainability metrics • Customer ratings. You can view all vendors on the Routes page and compare their performance metrics."
    }

    // Demand forecasting
    if (lowerQuery.includes("demand") || lowerQuery.includes("forecast")) {
      return "Our Demand Forecast Agent uses historical data and scenario modeling to predict future demand. It considers seasonal trends, market conditions, and supply chain disruptions. Run an analysis to see demand predictions for your route."
    }

    // Risk management
    if (lowerQuery.includes("risk") || lowerQuery.includes("disruption")) {
      return "The Risk Assessment Agent evaluates: • Weather conditions • Traffic patterns • Political stability • Infrastructure quality • Historical delay data. Check the Agents page to see detailed risk analysis for your routes."
    }

    // Cost queries
    if (lowerQuery.includes("cost") || lowerQuery.includes("price") || lowerQuery.includes("budget")) {
      return "Our Cost Optimization Agent analyzes: • Fuel costs • Labor expenses • Toll fees • Vehicle maintenance • Storage costs. It provides the most cost-effective route while maintaining quality standards."
    }

    // Tracking queries
    if (lowerQuery.includes("track") || lowerQuery.includes("shipment") || lowerQuery.includes("delivery")) {
      return "Track your shipments in real-time on the Shipments page. You can monitor: • Current location • ETA • Progress percentage • Carrier information • Delivery status. All shipments are updated in real-time."
    }

    // General queries about the system
    if (lowerQuery.includes("how") || lowerQuery.includes("what") || lowerQuery.includes("help")) {
      return "I can help you with: 📊 Route optimization and planning 🚚 Vendor and supplier selection 📈 Demand forecasting 🎯 Risk assessment ⚠️ Cost analysis 💰 📦 Shipment tracking. What specific area would you like to know more about?"
    }

    // Default response
    return "I'm here to help with your supply chain and logistics needs! You can ask me about route optimization, vendor selection, demand forecasting, risk management, cost analysis, or shipment tracking. What would you like to know?"
  }

  return (
    <>
      {/* Chat Button */}
      {!isOpen && (
        <Button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg bg-primary hover:bg-primary/90 z-50"
          size="icon"
        >
          <MessageCircle className="h-6 w-6" />
        </Button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <Card className="fixed bottom-6 right-6 w-96 h-[500px] shadow-2xl z-50 flex flex-col bg-card border-2 border-border">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-border bg-primary text-primary-foreground rounded-t-lg">
            <div className="flex items-center gap-2">
              <Bot className="h-5 w-5" />
              <div>
                <h3 className="font-semibold">AI Logistics Assistant</h3>
                <p className="text-xs opacity-90">Always here to help</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsOpen(false)}
              className="h-8 w-8 text-primary-foreground hover:bg-primary-foreground/20"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-2 ${
                  message.role === "user" ? "flex-row-reverse" : "flex-row"
                }`}
              >
                <div
                  className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-foreground"
                  }`}
                >
                  {message.role === "user" ? (
                    <User className="h-4 w-4" />
                  ) : (
                    <Bot className="h-4 w-4" />
                  )}
                </div>
                <div
                  className={`flex-1 rounded-lg p-3 ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground ml-8"
                      : "bg-muted text-foreground mr-8"
                  }`}
                >
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">
                    {message.content}
                  </p>
                  <p
                    className={`text-xs mt-1 opacity-70`}
                  >
                    {message.timestamp.toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </p>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex gap-2">
                <div className="flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center bg-muted text-foreground">
                  <Bot className="h-4 w-4" />
                </div>
                <div className="flex-1 rounded-lg p-3 bg-muted text-foreground mr-8">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-foreground/40 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-foreground/40 rounded-full animate-bounce delay-100" />
                    <div className="w-2 h-2 bg-foreground/40 rounded-full animate-bounce delay-200" />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-border">
            <form
              onSubmit={(e) => {
                e.preventDefault()
                handleSend()
              }}
              className="flex gap-2"
            >
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about logistics..."
                className="flex-1"
                disabled={isTyping}
              />
              <Button
                type="submit"
                size="icon"
                disabled={!input.trim() || isTyping}
                className="bg-primary hover:bg-primary/90"
              >
                <Send className="h-4 w-4" />
              </Button>
            </form>
          </div>
        </Card>
      )}
    </>
  )
}
