import { Routes, Route } from 'react-router-dom'
import { Home } from './Pages/Home'
import { Result } from './Pages/Result'

function App() {

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/result" element={<Result />} />
    </Routes>
  )
}

export default App
