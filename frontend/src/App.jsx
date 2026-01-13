import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import MangaLoader from './components/MangaLoader.jsx'
import MangaGenerator from './components/MangaGenerator.jsx'
import './App.css'

function App() {

  return (
    <Router>
      <div className="app-container">
        <main>
          <Routes>
            <Route path={"/manga/:id"} element={<MangaLoader />} />
            <Route path={"/"} element={<MangaGenerator />}/>
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
