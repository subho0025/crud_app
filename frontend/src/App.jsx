import { useEffect, useState } from "react"
import axios from "axios"
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd"
import Auth from "./Auth"
import "./App.css"

/*Mapping of database status values to the values that is being printed on the website*/
const STATUS_MAP = {
  pending: "Pending",
  in_progress: "In Progress",
  completed: "Completed",
}
/*for Linking the backend with the frontend */
const API_BASE = "http://127.0.0.1:8000"

function App() {

  const [tasks, setTasks] = useState([])
  const [trash, setTrash] = useState([])


  const [isFormOpen, setIsFormOpen] = useState(false)
  const [isRecycleView, setIsRecycleView] = useState(false)
  const [editingTaskId, setEditingTaskId] = useState(null)
  const [taskPreview, setTaskPreview] = useState(null)


  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [status, setStatus] = useState("pending")

  const [token, setToken] = useState(localStorage.getItem("token"))

  // This function adds the token to every request
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`
      loadTasks()
      loadTrash()
    } else {
      delete axios.defaults.headers.common["Authorization"]
      setTasks([]) // Clear data on logout
      setTrash([])
    }
  }, [token])

  const handleLogout = () => {
    localStorage.removeItem("token")
    setToken(null)
  }

/*This is for changing the date from UTC to IST */
  const formatDate = (value) => {
    if (!value) return "-"
    if (!value.includes("Z")) {
        value = value.replace(" ", "T") + "Z";
    }

    return new Date(value).toLocaleString("en-IN", {
      timeZone: "Asia/Kolkata",
      day: "2-digit",
      month: "short",
      year: "numeric",
      minute: "2-digit",
      hour: "2-digit",
      hour12: true
    })
  }
/*This is for fetching all the records */
  const loadTasks = async () => {
    try {
      const { data } = await axios.get(`${API_BASE}/tasks`)
      setTasks(data)
    } catch (err) {
      console.error("Failed to load tasks", err)
    }
  }
/*This is for fetching all the records in the recycle bin which are soft deleted */

  const loadTrash = async () => {
    try {
      const { data } = await axios.get(`${API_BASE}/recycle-bin`)
      setTrash(data)
    } catch (err) {
      console.error("Failed to load recycle bin", err)
    }
  }
/*For fetching a particular record */
  const getTask = async (id) => {
    const { data } = await axios.get(`${API_BASE}/tasks/${id}`)
    return data
  }

  useEffect(() => {
    loadTasks()
    loadTrash()
  }, [])

/*For creating a new record */
  const startCreate = () => {
    setEditingTaskId(null)
    setTitle("")
    setDescription("")
    setStatus("pending")
    setIsFormOpen(true)
  }
/*For editing a record */
  const startEdit = async (id) => {
    const task = await getTask(id)

    setEditingTaskId(task.id)
    setTitle(task.title)
    setDescription(task.description || "")
    setStatus(task.status)
    setIsFormOpen(true)
  }
/*Saving the edited record */
  const saveTask = async () => {
    if (!title.trim()) {
      alert("Title cannot be empty")
      return
    }

    const payload = { title, description, status } // A variable used as an alias for the record

    try {
      if (editingTaskId) {
        await axios.patch(`${API_BASE}/tasks/${editingTaskId}`, payload)
      } else {
        await axios.post(`${API_BASE}/tasks`, payload)
      }

      setIsFormOpen(false)
      loadTasks()
    } catch (err) {
      console.error("Save failed", err)
    }
  }

  //Soft delete
  const moveToTrash = async (id) => {
    await axios.delete(`${API_BASE}/tasks/${id}`)
    loadTasks()
    loadTrash()
  }
//Restoring a soft-deleted record
  const restoreTask = async (id) => {
    await axios.put(`${API_BASE}/recycle-bin/${id}`)
    loadTasks()
    loadTrash()
  }
//Permanent delete
  const deleteForever = async (id) => {
    if (!window.confirm("Permanently delete this task?")) return
    await axios.delete(`${API_BASE}/recycle-bin/${id}`)
    loadTrash()
  }

  const openDetails = async (id) => {
    const task = await getTask(id)
    setTaskPreview(task)
  }

  // Helper to group tasks into columns
  const getTasksByStatus = () => {
    const grouped = { pending: [], in_progress: [], completed: [] }
    tasks.forEach(t => {
      if (grouped[t.status]) grouped[t.status].push(t)
      else grouped['pending'].push(t)
    })
    return grouped
  }

  // Drag and drop handler
  const onDragEnd = async (result) => {
    const { source, destination, draggableId } = result

    if (!destination) return

    if (
      source.droppableId === destination.droppableId &&
      source.index === destination.index
    ) return

    const newStatus = destination.droppableId
    const taskId = parseInt(draggableId)

    //Optimistic Update (Instant UI change)
    const updatedTasks = tasks.map(t => 
      t.id === taskId ? { ...t, status: newStatus } : t
    )
    setTasks(updatedTasks)

    //API Update (Background)
    try {
      await axios.patch(`${API_BASE}/tasks/${taskId}`, { status: newStatus })
    } catch (err) {
      console.error("Failed to move task", err)
      loadTasks() // Revert if API fails
    }
  }

  if (!token) {
    return <Auth onLogin={() => setToken(localStorage.getItem("token"))} />
  }

  const list = isRecycleView ? trash : tasks
  const groupedTasks = getTasksByStatus()
  const COLUMNS = ["pending", "in_progress", "completed"]

  return (
    <div className="container">
      <div className="header">
        <h1>{isRecycleView ? "Recycle Bin" : "Task Dashboard"}</h1>
        
        <div style={{display: 'flex', gap: '10px'}}>
          <button onClick={handleLogout} style={{backgroundColor: '#ef4444', color: 'white'}}>Logout</button>

          {!isRecycleView && (
            <button onClick={startCreate}>+ Create</button>
          )}
          <button onClick={() => setIsRecycleView(v => !v)}>
            {isRecycleView ? "Back" : `Recycle Bin (${trash.length})`}
          </button>
        </div>
      </div>

      {isFormOpen && !isRecycleView && (
        <div className="form-card">
          <input placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} />
          <select value={status} onChange={e => setStatus(e.target.value)}>
            <option value="pending">Pending</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
          <input placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
          <div style={{ marginTop: 10 }}>
            <button onClick={saveTask}>{editingTaskId ? "Update" : "Save"}</button>
            <button onClick={() => setIsFormOpen(false)} style={{ marginLeft: 10, background: "#888" }}>Cancel</button>
          </div>
        </div>
      )}

      {taskPreview && (
        <div className="modal">
          <div className="modal-card">
            <h3>Task Details</h3>
            <p><b>Title:</b> {taskPreview.title}</p>
            <p><b>Description:</b> {taskPreview.description || "-"}</p>
            <p><b>Status:</b> {STATUS_MAP[taskPreview.status]}</p>
            <p><b>Created:</b> {formatDate(taskPreview.created_date)}</p>
            <p><b>Updated:</b> {formatDate(taskPreview.updated_date)}</p>
            <button onClick={() => setTaskPreview(null)}>Close</button>
          </div>
        </div>
      )}

      {!isRecycleView ? (
        <DragDropContext onDragEnd={onDragEnd}>
          <div className="kanban-board">
            {COLUMNS.map(colId => (
              <div key={colId} className="kanban-column">
                <div className="column-header">
                  {STATUS_MAP[colId]}
                  <span className="count-badge">{groupedTasks[colId]?.length || 0}</span>
                </div>
                
                <Droppable droppableId={colId}>
                  {(provided, snapshot) => (
                    <div
                      className="droppable-area"
                      ref={provided.innerRef}
                      {...provided.droppableProps}
                      style={{ background: snapshot.isDraggingOver ? '#e3f2fd' : 'transparent' }}
                    >
                      {groupedTasks[colId]?.map((task, index) => (
                        <Draggable key={task.id} draggableId={String(task.id)} index={index}>
                          {(provided, snapshot) => (
                            <div
                              className={`task-card status-${task.status} ${snapshot.isDragging ? "is-dragging" : ""}`}
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              onClick={() => openDetails(task.id)}
                              style={{ ...provided.draggableProps.style, cursor: 'pointer' }}
                            >
                              <div className="card-title">{task.title}</div>
                              {task.description && (
                                <div className="card-desc">{task.description}</div>
                              )}
                              <div className="card-actions">
                                <button className="action-btn view-btn" onClick={(e) => { e.stopPropagation(); openDetails(task.id); }}>View</button>
                                <button className="action-btn edit-btn" onClick={(e) => { e.stopPropagation(); startEdit(task.id); }}>Edit</button>
                                <button className="action-btn delete-btn" onClick={(e) => { e.stopPropagation(); moveToTrash(task.id); }}>Delete</button>
                              </div>
                            </div>
                          )}
                        </Draggable>
                      ))}
                      {provided.placeholder}
                    </div>
                  )}
                </Droppable>
              </div>
            ))}
          </div>
        </DragDropContext>
      ) : (
        <table>
          <thead>
            <tr>
              <th>#</th><th>Title</th><th>Status</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {list.map((task, i) => (
              <tr key={task.id}>
                <td>{i + 1}</td>
                <td>{task.title}</td>
                <td>{STATUS_MAP[task.status]}</td>
                <td>
                  <button onClick={() => restoreTask(task.id)}>Restore</button>
                  <button onClick={() => deleteForever(task.id)}>Delete</button>
                </td>
              </tr>
            ))}
            {list.length === 0 && (
              <tr><td colSpan="4" style={{textAlign:'center', padding: 20}}>Recycle Bin is empty</td></tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default App
