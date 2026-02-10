import { useState } from "react"
import axios from "axios"

const API_BASE = "http://127.0.0.1:8000"

export default function Auth({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false)
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")

    const endpoint = isRegister ? "/register" : "/login"
    
    try {
      let response
      if (isRegister) {
        response = await axios.post(`${API_BASE}/register`, { username, password })
        if (response.data) {
          alert("Registration successful! Please login.")
          setIsRegister(false)
        }
      } else {
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)

        response = await axios.post(`${API_BASE}/login`, formData)

        localStorage.setItem("token", response.data.access_token)
        onLogin() 
      }
    } catch (err) {
      console.error(err)
      setError(err.response?.data?.detail || "An error occurred")
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>{isRegister ? "Create Account" : "Welcome Back"}</h2>
        {error && <p className="error-msg">{error}</p>}
        
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            placeholder="Username" 
            value={username} 
            onChange={e => setUsername(e.target.value)}
            required 
          />
          <input 
            type="password" 
            placeholder="Password" 
            value={password} 
            onChange={e => setPassword(e.target.value)}
            required 
          />
          <button type="submit" className="primary-btn">
            {isRegister ? "Sign Up" : "Login"}
          </button>
        </form>

        <p className="toggle-text">
          {isRegister ? "Already have an account? " : "Create one "}
          <span onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? "Login" : "Create Account"}
          </span>
        </p>
      </div>
    </div>
  )
}